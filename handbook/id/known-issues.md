> **Dokumentasi untuk manusia.** Agen hanya boleh membaca halaman ini jika diminta oleh seseorang.

Bahasa: [English](../known-issues.md) · [Bahasa Indonesia](known-issues.md)

# Masalah yang diketahui dan batas bukti

Checkpoint inti 2026-11-09 telah dievaluasi, dengan batas host tertentu dan satu kekurangan kecil tercatat yang tetap terlihat. Perubahan byte berikutnya membutuhkan bukti baru; baca katalog saat ini dan [hasil yang dihasilkan](eval-results.md) untuk status serta cakupan digest masing-masing. Halaman ini memisahkan batas saat ini dari cacat yang diperbaiki; halaman ini tidak menyimpulkan bug dari jalur yang belum diuji.

## Daftar isi

- [Manual-only bukan batas akses berkas](#manual-only-bukan-batas-akses-berkas)
- [Batas dan kekurangan kecil saat ini](#batas-dan-kekurangan-kecil-saat-ini)
- [Cacat yang sudah diperbaiki](#cacat-yang-sudah-diperbaiki)
- [Hal yang belum diuji](#hal-yang-belum-diuji)
- [Cara melaporkan issue yang berguna](#cara-melaporkan-issue-yang-berguna)

## Manual-only bukan batas akses berkas

Status: batas visibilitas yang diketahui; satu pembacaan diamati, bukan trigger berulang yang dikonfirmasi. Claude menyembunyikan entri manual dari daftar skill-nya sendiri, tetapi prompt survei negatif tetap membaca entri itu melalui Bash. [Catatan publik awal](../../skills/to-questionnaire/evals/results/2026-11-09-claude-claude-opus-5-5-near-miss-3-claude.md) mempertahankan pengamatan tersebut. [Pengulangan baru](../../skills/to-questionnaire/evals/results/2026-11-09-claude-claude-opus-5-5-near-miss-3-round2-pre-claude.md) tidak membaca isi kandidat.

Gunakan pemilihan native eksplisit untuk pekerjaan manual yang dimaksud dan tinjau pembacaan isi tak terduga. Jangan menganggap settings visibilitas sebagai sandbox. Perbedaan umum pada filesystem yang sama berlaku bagi handbook untuk manusia ini.

## Batas dan kekurangan kecil saat ini

Setiap solusi sementara tetap berada dalam izin tugas dan host yang sudah ada.

| Butir | Status | Bukti dan respons praktis |
| --- | --- | --- |
| Penolakan izin Claude pada gabungan edit/readback PR offline | Kegagalan historis yang dipengaruhi host; pengulangan pada byte sama selesai | [PR #9](https://github.com/cravingmaker/skills/pull/9) mempertahankan kedua pengamatan; tidak ada cacat isi skill atau kelonggaran izin universal yang dibuktikan |
| Penulisan path hook dan eksekusi npm nyata pada Claude | Batas lingkungan dalam fixture yang tercatat | Penolakan path terlindungi dipisahkan dari trigger yang meleset dengan fixture hook sekali pakai; npm nyata dan kesetaraan staged-index tetap belum terbukti dalam konfigurasi itu |
| Root/wrapper instalasi Claude yang tidak didukung | Batas adapter fail-closed yang disengaja | [Kontrak instalasi](../../docs/installing.md#claude-code): linked worktree, direktori Git terpisah, subdirektori, dan skema native yang tidak didukung perlu diselesaikan |
| Injeksi memory/konteks host | Batasan isolasi | Memory host dapat menambah konteks di luar proyek bersih; adapter berpasangan menonaktifkannya, sementara konteks koordinator kampanye adalah batas terpisah |
| Cache plugin yatim setelah uninstall | Perilaku siklus hidup host yang diamati | Peralihan mengamati cache tersimpan saat sesi masih merujuknya; verifikasi discovery baru alih-alih menghapus cache bersama secara luas |
| Daftar plugin jarak jauh Codex menggantung | Batas peralihan yang diamati | Pemanggilan inventaris katalog jarak jauh dapat menggantung; diperlukan inventaris alternatif yang dibatasi |
| Kesalahan kecil label sumber dalam jawaban retrospektif final | Kekurangan respons yang masih terbuka | [Claude Outcome 6](../../skills/retro/evals/results/2026-11-09-claude-claude-opus-5-5-outcome-6-round4-fix5-claude.md) mengatribusikan instruksi di luar topik ke label sumber yang salah; pemeriksaan tujuan dan hasil cakupan tetap lulus |
| Bukti mentah tidak tersedia dalam clone publik | Batas akses bukti yang disengaja; path lokal bukan tautan publik | [Kontrak bukti harness](../../docs/eval-harness.md#read-the-evidence): trace mentah tetap privat; periksa ringkasan yang dikomit dan batasannya |
| `--host codex` saat ini tidak menambah perilaku | Kekurangan antarmuka installer yang terbuka | [`install-skills.py`](../../scripts/install-skills.py): flag di-parse pada baris 45, sementara hanya nilai Claude yang bercabang pada baris 53, 55, dan 161. Pemeriksaan kebijakan sumber pada baris 126-127 selalu berjalan; pertahankan flag untuk menyatakan tujuan atau hilangkan |
| Pemeriksaan status katalog tidak mengikat byte saat ini atau semantic hurt | Batas pemeriksaan struktural yang disengaja | [`check-catalog.py`](../../scripts/check-catalog.py) `missing_evaluations` (baris 25-52) memeriksa cakupan pasangan valid/selesai. Keputusan byte final dan hurt yang belum selesai membutuhkan tinjauan kampanye |
| Bukti Outcome baseline-first masih sempit | Batas bukti: hanya Codex, satu run per kasus; satu temuan belum terselesaikan | Lima pasangan Codex khusus. Dengan baseline terekam atau tanpa izin model ([baseline terekam lulus](../../skills/writing-for-agents/evals/results/2026-11-10-codex-gpt-6.1-sol-outcome-4-recorded-pass.md), [baseline terekam gagal](../../skills/writing-for-agents/evals/results/2026-11-10-codex-gpt-6.1-sol-outcome-4-recorded-fail.md), [tanpa izin model](../../skills/writing-for-agents/evals/results/2026-11-10-codex-gpt-6.1-sol-outcome-5-unauthorized.md)): 2 added, 1 matched, 0 hurt. Dua pasangan memakai runner tiruan yang terlihat oleh kedua lengan mencetak hasil tetap ([tiruan lulus](../../skills/writing-for-agents/evals/results/2026-11-10-codex-gpt-6.1-sol-outcome-4-passing-baseline.md), [tiruan gagal](../../skills/writing-for-agents/evals/results/2026-11-10-codex-gpt-6.1-sol-outcome-4-failing-baseline.md)); saat tiruan itu melaporkan gagal, lengan perlakuan tetap menulis body walau menilai kegagalannya belum terverifikasi. Run Outcome di Claude dan baseline bertingkat yang sungguhan tidak dijalankan |
| Tidak ada perintah uninstall umum | Batas kapabilitas installer yang terbuka | `parse` pada [`install-skills.py`](../../scripts/install-skills.py) menyediakan flag install/update tanpa operasi remove. Periksa kepemilikan dan paket dependen sebelum rekonsiliasi manual terbatas; penghapusan tidak diuji di sini |
| Adapter Claude memeriksa satu proyek sekali jalan | Batas cakupan adapter; perilaku override banyak proyek belum diuji | [`claudesettings.py`](../../scripts/claudesettings.py) menyelesaikan tujuan user/project/local untuk root yang diberikan. Settings proyek lain dapat berbeda |
| Checklist peralihan asli menggunakan bentuk rencana masa depan | Kalimat historis dipertahankan | [Checklist arsip](cutover.md) ditulis sebelum [peralihan yang diamati dalam PR #10](https://github.com/cravingmaker/skills/pull/10). Pembungkus barunya memberi tanggal; checklist asli tidak ditulis ulang |
| Langkah penulisan README dahulu mewajibkan baris tabel manual | Diperbaiki dalam perubahan handbook ini | [AGENTS.md](../../AGENTS.md#workflow), langkah 4, kini menjalankan generator beserta pemeriksaannya dan meminta panduan manusia yang dibutuhkan setiap skill baru |
| Panduan evaluasi belum mencakup beberapa rincian aktivasi Claude selanjutnya | Celah dokumentasi pada main | Bandingkan [panduan dasar](../../docs/eval-harness.md) dengan [PR #9](https://github.com/cravingmaker/skills/pull/9) dan [observer saat ini](../../scripts/evalharness/hosts.py) untuk replay native dan bukti isi Bash |
| Ikhtisar lama menyebut klien tambahan | Kalimat dukungan historis yang belum terbukti | [Ikhtisar asli](https://github.com/cravingmaker/skills/blob/812abc3e9ed0ffe1ffc85dc9505bb6473deb5081/README.md) menyebut Cursor dan klien lain; catatan instalasi serta perilaku yang disimpan mencakup Claude Code dan Codex. Kompatibilitas format tidak membuktikan runtime host lain |
| Field aktivasi otomatis lama mempertahankan kegagalan observer | Batas bukti historis; observer diperbaiki sebelum PR #8 masuk main | [Kontrak evaluasi](../../docs/eval-harness.md#codex) kini mengenali pemilihan native tepercaya. Catatan awal dapat mempertahankan field otomatis `false` dengan koreksi yang ditinjau; baca keduanya sebelum menyimpulkan perilaku |
| Bukti instalasi historis menjelaskan profil lama yang lebih kecil | Batas snapshot | Revisi yang dipatok valid sebagai bukti historis; [referensi profil yang dihasilkan saat ini](routing.md#isi-setiap-profil) menyediakan keanggotaan sekarang |

Pengamatan memory, cache, dan daftar menggantung diterbitkan di sini sebagai ringkasan yang disanitasi untuk dokumentasi peralihan. PR peralihan publik membuktikan keadaan kebijakan instalasi/discovery; PR itu tidak memuat setiap diagnostik tingkat rendah operasi tersebut.

## Cacat yang sudah diperbaiki

Ini kegagalan historis dengan koreksi dalam pekerjaan yang di-merge. Catatan lamanya tetap tersedia dan tidak boleh dihitung sebagai bukti kelulusan saat ini.

| Cacat | Status | Bukti |
| --- | --- | --- |
| Serialisasi dotenv dapat merusak nilai berisi apostrof | Diperbaiki dalam PR #6; masuk main melalui PR #8 | [PR #6](https://github.com/cravingmaker/skills/pull/6) menjelaskan round trip parser dan penolakan sebelum penulisan |
| Pengamanan rendering laporan arsitektur | Penguatan ditambahkan dalam PR #6; masuk melalui PR #8 | [PR #6](https://github.com/cravingmaker/skills/pull/6) mencatat keluaran offline statis yang di-escape dan Mermaid strict opsional yang dipatok |
| Injeksi skill native Codex dilewatkan observer aktivasi | Diperbaiki dalam stack yang masuk melalui PR #8 | Riwayat main menyertakan deteksi pemilihan native dan batas provenance teks input; [kontrak bukti saat ini](../../docs/eval-harness.md#codex) menyatakan event yang diterima |
| Pengecualian nama historis tidak sengaja mencakup rute aktif | Diperbaiki sebelum stack masuk dalam PR #8 | Riwayat main mengakhiri pengecualian sebelum panduan aktif; [referensi saat ini](../../skills/clear-communication/references/clarifying.md) memisahkan wilayahnya |
| Router dapat melaporkan penerimaan tanpa dispatch/isolasi wajib | Diperbaiki sebelum PR #8 masuk main | [Router saat ini](../../skills/agent-orchestrator/SKILL.md#build-from-an-approved-spec-and-code-tickets) berhenti pada preflight berbasis sumber saat fasilitas itu tidak tersedia |
| Skill bawaan Claude dapat membuat anak tak terkontrol selama evaluasi | Diperbaiki dalam harness pada PR #9 | [PR #9](https://github.com/cravingmaker/skills/pull/9) mencatat pengecualian skill bawaan dan penolakan fork; percobaan lama yang terdampak tetap invalid |
| Path sementara Claude panjang dapat fallback ke temp Bash bersama | Diperbaiki dalam harness pada PR #9 | Adapter menggunakan path fisik privat yang pendek dan pemeriksaan temp dua arm langsung yang disimpan; percobaan temp bersama yang terdampak invalid |
| Pemilihan slash native Claude dan pembacaan isi Bash dilewatkan | Diperbaiki dalam PR #9 | [PR #9](https://github.com/cravingmaker/skills/pull/9) dan [kontrak aktivasi saat ini](../../docs/eval-harness.md) membedakan replay native dan pembacaan isi terpasang yang terlihat |
| Deteksi listing/cat khusus Claude bocor ke klasifikasi Codex | Diperbaiki dalam PR #9 | Ekstensi listing/cat hanya untuk Claude; pembacaan gabungan Codex tetap tidak diklasifikasi untuk tinjauan trace manual |
| Retrospektif membaca di luar sumber yang disebutkan | Diperbaiki dan diuji ulang sampai revisi final PR #9 | Audit sumber berpasangan pada byte final lulus pada kedua host; [metode batas sumber](../../skills/retro/SKILL.md) menyertakan aturan path persis dan riwayat terpisah |
| Probe adversarial gagal atau diulang lolos dari jatah | Diperbaiki dalam PR #9 | [Entri](../../skills/interrogate/SKILL.md) menghitung setiap eksekusi dan menangkap keluaran/status sekali; kasus kegagalan wrapper terkontrol berjalan pada kedua host |
| Penanganan guardrail membuka ulang audit luas untuk celah helper hilang yang sudah disebutkan | Diperbaiki dalam PR #9 | [Metode](../../skills/project-guardrails/SKILL.md) kini melaporkan celah berdasarkan bukti yang diberikan dan menghentikan alur dependen |
| Deskripsi sempit melewatkan perbaikan kontekstual, pemeriksaan keputusan manusia, dan wiring staged-hook | Diperbaiki dan diuji ulang dalam PR #9 | [PR #9](https://github.com/cravingmaker/skills/pull/9) mencatat perubahan deskripsi dan pengujian ulang berpasangannya |

Baris laporan arsitektur menjelaskan pengamanan yang tersedia. Baris itu tidak mengklaim exploit yang direproduksi secara independen terhadap kode upstream lama. Ketatnya importer serta parsing blocker/Proof ditinjau dan diperbaiki dalam stack; fixture template/importer saat ini menentukan bentuk yang didukung.

## Hal yang belum diuji

Bukti yang disimpan mendukung fixture terbatas dan pemeriksaan host tertentu. Bukti itu tidak menetapkan setiap alur langsung yang dijelaskan skill.

| Permukaan atau klaim | Batas bukti saat ini |
| --- | --- |
| Versi CLI mendatang atau model/settings berbeda | Versi tercatat adalah snapshot; ulangi pemeriksaan kapabilitas dan sesi |
| Host Agent Skills lain | Kompatibilitas format diharapkan; routing runtime dan kebijakan manual belum diuji |
| Discovery produksi langsung dengan setiap plugin, namespace, hook, dan kebijakan server | Replay discovery dan sesi terisolasi tidak mereproduksi semua sumber terkelola |
| Merge yang dijaga dan berhasil, penyelesaian antrean, serta race head/base terlambat | Fixture pengiriman lokal terutama menguji kemajuan aman dan syarat yang terhambat |
| Siklus hidup watcher root pada forge langsung | Fallback satu pemeriksaan atau watcher simulasi tidak membuktikan perilaku layanan |
| Panel penyedia independen sebenarnya dan pemulihan pekerja terdelegasi native | Evaluasi berpasangan menonaktifkan delegasi; adapter alur harian menggunakan pekerja CLI serial terisolasi |
| Hosted CI nyata, bot wajib, dan penyelesaian tinjauan manusia | Metadata forge offline adalah pengganti |
| Cakupan native/UI/perangkat penuh dan setiap peta fitur yang dihasilkan | CLI yang dijalankan atau satu fitur hanya membuktikan permukaan/alur tersebut |
| Pemulihan crash di tengah publikasi checkpoint | Pemeriksaan catatan atomik bukan eksperimen injeksi crash |
| Npm nyata dan kesetaraan staged/local/CI lengkap dalam lingkungan yang menolak | Pengganti hook khusus membiarkan permukaan itu belum terbukti |
| Keandalan umum, keunggulan, dan penghematan biaya | Contoh pasangan tunggal dengan model default host berbeda tidak membuktikan pengaruh pada populasi |

## Cara melaporkan issue yang berguna

Sertakan host dan versi, entri yang dipilih secara persis, revisi sumber, settings pemanggilan terkait, cakupan tugas, hasil yang diharapkan, dan kejadian sebenarnya. Sebutkan perintah atau permukaan pengguna dan simpan exit status atau hasil yang terlihat. Pisahkan metode hilang, aktivasi yang meleset, penolakan izin, artefak salah, dan pengamatan yang tidak tersedia. Bagikan bukti yang disanitasi; jangan menerbitkan kredensial, path pribadi, atau transkrip privat.
