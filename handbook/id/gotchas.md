> **Dokumentasi untuk manusia.** Agen hanya boleh membaca halaman ini jika diminta oleh seseorang.

Bahasa: [English](../gotchas.md) · [Bahasa Indonesia](gotchas.md)

# Hal yang perlu diperhatikan

Kebanyakan kejutan muncul saat visibilitas dianggap sama dengan akses, instalasi dengan eksekusi, atau draf dengan kewenangan menyerahkan hasil. Setiap entri di bawah menyebutkan gejala, penyebab, dan tindakan berikutnya yang berguna.

## Daftar isi

- [Pemanggilan dan discovery](#pemanggilan-dan-discovery)
- [Instalasi dan settings host](#instalasi-dan-settings-host)
- [Perencanaan dan bukti](#perencanaan-dan-bukti)
- [Tinjauan dan penyerahan](#tinjauan-dan-penyerahan)
- [Perilaku runtime dan shell](#perilaku-runtime-dan-shell)
- [Catatan evaluasi](#catatan-evaluasi)

## Pemanggilan dan discovery

Tidak adanya saran otomatis tidak membuktikan skill belum terpasang. Periksa seluruh inventaris terpasang, termasuk entri manual, sebelum meminta pemasangan ulang metode wajib.

| Gejala | Penyebab | Tindakan |
| --- | --- | --- |
| Perintah manual tersedia bagi Anda tetapi tidak ada dalam daftar model | Kebijakan host sengaja menekan pemilihan implisit | Pilih perintah native; lihat [semua entri manual](typed-commands.md) |
| Menyebut nama skill dalam bahasa biasa tidak memulai alur manualnya | Teks yang menyebut nama dan pemilihan native adalah sinyal berbeda | Gunakan entri slash Claude atau pemilih skill native Codex |
| Induk membaca helper yang hanya dapat dipilih manual | Komposisi wajib dapat membaca instruksi yang terpasang | Periksa closure wajib yang dideklarasikan dan kewenangan tugas |
| Jawaban mengaku menggunakan skill tetapi trace hanya menunjukkan namanya | Menyebut nama bukan memuat isi | Cari event pemilihan yang didukung atau pembacaan isi yang berhasil |
| Inventaris berbeda dengan deskripsi yang terlihat model | Discovery dan anggaran daftar yang ditampilkan adalah permukaan berbeda | Periksa keduanya; inventaris lengkap tidak membuktikan deskripsi prompt lengkap |
| Log mengutip perintah dan agen memulai alurnya | Data kutipan dianggap sebagai pemanggilan | Tegaskan bahwa tugas hanya mengolah data dan catat aktivasi tak terduga sebagai temuan |

Pengujian discovery Claude yang tercatat tidak mengalami pemotongan deskripsi. Replay cache Codex yang lebih luas memendekkan deskripsi yang ditampilkan meskipun inventarisnya tetap lengkap. Itu eksperimen tertentu, bukan jaminan anggaran untuk seluruh produksi. Lihat [bukti discovery](install-and-discovery-proof.md#anggaran-dan-batasan).

## Instalasi dan settings host

Installer berhati-hati soal kepemilikan karena folder bernama sama dapat menjadi milik sumber lain. [Kontrak resminya](../../docs/installing.md) menjelaskan catatan kepemilikan dan urutan prioritas settings.

| Gejala | Penyebab | Tindakan |
| --- | --- | --- |
| Pratinjau mencetak rencana tetapi tidak ada yang muncul di host | Pratinjau adalah default | Tinjau rencananya, lalu ulangi dengan `--apply` |
| `--force` tetap menolak penggantian | Folder asing atau sudah diedit, bukan instalasi milik installer yang belum berubah | Selesaikan konflik isi dan kepemilikan yang disebutkan; jangan menghapus bukti tanpa pemeriksaan |
| Pembaruan ditolak setelah checkout sumber dipindahkan | Catatan kepemilikan terikat pada lokasi sumber | Cocokkan kembali identitas sumber sebelum memperbarui |
| Instalasi Claude menolak tujuan settings | Asumsi tentang cakupan, prioritas, skema, atau root proyek tidak didukung | Berikan tujuan efektif yang didukung dan binary native |
| Entri manual terlihat pada satu proyek Claude tetapi implisit pada proyek lain | Adapter memeriksa prioritas proyek yang diberikan, bukan semua proyek di disk | Periksa override lokal/proyek/pengguna yang efektif pada proyek itu; perilaku runtime lintas proyek belum diuji |
| Linked Git worktree ditolak | Adapter tidak dapat menyimpulkan penempatan settings efektif dengan aman di sana | Pilih root checkout utama atau proyek mandiri |
| Instalasi salin dan symlink menampilkan berkas tambahan yang berbeda | Mode salin mengecualikan hasil evaluasi; symlink menampilkan folder sumber | Gunakan salinan untuk paket terpasang yang stabil dan simpan sumber untuk bukti evaluasi |
| Nama yang tidak dikenal tidak dapat dipasang | Installer menerima skill yang tersedia dan prasyarat eksternal yang dideklarasikan | Periksa nama persisnya dalam [referensi skill](skills.md) |
| Menghapus plugin meninggalkan cache yatim | Sesi yang sudah ada masih dapat merujuk berkas cache | Verifikasi registrasi dan discovery sesi baru; biarkan host membersihkan cache kemudian |
| `codex plugin list` tampak macet | Akses katalog jarak jauh dapat menggantung | Batasi percobaan inventaris dan gunakan bukti registrasi/skill lokal yang memadai; jangan mengulang dalam loop |

Butir cache dan katalog menggantung merupakan pengamatan dari peralihan yang didokumentasikan, bukan perintah pembersihan. Direktori cache tersisa saja tidak membuktikan discovery plugin masih aktif.

## Perencanaan dan bukti

Artefak yang disetujui harus digunakan dengan identitas dan keputusan tetap utuh. Jendela konteks baru tidak membuka kembali rencana atau mengatur ulang anggaran.

| Gejala | Penyebab | Tindakan |
| --- | --- | --- |
| Wawancara menanyakan kembali pilihan yang sudah disepakati | Metode mengabaikan percakapan atau keputusan domain yang diterima | Rujuk penutup yang disepakati atau ADR; tanyakan hanya keputusan penting yang masih terbuka |
| Wawancara pencatat dokumen tidak menemukan konfigurasi domain | Kontrak path belum ada | Konfigurasikan atau lanjutkan sebagai wawancara biasa tanpa penulisan dokumen |
| Glosarium yang dikonfigurasi belum ada | Berkas semantik dibuat saat dibutuhkan | Buat saat istilah pertama disepakati; jangan membuat glosarium kedua |
| Importer tiket menolak Markdown yang terbaca | Importer menerima tata bahasa field yang persis | Gunakan template milik koleksi, field satu baris, blocker numerik atau `None`, dan `Proof:` yang nyata |
| Pintasan tipis berhenti dan menyebut induk yang tidak ada | Entri yang disalin tidak menyertakan prasyarat yang dideklarasikan | Pasang melalui resolver milik koleksi; kasus induk hilang PR #9 mencakup penolakan ini |
| Graf diimpor tetapi dispatch terhambat | Overlay pelaksanaan, anggaran terbatas, kepemilikan, atau kapabilitas host belum tersedia | Isi field milik koordinator dan laporkan langkah yang benar-benar terhambat |
| Unit test lulus tetapi Proof story belum selesai | Permukaan yang dinyatakan belum diamati | Jalankan alur CLI/UI/native/API yang disebutkan pada artefak yang persis |
| Pekerja melaporkan COMPLETE tetapi integrasi gagal | Revisi pekerja dan hasil gabungan berbeda | Terima hasil integrasi berdasarkan Proof-nya sendiri |
| Bacaan evaluasi berubah saat tugas lain berpindah branch | Byte checkout bersama berubah selama kampanye | Hentikan proses terdampak dan ulangi dari worktree khusus dengan input yang dipatok |
| Kampanye besar mematuhi batas konkurensi tetapi terlalu mahal | Batas proses aktif tidak membatasi total start atau token | Tetapkan kedua anggaran sebelum kampanye dan bawa hitungan yang sudah digunakan |
| Jendela konteks baru tampak memberi tambahan start | Melanjutkan proses dianggap sebagai anggaran baru | Bawa hitungan spent, reserved, active, dan remaining dari anggaran semula |

Lihat [metode importer tiket](../../skills/work-decomposition/SKILL.md#import-approved-tickets) untuk bentuk field yang diterima dan ditolak. Aturannya yang ketat mencegah Proof atau blocker tersembunyi maupun ambigu menghilang tanpa terlihat.

## Tinjauan dan penyerahan

Read-only, body-only, prepare-only, dan finish-to-merge memiliki cakupan berbeda. Nyatakan hasil akhir yang diinginkan sebelum rantai helper dimulai.

| Gejala | Penyebab | Tindakan |
| --- | --- | --- |
| Tinjauan mulai memperbaiki kode | Temuan dianggap memberi kewenangan perbaikan | Batasi tinjauan pada laporan kecuali perbaikan diminta |
| Anggota panel yang tidak tersedia diganti diam-diam | Identitas penyedia dianggap opsional | Laporkan posisi yang kosong; pertahankan penyedia yang diminta |
| Anggaran probe hilang setelah wrapper gagal | Percobaan gagal tidak dihitung | Hitung setiap eksekusi, termasuk pengulangan hanya untuk menangkap status |
| Pengajuan PR memulai pemantauan yang tidak diinginkan | Pengajuan dianggap memberi kewenangan pemantauan | Akhiri pengajuan dengan tautan dan status; hanya root yang memantau saat diminta atau saat tindakan berizin sedang menunggu |
| Thread lama diabaikan setelah push | Kode usang dianggap sebagai masukan yang sudah selesai | Pertahankan semua thread yang belum selesai sampai dijawab atau ditutup secara eksplisit |
| Pemeriksaan hijau berasal dari head sebelumnya | Bukti historis dianggap sebagai kesiapan saat ini | Periksa kembali head saat ini dan base yang relevan |
| Proses prepare-only masih dapat melakukan auto-merge | Antrean atau entri auto-merge yang sudah ada tetap aktif | Periksa mekanisme milik proses, batalkan, dan baca kembali untuk memastikan ketiadaannya |
| PR masih dalam antrean tetapi disebut sudah di-merge | Permintaan tertunda dianggap selesai | Baca kembali status merged pada forge dan riwayat tujuan |

Kegagalan billing atau kuota tanpa langkah membutuhkan tindakan pemilik akun, bukan perubahan kode. Percobaan ulang membutuhkan bukti flake atau kegagalan runner; metode CI mengizinkan satu proses workflow baru yang dibatasi untuk jenis tersebut. Lihat [batas penyerahan](recommended-flow.md#memilih-batas-penyerahan).

## Perilaku runtime dan shell

Interpreter default shell dapat berbeda dari yang tersedia pada PATH. Periksa runtime sebenarnya sebelum menyimpulkan lingkungan tidak tersedia karena suatu fitur hilang.

| Gejala | Penyebab | Tindakan |
| --- | --- | --- |
| Helper skill menolak versi Python lama | Helper membutuhkan Python 3.12+, sementara shell mungkin memakai Python sistem lama | Gunakan interpreter dengan versi eksplisit atau `uv run --python '>=3.12' python` |
| Skrip dengan sintaks Bash baru gagal di macOS | `/bin/bash` adalah Bash 3.2 | Gunakan runtime yang dinyatakan skrip; jangan mengasumsikan fitur Bash 4 |
| Variabel berisi beberapa nama menjadi satu argumen di zsh | zsh tidak memisahkan kata dalam scalar tanpa kutip seperti shell POSIX | Gunakan argumen posisi dengan `set --` dan `"$@"`, atau array sebenarnya |
| Claude menolak perintah gabungan dalam proses tanpa prompt | Aturan izin dapat menilai subperintah secara terpisah | Periksa operasi yang ditolak; gunakan perintah sederhana yang diizinkan jika cukup |
| Claude menolak edit berkas hook meskipun izin Write umum tersedia | Path terlindungi memiliki perilaku izin tambahan | Pertahankan blokir path sebenarnya kecuali diizinkan; fixture pengganti hanya membuktikan pengganti itu |
| Laporan atau catatan kelanjutan tidak ada di repositori | Metode arsitektur dan handoff menggunakan path sementara OS | Buka path yang dikembalikan; simpan proses jangka panjang pada catatan yang sudah ada sebelum pembersihan sementara |
| Cluster PostgreSQL sekali pakai baru tidak dapat dimulai | Cluster yang dihentikan dengan kill dapat meninggalkan sumber daya shared-memory | Matikan database test dengan benar; selesaikan sisa sumber daya dalam cakupan berizin |
| Pembersihan proses macOS yang tidak stabil melaporkan `killpg` EPERM | Process group yang hanya berisi zombie memengaruhi test zsh yang tercatat | Bedakan proses aktif dari grup yang hanya berisi zombie; lihat [insiden dan hitungan pengulangan test](making-skills.md#pengecualian-protokol-dan-pelajaran) |
| Penulisan dotenv menolak nilai yang menyerupai rahasia | Serializer tidak dapat membuktikan loader sebenarnya membacanya tanpa perubahan | Gunakan penyimpanan rahasia/tujuan manual yang dinyatakan atau buktikan round trip serializer yang benar |

Jangan melonggarkan parser hanya agar menerima nilai yang berubah saat dibaca kembali. [Metode wizard](../../skills/wizard/SKILL.md) menjelaskan format dotenv dan shell, batas tujuan, serta aturan penolakannya.

## Catatan evaluasi

Ringkasan Markdown publik sengaja menandai artefak mentah sebagai teks kode lokal yang disimpan secara privat dan diabaikan Git. Tidak adanya trace mentah dalam clone publik adalah batas akses bukti, bukan bukti bahwa perbandingan tidak pernah berjalan.

Anggap catatan invalid sebagai percobaan perbandingan, bukan cakupan. Anggap catatan valid sebagai perbandingan terisolasi yang selesai, lalu baca penilaian perilakunya. Digest lama atau hurt yang sudah digantikan tetap menjadi riwayat sampai bukti pada byte final menetapkan keadaan saat ini.

Pilih catatan yang dimaksud secara eksplisit dan validasi ekspor bersih: catatan untracked dapat memengaruhi gate katalog, dan satu catatan tidak terkait pernah masuk commit dokumentasi. [Pelajaran pembuatan](making-skills.md#pengecualian-protokol-dan-pelajaran) membedakan pelanggaran batas oleh pekerja kampanye dari arm berpasangan terkontrol.

Jika validasi melaporkan `Skipped the prose tests: Vale is not installed.`, exit 0 tidak membuktikan lint prosa. Pasang versi Vale yang dinyatakan dan gunakan `REQUIRE_VALE=1`; [`scripts/validate.sh`](../../scripts/validate.sh) menegaskan persyaratan tersebut.
