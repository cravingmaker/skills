> **Dokumentasi untuk manusia.** Agen hanya boleh membaca halaman ini jika diminta oleh seseorang.

Bahasa: [English](../making-skills.md) · [Bahasa Indonesia](making-skills.md)

# Cara koleksi ini dibuat

Koleksi ini dibangun dengan mengadopsi metode berguna, mengubah kesalahan berulang menjadi pemeriksaan, dan membandingkan hasilnya dengan model kuat yang bekerja tanpa skill kandidat. Keputusan penting berikutnya adalah menghentikan paket peran teknis saat manfaat terukurnya tidak sepadan dengan biaya. Skill baru kini dimulai dari baseline yang gagal.

Riwayat ini menggabungkan PR publik dengan ringkasan sesi pembuatan yang disanitasi dan diberikan pada 2026-11-10. Total kampanye adalah pengamatan bertanggal, bukan eksperimen baru atau pengganti katalog saat ini. [Hasil evaluasi yang dihasilkan](eval-results.md) menghitung catatan yang dikomit terhadap byte paket skill saat ini secara terpisah. [Penjelasan desain](how-and-why.md), [masalah yang diketahui](known-issues.md), dan [alur yang disarankan](recommended-flow.md) menjadi acuan kontrak yang terus berlaku.

## Daftar isi

