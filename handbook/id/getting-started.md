> **Dokumentasi untuk manusia.** Agen hanya boleh membaca halaman ini jika diminta oleh seseorang.

Bahasa: [English](../getting-started.md) · [Bahasa Indonesia](getting-started.md)

# Memulai

Pasang sedikit skill yang berguna, pertahankan kebijakan pemanggilan host, lalu verifikasi discovery dalam sesi baru. Memasang skill menyediakan instruksi dan sumber daya; pemasangan tidak memberi alat, kredensial, langganan, atau kewenangan tugas baru.

## Daftar isi

- [Menyiapkan sumber](#menyiapkan-sumber)
- [Memasang di Codex](#memasang-di-codex)
- [Memasang di Claude Code](#memasang-di-claude-code)
- [Memasang koordinator atau beberapa skill](#memasang-koordinator-atau-beberapa-skill)
- [Mengetahui apa yang berubah](#mengetahui-apa-yang-berubah)
- [Memverifikasi instalasi](#memverifikasi-instalasi)
- [Memperbarui, memindahkan, dan menghapus instalasi](#memperbarui-memindahkan-dan-menghapus-instalasi)
- [Menyiapkan proyek untuk alur utama](#menyiapkan-proyek-untuk-alur-utama)
- [Menerapkan gaya penulisan pada jawaban sehari-hari](#menerapkan-gaya-penulisan-pada-jawaban-sehari-hari)
- [Metode instalasi lainnya](#metode-instalasi-lainnya)
- [Saat terjadi kegagalan](#saat-terjadi-kegagalan)

## Menyiapkan sumber

Gunakan checkout yang sudah ditinjau dan lihat pratinjau setiap instalasi sebelum menerapkannya. Jalankan dari root repositori; ganti path proyek contoh dengan proyek Anda.

```sh
git clone https://github.com/cravingmaker/skills.git
cd skills
scripts/install-skills.py --help
scripts/build-host-config.py --check
```

Skrip repositori berjalan melalui uv, meminta Python 3.12 atau lebih baru, dan mematok PyYAML. Tidak adanya uv adalah kesalahan penyiapan; gunakan [petunjuk instalasi uv](https://docs.astral.sh/uv/getting-started/installation/). CLI host harus sudah terpasang dan dapat digunakan. Installer tidak membutuhkan pemanggilan model.

## Memasang di Codex

Installer memeriksa kebijakan sumber yang dihasilkan pada setiap jalur instalasi. `--host codex` diterima tetapi saat ini tidak menambah perilaku; flag itu memperjelas host yang dituju. Untuk instalasi pengguna default, peralihan yang tercatat menggunakan `~/.codex/skills`.

```sh
scripts/install-skills.py --host codex --target ~/.codex/skills clear-communication
scripts/install-skills.py --host codex --target ~/.codex/skills --apply clear-communication
```

Jika Anda mengubah preferensi pemanggilan dalam checkout sumber, lihat pratinjau dan terapkan berkas host yang dihasilkan di sana terlebih dahulu:

```sh
scripts/build-host-config.py
scripts/build-host-config.py --apply
scripts/build-host-config.py --check
```

Entri manual menyertakan `agents/openai.yaml` dengan `policy.allow_implicit_invocation: false`. Installer memeriksa berkas itu; installer tidak menghasilkannya melalui symlink yang terpasang. Jika Anda menetapkan `CODEX_HOME` khusus, cari lokasi skill host yang sebenarnya agar tidak memasang salinan kedua secara tidak sengaja pada path default. Codex juga dapat menemukan skill dari lokasi lain, termasuk `~/.agents/skills`; pemeriksaan discovery lengkap harus memperhitungkannya.

## Memasang di Claude Code

Berikan direktori skill, berkas settings, cakupan settings, dan root proyek yang sebenarnya. Direktori konfigurasi pengguna default adalah `~/.claude`; jika `CLAUDE_CONFIG_DIR` ditetapkan, gunakan direktori itu.

```sh
project_dir=/absolute/path/to/your/project
claude_config_dir="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"

scripts/install-skills.py --host claude \
  --target "$claude_config_dir/skills" \
  --settings "$claude_config_dir/settings.json" \
  --settings-scope user --project-root "$project_dir" clear-communication

scripts/install-skills.py --host claude \
  --target "$claude_config_dir/skills" \
  --settings "$claude_config_dir/settings.json" \
  --settings-scope user --project-root "$project_dir" --apply clear-communication
```

Variabel ini adalah contoh tujuan, bukan pengganti direktori home shell. Untuk instalasi tingkat proyek, pilih `<project>/.claude/skills`, `<project>/.claude/settings.json`, dan `--settings-scope project`. Settings lokal menggunakan direktori skill yang sama, `settings.local.json`, dan `--settings-scope local`.

Adapter memeriksa skema `skillOverrides` yang didukung binary native Claude yang terpasang dan memanggil `--version`. Adapter menulis `user-invocable-only` untuk entri manual sambil mempertahankan `off` yang lebih ketat. Gunakan `--claude-bin /path/to/native/claude` jika perintah di PATH berupa wrapper.

Adapter saat ini menerima proyek mandiri atau root checkout utamanya. Adapter menolak linked Git worktree, direktori Git terpisah, dan subdirektori repositori sebelum menulis. Pilih root yang didukung agar tidak menebak berkas settings mana yang berlaku lebih dahulu. Lihat [kontrak adapter resmi](../../docs/installing.md#claude-code).

## Memasang koordinator atau beberapa skill

Berikan beberapa nama dalam satu pemanggilan untuk memasang gabungan dependensi wajibnya. Memasang `agent-orchestrator` menyertakan closure dependensi wajib transitifnya; dependensi yang tumpang tindih hanya dipasang sekali.

```sh
scripts/install-skills.py --host codex --target ~/.codex/skills \
  agent-briefing decision-log
scripts/install-skills.py --host codex --target ~/.codex/skills --apply \
  agent-briefing decision-log
scripts/install-skills.py --host codex --target ~/.codex/skills agent-orchestrator
scripts/install-skills.py --host codex --target ~/.codex/skills --apply agent-orchestrator
```

Gunakan nama yang sama pada perintah Claude di atas untuk adapter Claude. [Referensi profil yang dihasilkan](routing.md#isi-setiap-profil) mencantumkan dependensi koordinator; skill lain dapat dipasang langsung.

Skill eksternal wajib dilaporkan beserta sumber upstream dan petunjuk instalasinya. Installer tidak mengambilnya secara otomatis. Profil orchestrator milik koleksi saat ini tidak memiliki prasyarat eksternal.

## Mengetahui apa yang berubah

Pratinjau mencetak JSON ke stdout dan diagnostik ke stderr. Tanpa `--apply`, installer tidak menulis apa pun.

| Lokasi | Dampak |
| --- | --- |
| Direktori skill tujuan | Satu folder atau symlink per skill dalam closure wajib |
| `<skills-dir>/.skills-installer.json` | Catatan kepemilikan untuk checkout sumber dan isi yang dipasang |
| Berkas settings Claude, saat adapternya dipilih | Hanya override visibilitas skill yang dipilih; settings lain tetap utuh |
| `<settings-file>.skills-installer.json` | Catatan kepemilikan perubahan settings Claude |
| Checkout sumber, hanya saat generasi host diterapkan | Berkas kebijakan Codex milik koleksi untuk entri manual |

Mode salin adalah default. Mode ini mempertahankan identitas berkas terpasang dan mode executable, sambil mengecualikan `evals/results/`. README repositori, handbook, katalog, dokumen penulisan, dan skrip validasi repositori tidak disalin. Sumber daya lain bernama `results` tetap disertakan.

Mode symlink menjaga hubungan langsung dengan folder skill sumber. Pertahankan checkout sumber; perubahan di sana mengubah instalasi yang ditautkan. Karena seluruh folder ditautkan, berkas evaluasi sumber tetap dapat dijangkau melalui tautan itu. Mode salin lebih sederhana untuk instalasi stabil yang sudah ditinjau.

## Memverifikasi instalasi

Jalankan kembali perintah instalasi yang sama setelah menerapkannya. Instalasi milik installer yang sesuai melaporkan `keep`; penerapan ulang seharusnya tidak mengubah isi dan settings.

Mulai sesi host baru dan periksa inventaris skill sebenarnya. Di Claude Code, bandingkan entri slash-command yang tersedia dengan daftar yang terlihat oleh model. Entri manual dapat tetap tersedia bagi pengguna meskipun tidak ada dalam daftar model. Di Codex, gunakan pemilihan skill eksplisit dan pastikan isi skill terpasang yang dipilih benar-benar digunakan; pencantuman nama tidak membuktikan aktivasi.

Untuk pemeriksaan kecil dari awal sampai akhir, pasang entri wawancara dan coba perintah eksplisit pada rencana hipotetis yang aman. Gunakan [referensi perintah yang dihasilkan](typed-commands.md) untuk sintaks host. Wawancara yang diharapkan tidak menulis berkas proyek dan menunggu konfirmasi penutupnya.

Bukti discovery yang tercatat tersedia untuk instalasi salin dan symlink pada kedua host. Eksperimen awal itu mencakup profil historis yang lebih kecil; profil yang dihasilkan saat ini menjadi acuan closure sekarang. [Halaman dukungan](harnesses.md) menjelaskan apa yang dibuktikan pengujian tersebut.

## Memperbarui, memindahkan, dan menghapus instalasi

Perbarui checkout sumber yang sama, periksa diff, hasilkan ulang kebijakan jika perlu, lalu lihat pratinjau instalasi lagi. Sumber yang tidak berubah menghasilkan `keep`. Tujuan yang masih dimiliki installer dan belum diubah membutuhkan `--force` untuk diperbarui jika sumbernya berubah.

```sh
scripts/install-skills.py --host codex --target ~/.codex/skills \
  --force clear-communication
scripts/install-skills.py --host codex --target ~/.codex/skills \
  --force --apply clear-communication
```

Di sini `--force` mengizinkan pembaruan tujuan yang masih dimiliki installer. Flag ini tidak menimpa folder asing, salinan yang diedit lokal, atau catatan kepemilikan yang diubah. Selesaikan konflik yang disebutkan terlebih dahulu. Catatan tersebut terikat pada lokasi checkout sumber; memindahkan sumber juga dapat membutuhkan rekonsiliasi.

Installer tidak memiliki perintah uninstall umum. Menghapus paket terpasang atau override settings membutuhkan pemeriksaan kepemilikan yang terbatas cakupannya; menghapus folder saja dapat meninggalkan settings atau paket dependen. Gunakan [checklist peralihan](cutover.md) saat mengganti koleksi upstream, dan simpan catatan rollback untuk berkas serta settings yang terdampak.

## Menyiapkan proyek untuk alur utama

Skill pembentukan rencana membaca kontrak proyek kecil: lokasi tracker, nama label triase, serta lokasi glosarium dan ADR. Buat sekali per proyek dengan mengetik `/setup-agent-skills` (Claude Code) atau `$setup-agent-skills` (Codex) dalam proyek tersebut.

Skill ini menulis satu blok `## Agent skills` dalam `AGENTS.md` atau `CLAUDE.md` dan hingga tiga berkas: `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, dan `docs/agents/domain.md`. Berkas glosarium dan ADR dibuat kemudian, saat istilah atau keputusan pertama dicatat.

Tanpa kontrak itu, `to-spec` dan `to-tickets` mengembalikan draf dalam percakapan alih-alih mengajukannya, dan `grill-with-docs` menawarkan wawancara biasa tanpa penulisan dokumen.

## Menerapkan gaya penulisan pada jawaban sehari-hari

Agar jawaban biasa mengikuti aturan komunikasi tanpa memuat skill, salin kontrak tetap dari [`skills/clear-communication/references/house-style.md`](../../skills/clear-communication/references/house-style.md) ke `AGENTS.md`, `CLAUDE.md`, atau instruksi global host Anda. Isinya tujuh baris: dahulukan jawaban, gunakan kata sesedikit mungkin yang tetap akurat, pertahankan fakta persis, gunakan kata sederhana, tanyakan hanya hal yang mengubah hasil, nyatakan asumsi yang dapat dibatalkan, dan ulangi hanya bagian yang belum pasti.

## Metode instalasi lainnya

README sebelumnya menyarankan `npx skills add cravingmaker/skills`, dan folder individual dapat disalin manual ke direktori skill host. Metode itu tidak membuktikan bahwa closure wajib repositori atau adapter settings Claude telah berjalan. Gunakan installer milik koleksi saat Anda membutuhkan penyelesaian dependensi, catatan kepemilikan, dan kebijakan entri manual sekaligus.

Host lain mungkin memahami format Agent Skills tetapi memiliki kontrol pemanggilan berbeda. Anggap perilakunya belum diuji sampai Anda memverifikasinya; lihat [harness yang didukung](harnesses.md).

## Saat terjadi kegagalan

| Pesan atau gejala | Tindakan |
| --- | --- |
| `... is required but is neither in .../skills nor an external skill in the catalog` | Skill wajib hilang dari sumber instalasi. Tarik repositori lengkap; jangan memasang dari salinan parsial. |
| `foreign or edited destination conflict; reconcile it explicitly (--force cannot overwrite it)` | Folder ada dan bukan salinan installer yang belum berubah. Periksa kepemilikan dan selesaikan konflik sebelum memasang kembali. |
| `owned installation changed at source; preview with --force to update it` | Anda menarik versi baru. Lihat pratinjau lalu terapkan dengan `--force`. |
| `host configuration drift; preview scripts/build-host-config.py, then run it with --apply` | Kebijakan Codex yang dihasilkan sudah tertinggal dalam clone Anda. Jalankan `scripts/build-host-config.py --apply` dalam clone bersih, atau tarik kembali. |
| `Claude settings in linked Git worktrees, separate Git directories or repository subdirectories are unsupported` | Berikan root checkout utama atau proyek mandiri kepada `--project-root`, bukan worktree. |
| `Claude user and project settings overlap; choose a separate project root` | Anda memberi folder home kepada `--project-root`. Gunakan folder proyek. |
| `Claude skillOverrides support not found ...` | `claude` pada `PATH` berupa wrapper atau build yang tidak didukung. Berikan executable native dengan `--claude-bin`. |
| `a higher-precedence Claude settings file exposes this user entry` | Berkas settings proyek atau lokal mengaktifkan skill kembali. Pasang pada cakupan tersebut, atau hapus override itu. |

Gejala lain beserta penyebab dan perbaikannya tersedia di [Hal yang perlu diperhatikan](gotchas.md).
