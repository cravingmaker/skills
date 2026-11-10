> **Dokumentasi untuk manusia.** Agen hanya boleh membaca halaman ini jika diminta oleh seseorang.

Bahasa: [English](../harness-differences.md) · [Bahasa Indonesia](harness-differences.md)

# Claude Code, Codex, dan T3 Code

Metode skill digunakan bersama, sementara discovery, kebijakan pemanggilan, trace aktivasi, dan alat eksekusi yang tersedia berbeda. Bukti mendukung perbedaan tertentu; bukti tidak memisahkan pengaruh host dari pengaruh model, izin, atau fixture.

## Daftar isi

- [Perbedaan teknis](#perbedaan-teknis)
- [Mengetik dan mengikuti alur](#mengetik-dan-mengikuti-alur)
- [Subagen dan delegasi](#subagen-dan-delegasi)
- [Alat PR dan penantian](#alat-pr-dan-penantian)
- [Pertanyaan dan penyelesaian](#pertanyaan-dan-penyelesaian)
- [Perbedaan izin dan sandbox](#perbedaan-izin-dan-sandbox)
- [Perbedaan hasil yang diamati](#perbedaan-hasil-yang-diamati)
- [Hal yang tidak dapat disimpulkan](#hal-yang-tidak-dapat-disimpulkan)

## Perbedaan teknis

Tabel ini menjelaskan CLI yang tercatat dan adapter repositori. Root host khusus harus ditentukan dari sesi sebenarnya.

| Aspek | Claude Code | Codex |
| --- | --- | --- |
| Tujuan skill pengguna default saat peralihan | `~/.claude/skills` | `~/.codex/skills` |
| Root isolasi terkait | HOME privat dan `CLAUDE_CONFIG_DIR` | HOME privat dan `CODEX_HOME`; perhitungkan juga `~/.agents/skills` |
| Pemilihan eksplisit | Perintah native `/<name>` | Pemilihan skill native `$<name>` |
| Penyimpanan manual-only | `skillOverrides` terpilih dalam berkas settings eksplisit | `agents/openai.yaml` hasil generasi milik koleksi dalam folder skill |
| Nilai manual-only | `user-invocable-only`, dengan mempertahankan `off` yang lebih ketat | `policy.allow_implicit_invocation: false` |
| Pengamatan inventaris dalam test discovery | Respons initialize SDK mencantumkan perintah | App-server `skills/list` |
| Bukti aktivasi | Skill atau Read langsung yang berhasil, replay slash native tepercaya, atau pembacaan isi Bash terlihat yang didukung | Provenance/isi skill terpilih native yang persis, atau pembaca berkas terpasang sederhana yang didukung dan berhasil |
| Eksekusi evaluasi | Sesi headless stream-JSON dengan sumber settings pengguna terkontrol | `codex exec --json` dengan konfigurasi terkontrol dan sesi baru |
| Pengamatan anggaran deskripsi | Tidak ada pemotongan dalam skenario daftar yang diuji | Replay cache lebih luas memendekkan deskripsi yang ditampilkan sementara inventaris mempertahankan deskripsi lengkap |

[Kontrak instalasi](../../docs/installing.md), [harness berpasangan](../../docs/eval-harness.md), dan [bukti discovery](install-and-discovery-proof.md) menetapkan rinciannya. Klaim model bahwa ia menggunakan skill tidak cukup pada kedua host.

## Mengetik dan mengikuti alur

Gunakan pemilihan native untuk entri manual pada kedua host. Entri yang sama seharusnya memilih metode yang sama dan mempertahankan cakupan yang sama. Perintah Claude `/grill-me` yang diamati membuka wawancara milik koleksi dalam mode tanpa dokumen; evaluasi manual positif Codex menggunakan pemilihan native `$<name>`.

Entri terpilih dapat membaca induk wajib tanpa perintah pengguna tambahan. Itulah komposisi metode. Komposisi tidak memberi izin wawancara kedua, implementasi, posting, atau merge di luar permintaan saat ini.

Tidak adanya daftar otomatis dapat disengaja untuk entri manual. Agen harus memeriksa seluruh inventaris terpasang sebelum melaporkan skill wajib tidak tersedia. [Referensi perintah](typed-commands.md) menyediakan penulisan untuk kedua host dan mode yang dipilih.

## Subagen dan delegasi

Router peran menyediakan keputusan dan serah terima; host menyediakan dispatch dan isolasi. Koleksi tidak menetapkan satu peta penyedia secara tetap atau mewajibkan agen terpisah untuk setiap metode.

Orchestrator mencatat satu jatah terbatas sebelum peluncuran. Pekerja adalah leaf kecuali brief secara eksplisit mengalokasikan pekerjaan lanjutan dari catatan anggaran yang sama. Batas konkurensi host atau pengguna yang lebih rendah mengalahkan batas koleksi. Model/penyedia yang diminta tetapi tidak tersedia dilaporkan tanpa penggantian.

T3 Code dapat menyediakan pekerjaan native dari penyedia yang sama, delegasi lintas penyedia, checkout milik host, penyelesaian tugas, dan pembatalan. Pilihan jalur bergantung pada deskripsi alat saat ini dan settings yang diminta pengguna. Fasilitas tersebut tidak membuat thread tingkat atas baru setara dengan subagen.

Harness contoh berpasangan menonaktifkan delegasi pada kedua host. Fixture alur harian terpisah menjalankan pekerja CLI serial terisolasi melalui adapter yang dinyatakan. Fixture tidak membuktikan dispatch pekerja native serentak, panel penyedia, race pembatalan, atau semua siklus hidup T3.

## Alat PR dan penantian

Gunakan alat forge terhubung atau alat host yang memadai sebelum beralih ke CLI. Metode bersama memisahkan kewenangan draf isi, pengajuan, pemantauan, dan merge pada kedua host. Metode mengembalikan setiap lapisan PR yang dibuat atau diperbarui dan membaca kembali keadaan head/base/check/review.

T3 Code dapat mewajibkan pengaitan sesi dan menyediakan mekanisme watcher PR. Dalam lingkungan itu, ikuti kontrak pengaitan dan penyelesaian yang sebenarnya. Root memiliki satu watcher; anak mengembalikan keadaan PR tanpa memantau.

Jika mekanisme penyelesaian yang didukung tersedia, tangani pekerjaan yang tersedia, aktifkan mekanismenya, lalu serahkan kendali sesuai aturan host. Lingkungan CLI biasa mungkin menyediakan perintah pemeriksaan blocking yang didukung; itu tidak menyiratkan API watcher T3 yang persis. Jika tidak ada mekanisme yang didukung, kembalikan satu pemeriksaan status terbatas dan tindakan berikutnya. Jangan membangun loop polling untuk meniru alat yang tidak ada.

## Pertanyaan dan penyelesaian

[Metode penyerahan](../../skills/full-send/SKILL.md#asking-the-user) mengajukan pertanyaan penghambat melalui alat pertanyaan host aktif. Jika alat tidak ada atau tidak memberi jawaban, metode membiarkan PR terbuka dan belum di-merge serta menempatkan pertanyaan di awal pesan akhir. Kampanye yang tercatat tidak menetapkan antarmuka interaktif mana yang menyediakan alat itu.

Harness berpasangan menjalankan CLI langsung; tidak ada perbandingan berpasangan yang membuktikan siklus pertanyaan, watcher, atau delegasi T3 Code. [Uji routing historis](install-and-discovery-proof.md#salah-rute-anggaran-dan-batasan) juga mencatat Claude menyarankan definisi agen native untuk peran yang tidak tersedia, meskipun kedua host dengan benar tidak memuat skill peran. Saran itu bukan prosedur instalasi peran koleksi ini.

## Perbedaan izin dan sandbox

Cakupan skill bukan sandbox, dan kewenangan pengujian yang diperlukan tidak melewati penegakan sistem atau harness.

| Konfigurasi evaluasi yang tercatat | Claude Code | Codex |
| --- | --- | --- |
| Perilaku persetujuan | `dontAsk` dengan Read/Write/Edit/Bash/Skill diizinkan dan alat delegasi/web ditolak | Kebijakan persetujuan `never` |
| Filesystem perintah | Sandbox Claude dengan direktori kerja terkontrol | Sandbox `workspace-write` |
| Jaringan perintah | Tidak ada domain jaringan yang diizinkan | Jaringan perintah dinonaktifkan |
| Sumber lain | Settings pengguna terkontrol, tanpa plugin/connector/hook/auto memory eksternal | Config terkontrol; skill/plugin/app/hook/memory/delegasi bawaan dinonaktifkan |
| Hambatan yang diamati | Penulisan hook terlindungi, beberapa perintah gabungan, dan eksekusi npm nyata ditolak | Beberapa probe fixture setara dapat berjalan; permukaan proyek/Git terlindungi tetap membutuhkan penanganan fixture khusus |

Ini adalah konfigurasi harness, bukan saran untuk melemahkan izin pengguna sebenarnya. Adapter sumber dan [PR #9](https://github.com/cravingmaker/skills/pull/9) membuktikan perilaku yang tercatat. Settings yang ditegakkan server di luar trace lokal tetap menjadi batas.

Daftar sumber settings Claude kosong menyembunyikan skill pengguna pada versi yang tercatat, sehingga harness hanya mengaktifkan sumber pengguna sementara yang terkontrol. Proyek bersih saja tidak menghapus plugin pengguna atau konteks memory. Path sementara Claude yang panjang juga memicu fallback ke temp bersama sebelum perbaikan harness. Faktor pengganggu itu menjelaskan mengapa beberapa percobaan perbandingan invalid, bukan bukti perilaku.

[Insiden pembuatan](making-skills.md#pengecualian-protokol-dan-pelajaran) juga mencatat dua pembacaan memory saat startup pekerja kampanye dan satu probe preferensi pribadi meskipun brief membatasinya. Insiden pekerja itu terpisah dari arm pasangan yang dikonfigurasi. Verifikasi konteks yang diinjeksi host, root temp per arm, penolakan fork, dan worktree khusus yang stabil; janji dalam prosa tidak cukup.

## Perbedaan hasil yang diamati

Baca sebagai pengamatan terbatas beserta faktor pengganggunya. Catatan tidak mendukung peringkat umum kedua host.

| Kasus | Perbedaan yang diamati | Penafsiran yang didukung |
| --- | --- | --- |
| Edit PR offline yang diizinkan | Gabungan edit/readback pada satu treatment Claude ditolak; pasangan Claude dan Codex baru menyelesaikannya | Kegagalan historis yang dipengaruhi izin, bukan cacat isi skill yang terbukti |
| Setup hook dan probe runtime | Claude menolak penulisan path terlindungi dan npm nyata dalam fixture tercatat; fixture hook khusus memisahkan pertanyaan trigger, dan beberapa probe Codex berjalan | Ketersediaan alat/izin memengaruhi bukti yang dapat dicapai; pengganti tidak membuktikan kesetaraan staged-hook nyata |
| Kasus aturan duplikat pada retrospektif final | Kedua treatment final menolak panduan duplikat dan menghormati sumber yang disebutkan; Claude memiliki kesalahan kecil label sumber di luar topik | Hasil inti serupa dengan satu cacat respons yang dipertahankan; tidak ada kesimpulan ketepatan seluruh host |
| Draf PR faktual singkat terdahulu | Satu uji Codex memuat metode komunikasi tanpa perlu; pengujian ulang deskripsi pada kedua host menangani batas tersebut | Biaya alur tambahan historis, bukan tingkat trigger universal |
| Induk manual hilang | Entri manual berhenti alih-alih mengarang prosedur induk yang tidak ada pada kampanye Claude selanjutnya | Ketersediaan dan disiplin dependensi penting; perbandingan tidak mengisolasi metode induk baru |

[Catatan retrospektif final](../../skills/retro/evals/results/2026-11-09-claude-claude-opus-5-5-outcome-6-round4-fix5-claude.md), [pengulangan questionnaire](../../skills/to-questionnaire/evals/results/2026-11-09-claude-claude-opus-5-5-near-miss-3-round2-pre-claude.md), dan [hasil PR #9](https://github.com/cravingmaker/skills/pull/9) mempertahankan batasan itu. [Halaman masalah yang diketahui](known-issues.md) membedakan cacat yang sudah diperbaiki dari batas saat ini.

## Hal yang tidak dapat disimpulkan

Model default host berbeda, dan fixture izin/settings dapat berbeda antar-kampanye. Masing-masing pasangan dipadankan dalam satu host; itu tidak membuat eksperimen lintas host yang terkontrol.

Jangan menyimpulkan keunggulan umum, penghematan biaya, penekanan manual universal, atau keandalan versi mendatang. Peninjau independen, permukaan produksi/native, syarat hosted CI nyata, atau merge yang tidak tersedia tidak boleh mendapat kredit hasil. Alat khusus T3 harus dijelaskan sebagai tersedia dalam sesi, bukan dijamin oleh paket skill.
