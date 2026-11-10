> **Dokumentasi untuk manusia.** Agen hanya boleh membaca halaman ini jika diminta oleh seseorang.

Bahasa: [English](../recommended-flow.md) · [Bahasa Indonesia](recommended-flow.md)

# Alur yang disarankan

Alur biasa dimulai dari wawancara berbasis sumber, spec yang disepakati, tiket stabil, implementasi dengan bukti, lalu retrospektif yang diminta. Mulailah pada tahap yang dibutuhkan pekerjaan Anda; keputusan yang sudah disepakati atau perbaikan kecil tidak membutuhkan seluruh rangkaian.

## Daftar isi

- [Memilih titik awal](#memilih-titik-awal)
- [Menyiapkan sekali saat diperlukan](#menyiapkan-sekali-saat-diperlukan)
- [Menyepakati istilah dan keputusan](#menyepakati-istilah-dan-keputusan)
- [Menulis spec yang disepakati](#menulis-spec-yang-disepakati)
- [Menyetujui tiket stabil](#menyetujui-tiket-stabil)
- [Mengimplementasikan satu irisan atau seluruh graf](#mengimplementasikan-satu-irisan-atau-seluruh-graf)
- [Memilih cabang untuk ketidakpastian, cacat, dan tinjauan](#memilih-cabang-untuk-ketidakpastian-cacat-dan-tinjauan)
- [Memilih batas penyerahan](#memilih-batas-penyerahan)
- [Meninjau atau melanjutkan sesi](#meninjau-atau-melanjutkan-sesi)
- [Melihat peta tahap router yang tersedia](#melihat-peta-tahap-router-yang-tersedia)
- [Contoh lengkap: menambah keluaran JSON pada CLI](#contoh-lengkap-menambah-keluaran-json-pada-cli)

## Memilih titik awal

Berikan tujuan, input persis, cakupan penulisan, dan titik berhenti yang diinginkan kepada agen. Permintaan bahasa biasa dapat mengaktifkan metode yang dapat dipanggil model. Pilih perintah native untuk entri manual; gunakan `/<name>` di Claude dan `$<name>` di Codex.

Contoh prompt awal yang berguna: "Add JSON output to the word-count CLI, preserve its existing text output and errors, and stop after a local reviewed implementation." Permintaan lain, "get this ready without merging," sengaja memperluas batas penyerahan. Kedua permintaan itu tidak boleh diam-diam berubah menjadi deployment produksi.

Alur inti adalah `grill-with-docs → to-spec → to-tickets → implement or implement-spec → retro`. Retrospektif terakhir adalah pekerjaan yang diminta, bukan kampanye tambahan otomatis. Koleksi menggabungkan alur ini dengan metode penelusuran sumber, bukti, tinjauan, dan penyerahan yang diadopsi dari pstack dan tstack.

## Menyiapkan sekali saat diperlukan

Konfigurasi proyek memberi tahu metode pembentukan rencana tentang lokasi tracker, glosarium, dan ADR. Jika belum ada, minta secara eksplisit agar entri setup menetapkan kontrak tersebut. Entri ini memelihara satu blok Agent skills dan berkas yang berlaku di bawah `docs/agents/`.

Untuk contoh lokal, pilih direktori spec, direktori tiket, satu glosarium, dan direktori ADR. Konfigurasi dapat menyebut berkas semantik yang belum ada. Berkas itu dibuat hanya saat istilah atau keputusan perlu dicatat.

Setup tidak diperlukan untuk penggantian nama biasa, penelusuran sumber, atau tinjauan lokal. Jika konfigurasi pengajuan belum ada, metode pembentukan rencana dapat mengembalikan draf alih-alih mengarang tracker.

## Menyepakati istilah dan keputusan

Gunakan wawancara pencatat dokumen saat keputusan desain perlu dipertahankan bersama bahasa domain. Ketik `/grill-with-docs` atau `$grill-with-docs`, lalu sebutkan rencana dan batasan yang sudah ada.

Untuk contoh CLI, minta: "Keep default text output stable; help me settle the JSON schema and error behavior, and record resolved terms at the configured paths." Agen membaca kode dan keputusan yang sudah ada sebelum bertanya. Agen menanyakan kumpulan pertanyaan penting yang independen dan dapat dijawab saat itu, menyarankan jawaban, lalu menunggu.

Hasil serah terimanya adalah penutup yang dikonfirmasi: pilihan yang disepakati, asumsi yang dinyatakan, keputusan tertunda beserta penanggung jawab, dan langkah berikutnya. Entri glosarium yang disepakati dicatat dalam cakupan penulisan. ADR hanya diusulkan untuk pilihan mengejutkan yang sulit dibatalkan dan memiliki trade-off nyata, lalu ditulis setelah diterima.

Gunakan entri tanpa dokumen jika Anda ingin wawancara tetap dalam percakapan. Wawancara eksplisit menunggu konfirmasi sebelum menjalankan rencananya. Klarifikasi di dalam tugas mengisi celah tertentu milik pemanggil tanpa membuka kembali seluruh rencana.

## Menulis spec yang disepakati

Pilih entri spec setelah pemahaman disepakati. Contohnya: "Write up this confirmed close as a draft spec; do not file it yet."

Spec mempertahankan cakupan dan menggunakan user story bernomor. Setiap story menyatakan acceptance yang dapat diamati dan Proof yang disebutkan: permukaan yang dijalankan atau sumber yang dibuka, serta hasil yang diamati. Input berkas diikat dengan SHA-256 agar tahap berikutnya dapat mendeteksi drift.

Untuk contoh CLI, satu story dapat mewajibkan `--json` menghasilkan angka JSON sementara keluaran default tetap sama. Proof harus menjalankan CLI sebenarnya dan memeriksa stdout serta exit status. Unit test saja bukan pengamatan CLI yang dijanjikan.

Hasil serah terimanya adalah spec yang disetujui, sumber beserta hash-nya, test seam, acceptance, dan Proof. Pertanyaan terbuka tetap memiliki penanggung jawab dan membuat spec tetap berstatus draf. Tahap ini tidak memulai ulang wawancara atau mengimplementasikan fitur.

## Menyetujui tiket stabil

Pilih entri tiket dengan spec yang disetujui secara persis. Entri mengusulkan irisan vertikal, menyajikan blocker dan Proof, lalu meminta persetujuan pembagian sebelum mengajukannya. Pembagian yang sudah disetujui digunakan kembali.

Untuk contoh CLI, satu tiket dapat menambah perilaku JSON beserta pemeriksaan kompatibilitas. Tiket dependen dapat mencakup sisa perilaku help dan error yang didokumentasikan. Setiap irisan harus berguna dan dapat diverifikasi; tiket schema-only diikuti API-only biasanya pembagian yang keliru.

Tiket lokal menggunakan satu berkas `NN-slug.md` per tiket, nomor stabil, Status, checkbox acceptance, `Proof:` satu baris, serta nomor `Blocked by:` atau `None`. Jika tersedia, importer milik koleksi memvalidasinya terhadap spec yang disetujui secara persis. Jangan gabungkan tiket dalam satu berkas atau mengubah persyaratan yang disetujui selama impor.

Hasil serah terimanya adalah graf yang disetujui dan isi tiket persis. Refaktor mekanis luas dapat menggunakan expand, batch migrasi, dan contract, sementara konsumen yang di-deploy secara independen tetap memiliki kewajiban kompatibilitas.

## Mengimplementasikan satu irisan atau seluruh graf

Pilih entri satu irisan untuk satu tiket berizin atau perubahan yang disepakati. Entri menelusuri dasar pekerjaan, memilih bukti perilaku yang bermakna, membangun irisan, menjalankan pemeriksaan terkait, meninjau sendiri, dan melaporkan COMPLETE, PARTIAL, atau BLOCKED. Agen leaf tidak memulai peninjau atau pengendali kedua.

Pilih pelaksana graf untuk spec yang disetujui beserta tiketnya. Pelaksana mengimpor ID, status, blocker, acceptance, Proof, dan hash sumber yang ada tanpa wawancara atau pembagian baru. Satu koordinator bertanggung jawab atas branch integrasi, catatan, start pekerja, peninjau, percobaan ulang, dan penerimaan akhir.

Sebelum dispatch, koordinator mencatat anggaran terbatas dan memeriksa kepemilikan penulisan. Delapan adalah batas maksimum subagen aktif koleksi; batas pengguna atau host saat ini yang lebih rendah berlaku. Pekerja menerima rujukan persis dan brief leaf. Koordinator menjalankan ulang Proof yang disebutkan pada artefak pekerja dan kembali pada hasil terintegrasi sebelum menerima atau menutup tiket yang diizinkan.

Jika dispatch wajib atau isolasi milik host tidak tersedia, orchestrator tetap pada preflight berbasis sumber. Pelaksanaan pekerja dan penerimaan integrasi harus dilaporkan terhambat. Edit lokal bukan bukti bahwa alur delegasi yang diminta telah berjalan.

## Memilih cabang untuk ketidakpastian, cacat, dan tinjauan

Pilih cabang berdasarkan pertanyaan yang belum terjawab, bukan keinginan memuat lebih banyak skill. [Panduan tujuan yang dihasilkan](choosing-skills.md) dan [contoh batasan](skills.md) menyediakan rujukan lengkap.

Prototype menjawab pertanyaan desain terbatas dengan artefak sekali pakai. Contohnya: "Try two JSON error shapes with realistic CLI consumers; stop at the observed trade-off." Prototype tidak otomatis menjadi produksi atau mewajibkan branch dan push baru.

Riset menjawab pertanyaan faktual terbatas dari sumber primer. Gunakan sebelum keputusan yang bergantung pada fakta API atau spesifikasi. Penelusuran sumber menjelaskan jalur saat ini; alasan historis membutuhkan riwayat yang dapat diatribusikan.

Diagnosis dimulai dari gejala yang dilaporkan dan siklus umpan balik yang membedakan penyebab. Contohnya: "This CLI returns exit 0 on malformed JSON; reproduce it, rank causes, and verify the causal fix." Diagnosis statis atau hanya melalui rekaman dapat berguna tetapi harus menyatakan batas buktinya.

Pekerjaan test terlebih dahulu menggunakan seam publik yang bermakna dan kegagalan karena alasan yang diprediksi sebelum perbaikan. Edit kecil yang dapat dibatalkan tidak memerlukan test seremonial. Refaktor menetapkan perilaku yang ada sebelum memindahkannya.

Tinjauan perubahan melaporkan Standards dan Spec secara terpisah dan tidak mengedit produk. Sol loop menambahkan perbaikan berizin dan pemeriksaan ulang dalam batas putaran yang dinyatakan. Council memilih perilaku panel code-fix, design, atau report-only sesuai permintaan; penyedia yang disebutkan tetapi tidak tersedia dilaporkan, bukan diganti. Probe adversarial memisahkan bukti statis dari pengamatan runtime dan menghitung percobaan gagal dalam jatah yang dinyatakan.

## Memilih batas penyerahan

Nyatakan hasil akhir yang Anda inginkan sebelum proses pengiriman dimulai. Nama skill tidak membatalkan instruksi yang lebih sempit seperti "draft only," "do not post," atau "do not merge."

| Permintaan | Keadaan akhir yang diharapkan |
| --- | --- |
| "Write the PR body" | Draf judul/isi lokal berdasarkan diff; tanpa perubahan jarak jauh |
| "Create the PR" | PR yang diminta diajukan dan dibaca kembali beserta keadaan saat ini |
| "Watch this PR" | Root memiliki satu watcher yang didukung dan menangani hambatan yang diizinkan |
| "Full stop; prepare this without merging" | PR siap yang sudah diverifikasi, atau persetujuan/hambatan tersisa yang dinyatakan jelas; terbuka dan belum di-merge |
| "Full send; take this to a merged PR" | Merge melalui penjagaan setelah bukti, pemeriksaan, tinjauan, dan syarat repositori lulus |

Entri isi PR mengarah ke mode body-only dari metode penulisan PR, kecuali permintaan yang sama atau kewenangan tugas yang sudah ada mengizinkan pengajuan. Tugas pengajuan saja mengembalikan tautan dan keadaan; tugas itu tidak otomatis memulai pemantauan. Hanya root yang memantau, dan hanya saat diminta atau saat tindakan yang sudah diizinkan sedang menunggu.

Mode prepare-only harus meneruskan no-merge kepada setiap helper dan anak. Mode ini memeriksa auto-merge dan entri antrean miliknya, membatalkan mekanisme tertunda yang dimilikinya, lalu memverifikasi ketiadaannya. Mode ini juga membawa izin pengujian yang dibutuhkan tugas dari metode induk, dengan tetap tunduk pada batas tugas dan host yang lebih sempit.

Finish-to-merge tidak mengabaikan pemeriksaan, bot, CODEOWNERS, persetujuan, atau permintaan perubahan manusia yang wajib. Bukti harus mencakup head saat ini dan base yang relevan. Masukan lama yang belum selesai tetap relevan setelah push. PR dalam antrean belum merupakan PR yang di-merge; penyelesaian merge membutuhkan pembacaan kembali.

## Meninjau atau melanjutkan sesi

Minta retrospektif saat ingin belajar dari sesi sebenarnya. Berikan bukti yang diizinkan secara eksplisit saat privasi atau cakupan penting. Metode memisahkan berkas saat ini dari bukti historis dan mengutamakan pemeriksaan yang bekerja dibanding paragraf instruksi tambahan.

Gunakan catatan kelanjutan untuk sesi baru, catatan jangka panjang untuk proses yang diketahui, dan penelusuran riwayat saat lokasi lama tidak diketahui. Catatan mempertahankan rujukan persis, sisa anggaran, kepemilikan yang belum pasti, dan syarat pertama yang belum terpenuhi. Catch-up hanya membaca dan mempertahankan setiap keputusan pengguna yang masih tertunda, termasuk yang lebih lama daripada rentang default sejak pesan manusia terakhir.

## Melihat peta tahap router yang tersedia

[Tabel alur peran yang dihasilkan](routing.md#di-main-agent-orchestrator) menyebutkan setiap tahap router yang tersedia beserta metode bersyaratnya.

## Contoh lengkap: menambah keluaran JSON pada CLI

Pada 2026-11-09 alur utama berjalan dari awal sampai akhir dalam fixture Codex sekali pakai: CLI penghitung kata Python kecil yang mendapat flag `--json`. Berikut hasil setiap tahap. Proses berjalan pada Codex CLI 0.167.0 dengan `gpt-6.1-sol`; Claude Code tidak ikut dalam proses ini.

| Tahap | Yang Anda ketik | Hasil |
| --- | --- | --- |
| Setup | `$setup-agent-skills` | Satu blok `AGENTS.md` dan tiga berkas `docs/agents/`; pengulangan tidak mengubah apa pun; berkas glosarium dan ADR tetap tidak ada sampai dibutuhkan. |
| Pembentukan | `$grill-with-docs add --json output` | Pertanyaan diajukan hanya setelah membaca kode dan path domain. Istilah glosarium ditulis saat disepakati; ADR "exact JSON output contract" dan penutup ditulis hanya setelah diterima. |
| Spec | `$to-spec` | Lima story, masing-masing dengan acceptance yang dapat diamati dan Proof CLI nyata; semua 11 hash sumber sesuai saat diajukan; tanpa wawancara kedua. |
| Tiket | `$to-tickets` | Dua irisan vertikal (story 1 sampai 3, dan 4 sampai 5), tiket 02 terhambat oleh 01; importer keluar dengan 0. |
| Implementasi | `$implement-spec` | Satu koordinator, dua pekerja, dan satu peninjau baru: 3 dari anggaran 12 start. Test tiket 01 gagal karena alasan yang diprediksi sebelum fitur dibuat, lalu lulus. Penerimaan akhir menjalankan kelima Proof (22 pemanggilan CLI) dan delapan test. Peninjau tidak menemukan temuan Standards maupun Spec. |
| Pengiriman | "open a PR" | Branch integrasi di-push ke bare remote lokal dan PR simulasi dibaca kembali dengan head, base, pemeriksaan, dan thread-nya. Tanpa watcher dan tanpa merge. |
| Pembelajaran | `$retro` | Laporan yang memisahkan cacat harness dari seed test yang disengaja dan tidak mengusulkan penulisan ulang skill tanpa dasar. |

Yang tidak dibuktikan proses ini: pemanggilan subagen native (pekerja berjalan melalui adapter serial), API GitHub sebenarnya, bot, watcher atau merge, dan perilaku Claude Code apa pun. Proses ini juga mengungkap pembacaan panduan harness terpasang oleh evaluator luar sebelum memeriksa implementasi yang dipatok; kelulusan fixture tidak membuktikan evaluator sama sekali tidak membaca home sebenarnya. Proses menemukan satu cacat pada harness evaluasi, bukan pada skill: penghitung aktivasi Codex melewatkan pemilihan native `$<name>`. Cacat itu diperbaiki sebelum stack masuk ke `main`.
