> **Dokumentasi untuk manusia.** Agen hanya boleh membaca halaman ini jika diminta oleh seseorang.

Bahasa: [English](../README.md) · [Bahasa Indonesia](README.md)

# Menggunakan koleksi skill

Handbook ini menjelaskan perintah yang diketik, tindakan agen berikutnya, dan hal yang benar-benar dibuktikan oleh bukti yang tersedia. Mulailah dengan instalasi, lalu gunakan panduan berdasarkan tujuan untuk pekerjaan Anda.

Dalam blok yang dihasilkan otomatis, hanya label tetap dan teks penghubung yang diterjemahkan. Deskripsi skill, contoh prompt, nama perintah, dan nilai katalog tetap sama dengan sumbernya. Contoh prompt dalam `intent-guide.json` juga tetap berbahasa Inggris; penjelasan tujuannya tersedia dalam kedua bahasa.

## Daftar isi

- [Mulai dan memilih](#mulai-dan-memilih)
- [Merencanakan, membangun, dan menyerahkan](#merencanakan-membangun-dan-menyerahkan)
- [Memahami batasannya](#memahami-batasannya)
- [Cara koleksi ini dipelihara](#cara-koleksi-ini-dipelihara)
- [Istilah yang digunakan](#istilah-yang-digunakan)
- [Alasan handbook dipisahkan](#alasan-handbook-dipisahkan)

## Mulai dan memilih

| Pertanyaan Anda | Bacaan |
| --- | --- |
| Bagaimana memasangnya di Claude Code atau Codex? | [Memulai](getting-started.md) |
| Perintah mana yang saya ketik, dan mengapa hanya bisa dipilih manual? | [Perintah yang diketik](typed-commands.md) |
| Skill mana yang sesuai dengan tujuan saya? | [Memilih berdasarkan tujuan](choosing-skills.md) |
| Apa fungsi satu skill, dan kapan sebaiknya tidak digunakan? | [Referensi skill lengkap](skills.md) |

## Merencanakan, membangun, dan menyerahkan

| Pertanyaan Anda | Bacaan |
| --- | --- |
| Bagaimana membawa ide melalui spec, tiket, implementasi, dan tinjauan? | [Alur yang disarankan](recommended-flow.md) |
| Apa yang dimuat koordinator, dan apa yang ikut dipasang? | [Routing dan dependensi](routing.md) |
| Bagaimana berhenti pada draf, PR yang diajukan, PR siap, atau merge? | [Batas penyerahan](recommended-flow.md#memilih-batas-penyerahan) |

## Memahami batasannya

| Pertanyaan Anda | Bacaan |
| --- | --- |
| Apa yang sering mengejutkan pengguna? | [Hal yang perlu diperhatikan](gotchas.md) |
| Apa yang rusak, sudah diperbaiki, terhambat, atau belum terbukti? | [Masalah yang diketahui](known-issues.md) |
| Apa hasil evaluasi yang dikomit pada byte skill saat ini? | [Hasil evaluasi](eval-results.md) |
| Host dan versi mana yang memiliki bukti? | [Harness yang didukung](harnesses.md) |
| Apa perbedaan mekanisme, alur, dan hasil antar-host? | [Perbedaan harness](harness-differences.md) |

## Cara koleksi ini dipelihara

Baca [cara koleksi ini dibuat](making-skills.md), [alasan dan cara pemeliharaannya](how-and-why.md), [changelog PR yang di-merge](../../CHANGELOG.md), dan [cara halaman ini dihasilkan](maintaining-docs.md). [Panduan penulisan](../../docs/authoring-guide.md), [kontrak instalasi](../../docs/installing.md), dan [harness evaluasi](../../docs/eval-harness.md) tetap menjadi dokumen teknis untuk agen. [Checklist peralihan](cutover.md) dan [bukti instalasi dan discovery](install-and-discovery-proof.md) adalah catatan sejarah khusus manusia.

## Istilah yang digunakan

| Istilah | Arti di sini |
| --- | --- |
| Skill | Folder berisi `SKILL.md` yang dimuat agen saat tugas membutuhkannya, mengikuti [spesifikasi Agent Skills](https://agentskills.io/specification). |
| Capability skill | Skill untuk satu pekerjaan, seperti `tdd` atau `file-pr`. |
| Router | `agent-orchestrator`, skill inti yang mengoordinasikan pekerjaan dan mengarahkannya melalui metode kapabilitas. |
| Model selection | Agen dapat memilih skill sendiri saat permintaan Anda sesuai dengan deskripsinya. Pemilihan eksplisit bergantung pada host. |
| Manual only | Katalog menandai skill dengan `invocation: user`: host menekan pemilihan implisit, dan Anda memilihnya dengan mengetik `/<name>` di Claude Code atau `$<name>` di Codex. |
| Requires | Hubungan `metadata.requires`: skill tidak dapat bekerja tanpa skill lainnya, sehingga memasangnya juga memasang skill tersebut. |
| Optional route | Kalimat seperti "use the `how` skill" dalam instruksi skill. Rute diikuti hanya jika cabang itu berlaku dan tidak memasang apa pun. |
| Profile | Seluruh skill yang dipasang koordinator: router beserta setiap skill yang dapat dicapai melalui `requires`. |
| Proof | Permukaan yang dijalankan atau sumber yang dibuka, beserta hasil yang diamati di sana, untuk menunjukkan bahwa story atau tiket selesai. |
| Evaluated | Status katalog untuk skill yang semua contoh Activation dan Near miss-nya memiliki catatan pasangan evaluasi valid, tanpa regresi yang belum diselesaikan dibanding proses tanpa skill. Lihat [arti evaluated](how-and-why.md#arti-evaluated). |
| Host atau harness | Program agen yang memuat skill: Claude Code atau Codex CLI. T3 Code adalah antarmuka yang menjalankan keduanya. |

## Alasan handbook dipisahkan

Handbook ditujukan kepada manusia dan berada di luar paket skill. Installer menyelesaikan nama skill wajib dan hanya menyalin atau menautkan foldernya di bawah `skills/`; direktori ini tidak pernah dipasang. Mode salin juga tidak menyertakan bukti `evals/results/` milik setiap skill.

Secara default, tidak ada instruksi atau metode untuk agen yang menaut ke sini. Generator dokumentasi memeriksa tautan tersebut, sementara README singkat repositori menyediakan navigasi bagi manusia. Ini mengurangi pemuatan tidak sengaja; berkas yang dapat dibaca tetap dapat diakses agen. Seseorang tetap dapat meminta agen membaca halaman handbook mana pun.
