> **Dokumentasi untuk manusia.** Agen hanya boleh membaca halaman ini jika diminta oleh seseorang.

Bahasa: [English](../harnesses.md) · [Bahasa Indonesia](harnesses.md)

# Harness yang didukung

Claude Code dan Codex CLI memiliki bukti tercatat tentang instalasi, discovery, pemanggilan, dan evaluasi berpasangan. T3 Code adalah antarmuka untuk penyedia tersebut; T3 Code bukan host model ketiga yang dievaluasi secara independen dalam repositori ini.

## Daftar isi

- [Membaca tingkat dukungan](#membaca-tingkat-dukungan)
- [Versi host yang tercatat](#versi-host-yang-tercatat)
- [Yang dibuktikan instalasi](#yang-dibuktikan-instalasi)
- [Yang dibuktikan discovery dan routing](#yang-dibuktikan-discovery-dan-routing)
- [Yang dibuktikan evaluasi](#yang-dibuktikan-evaluasi)
- [Host lain dan versi mendatang](#host-lain-dan-versi-mendatang)
- [Ringkasan tercatat menurut host](#ringkasan-tercatat-menurut-host)
- [Platform](#platform)

## Membaca tingkat dukungan

"Didukung" dibatasi oleh bukti yang tersedia, bukan janji bahwa semua host menyediakan alat atau kebijakan yang sama.

| Tingkat | Arti |
| --- | --- |
| Format | Paket mengikuti spesifikasi Agent Skills |
| Installed | Installer milik koleksi menghasilkan dan memeriksa berkas/settings wajib |
| Discovered | Inventaris host atau sesi baru menampilkan nama yang diharapkan |
| Invoked | Event native yang didukung atau pembacaan isi membuktikan pemilihan |
| Evaluated | Sesi kandidat/tanpa kandidat yang sepadan tersedia untuk contoh yang diwajibkan |
| Surface verified | Perilaku sebenarnya yang disebutkan dijalankan pada artefak yang diidentifikasi |

Instalasi tidak membuktikan aktivasi. Aktivasi tidak membuktikan ketepatan semantik. Kelulusan lokal pada fixture tidak membuktikan deployment atau perilaku produksi.

## Versi host yang tercatat

Peralihan dan kampanye host yang tercatat menggunakan versi ini; versi lebih baru membutuhkan pemeriksaan baru.

| Permukaan | Konteks versi/model yang tercatat | Cakupan bukti |
| --- | --- | --- |
| Claude Code | 2.1.311; evaluasi Claude menggunakan `claude-opus-5-5`, high effort | Instalasi pengguna, visibilitas manual, discovery sesi baru, contoh berpasangan |
| Codex CLI | 0.167.0; proses model default yang disimpan melaporkan `gpt-6.1-sol` | Instalasi pengguna, kebijakan pemanggilan yang dihasilkan, discovery, contoh berpasangan |
| T3 Code | Tidak ada versi rilis antarmuka terpisah yang diikat oleh pengujian yang dirujuk | Menjalankan Claude atau Codex dan dapat menyediakan alat dispatch, isolasi, tautan PR, dan watcher |
| Host Agent Skills lain | Tidak ada versi atau kampanye perilaku yang tercatat di sini | Paket sesuai spesifikasi; adapter instalasi dan perilaku belum diuji |

[PR kampanye host](https://github.com/cravingmaker/skills/pull/9), [PR peralihan](https://github.com/cravingmaker/skills/pull/10), dan [bukti discovery](install-and-discovery-proof.md) menyediakan rujukan publik. Perbedaan model efektif adalah bagian pengamatan, bukan perbandingan terkontrol yang hanya membedakan host.

## Yang dibuktikan instalasi

Installer milik koleksi menyelesaikan closure wajib transitif, mendeteksi konflik, mencatat kepemilikan, dan mendukung mode salin atau symlink. Generator host memeriksa berkas kebijakan manual Codex. Adapter eksplisit Claude memeriksa skema native dan prioritas settings sebelum mengubah override terpilih.

Pemeriksaan discovery salin dan symlink yang tercatat berjalan di luar checkout sumber pada kedua CLI sebenarnya. Peralihan yang diamati memasang seluruh inti milik koleksi ke direktori skill pengguna setiap host dan memverifikasi bahwa instalasi ulang tidak mengubah apa pun. [Panduan instalasi](getting-started.md) menyediakan perintah saat ini.

## Yang dibuktikan discovery dan routing

Pengukuran discovery awal menggunakan profil peran kecil yang dipatok, snapshot skill yang sudah ada, serta peran/deskripsi tambahan sintetis. Pengukuran itu menunjukkan inventaris dan prompt yang diuji, termasuk pemendekan deskripsi Codex pada kasus cache lebih luas. Pengukuran tidak menetapkan anggaran daftar persis bagi model produksi langsung.

Eksperimen routing yang tercatat sesuai dengan himpunan pemilihan pertama yang sudah ditetapkan pada skenario yang diuji. Eksperimen menguji pemilihan awal dengan instruksi routing-only eksplisit dan model default berbeda. Eksperimen tidak menjalankan seluruh alur delegasi, membuktikan ketepatan routing universal, atau mereproduksi semua alat plugin langsung dan sumber terkelola.

Sesi peralihan baru memberikan bukti lebih lanjut tentang nama terpasang inti lengkap dan visibilitas manual. Gunakan [profil yang dihasilkan](routing.md) untuk dependensi saat ini, bukan jumlah profil lama.

## Yang dibuktikan evaluasi

Harness berpasangan menyiapkan home, konfigurasi, cache, fixture, dan sesi baru yang privat. Harness memverifikasi kesamaan inventaris nonkandidat dan model dalam satu pasangan. Aktivasi, ketepatan hasil, dan biaya alur yang tidak perlu dinilai terpisah.

Claude dan Codex memiliki trace aktivasi serta perilaku sandbox berbeda. [Panduan perbedaan harness](harness-differences.md) menjelaskan keduanya. Ringkasan publik mempertahankan percobaan invalid dan batasan semantik atau protokol tertentu; percobaan invalid tidak mendapat kredit hasil.

Tidak ada jaminan menyeluruh tentang alat browser/native langsung, hosted CI, syarat layanan PR nyata, panel penyedia independen, atau merge produksi yang berhasil. Baca [batas yang diketahui](known-issues.md#hal-yang-belum-diuji).

## Host lain dan versi mendatang

Host yang kompatibel dengan Agent Skills mungkin dapat membaca `SKILL.md` yang sama dan sesuai spesifikasi. Itu saja tidak mengimplementasikan `skillOverrides` Claude, `agents/openai.yaml` Codex, catatan kepemilikan installer ini, atau API delegasi tertentu.

Sebelum mengklaim dukungan setara, verifikasi root discovery, nama perintah eksplisit, penekanan manual, closure wajib, prioritas settings, alat, sandbox, dan bukti aktivasi host yang sebenarnya. Gunakan lingkungan sekali pakai dan simpan identitas versi/sumber. Pembaruan host dapat mengubah fakta tersebut, sehingga versi tercatat menjadi batas yang berguna, bukan klaim permanen.

## Ringkasan tercatat menurut host

Tabel yang dihasilkan menghitung ringkasan historis yang disimpan pada semua revisi. Valid berarti perbandingan terisolasi yang selesai; status itu tidak menjamin ketepatan atau cakupan byte final.

<!-- BEGIN GENERATED eval-records: generated by scripts/build-docs.py; edit the catalog or SKILL.md files, then rerun it -->

| Host yang tercatat | Model efektif | Valid | Tidak valid | Total |
| --- | --- | ---: | ---: | ---: |
| `2.1.311 (Claude Code)` | `claude-opus-5-5` | 626 | 108 | 734 |
| `2.1.311 (Claude Code)` | `default` | 0 | 2 | 2 |
| `codex-cli 0.167.0` | `default` | 0 | 3 | 3 |
| `codex-cli 0.167.0` | `gpt-6.1-sol` | 807 | 0 | 807 |
| Semua | | 1433 | 113 | 1546 |

<!-- END GENERATED eval-records -->

## Platform

Sesi host yang tercatat berjalan pada macOS. CI repositori menjalankan pemeriksaan deterministik dan fixture pada Ubuntu; CI tidak menjalankan kedua host model. Discovery dan pemanggilan host Linux serta Windows belum diuji.
