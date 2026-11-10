> **Dokumentasi untuk manusia.** Agen hanya boleh membaca halaman ini jika diminta oleh seseorang.

Bahasa: [English](../how-and-why.md) · [Bahasa Indonesia](how-and-why.md)

# Alasan dan cara koleksi ini dibuat

Ini satu koleksi pribadi dengan satu skill milik koleksi untuk setiap pekerjaan. Prioritasnya adalah pemahaman bersama tanpa bertele-tele, lalu lingkungan yang menolak pekerjaan salah melalui struktur dan pemeriksaan.

## Daftar isi

- [Alasan memiliki koleksi sendiri](#alasan-memiliki-koleksi-sendiri)
- [Mengutamakan pemeriksaan yang mengubah hasil](#mengutamakan-pemeriksaan-yang-mengubah-hasil)
- [Memisahkan kapabilitas dan koordinasi](#memisahkan-kapabilitas-dan-koordinasi)
- [Membuat draf, meninjau, dan mengevaluasi](#membuat-draf-meninjau-dan-mengevaluasi)
- [Arti evaluated](#arti-evaluated)
- [Mempertahankan asal-usul](#mempertahankan-asal-usul)
- [Sumber utama](#sumber-utama)
- [Memahami lapisan validasi](#memahami-lapisan-validasi)
- [Membaca riwayat](#membaca-riwayat)

## Alasan memiliki koleksi sendiri

Metode pilihan dari skill Matt Pocock, port pstack Claude/Codex, tstack, dan Superpowers diadopsi menjadi paket milik koleksi. Sebagian mempertahankan kalimat berguna; sebagian diadaptasi untuk menjaga cakupan, nilai sumber persis, eksekusi portabel, dan satu alur yang konsisten. Plugin upstream dihentikan agar tidak menjadi sumber instruksi yang saling bersaing.

[Peralihan yang diamati dalam PR #10](https://github.com/cravingmaker/skills/pull/10) melaporkan uninstall koleksi Matt pada kedua host. Tiga sumber lainnya sudah tidak ada. Perbedaan itu penting: hasilnya adalah satu koleksi milik sendiri, bukan klaim bahwa keempat sumber terpasang dan dihapus dalam operasi tersebut.

Kepemilikan berarti repositori memelihara metode, memperbaikinya, mengevaluasinya, dan mempertahankan atribusi legalnya. Kepemilikan tidak berarti setiap kalimat yang dipertahankan ditulis dari awal. Alur biasa dari pembentukan rencana sampai implementasi tetap seperti yang dijelaskan dalam [panduan alur](recommended-flow.md).

## Mengutamakan pemeriksaan yang mengubah hasil

Aturan yang diingat dapat dilewati; tipe, aturan lint, atau pemeriksaan CI yang bekerja dapat menolak perubahan salah. Koleksi mengutamakan lapisan tertinggi yang dapat menegakkan persyaratan: arsitektur dan kepemilikan, lalu tipe dan pemeriksaan statis, kemudian bukti yang dijalankan, dengan prosa untuk penilaian yang tidak dapat diputuskan pemeriksaan.

Misalnya, tabel dependensi yang dipelihara manual sebaiknya menjadi keluaran yang dihasilkan dengan pemeriksaan drift. Hook gagal yang sudah ada pada proyek perlu diperbaiki atau dihubungkan sebelum menambah hook kedua. Guardrail yang baik membuktikan penolakan kesalahan sebenarnya, penerimaan pekerjaan valid, dan setup berulang tanpa diff baru.

Biaya token penting saat memengaruhi keputusan. Deskripsi singkat dan referensi bersyarat mengurangi pemuatan default; keduanya tidak membenarkan penyembunyian aturan penyelesaian wajib. Tujuannya pemahaman bersama, bukan batas kata kaku atau pabrik perangkat lunak yang lebih besar.

## Memisahkan kapabilitas dan koordinasi

Kapabilitas memiliki satu pekerjaan yang dapat digunakan ulang dan bukti penyelesaiannya. `agent-orchestrator` adalah router inti: memilih metode dan mengoordinasikan pekerjaan lintas agen. Perencanaan, implementasi, tinjauan, dan verifikasi tetap menjadi tanggung jawab kapabilitas masing-masing.

Fleet memiliki satu koordinator untuk cakupan, anggaran, integrasi, dan penerimaan akhir. Pekerja menerima brief leaf yang terbatas. Delegasi harus sepadan dengan biayanya melalui isolasi yang berguna, pekerjaan independen, pemeriksaan independen, atau kapabilitas berbeda yang diminta. Adanya alat fleet tidak membuat setiap tugas menjadi tugas fleet.

[Referensi routing](routing.md) mencantumkan alur koordinator dan dependensi wajibnya. [Changelog](../../CHANGELOG.md) mencatat alasan usulan backend dan DevOps ditutup tanpa merge.

## Membuat draf, meninjau, dan mengevaluasi

Skill baru dimulai dari contoh dan fixture, bukan isinya. Contoh dijalankan lebih dahulu tanpa skill apa pun. Jika baseline itu sudah menghasilkan outcome yang diharapkan, skill tidak ditulis: model sudah dapat mengerjakannya. Aturan ini berasal dari skill peran yang dihentikan, karena evaluasi outcome-nya kebanyakan menyamai baseline tanpa skill setelah seluruh biaya penyusunan dibayar. Jika celahnya adalah aturan yang dapat ditegakkan skrip, pemeriksaan proyek (CI, lint, atau hook) lebih diutamakan daripada skill.

Saat baseline gagal, metode ditulis dari riset primer atau sumber upstream berlisensi, dengan fokus pada hal yang dilewatkan baseline: pemeriksaan, batas kewenangan, dan bukti wajib. Penulis menetapkan trigger, hasil konkret, standar bukti, mode kegagalan, dan titik berhenti.

Evaluator independen meninjau artefak serta bukti sebenarnya sampai temuan penting yang tersisa diselesaikan. Perbedaan pendapat diselesaikan dengan bukti sumber atau pemeriksaan pembeda; persetujuan saja tidak menjamin kebenaran. Aturan tinjauan terbatas membiarkan keputusan yang belum selesai terlihat, bukan menganggap anggaran habis sebagai persetujuan.

Metode kemudian dibandingkan dengan dan tanpa skill dalam sesi baru yang sepadan pada Codex dan Claude Code. Prasyarat wajib dan input tugas sama dalam kedua arm. Hanya ketersediaan kandidat yang berubah. Edit material mengubah byte yang diuji dan membutuhkan cakupan sepadan pada revisi final.

[Dokumentasi harness berpasangan](../../docs/eval-harness.md) menjelaskan persiapan, model, fixture, catatan, dan isolasi. Evaluasi yang dijalankan menggunakan sesi model sebenarnya. Menyiapkan contoh dan fixture, mengedit instruksi yang ada, dan validasi deterministik tidak membutuhkan pemanggilan model; isi skill baru tetap membutuhkan catatan baseline yang gagal.

## Arti evaluated

Katalog menggunakan dua keadaan: unevaluated dan evaluated. Evaluated berarti setiap Activation dan Near miss memiliki catatan pasangan valid pada byte kandidat final, tanpa comparative hurt yang belum diselesaikan menurut kebijakan bukti yang ditinjau. Pemeriksaan Outcome wajib ditinjau dalam kampanye evaluasi. Pemeriksa katalog memverifikasi cakupan valid/selesai secara struktural. Kesesuaian byte final dan comparative hurt yang belum selesai membutuhkan tinjauan sumber dan kampanye; pemeriksa tidak membuktikannya.

Validitas, aktivasi, ketepatan semantik, dan nilai tambah adalah pertanyaan berbeda:

| Pertanyaan | Bukti |
| --- | --- |
| Apakah perbandingannya valid? | Sesi baru, input/settings sepadan, discovery terkontrol, kedua arm selesai |
| Apakah metode aktif? | Pemilihan native yang didukung atau pembacaan isi terpasang yang berhasil |
| Apakah hasil memenuhi harapan? | Tinjauan respons, artefak, perintah, dan cakupan |
| Apakah skill memperbaiki hasil? | Perbandingan sepadan yang memisahkan nilai kandidat dari baseline, prasyarat, dan pengaruh host |

Pasangan valid dapat menunjukkan harapan yang gagal. Hasil sepadan tidak membuktikan keunggulan terhadap baseline. Kasus positif entri manual dapat lebih banyak mengukur ketersediaan entri yang diminta daripada manfaat unik metodenya. Komponen dependensi bersama juga membatasi atribusi per skill.

Pada snapshot inti 2026-11-09, semua skill yang tersedia ditandai evaluated setelah [kampanye host selesai dalam PR #9](https://github.com/cravingmaker/skills/pull/9). Pembersihan peran dalam [PR #14](https://github.com/cravingmaker/skills/pull/14) mengubah empat skill dan mengembalikan statusnya. [PR #13](https://github.com/cravingmaker/skills/pull/13) memulihkan tiga skill dengan pasangan trigger baru, dan [PR #15](https://github.com/cravingmaker/skills/pull/15) memulihkan `writing-for-agents` dengan pasangan Outcome, sehingga semua 58 skill kembali evaluated pada 2026-11-10. Pernyataan itu tidak menjanjikan aktivasi sempurna, setiap cabang opsional, hosted CI nyata, penyerahan produksi berhasil, atau perilaku model masa depan tertentu. [Halaman masalah yang diketahui](known-issues.md) mempertahankan batasan tersebut.

## Mempertahankan asal-usul

Materi adaptasi mempertahankan URL upstream, revisi sumber lengkap, inventaris berkas sumber, penjelasan perubahan lokal, dan teks lisensi yang berlaku. Manifest per berkas mencatat hash asli, tujuan, metode yang dipertahankan, pemegang hak cipta, dan berkas legal. Materi Apache juga mempertahankan pemberitahuan wajib dan menandai berkas yang diubah.

[Skema asal-usul panduan penulisan](../../docs/authoring-guide.md#provenance-manifests) menjadi kontrak pemeliharaan. Pemeriksaan otomatis membuktikan skema, sintaks revisi/hash lengkap, header legal, dan keberadaan berkas. Peninjau tetap memverifikasi identitas sumber, byte asli, atribusi lengkap, serta kontribusi yang dipertahankan dari prompt dan aset.

Kurikulum yang digunakan sebagai rujukan cakupan tidak disalin hanya karena berguna. Status instalasi plugin upstream tidak menghapus kewajiban atribusi teks yang diadopsi.

## Sumber utama

Sumber utama dibaca dari metadata setiap skill; kontribusi sekunder yang dipertahankan memiliki berkas legal dan baris manifest per berkas sendiri.

<!-- BEGIN GENERATED upstream: generated by scripts/build-docs.py; edit the catalog or SKILL.md files, then rerun it -->

| Sumber utama | Skill |
| --- | --- |
| [Matt Pocock's skills](https://github.com/mattpocock/skills) | 27: `agent-orchestrator`, `change-review`, `codebase-design`, `diagnosing-bugs`, `domain-modeling`, `grill-me`, `grill-with-docs`, `grilling`, `handoff`, `implement`, `implement-spec`, `improve-codebase-architecture`, `pr`, `prototype`, `research`, `retro`, `setup-agent-skills`, `tdd`, `to-questionnaire`, `to-spec`, `to-tickets`, `triage`, `wait-what`, `wayfinder`, `wizard`, `work-decomposition`, `writing-for-agents` |
| [pstack](https://github.com/cursor/plugins) | 19: `agent-briefing`, `agent-debate`, `architect`, `benchmark-checklist`, `blast-radius`, `bro`, `clear-communication`, `correct`, `create-verification-skill`, `decision-log`, `how`, `ketchup`, `maintain-verification-skill`, `project-guardrails`, `recall`, `result-verification`, `sharpen`, `teach`, `why` |
| [pstack Claude/Codex port](https://github.com/michael-denyer/pstack-claude) | 2: `fix-ci`, `interrogate` |
| [tstack](https://github.com/t3dotgg/tstack) | 9: `babysit-pr`, `council`, `file-pr`, `full-send`, `full-stop`, `leaving-pr-comments`, `modernize`, `sol-loop`, `takeover` |
| Asli dari repositori ini | 1: `toolchain-upgrade` |

| Berkas legal | Skill yang menyertakannya |
| --- | --- |
| `LICENSE-cravingmaker` | 1 |
| `LICENSE-cursor-team-kit` | 6 |
| `LICENSE-humanlayer` | 1 |
| `LICENSE-mattpocock` | 31 |
| `LICENSE-pstack` | 37 |
| `LICENSE-pstack-claude` | 39 |
| `LICENSE-superpowers` | 13 |
| `LICENSE-thermos` | 1 |
| `LICENSE-tstack` | 11 |
| `NOTICE-pstack-claude.md` | 6 |
| `NOTICE-skills.md` | 33 |

<!-- END GENERATED upstream -->

## Memahami lapisan validasi

Validator repositori memeriksa skema referensi Agent Skills yang dipatok, aturan paket repositori, konsistensi katalog dan dependensi, profil serta kebijakan host yang dihasilkan, fixture test, freshness, keamanan workflow, dan prosa. Kelulusan pemeriksaan membuktikan sifat yang dicakupnya.

Fixture deterministik tidak membutuhkan pemanggilan model. Evaluasi model membutuhkan anggaran proses yang dicatat secara eksplisit dan autentikasi host sebenarnya yang ditangani privat. Fixture yang membutuhkan alat eksternal yang tidak tersedia dapat membiarkan permukaan itu belum terbukti meskipun test wrapper lulus. Permukaan native atau peninjau yang tidak tersedia tetap menjadi batas eksplisit.

Dokumentasi manusia memiliki pemeriksaan generasi dan pemisahannya sendiri. Lihat [pemeliharaan halaman ini](maintaining-docs.md) untuk perintah persis dan kasus kegagalannya.

## Membaca riwayat

[Cara koleksi ini dibuat](making-skills.md#tahap-pembuatan-dan-pull-request) mencatat tahap pekerjaan, model, draf buta, tinjauan independen, adopsi inti, eksperimen peran, dan retrospektif 2026-11-10. Halaman itu membedakan merge PR #2–#7 ke induk bertingkat dari PR #8 yang memasukkannya ke main, serta memisahkan PR #11–#12 yang ditutup tanpa merge dari tindak lanjut pembersihan dan dokumentasi. [Tabel metode pembuatan skill](making-skills.md#skill-dan-alat-untuk-membuat-skill) juga membedakan metode yang diikuti secara manual dari pemuatan skill sebenarnya.

[Changelog](../../CHANGELOG.md) menyediakan satu entri bahasa sederhana untuk setiap PR yang di-merge sampai snapshot main yang didokumentasikan. Isi PR publik menyediakan riwayat, termasuk draf lama dan pernyataan "not yet verified". Gunakan katalog saat ini, byte sumber saat ini, catatan evaluasi lebih baru, dan PR selanjutnya untuk menetapkan keadaan sekarang.