- [Tujuan dan keputusan](#tujuan-dan-keputusan)
- [Manusia, agen, model, dan batasan](#manusia-agen-model-dan-batasan)
- [Tahap pembuatan dan pull request](#tahap-pembuatan-dan-pull-request)
- [Draf buta dan tinjauan independen](#draf-buta-dan-tinjauan-independen)
- [Adopsi dan asal-usul legal](#adopsi-dan-asal-usul-legal)
- [Skill dan alat untuk membuat skill](#skill-dan-alat-untuk-membuat-skill)
- [Kampanye evaluasi dan batasannya](#kampanye-evaluasi-dan-batasannya)
- [Peralihan ke koleksi milik sendiri](#peralihan-ke-koleksi-milik-sendiri)
- [Eksperimen peran dan keputusan berhenti](#eksperimen-peran-dan-keputusan-berhenti)
- [Cara membuat skill baru sekarang](#cara-membuat-skill-baru-sekarang)
- [Pengecualian protokol dan pelajaran](#pengecualian-protokol-dan-pelajaran)
- [Retrospektif](#retrospektif)
- [Ringkasan publik dan bukti privat](#ringkasan-publik-dan-bukti-privat)

## Tujuan dan keputusan

Pengguna menginginkan pemahaman bersama tanpa bertele-tele; lingkungan skrip, lint, CI, dan hook yang menolak pekerjaan salah melalui desainnya; serta orchestrator dengan fleet agen. Token harus membayar pekerjaan yang berguna tanpa mekanisme yang tidak perlu. Usulan fleet awal juga mencakup router peran yang menggabungkan kapabilitas; bagian itu kemudian dihentikan berdasarkan bukti.

Aturan kepemilikannya adalah satu skill per pekerjaan, dipelihara di sini. Metode pilihan dari koleksi Matt Pocock, port pstack Claude/Codex, tstack, dan Superpowers dapat dipertahankan atau diadaptasi jika lisensinya mengizinkan. `correct` milik koleksi didahulukan daripada entri upstream. Alur utama tetap `grill-with-docs → to-spec → to-tickets → implement or implement-spec → retro`, digabungkan dengan praktik pstack dan tstack.

Dependensi wajib tetap dalam `metadata.requires`, yang mengendalikan instalasi. Usulan field `metadata.handoffs` dibatalkan: rute opsional berupa prosa bersyarat, diperiksa terhadap nama skill yang dikenal, dan tidak memasang apa pun. Pemanggilan manual berada dalam `catalog/skills.yaml` sebagai `invocation: user` dan dalam adapter host, bukan field host dalam `SKILL.md`. Entri `/grill-me`, `/council`, `/interrogate`, `/wait-what`, `/bro`, `/pr`, dan `/ketchup` dipertahankan bersama `/full-stop`; komposisi sebenarnya didokumentasikan dalam [perintah manual](typed-commands.md).

## Manusia, agen, model, dan batasan

Pemilik manusia menetapkan tujuan, kewenangan, perubahan konkurensi, dan keputusan berhenti. Orchestrator adalah Claude Opus 5.5 melalui Claude Code dalam T3 Code. Orchestrator menulis brief, mengintegrasikan hasil, melakukan commit, push, dan membuka PR. Pekerja mengembalikan perubahan tanpa commit atau patch; pekerja tidak melakukan commit.

Pekerja menggunakan GPT-6.1 Sol pada max reasoning effort dan Claude Opus 5.5 pada high, terkadang max, effort. Pekerja melakukan riset, membuat draf, menggabungkan draf, dan menjalankan evaluasi. GPT-6 Astra pada max effort dikhususkan untuk tinjauan independen dan debat terhadap artefak serta bukti sebenarnya. Penugasan itu menjelaskan sesi pembuatan ini, bukan model yang diwajibkan untuk menggunakan koleksi.

Batas aktif awal adalah delapan agen, termasuk proses model evaluasi; pengguna kemudian menurunkannya menjadi enam. Pekerja evaluasi umumnya menjalankan tiga sampai enam proses model secara paralel dan membaca ulang pengaturan konkurensi yang dapat disesuaikan sebelum setiap start. Satu usulan peran memiliki satu PR. Batas ini berbeda dari anggaran total start atau token: mengendalikan konkurensi saja tidak mengendalikan biaya total, seperti pelajaran di bawah.

## Tahap pembuatan dan pull request

| Tahap | Pekerjaan dan hasil | Catatan publik |
| --- | --- | --- |
| Riset | Sol dan Opus membuat dossier menurut peran dan koleksi. Katalog global 563 baris memetakan peran dan spesialisasi yang diminta ke keep-core, keep-extended, fold, atau drop, lalu menggabungkan cakupan administrasi database. | Persiapan dirangkum di sini; input riset privat tidak diterbitkan ulang |
| Gelombang pertama milik koleksi | `clear-communication`, diadaptasi dari unslop pstack dan metode terkait dengan gaya Vale; `correct` milik koleksi; `project-guardrails`; `toolchain-upgrade`; pemeriksaan repositori. | [PR #1](https://github.com/cravingmaker/skills/pull/1) |
| Fondasi | Panduan penulisan, template, pemeriksaan katalog, profil, freshness, harness berpasangan, dan installer. | [PR #2](https://github.com/cravingmaker/skills/pull/2) |
| Koordinasi | `agent-orchestrator` beserta `work-decomposition`, `agent-briefing`, `agent-debate`, `result-verification`, dan `decision-log`. | [PR #3](https://github.com/cravingmaker/skills/pull/3) |
| Rencana adopsi | Posisi buta Sol dan Opus mencakup 237 dan 156 baris sumber. Koordinator menggabungkan posisi eksplisit; tiga putaran tinjauan Astra mencapai FULL AGREEMENT. Rencana menjelaskan 64 paket, 48 skill inti baru, entri manual, perubahan per skill, dan aturan asal-usul. Jumlah rencana menjelaskan tahap itu, bukan instalasi 58 paket berikutnya. | Rencana diwujudkan melalui [PR #4](https://github.com/cravingmaker/skills/pull/4), [PR #5](https://github.com/cravingmaker/skills/pull/5), [PR #6](https://github.com/cravingmaker/skills/pull/6), dan [PR #7](https://github.com/cravingmaker/skills/pull/7) |
| Alat adopsi | Preferensi pemanggilan katalog, generasi Codex `agents/openai.yaml`, adapter instalasi Claude `skillOverrides`, dan pemeriksaan nama dalam prosa menggantikan handoffs. | [PR #4](https://github.com/cravingmaker/skills/pull/4) |
| Adopsi inti | Pembentukan dan pemahaman; desain, implementasi, dan verifikasi; pengiriman dan kelanjutan, termasuk checklist peralihan. Masing-masing mengikuti rencana, tinjauan independen sampai sepakat, dan evaluasi Codex. | [PR #5](https://github.com/cravingmaker/skills/pull/5), [PR #6](https://github.com/cravingmaker/skills/pull/6), [PR #7](https://github.com/cravingmaker/skills/pull/7) |
| Pemeriksaan stack | Tinjauan seluruh stack dan proses CLI sekali pakai dari awal sampai akhir. Injeksi skill native Codex ditambahkan pada deteksi aktivasi; replay memperbaiki 63 pengamatan false-to-true yang nyata. | Stack masuk melalui [PR #8](https://github.com/cravingmaker/skills/pull/8); [contoh alur harian](recommended-flow.md#contoh-lengkap-menambah-keluaran-json-pada-cli) |
| Masuk main | PR #2–#7 sebelumnya di-merge ke branch induk bertingkat, bukan main. PR #8 memasukkan stack gabungan. | [PR #8](https://github.com/cravingmaker/skills/pull/8) |
| Kampanye host Claude | Empat putaran, koreksi harness, dan enam perbaikan skill; seluruh 58 skill inti mencapai evaluated pada checkpoint itu. | [PR #9](https://github.com/cravingmaker/skills/pull/9) |
| Peralihan instalasi | Pada 2026-11-09 inti milik koleksi berisi 58 paket menggantikan instalasi upstream yang tersisa pada kedua host; reservasi lama dibebaskan. | [PR #10](https://github.com/cravingmaker/skills/pull/10) |
| Eksperimen peran | Draf backend dan DevOps mencapai persetujuan tinjauan tetapi ditutup tanpa merge setelah nilai tambah terukurnya lemah; penyusunan sysadmin dibatalkan. | [PR #11](https://github.com/cravingmaker/skills/pull/11), [PR #12](https://github.com/cravingmaker/skills/pull/12) |
| Pembersihan dan dokumentasi | Tindak lanjut pembersihan menghapus jejak peran. Pekerjaan dokumentasi menambah panduan manusia, changelog, README berkategori, prosedur agen, aturan baseline-first, edisi Indonesia, dan hasil evaluasi. Ini pekerjaan tindak lanjut, terpisah dari masuknya stack ke main sebelumnya. | [PR #14](https://github.com/cravingmaker/skills/pull/14), [PR #13](https://github.com/cravingmaker/skills/pull/13) |
| Evaluasi Outcome baseline-first | Lima pasangan Outcome Codex khusus menguji aturan baseline-first pada `writing-for-agents`; skill itu menjadi evaluated, sehingga semua 58 skill evaluated. | [PR #15](https://github.com/cravingmaker/skills/pull/15) |

[Changelog](../../CHANGELOG.md) membedakan pekerjaan yang di-merge, masuknya stack ke main, dan usulan yang ditutup tanpa merge. Ubah base anak bertingkat yang masih terbuka ke base tujuan setelah induknya masuk, periksa diff yang dihasilkan, lalu merge; merge ke branch induk bukan bukti main sudah memuatnya.

## Draf buta dan tinjauan independen

Selama usulan peran, setiap irisan menerima dua draf buta dari brief yang sama, satu oleh Sol dan satu oleh Opus. Pekerja Sol menilai keduanya per skill menurut kesetiaan cakupan, ketepatan dan keamanan, determinisme, trigger dan evaluasi, serta kehematan. Pekerja memilih satu dasar dan hanya menggabungkan bagian yang terbukti lebih baik dari draf lain. Kedua paket peran menggunakan lima irisan. Skrip sengaja dirusak untuk membuktikan test menolak kesalahan yang dituju.

Astra meninjau hasil terintegrasi dan bukti sebenarnya, bukan klaim penyelesaian pekerja. Temuan memiliki ID stabil, tingkat blocker/should/nit, skenario kegagalan, dan patch minimal. Koordinator memperbaiki atau menyanggah setiap temuan dengan bukti, lalu meminta tinjauan lagi. Putaran tercatat berlanjut sampai FULL AGREEMENT; persetujuan adalah hasil tinjauan, bukan bukti perilaku runtime. Setelah penghentian peran, draf ganda dikhususkan untuk isi berisiko tinggi yang kebutuhannya lebih dahulu ditunjukkan oleh baseline gagal.

## Adopsi dan asal-usul legal

Penyalinan dibatasi lisensi: materi MIT dan Apache-2.0 dapat diadopsi; materi copyleft, non-commercial, atau tanpa lisensi tidak dapat diadopsi. Adaptasi Apache mempertahankan teks NOTICE wajib dan penandaan berkas yang diubah. roadmap.sh hanya menyediakan ide cakupan dan tidak pernah disalin.

Setiap kontributor yang materinya dipertahankan membutuhkan berkas legal sendiri. Adaptasi mencatat URL sumber, revisi commit lengkap, hash berkas asli, berkas tujuan, materi yang dipertahankan, dan perubahan lokal dalam manifest per berkas. Tinjauan membandingkan sumber asli yang dipatok dengan tujuan. Pemeriksaan otomatis menangkap field atau berkas atribusi yang rusak maupun hilang; pemeriksaan tidak membuktikan atribusi lengkap atau hash asli yang benar tanpa memeriksa sumber. [Kontrak asal-usul](how-and-why.md#mempertahankan-asal-usul) dan [skema penulisan](../../docs/authoring-guide.md#provenance-manifests) menyediakan prosedur yang dipelihara.

## Skill dan alat untuk membuat skill

Metode ini menjelaskan cara pekerjaan pembuatan diatur. Orchestrator mengikutinya secara manual dalam sesinya sendiri; ini bukan klaim bahwa setiap skill yang disebutkan benar-benar dimuat. Brief pekerja mewajibkan panduan penulisan repositori, `AGENTS.md`, dan gaya komunikasi. Arm evaluasi diisolasi dari koleksi skill terpasang: keduanya menerima dependensi wajib yang sama, sementara hanya treatment menerima kandidat yang disalin dari checkout.

| Metode milik koleksi | Penggunaan untuk membuat skill |
| --- | --- |
| [`writing-for-agents`](../../skills/writing-for-agents/SKILL.md) | Penulisan instruksi, trigger sempit, kriteria penyelesaian, dan persyaratan baseline-first |
| [`clear-communication`](../../skills/clear-communication/SKILL.md) | Prosa yang setia, sederhana, dan hemat serta gaya dokumen dan instruksi skill |
| [`agent-orchestrator`](../../skills/agent-orchestrator/SKILL.md) | Satu pemilik koordinasi, integrasi, dan penerimaan |
| [`work-decomposition`](../../skills/work-decomposition/SKILL.md) | Kepemilikan, dependensi, delegasi berguna, dan anggaran terbatas |
| [`agent-briefing`](../../skills/agent-briefing/SKILL.md) | Instruksi pekerja mandiri dan bukti yang disebutkan |
| [`agent-debate`](../../skills/agent-debate/SKILL.md) | Posisi buta dan penyelesaian perbedaan pendapat berbasis bukti |
| [`result-verification`](../../skills/result-verification/SKILL.md) | Memeriksa laporan terhadap artefak sumber dan menjalankan ulang bukti acceptance |
| [`decision-log`](../../skills/decision-log/SKILL.md) | Menyimpan keputusan, catatan dispatch, dan keadaan proses saat konteks hilang |
| [`project-guardrails`](../../skills/project-guardrails/SKILL.md) | Mengubah persyaratan yang dapat ditegakkan menjadi pemeriksaan repositori |
| [`correct`](../../skills/correct/SKILL.md) | Membuat kesalahan nyata berulang gagal pada pemeriksaan tertinggi yang sesuai |
| [`research`](../../skills/research/SKILL.md) | Dossier sumber primer dan fakta adopsi |
| [`grilling`](../../skills/grilling/SKILL.md) | Menyelesaikan keputusan penting dengan pengguna |
| [`change-review`](../../skills/change-review/SKILL.md) | Membandingkan perubahan sebenarnya dengan Standards dan Spec |
| [`sol-loop`](../../skills/sol-loop/SKILL.md) | Tinjauan, perbaikan, dan pemeriksaan ulang terbatas |
| [`benchmark-checklist`](../../skills/benchmark-checklist/SKILL.md) | Menjaga klaim pengukuran tetap sebanding dan dibatasi bukti |
| [`file-pr`](../../skills/file-pr/SKILL.md) | Judul dan isi PR berdasarkan diff final |

| Alat repositori | Yang diperiksa atau dilakukan |
| --- | --- |
| `skills-ref` yang dipatok | Validasi skema referensi Agent Skills |
| `scripts/check-skills.py` | Aturan paket milik koleksi, manifest, skrip, dan struktur berkas legal |
| `scripts/check-catalog.py` | Keanggotaan katalog, nama, dependensi, dan cakupan struktural status evaluated |
| `scripts/build-profiles.py` | Closure instalasi wajib dan drift profil |
| `scripts/build-host-config.py` | Pratinjau, penerapan, dan pemeriksaan kebijakan pemanggilan host milik koleksi |
| `scripts/check-freshness.py` | Melaporkan fakta khusus versi yang perlu diverifikasi ulang |
| `scripts/build-docs.py` | Menghasilkan inventaris dan hasil untuk manusia; menolak keluaran usang, tautan rusak, dan drift bilingual |
| `scripts/install-skills.py` | Pratinjau dan penerapan instalasi milik koleksi dengan pemeriksaan dependensi serta kepemilikan |
| `scripts/eval-skill.py` dan `scripts/evalharness/` | Menyiapkan proses host berpasangan yang terisolasi dan menyimpan pengamatannya |
| Vale dan gaya `clear-communication` | Memeriksa prosa Inggris secara mekanis |
| zizmor | Menganalisis keamanan GitHub Actions |
| `tests/<skill>/run.sh` dan suite fixture repositori | Menolak kesalahan yang dituju, menerima pekerjaan valid, dan menguji setup berulang |
| `scripts/validate.sh` | Menjalankan pemeriksaan deterministik repositori bersama; tidak menjalankan evaluasi model |

Perintah penulisan, evaluasi, instalasi, dan penyerahan sebenarnya berada dalam [prosedur untuk agen](../../docs/skill-workflows.md), [panduan evaluasi](../../docs/running-evals.md), dan [prosedur validasi](../../docs/validating.md). Ketersediaan alat tidak memberi izin pembelanjaan model, publikasi, atau merge.

## Kampanye evaluasi dan batasannya

Setiap contoh berpasangan menggunakan sesi baru terisolasi, home sementara, settings nonkandidat dan dependensi yang sepadan, serta tanpa settings pribadi, plugin, atau memory dalam arm evaluasi. Aktivasi berasal dari pembacaan isi terpasang atau pemilihan native tepercaya: Skill/pembacaan Claude dan injeksi/pembacaan native Codex. Perbandingan valid membuktikan isolasi dan penyelesaian, bukan perilaku benar atau nilai tambah. Percobaan invalid tidak pernah dihitung sebagai kegagalan skill atau cakupan yang berhasil.

Kebijakan status yang ditinjau mewajibkan pasangan valid pada byte final untuk setiap Activation dan Near miss serta tanpa hurt yang belum selesai; kriteria Outcome wajib ditinjau dalam kampanye. Gate deterministik katalog memeriksa cakupan catatan valid/selesai, bukan seluruh syarat semantik tersebut. [Halaman hasil](eval-results.md) menambahkan pencocokan digest tanpa mengubah gate itu.

| Checkpoint kampanye | Perbandingan dan penilaian yang dilaporkan | Batasan |
| --- | --- | --- |
| Seluruh pekerjaan inti Codex | Sekitar 1,000 pasangan di seluruh kampanye inti dan tindak lanjut | Total kampanye perkiraan; jangan menjumlahkan checkpoint tumpang tindih sebagai kasus unik |
| PR #5 | 140 pasangan; 37 added / 94 matched / 5 hurt; tindak lanjut 70 pasangan melaporkan 17 / 51 / 1 | Penilaian yang disebutkan tidak mencakup seluruh total pasangan |
| PR #6 | 120 pasangan; 39 added / 75 matched / 2 hurt; tindak lanjut 60 pasangan | Rincian outcome tindak lanjut tidak diberikan |
| PR #7 | 113 pasangan; 29 added / 72 matched / 3 hurt; tindak lanjut 50 pasangan | Penilaian yang disebutkan tidak mencakup seluruh total pasangan |
| Checkpoint Codex berikutnya | Kampanye final 80 pasangan; dua skill terakhir 30 pasangan | Checkpoint kampanye terpisah, bukan klaim total yang tidak tumpang tindih |
| Claude putaran 1 | 398 dari 423 perbandingan valid; Outcome 9 added / 44 matched / 5 hurt | Percobaan invalid dikecualikan; hurt memicu koreksi |
| Claude putaran 2 | Seluruh 25 perbandingan invalid diulang menjadi valid; koreksi `retro`, `interrogate`, `why`, dan `project-guardrails` | Putaran berikutnya membuktikan perilaku final yang dikoreksi |
| Claude putaran 3–4 | Batas sumber `retro` dikoreksi; checkpoint final 13 added / 1 matched / 0 hurt | Himpunan tinjauan final terbatas, bukan seluruh kampanye |
| Tindak lanjut pembersihan peran | Empat skill yang berubah memiliki 31 contoh trigger yang diulang pada kedua host: 62 pasangan | `agent-orchestrator`, `agent-briefing`, `codebase-design`, `writing-for-agents`; skill terakhir tetap unevaluated sambil menunggu Outcome baseline-first |
| Tindak lanjut Outcome baseline-first | Lima pasangan Outcome Codex khusus untuk `writing-for-agents` | Dengan laporan baseline yang diberikan (premis fixture, bukan sesi sungguhan) atau tanpa izin model: 2 added / 1 matched / 0 hurt ([baseline terekam lulus](../../skills/writing-for-agents/evals/results/2026-11-10-codex-gpt-6.1-sol-outcome-4-recorded-pass.md), [baseline terekam gagal](../../skills/writing-for-agents/evals/results/2026-11-10-codex-gpt-6.1-sol-outcome-4-recorded-fail.md), [tanpa izin model](../../skills/writing-for-agents/evals/results/2026-11-10-codex-gpt-6.1-sol-outcome-5-unauthorized.md)). Dua pasangan sebelumnya memakai runner tiruan yang mudah dikenali dan kesimpulannya dibatasi ([tiruan lulus](../../skills/writing-for-agents/evals/results/2026-11-10-codex-gpt-6.1-sol-outcome-4-passing-baseline.md), [tiruan gagal](../../skills/writing-for-agents/evals/results/2026-11-10-codex-gpt-6.1-sol-outcome-4-failing-baseline.md)). Kampanye ini memakai pengendali kecil untuk memilih Outcome; [Run and review evals](../../docs/running-evals.md) menjelaskan jalur biasanya. Skill itu kemudian ditandai evaluated dalam [PR #15](https://github.com/cravingmaker/skills/pull/15) |

Ringkasan pembuatan melaporkan bahwa setiap hurt inti dikoreksi dan diuji ulang sebelum checkpoint evaluated. Checkpoint pembersihan adalah riwayat berikutnya: perubahan byte memperbarui kewajiban bukti terkait. Katalog saat ini dan tampilan catatan yang dihasilkan tetap merupakan sumber terpisah; riwayat ini tidak diam-diam mengubah keduanya. Pemilih contoh biasa harness menjalankan Activation dan Near miss, sehingga kampanye ini menjalankan Outcome baseline-first sebagai job terpisah, dengan bukti pelaksanaannya sendiri.

Model kuat menyamai hasil pada sebagian besar tugas. Nilai paling jelas berasal dari pemeriksaan yang menolak kesalahan, batas kewenangan, dan bukti wajib. Kebijakan manual-only menyembunyikan entri dari daftar model tetapi tidak mencegah pembacaan berkas; contoh Claude yang tercatat tidak terulang dalam proses baru. Lihat [batas yang diketahui](known-issues.md) dan [perbedaan host](harness-differences.md) sebelum menggeneralisasi hitungan apa pun.

## Peralihan ke koleksi milik sendiri

Operasi 2026-11-09 menginventarisasi kedua host, menyimpan catatan rollback privat terbatas, menyiapkan pengganti dalam home sementara, dan memeriksa berkas serta kebijakannya. Operasi meng-uninstall plugin Matt Pocock dari Claude Code dan Codex. Port pstack, tstack, dan Superpowers sudah tidak ada; ketiganya tidak baru di-uninstall dalam operasi itu.

Sebanyak 58 skill milik koleksi dipasang ke kedua lokasi skill pengguna. Sesi baru memverifikasi discovery dan perintah manual. PR #10 membebaskan reservasi sumber lama setelah keadaan yang diamati dibuktikan. [Checklist arsip](cutover.md) mempertahankan pemeriksaan wajib yang direncanakan dan disiplin rollback; [Memulai](getting-started.md) adalah panduan instalasi saat ini.

## Eksperimen peran dan keputusan berhenti

Usulan mencakup 17 router peran beserta kapabilitasnya: backend, frontend, mobile, UI/UX, QA, DevOps, sysadmin, security, data engineer, data analyst, data scientist, technical writer, SEO, business analyst, financial analyst, marketing, dan copywriter. Setelah backend, urutan yang diminta adalah DevOps, sysadmin, security, data engineer, data analyst, lalu data scientist.

`backend-engineer` dalam PR #11 dan `devops-engineer` dalam PR #12 masing-masing berisi 22 skill, dibangun dalam lima irisan draf buta dan ditinjau sampai FULL AGREEMENT. Penyusunan sysadmin dimulai tetapi dibatalkan. DevOps tidak pernah dievaluasi.

Evaluasi backend mencakup contoh Codex dan trigger Claude sebelum dihentikan pada 147 dari rencana 432 pasangan dan 493 dari anggaran 1,100 proses model. Dari 15 Outcome yang ditinjau, satu menambah nilai (`api-design` menangkap ukuran halaman invalid), 13 matched, satu blocked, dan tidak ada hurt. Penyebut itu menjelaskan penghitung berbeda dan tidak boleh dibagi menjadi satu tingkat penyelesaian.

Pengguna menyimpulkan bahwa pengetahuan peran teknis tidak membenarkan pembuatan paket saat model kuat sudah mampu mengerjakan tugasnya. Sebanyak 44 skill yang disusun akan menambah sekitar 3,000 token deskripsi pada setiap sesi, membutuhkan lebih dari 1,000 proses evaluasi per peran, dan menimbulkan pemeliharaan fakta yang cepat berubah. Persetujuan tinjauan membuktikan mutu draf, bukan nilai ekonomis terhadap baseline.

Kedua PR ditutup tanpa merge dengan komentar penjelas, dan branch-nya disimpan sebagai referensi. Tindak lanjut pembersihan menghapus jejak peran. Pemeriksaan domain khusus proyek menjadi bagian guardrail proyek melalui `project-guardrails` dan `correct`; skill baru yang dapat digunakan ulang harus lebih dahulu membuktikan celah tanpa dirinya.

## Cara membuat skill baru sekarang

1. Periksa katalog dan cakupan yang ada untuk menemukan pemilik. Tetapkan satu pekerjaan yang dapat digunakan ulang dan trigger sempit. Jabatan peran atau domain yang dikenal saja tidak membuktikan kebutuhan.
2. Tulis contoh Activation, Near miss, dan Outcome yang dapat diamati beserta fixture sebelum isi skill. Tetapkan anggaran proses dan token sebelum kampanye besar dan isolasikan dalam worktree khusus.
3. Jalankan Outcome tanpa skill kandidat. Jika baseline sudah memenuhinya, berhenti; skill baru tidak diperlukan. Jika skrip dapat menegakkan aturan yang hilang, utamakan CI, lint, tipe, hook, atau pemeriksaan proyek lain.
4. Hanya setelah baseline gagal tercatat, tulis pemeriksaan, batas kewenangan, dan bukti wajib untuk celah itu. Gunakan template, panduan penulisan, dan prosedur lisensi/asal-usul. Batasi draf ganda pada isi dengan tingkat risiko yang membenarkannya.
5. Tambahkan entri katalog dan cakupan, hubungan dependensi wajib, contoh, dan fixture bermakna. Hasilkan profil, lihat pratinjau/terapkan kebijakan host bila perlu, lalu hasilkan kedua edisi handbook dengan panduan tujuan berguna.
6. Tinjau diff dan bukti sebenarnya. Buktikan guardrail menolak kesalahan yang dituju, menerima pekerjaan valid, dan berulang tanpa drift. Biarkan temuan yang belum selesai tetap terlihat.
7. Jalankan contoh berpasangan yang diizinkan dalam sesi baru terisolasi terhadap byte final, tinjau perilaku Outcome dan hurt, dan pertahankan status yang jujur. Validasi berkas terpilih dalam ekspor bersih dengan Vale wajib. Commit, publikasi, atau merge hanya dalam kewenangan tugas.

Ini [prosedur pembuatan skill](../../docs/skill-workflows.md#create-a-skill) yang dipelihara, dengan [standar penulisan](../../docs/authoring-guide.md) sebagai acuan rincian paket. Menulis dokumentasi atau menjalankan pemeriksaan deterministik saja tidak memberi izin kampanye model baru.

## Pengecualian protokol dan pelajaran

| Pengecualian atau kesalahan yang tercatat | Dampak dan pelajaran yang dipertahankan |
| --- | --- |
| Pekerja evaluasi dua kali membaca memory host saat startup meskipun brief melarang; ringkasan sesi mengaitkan paparan itu dengan injeksi memory otomatis Codex. Satu preflight menanyakan domain preferensi pribadi macOS, tanpa hasil atau perubahan | Proyek bersih dan batas dalam prosa tidak menjamin isolasi. Tegakkan discovery dan batas sumber dalam alat; jangan menerbitkan input pribadi. Ini menyangkut pekerja kampanye, berbeda dari arm pasangan terisolasi. |
| Penulisan sementara Claude awal masuk ke root temp bersama | Perbaiki root temp per arm; batalkan validitas perbandingan terdampak alih-alih menyalahkan skill. |
| Anak hasil fork sempat melebihi batas konkurensi | Tolak fork tak terkontrol dan hitung setiap start model. |
| Cluster PostgreSQL sekali pakai dihentikan dengan kill tanpa shutdown | Tiga puluh dua segmen shared-memory menumpuk sampai batas macOS menghalangi cluster baru. Pembersihan membutuhkan izin pengguna; matikan database test dengan benar. |
| Orchestrator berpindah branch saat evaluasi membaca checkout | Hentikan proses terdampak dan ulangi dari worktree khusus dengan byte sumber stabil. |
| Pemisahan kata scalar zsh diasumsikan dua kali; Bash sistem macOS lebih lama | Berikan daftar argumen atau array sebenarnya dan periksa interpreter yang digunakan; `/bin/bash` adalah Bash 3.2. |
| Catatan evaluasi yang tidak terkait ikut masuk commit dokumentasi | Catatan untracked dapat memengaruhi gate status katalog. Pilih kandidat secara eksplisit dan validasi ekspor bersih. |
| Process group yang hanya berisi zombie di macOS membuat `killpg` melempar EPERM dalam test zsh | Sebelum perbaikan, 17 dari 24 proses paralel gagal; setelahnya, nol gagal. Ini hitungan pengulangan test yang dilaporkan, bukan estimasi keandalan universal. |

Gejala dan respons yang terus berlaku berada dalam [Hal yang perlu diperhatikan](gotchas.md), sementara [Masalah yang diketahui](known-issues.md) membedakan cacat yang diperbaiki dari bukti yang tidak tersedia. Catatan insiden di sini mempertahankan pelajarannya tanpa menerbitkan ulang diagnostik privat.

## Retrospektif

Retrospektif 2026-11-10 menilai baik inti milik koleksi, guard deterministik yang menangkap masalah nyata, tinjauan independen yang menemukan cacat penting, dan bukti yang mendukung penghentian pekerjaan bernilai lemah. Hasil inti berguna meskipun perluasan peran dihentikan.

Retrospektif juga mengidentifikasi pembuatan sebelum pengukuran, kontrol biaya terlambat yang hanya membatasi konkurensi tanpa total anggaran token/proses, draf ganda yang tidak sepadan, kebersihan lingkungan evaluasi lemah, kesalahan koordinator yang dapat dihindari, dan perluasan cakupan menuju overengineering.

Aturan hasilnya adalah baseline terlebih dahulu, pemeriksaan proyek sebelum skill baru, worktree evaluasi khusus, validasi ekspor bersih, shutdown database yang benar, perubahan base PR bertingkat sebelum merge, dan anggaran proses/token eksplisit sebelum pekerjaan besar. Aturan ini menjadi bagian prosedur yang dipelihara atau guard yang dapat dijalankan; retrospektif mencatat alasan penerapannya.

## Ringkasan publik dan bukti privat

Catatan Markdown yang dikomit adalah ringkasan publik. Trace mentah, respons, artefak, dan berkas perbandingan tetap di luar Git demi privasi dan ukuran. Bukti mentah untuk 1.535 dari 1.541 catatan diarsipkan secara privat: satu arsip terkompresi per skill (58 berkas) di Google Drive milik pemilik, dipindai untuk kredensial dan token sebelum diunggah, dengan akses khusus pemilik yang sudah diperiksa pada berkas yang diunggah. Berkas mentah untuk enam catatan lainnya hilang sebelum diarsipkan.

Baris **Private raw evidence** di setiap catatan menautkan arsip skill-nya dan menyebut folder catatan di dalamnya; hanya pemilik yang bisa membuka tautan itu. Di dalam catatan, path mentah tetap berupa teks kode berlabel "local only, not committed", karena path itu menunjuk berkas di dalam arsip, bukan di repositori. Catatan baru dimulai dengan label lokal itu dan mendapat baris arsip setelah buktinya diunggah. Writer mempertahankan perbedaan itu dan pemeriksaan dokumentasi menolak tautan catatan ke berkas repositori yang hilang. [Halaman hasil](eval-results.md) publik menggunakan ringkasan yang dikomit; halaman itu tidak pernah menganggap berkas mentah yang tidak ada sebagai bukti yang baru diperiksa. Rincian akun privat, susunan penyimpanan, path pribadi, dan transkrip mentah sengaja tidak diterbitkan.
