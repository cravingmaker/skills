> **Dokumentasi untuk manusia.** Agen hanya boleh membaca halaman ini jika diminta oleh seseorang.

Bahasa: [English](../install-and-discovery-proof.md) · [Bahasa Indonesia](install-and-discovery-proof.md)

# Bukti historis instalasi dan discovery

Ini eksperimen 2026-11-08 pada sumber yang dipatok, termasuk profil historis tujuh paket. Keanggotaan katalog dan profil saat ini dihasilkan secara terpisah.

## Daftar isi

- [Mencatat konteks](#mencatat-konteks)
- [Metode dan isolasi](#metode-dan-isolasi)
- [Hasil instalasi](#hasil-instalasi)
- [Biaya discovery](#biaya-discovery)
- [Anggaran dan batasan](#anggaran-dan-batasan)
- [Ketepatan routing dengan skill yang sudah ada](#ketepatan-routing-dengan-skill-yang-sudah-ada)
- [Mereproduksi dan memvalidasi](#mereproduksi-dan-memvalidasi)

## Mencatat konteks

[PR #10](https://github.com/cravingmaker/skills/pull/10) mencatat inti yang kemudian dipasang dan discovery yang diamati. Catatan ini bukan petunjuk instalasi saat ini; gunakan [Memulai](getting-started.md) dan [referensi profil saat ini](routing.md#isi-setiap-profil).

# Bukti instalasi dan discovery

Instalasi salin dan symlink membuat tepat tujuh skill profil `agent-orchestrator` ditemukan pada kedua host sebenarnya di luar checkout ini. Installer menolak distribusi tidak lengkap dengan pesan yang menyebutkan prasyarat hilang.

Diukur pada macOS pada 2026-11-08 menggunakan tree downstream `feat/role-agent-orchestrator` pada `822565a127508fe88dd0909a7d9587a81d304c3e`, Codex CLI `0.167.0`, dan Claude Code `2.1.311`. Branch fondasi tidak berisi router peran atau profil peran yang dihasilkan; pengukuran ini membutuhkan distribusi sumber downstream tersebut.

## Metode dan isolasi

[Probe discovery](../../scripts/measure-skill-discovery.py) memanggil `install-skills.py` dari direktori kerja sementara baru menuju `$HOME/.codex/skills` atau `$HOME/.claude/skills` sementara yang privat. Probe menggunakan allowlist lingkungan dan konfigurasi host harness evaluasi, dengan direktori home, konfigurasi, cache, dan temp privat. Home asli, cache terpasang, settings, dan kredensial tidak menerima penulisan. Probe tidak membaca atau menyalin autentikasi.

Discovery Codex menggunakan app-server `initialize`, `initialized`, lalu `skills/list` dengan `forceReload: true`. Discovery Claude mengirim permintaan kontrol SDK `initialize` tanpa pesan pengguna; respons berisi perintah terpasang dan deskripsi lengkap. Perintah bawaan dihitung terpisah, skill bawaan dinonaktifkan, dan skill `plugin-authoring` Claude yang tersisa dimatikan dalam settings sementara. `get_context_usage` Claude dengan `detail: summary` juga melaporkan estimasi lokal, dengan `apiUsage: null`.

Untuk mengukur daftar yang benar-benar ditampilkan, probe mengarahkan CLI sebenarnya ke penampung permintaan loopback-only, menggunakan penyedia Codex tanpa autentikasi atau key API Claude dummy. Penampung menangkap permintaan tertunda; probe menghentikan CLI sebelum mengembalikan respons. Proses ini melakukan nol inferensi model dan tidak menggunakan kuota langganan. Home host sementara dan permintaan mentah dihapus; JSON ekspor berisi metadata discovery dan daftar yang ditampilkan.

## Hasil instalasi

| Host | Mode instalasi | Terpasang / ditemukan | Symlink profil | Byte `SKILL.md` sumber sesuai |
| --- | --- | ---: | ---: | --- |
| Codex | Salin | 7 / 7 | 0 | Ya |
| Codex | Symlink | 7 / 7 | 7 | Ya |
| Claude Code | Salin | 7 / 7 | 0 | Ya |
| Claude Code | Symlink | 7 / 7 | 7 | Ya |

Setiap inventaris persis berisi `agent-briefing`, `agent-debate`, `agent-orchestrator`, `clear-communication`, `decision-log`, `result-verification`, dan `work-decomposition`. Instalasi salin dan symlink menghasilkan daftar ternormalisasi yang sama pada masing-masing host.

Untuk setiap host, bukti dependensi hilang menghapus `result-verification` dari instalasi salin sementaranya, mengekspos instalasi itu sebagai `skills/` distribusi sekali pakai, dan menyediakan salinan sementara `catalog/skills.yaml`. Memasang router dari distribusi itu keluar dengan `1`, melaporkan `result-verification is required but is neither in .../skills nor an external skill in the catalog`, dan tidak membuat folder tujuan. Memasang ulang dari checkout lengkap dengan `--force` memulihkan dependensi; kedua host kembali menemukan ketujuh skill. Installer menyelesaikan distribusi yang diberikan; installer tidak otomatis mengaudit sembarang tujuan yang sudah ada. Aturan prasyarat dan berhenti milik router dibaca, tetapi tidak ada klaim eksekusi model atas aturan itu.

## Biaya discovery

Karakter menghitung baris skill yang ditampilkan, ditambah tabel root bersama dan heading Codex; instruksi host tetap, encoding JSON, alat, dan isi skill dikecualikan. Prefix home sementara dinormalisasi menjadi `$HOME`; ukuran mentah terukur juga ditampilkan. Estimasi token bersama adalah `ceil(normalized characters / 4)` dan bukan hitungan tokenizer persis.

Snapshot terpasang memutar ulang metadata dan kebijakan visibilitas dari registrasi plugin lokal aktif Codex ditambah lima skill sistem (42 skill yang sudah ada), serta plugin terdaftar Claude ditambah 16 skill tersinkron (43 skill yang sudah ada). Deklarasi plugin mengecualikan folder yang belum diterbitkan dan fixture test tertanam. Isi skill, hook, alat, connector, dan konfigurasi pribadi tidak disertakan dalam replay. Kasus sintetis menambah 30 placeholder berbeda, masing-masing dengan deskripsi 288 karakter; kasus itu memperkirakan biaya daftar tambahan tanpa mengklaim beberapa profil peran nyata tersedia.

| Host | Skenario | Ditemukan | Ditampilkan | Karakter, ternormalisasi (mentah) | Estimasi token | Deskripsi dipendekkan | Dihilangkan oleh kebijakan visibilitas |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Codex | Hanya profil | 7 | 7 | 2,353 (2,434) | 589 | 0 | 0 |
| Codex | Profil + snapshot terpasang | 49 | 32 | 9,601 (9,682) | 2,401 | 0 | 17 |
| Codex | Snapshot + 30 placeholder | 79 | 62 | 19,861 (19,942) | 4,966 | 0 | 17 |
| Claude Code | Hanya profil | 7 | 7 | 2,026 (2,026) | 507 | 0 | 0 |
| Claude Code | Profil + snapshot terpasang | 50 | 34 | 15,147 (15,147) | 3,787 | 0 | 16 |
| Claude Code | Snapshot + 30 placeholder | 80 | 64 | 24,357 (24,357) | 6,090 | 0 | 16 |

Kedua antarmuka discovery tidak memendekkan deskripsi dalam skenario ini; keduanya mengembalikan setiap nama terpasang. Claude menormalkan whitespace deskripsi `learn` tersinkron dari 982 menjadi 979 karakter; teks tidak dipotong karena anggaran. Estimasi SDK Claude yang terpisah untuk ketiga skenario adalah 673, 5,038, dan 8,098 token; estimasi lokal itu menggunakan metode berbeda dari estimasi berbasis karakter bersama.

Sebagai pembacaan kedua permintaan sintetis, profil + 30 placeholder saja mengukur 12,613 karakter / sekitar 3,154 token di Codex dan 11,236 karakter / sekitar 2,809 token di Claude, dengan seluruh 37 deskripsi utuh.

Replay cache Codex yang lebih luas mencakup skill yang dideklarasikan paket cache tingkat atas, tujuh berkas langsung `skills/*/SKILL.md` Neon tanpa manifest, dan skill sistem, termasuk paket dorman; ini batas atas, bukan klaim semua paket cache aktif. Replay menemukan 140 skill, menampilkan 98 setelah kebijakan visibilitas, memendekkan 75 deskripsi, dan menggunakan 21,786 karakter ternormalisasi (21,867 mentah), sekitar 5,447 token. Penambahan 30 placeholder menemukan 170, menampilkan 128, memendekkan 121 deskripsi, dan menggunakan 21,812 karakter (21,893 mentah), sekitar 5,453 token. Semua deskripsi tetap lengkap dalam `skills/list`; pemendekan hanya muncul dalam prompt yang ditangkap. Deskripsi router 317 karakter menjadi 178 pada kasus cache luas dan 118 dengan placeholder. Tidak ada skill tambahan yang dihilangkan karena anggaran pada kedua proses cache luas itu.

## Anggaran dan batasan

[Dokumentasi Codex](https://learn.chatgpt.com/docs/build-skills) menyebut anggaran daftar awal default 2% dari konteks model, fallback 8,000 karakter saat ukuran konteks tidak diketahui, pemendekan deskripsi sebelum penghilangan skill dengan peringatan, dan `skills.max_context_tokens` yang dapat dikonfigurasi hingga 10,000 token. Rekaman menunjukkan pemendekan pada CLI terpasang. Penyedia Codex loopback menggunakan nama model yang tidak dikenal dan metadata model fallback CLI; ini tidak menetapkan anggaran model produksi atau secara independen menguji cabang 8,000 karakter untuk konteks tidak diketahui.

[Dokumentasi Claude](https://code.claude.com/docs/en/skills#skill-descriptions-are-cut-short) menyebut anggaran daftar default 1% dari konteks model, batas 1,536 karakter per deskripsi, dan penghilangan deskripsi dengan tetap mempertahankan nama saat daftar melebihi anggaran. Tidak ada daftar Claude yang diuji membutuhkan pengurangan itu. Ringkasan SDK melaporkan konteks satu juta token menggunakan metadata model default; tangkapan permintaan independen memilih `haiku`.

Replay mempertahankan nama sumber, deskripsi, flag manual-only, dan kebijakan Codex `agents/openai.yaml`, tetapi memasang metadata sebagai skill mandiri. Namespace dan path plugin asli dapat menambah karakter dalam sesi plugin langsung. Pengaktifan plugin yang dikelola server, peringkat berbasis penggunaan, dan ketepatan routing berada di luar bukti daftar lokal ini. Isi cache dan versi host dapat berubah, sehingga pengulangan menyimpan hash sumber serta hitungannya sendiri.

## Ketepatan routing dengan skill yang sudah ada

Seluruh 32 uji routing valid sesuai dengan himpunan pemilihan yang ditetapkan sebelum eksekusi: delapan prompt, dua skenario profil, dan kedua host. Tidak ada pemilihan pertama tak terduga atau pengalihan ke skill terpasang yang sudah ada. Ini menyediakan pengamatan routing untuk skenario di bawah; ini tidak menetapkan tingkat kesalahan routing umum.

Diukur pada 2026-11-08 terhadap worktree downstream `feat/role-agent-orchestrator` pada `10fa1016a0a87e8c1c501d1adde11a9bde6fd683`. Claude Code `2.1.311` melaporkan model efektif `claude-opus-5-5`; Codex CLI `0.167.0` melaporkan `gpt-6.1-sol`. Keduanya menggunakan default host dalam konfigurasi bersih yang dihasilkan. `system.init` Claude dan rollout sesi Codex membuktikan nama model itu; revisi bobot backend yang lebih spesifik tidak ditampilkan.

### Profil dan closure dependensi bersama

Skenario satu peran memasang `agent-orchestrator` bersama skill pengguna yang sudah terpasang. Skenario tumpang tindih memasangnya dengan tiga router peran sintetis dari distribusi sekali pakai di luar semua repositori. Skill sintetis adalah fixture test, bukan peran yang tersedia.

| Profil | Closure wajib lengkap |
| --- | --- |
| `agent-orchestrator` | `agent-briefing`, `agent-debate`, `agent-orchestrator`, `clear-communication`, `decision-log`, `result-verification`, `work-decomposition` |
| `proof-quality-lead` | `agent-briefing`, `agent-debate`, `clear-communication`, `decision-log`, `proof-quality-lead`, `proof-quality-review`, `result-verification`, `work-decomposition` |
| `proof-release-lead` | `clear-communication`, `decision-log`, `proof-release-lead`, `proof-release-plan`, `work-decomposition` |
| `proof-design-chair` | `agent-briefing`, `agent-debate`, `clear-communication`, `decision-log`, `proof-design-chair`, `proof-design-options`, `work-decomposition` |

Keempat closure berisi total 27 entri dan menghasilkan 13 direktori skill berbeda, menghindari 14 salinan duplikat. Setiap kapabilitas bersama muncul sekali dalam inventaris setiap profil terpasang. Khususnya, `agent-debate` digunakan bersama oleh orchestrator, quality lead, dan design chair. Deskripsi kapabilitas sintetis sengaja menyerupai `result-verification`, `work-decomposition`, dan `agent-debate`, sementara isinya membedakan QA manusia, rilis manusia, dan perbandingan usulan desain.

Setiap sesi model menggunakan `install-skills.py --root DISTRIBUTION --target PRIVATE_SKILLS --mode copy NAME...` sebenarnya dari workspace baru di luar checkout. Installer menerima satu nama peran atau keempatnya sekaligus; keluaran dan byte terpasang diperiksa terhadap gabungan yang dideklarasikan. Rute prosa opsional tidak ditambahkan ke closure profil.

Inventaris yang sudah ada disalin dengan isi skill lengkap, sumber daya, dan field visibilitas asli, termasuk Codex `agents/openai.yaml`. Himpunan sumbernya sesuai dengan snapshot plugin-terdaftar/sistem atau tersinkron di atas: 42 nama skill Codex dan 43 nama skill Claude yang sudah ada. Semua 85 hash `SKILL.md` sumber tetap sesuai setelah eksperimen. Eksekusi plugin, connector, hook, dan settings pribadi tidak disertakan; ini salinan mandiri skill terpasang.

| Host | Inventaris satu peran | Inventaris peran tumpang tindih |
| --- | ---: | ---: |
| Claude Code | 50 nama skill pengguna | 56 nama skill pengguna |
| Codex | 50 catatan, 49 nama berbeda | 56 catatan, 55 nama berbeda |

Catatan Codex tambahan adalah template `starter-workflow` dengan byte identik yang tertanam dalam aset `create-plugin` yang sudah ada sekaligus terpasang di tingkat atas; ini tidak terkait dependensi profil. Claude juga mencantumkan skill bawaan `doctor` yang dideklarasikan SDK dalam setiap trace startup valid; skill itu tidak pernah dipanggil. Inventaris discovery dan startup diperiksa terhadap sumber yang tidak terkontrol.

### Prompt tetap dan pemilihan yang diharapkan

Kumpulan prompt dan rubrik pemilihan ditulis pada `2026-11-08T10:04:29Z`, sebelum start model pertama pada `10:05:43Z`. SHA-256 himpunan kasus JSON terurut adalah `b27947959471894da745bbd6843176ed63fc75ddc59002767791aa71e4eb9718`. Setiap sesi menerima kontrak komunikasi tetap yang sama dan batas routing-only: pilih dan baca skill terkait, berikan tindakan berikutnya, lalu berhenti sebelum mengerjakan tugas lebih besar, menulis artefak, atau melakukan dispatch pekerja.

Aktivasi pertama yang dikonfirmasi harus berada dalam himpunan yang dinyatakan. `None` mewajibkan tidak ada aktivasi skill; kontrol peran tidak tersedia juga mewajibkan pelaporan ketidaktersediaan peran itu. Pembacaan berikutnya dapat memuat prasyarat wajib atau kapabilitas terkait tugas yang beralasan. Prompt ambigu sengaja mengizinkan beberapa titik masuk yang dapat diterima; prompt tidak menguji satu skill pemenang unik.

| ID | Prompt persis | Pemilihan pertama yang diharapkan, satu peran | Pemilihan pertama yang diharapkan, tumpang tindih |
| --- | --- | --- | --- |
| R1 | Act as agent-orchestrator. Plan a fleet of three AI agents to compare data-migration approaches, with one integration owner, disjoint write paths, at most two concurrent workers, and six total worker starts. Give the initial plan only; do not dispatch. | `agent-orchestrator` | `agent-orchestrator` |
| R2 | Coordinate a resumed multi-agent run. One worker report is saved, a second worker has no receipt, and two incompatible approaches remain. Describe reconciliation and the next step before starting more agents. | `agent-orchestrator` atau `decision-log` | Sama |
| R3 | Act as proof-quality-lead. Assess this human QA handoff: the criterion is that all five exports open; the handoff says exports pass but supplies screenshots for only two. Identify the acceptance gap and next check. If that role is unavailable, report it unavailable and stop. | None; peran tidak tersedia | `proof-quality-lead` |
| R4 | Act as proof-release-lead. Plan a human release with database, documentation, and support owners; database and documentation both change release-notes.md, and the release budget is not yet set. Identify ownership, order, and the first budget decision. If that role is unavailable, report it unavailable and stop. | None; peran tidak tersedia | `proof-release-lead` |
| R5 | Compare two proposed database migration approaches with an evidence rubric and a bounded disagreement process. Give the process only; no workers or live checks. | `agent-debate` | `agent-debate`, `proof-design-chair`, atau `proof-design-options` |
| R6 | The plan has tasks, owners, shared files, and an unknown worker budget. Check whether splitting it is worthwhile and identify the first budget decision. Do not start anyone. | `work-decomposition` atau `agent-orchestrator` | Sama |
| R7 | What does the English word 'orchestrator' mean? Answer in one sentence. | None | None |
| R8 | Compute 19 + 23. Reply with only the number. | None | None |

### Pemilihan yang diamati dan bukti trace

| Prompt | Claude, tunggal | Codex, tunggal | Claude, tumpang tindih | Codex, tumpang tindih |
| --- | --- | --- | --- | --- |
| R1 | `agent-orchestrator` | `agent-orchestrator` | `agent-orchestrator` | `agent-orchestrator` |
| R2 | `agent-orchestrator` | `agent-orchestrator` | `agent-orchestrator` | `agent-orchestrator` |
| R3 | None; tidak tersedia | None; tidak tersedia | `proof-quality-lead` | `proof-quality-lead` |
| R4 | None; tidak tersedia | None; tidak tersedia | `proof-release-lead` | `proof-release-lead` |
| R5 | `agent-debate` | `agent-debate` | `proof-design-options` | `proof-design-options` |
| R6 | `work-decomposition` | `work-decomposition` | `work-decomposition` | `work-decomposition` |
| R7 | None | None | None | None |
| R8 | None | None | None | None |

Pemanggilan `Skill` Claude yang berhasil atau `Read` langsung atas isi terpasang dihitung sebagai aktivasi. Codex membutuhkan perintah pembaca sederhana yang berhasil, memuat path absolut `SKILL.md`, dan menampilkan isi, sesuai aturan harness. Nama skill dalam jawaban, pencarian, perintah gagal, dan entri inventaris tidak dihitung. Semua 60 event aktivasi tercatat diperiksa terhadap baris trace mentahnya. Satu-satunya perintah Codex yang tidak terklasifikasi, R4 satu peran pada baris trace 5, adalah `rg --files`; pemeriksaan manual memastikan perintah itu hanya mencantumkan path tanpa membaca isi skill, sehingga tidak ada aktivasi ditambahkan.

Bukti mentah tetap di luar repositori publik ini, seperti bukti evaluasi mentah: eksperimen yang dibekukan, catatan anggaran proses, pemeriksaan integritas, urutan aktivasi setiap proses, trace mentah, catatan hasil, profil, prompt persis, hash sumber, konfigurasi, inventaris efektif, model, sesi, penggunaan, keluaran installer, dan keputusan trace manual. Catatan Codex juga menyertakan rollout sesi. Tidak satu pun dari 32 fixture valid berubah, dan semua sesi berbeda.

### Salah rute, anggaran, dan batasan

Tidak ada pemilihan pertama tak terduga menurut rubrik tetap. Kedua host mengubah R5 dari `agent-debate` menjadi `proof-design-options` saat profil tumpang tindih tersedia; pemilihan itu diizinkan. Deskripsi sintetis sangat sesuai dengan frasa rubrik bukti dan proses perbedaan pendapat terbatas pada prompt, sehingga menjadi penjelasan yang mungkin untuk pergeseran itu, bukan hasil kausal yang terbukti. Ini tidak membuktikan router peran harus selalu didahulukan daripada kapabilitas yang langsung sesuai.

Kontrol peran tidak tersedia mengungkap masalah keluaran terpisah: Claude mencari definisi agen native dan menyarankan berkas `.claude/agents` untuk peran yang hilang. Claude tetap tidak memuat skill dan memenuhi harapan routing, tetapi saran itu tidak mereproduksi alur instalasi skill peran repositori ini. Codex terkadang membaca ulang isi kapabilitas, termasuk `agent-debate` saat melanjutkan proses; pembacaan tambahan itu dipertahankan dalam laporan, bukan dihitung sebagai pemilihan skill baru.

Ada 33 start model, termasuk satu uji validasi startup Claude yang dibuang, dengan puncak dua proses aktif dan tujuh start tersisa dari batas 40 proses. Parser lokal pertama keliru menolak entri bawaan `doctor` yang dideklarasikan. Trace uji pertama itu tidak disimpan dan tidak mendukung klaim routing; R1 diulang sekali. Trace R2 yang disimpan diklasifikasi ulang setelah perbaikan parser tanpa pemanggilan model tambahan, dengan catatan parser awal tetap disimpan. Tidak ada prompt atau harapan pemilihan yang berubah. Empat preflight discovery awal menggunakan nol giliran model.

Ini uji tunggal per host, prompt, dan skenario profil, dengan model default host berbeda. Uji mengukur pemilihan awal, bukan delegasi selesai, pembacaan seluruh prasyarat, mutu hasil akhir, atau pengaruh kausal deskripsi. Batas routing umum secara eksplisit meminta model membaca instruksi terkait, sehingga pengamatan bukan estimasi tingkat aktivasi tanpa arahan. Namespace plugin, alat plugin, discovery terkelola server, paket cache dorman, dan routing produksi dengan konfigurasi plugin langsung tidak direproduksi. Tidak ada pengukuran anggaran daftar model produksi dalam uji ini. Rekaman biaya discovery di atas tetap merupakan bukti terpisah.

Setiap proses menggunakan home, konfigurasi, cache, direktori temp, dan workspace privat baru dengan allowlist lingkungan serta settings host yang dihasilkan harness evaluasi. Hanya autentikasi yang disalin ke berkas sementara mode-0600; autentikasi tidak pernah diekspor atau dicetak. Bukti ekspor diperiksa terhadap nilai kredensial yang diketahui. Semua home host privat dihapus, dan bukti yang disimpan tidak mengandung berkas autentikasi. Folder terpasang pengguna tidak menerima penulisan.

## Mereproduksi dan memvalidasi

Jalankan probe fondasi saat ini terhadap distribusi sumber terpisah yang berisi peran tersebut. Jika commit downstream yang diukur tersedia secara lokal, ekspor tanpa mengubah kedua checkout, lalu jalankan dari direktori sementara:

```sh
repo=$(pwd -P)
proof_root=$(mktemp -d)
mkdir "$proof_root/source"
git -C "$repo" archive 822565a127508fe88dd0909a7d9587a81d304c3e | tar -x -C "$proof_root/source"
cd "$proof_root"
export UV_CACHE_DIR="$proof_root/uv-cache" PYTHONDONTWRITEBYTECODE=1
for host in codex claude; do
  for mode in copy symlink; do
    "$repo/scripts/measure-skill-discovery.py" --root "$proof_root/source" --host "$host" --mode "$mode" \
      --output "$proof_root/$host-$mode.json"
  done
done
"$repo/scripts/measure-skill-discovery.py" --root "$proof_root/source" --host codex --placeholders 30 \
  --output "$proof_root/codex-synthetic.json"
```

Untuk snapshot terpasang, tambahkan `--plugin-root /absolute/cache/package/version` untuk setiap registrasi terpilih dan `--extra-skill /absolute/SKILL.md` untuk metadata sistem atau tersinkron. Tambahkan `--placeholders 30` pada perintah yang sama untuk kasus sintetis gabungan. Laporan pekerja menyimpan perintah lengkap persis dan nama sumber beserta panjang deskripsinya. Setiap catatan JSON menyertakan versi host, hasil installer, baris discovery, teks dan hash daftar, flag kebijakan, serta hasil per deskripsi; catatan snapshot juga menyertakan hash berkas sumber yang sudah ada.

Kesembilan [test probe offline](../../tests/discovery-cost.py), fixture installer, dan 22 test isolasi harness evaluasi lulus tanpa pemanggilan model. `./scripts/validate.sh` keluar dengan `0`, termasuk validator skill yang dipatok, pemeriksaan katalog/profil, fixture skill, pemeriksaan freshness, dan zizmor. Vale tidak terpasang, sehingga suite melewati lint prosa; perintah prosa terpisah keluar dengan `2` beserta diagnostik penyiapan tersebut. Jalankan `uv run --script tests/discovery-cost.py`, `tests/install/run.sh`, dan `tests/eval-harness/run.sh` untuk mengulang pemeriksaan terfokus.

Eksperimen routing menggunakan driver lokal sekali pakai yang dibangun di atas adapter harness yang ada dan installer sebenarnya; tidak diperlukan skrip repositori baru. Driver mempertahankan prompt yang dibekukan, menolak menimpa catatan proses, memeriksa snapshot sumber sebelum persiapan, menolak perubahan inventaris tak terkelola, mencadangkan setiap start model dalam catatan anggaran sebelum peluncuran, dan menghapus setiap home host saat berhasil maupun gagal. Driver bukan harness routing publik yang didukung, sehingga replay membutuhkan driver baru dan anggaran baru yang dialokasikan secara eksplisit untuk 32 sesi model.
