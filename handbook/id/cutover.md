> **Dokumentasi untuk manusia.** Agen hanya boleh membaca halaman ini jika diminta oleh seseorang.

Bahasa: [English](../cutover.md) · [Bahasa Indonesia](cutover.md)

# Checklist historis peralihan inti

Checklist ini ditulis sebelum peralihan. PR #10 mencatat hasil yang diamati pada 2026-11-09; bentuk rencana masa depan di bawah tetap dipertahankan sebagai riwayat.

## Daftar isi

- [Mencatat konteks](#mencatat-konteks)
- [Melewati pemeriksaan wajib](#melewati-pemeriksaan-wajib)
- [Inventaris dan rollback](#inventaris-dan-rollback)
- [Menyiapkan pengganti](#menyiapkan-pengganti)
- [Menghapus keempat sumber](#menghapus-keempat-sumber)
- [Memasang dan memverifikasi setiap host](#memasang-dan-memverifikasi-setiap-host)

## Mencatat konteks

[PR #10](https://github.com/cravingmaker/skills/pull/10) mencatat inti yang kemudian dipasang dan discovery yang diamati. Catatan ini bukan petunjuk instalasi saat ini; gunakan [Memulai](getting-started.md) dan [referensi profil saat ini](routing.md#isi-setiap-profil).

# Peralihan skill inti

Ganti mattpocock-skills, port pstack, tstack, dan Superpowers dengan inti milik koleksi yang berisi 58 paket hanya setelah PR ini di-merge dan pemeriksaan perilaku serta host di bawah lulus. Checklist ini mencatat operasi mendatang; menerbitkan checklist atau lulus pemeriksaan statis tidak menjalankan maupun membuktikan peralihan. A1-08 mewajibkan uninstall sebenarnya terhadap keempat sumber. Menonaktifkannya saja belum lengkap.

## Melewati pemeriksaan wajib

- Bangun ulang profil dan berkas host yang dihasilkan, lalu jalankan validator lengkap dengan Vale wajib. Tinjau asal-usul dan diff sumber/tujuan yang dinormalisasi, lalu pastikan closure 58 paket di bawah persis.
- Catat proses Activation, Near miss, dan Outcome berpasangan antara skill final dan tanpa skill untuk semua skill baru maupun yang berubah secara material. Tampilkan bukti yang hilang, gagal, atau tidak konklusif dan pertahankan status terkait sebagai unevaluated. Skill yang tidak berubah hanya mempertahankan bukti lama yang masih berlaku.
- Luluskan alur harian dari wawancara berbasis sumber melalui spec, tiket stabil, satu pelaksana kode yang disetujui, tinjauan, dan penyerahan PR. Pertahankan hash sumber persis, blocker, Proof yang disebutkan, anggaran bersama terbatas, penerimaan pekerja, dan penerimaan integrasi tanpa wawancara, pembagian, atau pengendali baru.
- Sertakan kasus council read-only, PR-body-only, full-stop dengan no-merge di rantai helper, penyedia hilang, tinjauan lama yang belum selesai, bot wajib, bukti hilang/usang/proxy, dan putaran habis. Anak tidak pernah memulai watcher PR; root hanya memantau atas permintaan atau saat tindakan berizin masih menunggu.
- Dalam home dan konfigurasi sekali pakai, verifikasi discovery Claude Code dan Codex yang didukung, pemanggilan eksplisit, dan penekanan entri manual dengan keempat sumber upstream serta injeksi otomatisnya tidak ada. Direktori proyek bersih saja tidak mengisolasi plugin global. Catat versi host, kebijakan efektif, dan identitas skill yang dimuat.

## Inventaris dan rollback

Inventarisasi kedua host pada cakupan pengguna, proyek, dan lokal yang sebenarnya sebelum mengubah apa pun. Sertakan kebijakan terkelola dan override command-line jika memengaruhi discovery. Gunakan inventaris host yang didukung dan periksa hanya catatan registrasi serta instalasi terkait.

Untuk masing-masing dari empat sumber, catat nama paket atau registrasi sebenarnya, revisi sumber, mekanisme instalasi, cakupan, lokasi registrasi, root skill terpasang, salinan lepas, symlink beserta targetnya, serta aturan startup, injeksi, dan hook milik sumber. Deteksi salinan tstack tanpa registrasi serta instalasi plugin. Inventaris registrasi saja melewatkan isi yang terpisah.

Catat bukti kepemilikan serta key dan nilai settings yang terdampak secara persis. Identifikasi plugin, nama, berkas, pilihan disabled/manual yang lebih ketat, dan settings lain yang perlu dipertahankan. Pertahankan reservasi host independen, termasuk code-review, review, security-review, init, verify, dan run-skill-generator, serta nama plugin lain seperti standup. Jangan kumpulkan kredensial atau riwayat transkrip yang tidak terkait.

Simpan catatan rollback privat dengan cakupan terbatas di luar lokasi yang diganti. Catat registrasi terdampak, keadaan settings milik sumber secara persis, identitas isi salinan dan sumber asli yang dapat dipulihkan, target tautan, isi dan kepemilikan hook/aturan, identitas sumber, mekanisme uninstall/reinstall, dan urutan pemulihan. Pastikan input pemulihan dapat dijangkau. Jangan masukkan konfigurasi berisi rahasia ke laporan; simpan hanya key terdampak yang diizinkan dan rujukan aman. Catat keadaan yang diharapkan sebelum dan setelah setiap operasi agar peralihan parsial dapat diselesaikan.

## Menyiapkan pengganti

Siapkan tree milik koleksi yang sudah di-merge dan diverifikasi beserta closure wajib lengkapnya pada tujuan sementara bebas konflik. Gunakan HOME sementara serta direktori host/config/cache terpisah untuk persiapan dan pemeriksaan installer ini. Tentukan direktori host final dan tujuan settings sebenarnya dari inventaris; jangan mengasumsikan override plugin menghapus isi plugin.

Installer yang ada menerima beberapa nama. Sebanyak 48 nama baru berikut beserta empat root yang sudah ada menghasilkan tepat 58 paket, termasuk kesepuluh paket awal. Ini daftar argumen eksplisit, bukan profil inti:

```sh
set -- \
  grilling grill-with-docs domain-modeling to-spec to-tickets triage wayfinder \
  to-questionnaire setup-agent-skills prototype sharpen research how why \
  grill-me bro wait-what \
  codebase-design architect improve-codebase-architecture implement implement-spec \
  tdd diagnosing-bugs wizard change-review sol-loop blast-radius benchmark-checklist \
  create-verification-skill maintain-verification-skill council interrogate \
  file-pr babysit-pr fix-ci leaving-pr-comments modernize takeover full-send full-stop \
  retro handoff writing-for-agents teach recall ketchup pr \
  agent-orchestrator correct project-guardrails toolchain-upgrade

# Resolve stage_skills_dir to the new conflict-free temporary target first.
scripts/install-skills.py --target "$stage_skills_dir" --mode copy "$@"
scripts/install-skills.py --target "$stage_skills_dir" --mode copy --apply "$@"
```

Periksa pratinjau sebelum menerapkan. Verifikasi himpunan berkas yang disiapkan, byte, mode executable, kebijakan yang dihasilkan, nama persis, dan closure 58 paket tanpa prasyarat eksternal. Instalasi ulang harus mempertahankan tree dan settings milik installer tanpa perubahan. Berhenti jika tujuan asing atau sudah diedit, lalu cocokkan dengan inventaris; jangan paksa penimpaan. Pastikan tree yang disiapkan dan catatan rollback dapat digunakan sebelum menghapus sumber mana pun.

## Menghapus keempat sumber

Uninstall mattpocock-skills, port pstack, tstack, dan Superpowers melalui mekanisme instalasi sebenarnya yang didukung setiap sumber. Gunakan nama dan cakupan persis yang dicatat; jangan menebak satu perintah uninstall universal. Hapus hanya salinan lepas, symlink, injeksi startup, aturan, dan hook yang terbukti milik sumber dan ditinggalkan mekanismenya. Pertahankan settings dan registrasi lain.

Baca kembali inventaris host/plugin sebenarnya serta root skill terkait setelah uninstall. Pastikan registrasi dan jalur discovery lepas tidak ada, termasuk salinan tstack non-plugin. Entri disabled, registrasi terhapus dengan salinan tersisa, atau skill tersembunyi dalam sesi berjalan belum cukup. Setelah uninstall sebenarnya diverifikasi, hapus sisa reservasi sumber yang dihentikan dari katalog sambil mempertahankan reservasi host independen dan plugin lain. PR pengenalan hanya membebaskan reservasi khusus sumber untuk nama yang baru dimilikinya; perubahan tersebut tidak membuktikan sumber host sudah di-uninstall. Nama upstream yang dilewati tetap tidak terpasang.

Catat setiap hasil yang diamati dan selesaikan dampak yang belum pasti atau parsial sebelum melanjutkan. Jika penghapusan gagal, nyatakan celahnya dan pulihkan keadaan sebelumnya sesuai cakupan bila perlu; jangan tinggalkan instalasi campuran yang ambigu.

## Memasang dan memverifikasi setiap host

Gunakan daftar argumen beberapa nama yang sama untuk setiap direktori skill host final yang sudah dikonfirmasi, dalam mode salin. Lihat pratinjau, lalu terapkan instalasi secara eksplisit. Cocokkan salinan milik installer yang sudah ada dengan inventaris; jangan paksa penggantian.

```sh
# Resolve host_skills_dir from the completed inventory; retain the NAME arguments.
scripts/install-skills.py --target "$host_skills_dir" --mode copy "$@"
scripts/install-skills.py --target "$host_skills_dir" --mode copy --apply "$@"
scripts/build-host-config.py --check
```

Gunakan adapter host yang diimplementasikan dalam [kontrak instalasi](../../docs/installing.md) pada tujuan settings yang sudah dikonfirmasi. Untuk Claude, berikan host, tujuan, path settings, cakupan settings, dan root proyek sebenarnya, lalu periksa pratinjau dan terapkan secara eksplisit hanya perubahan preferensi milik installer. Untuk Codex, pasang berkas hasil generasi yang sudah diperiksa; jangan menghasilkan berkas melalui symlink upstream atau bersama. Pertahankan key lain, settings disabled/manual yang lebih ketat, dan prioritas efektif. Skema yang tidak didukung atau settings rusak adalah kegagalan yang perlu diselesaikan, bukan izin menimpa.

Buka kembali sesi Claude Code dan Codex bersih. Verifikasi discovery sebenarnya dan pemilihan eksplisit grill-me, council, interrogate, wait-what, bro, pr, dan ketchup, serta full-stop, correct milik koleksi, dan setiap helper wajib. Periksa semua 58 nama yang diharapkan beserta penekanan manual dan mode eksplisit setiap entri user katalog. Uji bahwa body-only tidak membuat tindakan jarak jauh, full-stop mempertahankan no-merge pada helper lebih dalam, dan anak mengembalikan status PR tanpa memantau. Tidak ada rute runtime yang boleh menuju cache sumber yang dihentikan.

Periksa kembali daftar plugin/skill sebenarnya dan settings efektif. Pastikan keempat sumber beserta injeksi otomatisnya sudah hilang, nama serta settings lain tetap ada, dan tree milik koleksi, kebijakan, serta closure wajib sesuai dengan identitas yang disiapkan. Catat versi, keadaan, pemeriksaan, dan bukti perilaku yang benar-benar diamati. Nyatakan peralihan selesai hanya setelah kedua host lulus. Jika gagal, pertahankan bukti dan pulihkan melalui catatan rollback yang dibatasi cakupannya, lalu verifikasi keadaan yang dipulihkan.
