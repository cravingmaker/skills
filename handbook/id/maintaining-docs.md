> **Dokumentasi untuk manusia.** Agen hanya boleh membaca halaman ini jika diminta oleh seseorang.

Bahasa: [English](../maintaining-docs.md) · [Bahasa Indonesia](maintaining-docs.md)

# Memelihara handbook ini

Edit penjelasan yang membutuhkan pertimbangan dan hasilkan ulang inventaris dari berkas sumbernya. Generator juga gagal saat rujukan untuk agen masuk ke handbook bagi manusia.

## Daftar isi

- [Pemilik sumber](#pemilik-sumber)
- [Menghasilkan dan memeriksa](#menghasilkan-dan-memeriksa)
- [Memperbarui kedua bahasa bersama](#memperbarui-kedua-bahasa-bersama)
- [Memahami pemeriksaan](#memahami-pemeriksaan)
- [Menjauhkan agen secara default](#menjauhkan-agen-secara-default)
- [Memperbarui bukti tanpa melebihkannya](#memperbarui-bukti-tanpa-melebihkannya)

## Pemilik sumber

| Isi | Sumber acuan |
| --- | --- |
| Keanggotaan skill, jenis, penugasan cakupan, alias, preferensi pemanggilan, status evaluasi | `catalog/skills.yaml` |
| Deskripsi, hubungan wajib, rujukan metode bersyarat berdasarkan nama | Setiap `skills/*/SKILL.md` dan referensi/aset Markdown milik koleksi yang ditautkan langsung |
| Contoh Activation, Near miss, dan Outcome | `evals/examples.md` milik setiap skill |
| Hasil evaluasi | Catatan Markdown yang dikomit di bawah `skills/*/evals/results/`, tabel dan baris Value yang ditinjau, dibandingkan dengan digest paket skill saat ini |
| Keanggotaan profil | Closure wajib, diperiksa terhadap `catalog/profiles/` |
| Penjelasan, contoh alur lengkap, batasan status | Teks handbook yang ditulis dengan tautan sumber publik |
| Changelog | Metadata PR yang di-merge dan riwayat main |

Bagian yang dihasilkan memiliki pasangan penanda `BEGIN GENERATED` dan `END GENERATED`. Edit sumbernya, bukan baris hasilnya. Katalog menentukan keanggotaan dan mode. `handbook/intent-guide.json` menambahkan penjelasan tujuan, prompt, dan pekerjaan serupa tanpa menyalin status atau hubungan wajib. Kelompoknya menentukan judul dan urutan baris tabel README yang terlihat. Setiap entri katalog membutuhkan tepat satu baris panduan tidak kosong; baris tidak dikenal, hilang, atau ganda membuat pemeriksaan gagal. Setiap kelompok juga membutuhkan `heading_id`; setiap baris membutuhkan `want_id` dan `neighbor_id`. Field `prompt` tetap berbahasa Inggris dalam kedua edisi.

## Menghasilkan dan memeriksa

Gunakan Python 3.12 atau lebih baru. Generator hanya menggunakan standard library dan tidak memanggil model atau host.

```sh
python3.12 scripts/build-docs.py --help
python3.12 scripts/build-docs.py
python3.12 scripts/build-docs.py --record-sync
python3.12 scripts/build-docs.py --check
tests/build-docs/run.sh
REQUIRE_VALE=1 ./scripts/validate.sh
```

Jika Python shell lebih lama, gunakan `uv run --python '>=3.12' python` sebagai pengganti `python3.12`. Mode default menulis bagian yang dihasilkan dalam kedua bahasa. `--record-sync` hanya menulis manifest hash teks buatan setelah memvalidasi kedua edisi; mode ini menolak struktur berbeda, bagian generasi usang, dan tautan invalid. Mode check hanya membaca dan keluar dengan 1 jika ada drift hasil generasi atau hash bilingual, panduan tujuan hilang, maupun temuan input/tautan. Semua pemeriksaan sumber, penanda, dan tautan berjalan sebelum mode tulis mengubah keluaran. Setiap mode yang berhasil mencetak ringkasan JSON ke stdout; diagnostik menuju stderr.

Data dan bantuan menuju stdout. Diagnostik menuju stderr. Exit 0 berarti berhasil; 1 berarti drift, rujukan terlarang, atau input invalid; 2 berarti penggunaan command-line salah. Pembaca YAML kecil sengaja menolak bentuk yang tidak didukung alih-alih menebak; perluasan skema sumber membutuhkan fixture parser yang sesuai.

## Memperbarui kedua bahasa bersama

Perbarui halaman Inggris dan pasangannya di `handbook/id/` dalam perubahan yang sama setiap kali salah satu edisi berubah. Pertahankan himpunan halaman, urutan bagian, tingkat heading, tabel, daftar, blok kode, dan tujuan tautan yang sama. Terjemahkan prosa dan label heading; pertahankan perintah, identifier, dan kode. Arahkan tautan lokal handbook ke edisi tersebut dan heading terjemahannya. Setiap halaman dimulai dengan pemberitahuan khusus manusia dalam bahasanya dan menyediakan pilihan bahasa.

Generator menulis setiap blok handbook ke kedua edisi. Tabel labelnya menerjemahkan teks tampilan tetap; deskripsi, contoh, dan nilai katalog dari sumber tetap persis. Field tujuan editorial tersedia dalam kedua bahasa. Blok generasi baru otomatis mendapat lokasi bahasa Indonesia.

Jalankan generator, tinjau kedua edisi, lalu jalankan `scripts/build-docs.py --record-sync`. `handbook/id/SYNC.json` mencatat SHA-256 kedua halaman setelah blok generasi dikeluarkan, termasuk kode buatan dan pilihan bahasa. `--check` menolak pasangan hilang, struktur berurutan atau tujuan tautan terpetakan yang berbeda, atau salah satu hash yang berbeda dari manifest. Diagnostik menyebut kedua halaman dan meminta editor memperbarui kedua bahasa lalu mencatat sinkronisasi. Pencatatan menolak pasangan dengan struktur berbeda dan tidak menerjemahkan atau menjamin kesetaraan makna; peninjau bertanggung jawab atas kesetiaan kalimat.

Vale tetap memeriksa halaman handbook Inggris melalui pemilihan `handbook/*.md` yang sudah ada dalam `scripts/validate.sh`. Halaman Indonesia berada satu tingkat lebih dalam dan tidak masuk pemilihan khusus Inggris itu. Gaya Inggris dan semua target Inggris yang sudah ada tetap sama.

## Memahami pemeriksaan

Validator memanggil `uv run --quiet --python '>=3.12' python scripts/build-docs.py --check` setelah pemeriksaan profil dan kebijakan host. Validator secara eksplisit menjalankan `tests/build-docs/run.sh` karena loop test skill hanya menjalankan direktori dengan paket skill yang sesuai. Validator juga memeriksa prosa handbook dan changelog.

Skill baru harus memiliki panduan tujuan yang berguna dalam tepat satu kelompok di `handbook/intent-guide.json`. Hasilkan ulang setiap halaman yang berubah dan tambahkan bagian perintah terperinci untuk entri manual baru. Panduan hilang tetap merupakan kesalahan yang menggagalkan pemeriksaan.

Fixture membuktikan keluaran bersih, generasi ulang deterministik, urutan kategori README yang terlihat, penolakan skill hilang dan ganda, penolakan drift, penolakan metadata rusak, penolakan dependensi wajib hilang, penolakan drift profil, dan tautan terlarang dalam berkas representatif untuk agen. Fixture bilingual juga menolak halaman hilang, hash usang pada kedua bahasa, field tujuan Indonesia hilang, dan perbedaan struktur/tautan berurutan, serta membuktikan bahwa pencatatan menolak ketidakcocokan. Fixture evaluasi mem-parse catatan saat ini, memisahkan riwayat invalid dan byte usang, serta menolak tujuan tautan catatan yang hilang. Salinan generator yang sengaja dirusak harus gagal pada test tersebut. Fixture tidak menilai mutu prosa, perilaku host mendatang, atau bukti evaluasi mentah privat.

## Menjauhkan agen secara default

Handbook berada di luar tree `skills/` installer. Tidak ada instruksi default, skill, referensi, aset, template, atau skrip yang merujuk ke dalamnya. README singkat menjadi pintu masuk manusia. Setiap halaman handbook dimulai dengan pemberitahuan dokumentasi manusia.

Guard menolak path ke direktori manusia dari berkas untuk agen, termasuk tautan Markdown/HTML, definisi referensi, rujukan dalam font kode, dan path ter-encode. Laporan tinjauan yang secara eksplisit untuk manusia, generator, test-nya, dan validator adalah pengecualian terbatas. Guard tidak mengklaim memahami setiap path yang dirangkai secara dinamis atau petunjuk bahasa biasa. Pencarian filesystem luas atau instruksi manusia eksplisit tetap dapat menjangkau berkas ini.

Settings ignore host dapat mengurangi indexing tidak sengaja, tetapi tugas ini tidak memiliki bukti lintas host tentang perilaku persisnya. Aturan penolakan baca keras juga akan mencegah manusia meminta agen membaca handbook. Keduanya tidak ditambahkan di sini. Pemisahan, batas installer, pemberitahuan, dan pemeriksaan rujukan yang diuji adalah default yang berguna tanpa pembatasan tersebut.

## Memperbarui bukti tanpa melebihkannya

Perbarui issue hanya jika revisi saat ini dan permukaan yang diklaim memiliki bukti. Pertahankan label kegagalan historis dan percobaan invalid. Build dokumentasi deterministik yang bersih bukan hasil evaluasi model atau host langsung yang baru.

Changelog menggunakan satu entri per PR yang di-merge, terbaru lebih dahulu, dengan masuknya stack ke main dibedakan dari merge bertingkat sebelumnya. Beri label pekerjaan terbuka dan ditutup tanpa merge secara terpisah dari entri tersebut. Prosa publik tidak boleh memuat path privat, identitas pribadi, kredensial, atau transkrip tinjauan.
