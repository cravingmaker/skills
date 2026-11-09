// Original Rust starter. Compare with the project's locked sqlx/tokio versions,
// required crate features and disposal fixture before copying; compile locally.
// Only use connections from an explicitly disposable, identity-checked fixture.
// The owner seeds counter(value=0) and duty(id=1,2; active=true), then reads the
// committed result through a third connection and removes its own resources.
use std::{future::Future, pin::Pin, sync::Arc, time::Duration};
use sqlx::{Connection, PgConnection, PgPool};
use tokio::{sync::Barrier, time::{timeout, timeout_at, Instant}};

type Body<'a, T> = Pin<Box<dyn Future<Output = Result<T, sqlx::Error>> + Send + 'a>>;

fn retryable(error: &sqlx::Error) -> bool {
    error.as_database_error().and_then(|e| e.code())
        .is_some_and(|code| matches!(code.as_ref(), "40001" | "40P01"))
}

// One deadline covers acquisition, body, commit and backoff. Timeout is not a
// retryable SQLSTATE: a lost commit acknowledgement needs reconciliation.
pub async fn serializable<T, F, B>(pool: &PgPool, attempts: usize, budget: Duration,
                                  mut backoff: B, mut body: F) -> Result<T, sqlx::Error>
where T: Send, F: for<'a> FnMut(&'a mut PgConnection, usize) -> Body<'a, T>,
      B: FnMut(usize, Duration) -> Duration {
    assert!(attempts > 0 && !budget.is_zero());
    let deadline = Instant::now() + budget;
    for number in 1..=attempts {
        let result = timeout_at(deadline, async {
            let mut tx = pool.begin().await?;
            sqlx::query("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE").execute(&mut *tx).await?;
            match body(&mut tx, number).await {
                Ok(value) => { tx.commit().await?; Ok(value) }
                Err(error) => { tx.rollback().await?; Err(error) }
            }
        }).await.map_err(|_| sqlx::Error::PoolTimedOut)?;
        match result {
            Ok(value) => return Ok(value),
            Err(error) if retryable(&error) && number < attempts => {
                // The caller supplies full jitter using its existing RNG;
                // clamp that delay to the one remaining transaction budget.
                let remaining = deadline.saturating_duration_since(Instant::now());
                let pause = backoff(number, remaining).min(remaining);
                timeout_at(deadline, tokio::time::sleep(pause)).await
                    .map_err(|_| sqlx::Error::PoolTimedOut)?;
            }
            Err(error) => return Err(error),
        }
    }
    unreachable!()
}

pub async fn lost_update(left: &mut PgConnection, right: &mut PgConnection,
                         expected_database: &str, disposable: bool,
                         schema: &str, bound: Duration, atomic: bool) -> Result<(), sqlx::Error> {
    assert!(disposable && !expected_database.is_empty() && !bound.is_zero());
    assert!(!schema.is_empty() && schema.bytes().all(|c| c.is_ascii_lowercase() || c.is_ascii_digit() || c == b'_'));
    let table = format!("\"{}\".counter", schema);
    let mut a = left.begin().await?;
    let mut b = right.begin().await?;
    let identity_a: (String, i32) = sqlx::query_as("SELECT current_database(), pg_backend_pid()")
        .fetch_one(&mut *a).await?;
    let identity_b: (String, i32) = sqlx::query_as("SELECT current_database(), pg_backend_pid()")
        .fetch_one(&mut *b).await?;
    assert!(identity_a.0 == expected_database && identity_b.0 == expected_database && identity_a.1 != identity_b.1);
    let gate = Arc::new(Barrier::new(2));
    let run_a = async {
        let old: i32 = sqlx::query_scalar(&format!("SELECT value FROM {}", table)).fetch_one(&mut *a).await?;
        timeout(bound, gate.wait()).await.map_err(|_| sqlx::Error::PoolTimedOut)?;
        if atomic { sqlx::query(&format!("UPDATE {} SET value = value + 1", table)).execute(&mut *a).await?; }
        else { sqlx::query(&format!("UPDATE {} SET value = $1", table)).bind(old + 1).execute(&mut *a).await?; }
        a.commit().await
    };
    let run_b = async {
        let old: i32 = sqlx::query_scalar(&format!("SELECT value FROM {}", table)).fetch_one(&mut *b).await?;
        timeout(bound, gate.wait()).await.map_err(|_| sqlx::Error::PoolTimedOut)?;
        if atomic { sqlx::query(&format!("UPDATE {} SET value = value + 1", table)).execute(&mut *b).await?; }
        else { sqlx::query(&format!("UPDATE {} SET value = $1", table)).bind(old + 1).execute(&mut *b).await?; }
        b.commit().await
    };
    // join! settles both participants; try_join! could drop one early.
    let (first, second) = tokio::join!(run_a, run_b);
    first?;
    second?;
    Ok(())
}

pub async fn write_skew(left: &mut PgConnection, right: &mut PgConnection,
                        expected_database: &str, disposable: bool,
                        schema: &str, bound: Duration) -> Result<(), sqlx::Error> {
    assert!(disposable && !expected_database.is_empty() && !bound.is_zero());
    assert!(!schema.is_empty() && schema.bytes().all(|c| c.is_ascii_lowercase() || c.is_ascii_digit() || c == b'_'));
    let table = format!("\"{}\".duty", schema);
    let mut a = left.begin().await?;
    let mut b = right.begin().await?;
    for tx in [&mut a, &mut b] {
        sqlx::query("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ").execute(&mut **tx).await?;
    }
    let identity_a: (String, i32) = sqlx::query_as("SELECT current_database(), pg_backend_pid()")
        .fetch_one(&mut *a).await?;
    let identity_b: (String, i32) = sqlx::query_as("SELECT current_database(), pg_backend_pid()")
        .fetch_one(&mut *b).await?;
    assert!(identity_a.0 == expected_database && identity_b.0 == expected_database && identity_a.1 != identity_b.1);
    let gate = Arc::new(Barrier::new(2));
    let run_a = async {
        let count: i64 = sqlx::query_scalar(&format!("SELECT count(*) FROM {} WHERE active", table))
            .fetch_one(&mut *a).await?;
        timeout(bound, gate.wait()).await.map_err(|_| sqlx::Error::PoolTimedOut)?;
        if count > 1 {
            sqlx::query(&format!("UPDATE {} SET active = false WHERE id = $1", table))
                .bind(1_i32).execute(&mut *a).await?;
        }
        a.commit().await
    };
    let run_b = async {
        let count: i64 = sqlx::query_scalar(&format!("SELECT count(*) FROM {} WHERE active", table))
            .fetch_one(&mut *b).await?;
        timeout(bound, gate.wait()).await.map_err(|_| sqlx::Error::PoolTimedOut)?;
        if count > 1 {
            sqlx::query(&format!("UPDATE {} SET active = false WHERE id = $1", table))
                .bind(2_i32).execute(&mut *b).await?;
        }
        b.commit().await
    };
    let (first, second) = tokio::join!(run_a, run_b);
    first?;
    second?;
    Ok(())
}

// Serializable repair: seed two active rows. In each retry body read the
// active count; on attempt 1 only, meet a bounded two-party Barrier after that
// read; update the worker's own row only when count > 1. Use one retry loop per
// worker. Repeatable Read with the same two reads exposes zero active rows.
// Never put the read barrier after a conflicting row lock, or on every retry.
// The fixture owner bounds socket/statement waits and reaps resources after
// killed processes; a dropped future is not proof of interrupted cleanup.
