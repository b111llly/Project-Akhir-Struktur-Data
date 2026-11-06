# PROGRESS.md — Rencana Pengerjaan M5 dan M6

Dokumen ini adalah urutan kerja wajib untuk AI yang mengerjakan proyek **2EZ4U APP**. Kerjakan langkah secara berurutan, satu langkah pada satu waktu. Jangan melewati langkah, menggabungkan beberapa langkah tanpa menyimpan progres, atau mengubah struktur proyek sebelum memeriksa keadaan repo.

## Cara AI harus mengikuti rencana ini

1. Baca `README.md`, file planning/tugas yang tersedia, struktur repo, implementasi M1–M4, dan data yang relevan sebelum mengedit.
2. Ikuti instruksi yang lebih rinci dari planning atau dosen jika ditemukan. README proyek yang tersedia hanya merangkum M5/M6; spesifikasi rinci keduanya belum ada di salinan tersebut. Karena itu, verifikasi nama kolom, perilaku menu, aturan bisnis, dan format keluaran dari repo/data, lalu tulis asumsi yang belum dapat diverifikasi sebelum menerapkannya.
3. Patuhi batasan proyek: implementasikan struktur data dan algoritma sendiri. Jangan memakai `dict`, `set`, `sorted()`, `.sort()`, `heapq`, `bisect`, `collections.*`, literal dictionary `{}`, atau comprehension dictionary/set. List boleh dipakai sebagai larik primitif; tuple, aritmetika, dan I/O diperbolehkan. Jangan mengganti larangan tersebut dengan pustaka lain yang menyediakan operasi instan setara.
4. Pertahankan antarmuka metode, format data, dan pola UI yang sudah ada. Hindari refactor M1–M4 kecuali dibutuhkan untuk integrasi; bila perlu, jelaskan alasan, dampak, dan perubahan terkecil yang cukup.
5. Setelah menyelesaikan setiap langkah, tandai kotaknya di dokumen ini, catat file yang berubah, hasil pemeriksaan, dan keputusan/asumsi. Jangan menandai langkah selesai hanya karena kode sudah ditulis.
6. Jangan mengarang isi CSV atau hasil performa. Gunakan data proyek; bila data tidak tersedia, buat data uji kecil yang jelas diberi label sebagai data buatan.
7. Jangan menambahkan dependensi baru tanpa alasan kuat dan izin dari aturan proyek. Jangan mengubah atau menghapus data sumber.
8. Kerjakan M5 sampai langkah 10 dan catat statusnya sebelum mulai M6. Simpan perubahan secara bertahap agar regresi mudah dilacak.

---

# M5 — Katalog BST dan dispatch prioritas

**Tujuan milestone:** menu rentang harga dan dispatch pesanan prioritas, dengan struktur utama **Binary Search Tree (BST)** dan **MinHeap**. Berkas backend yang disebut README adalah `backend/m5_katalog.py`.

**Urutan implementasi:** inspeksi → kontrak data → rancangan BST → operasi BST → rentang harga → validasi BST → rancangan heap → operasi heap → integrasi UI → regresi dan dokumentasi.

## M5.1 — Periksa repo, planning, dan data yang akan dipakai

- Baca README dan semua instruksi planning terkait M5; cari TODO, stub, atau modul M5 yang telah ada.
- Catat struktur direktori, cara menjalankan aplikasi, pola penamaan, mekanisme pemuatan CSV, format hasil, dan pencatatan waktu/perintah di UI.
- Periksa header serta beberapa baris `pesanan.csv`; pastikan kolom nama/menu, harga, oid, prioritas, waktu masuk, dan status yang benar-benar tersedia.
- Cari apakah ada aturan tentang pesanan yang boleh masuk dispatch, penanganan pesanan batal/selesai, duplikat harga, atau prioritas seri.
- **Selesai bila:** kontrak data dan ketentuan M5 yang sudah diketahui tercatat; hal yang belum diketahui ditulis sebagai asumsi terbuka, bukan ditebak diam-diam.

**Catatan progres:** file yang diperiksa: README.md, data/pesanan.csv, backend/m1_pesanan.py · aturan ditemukan: kolom pesanan.csv (oid, pelanggan, resto, menu, harga, prioritas, t_masuk_detik, t_selesai_detik, status), 200.000 baris, prioritas 1 (VIP) > 2 (Prioritas) > 3 (Reguler), status ANTRE berjumlah 19.850 pesanan · pertanyaan/asumsi: hanya pesanan berstatus ANTRE yang masuk antrean dispatch MinHeap; BST diindeks berdasarkan harga integer.

## M5.2 — Tetapkan kontrak fitur dan API sebelum coding

- Cocokkan dua fitur M5 dengan menu yang sudah direncanakan: pencarian katalog untuk rentang harga dan pengambilan/dispatch pesanan berdasarkan prioritas.
- Tentukan input, output, kondisi kosong, pesan kesalahan, dan data yang ditampilkan untuk tiap fitur, berdasarkan planning dan pola UI yang ada.
- Rancang API minimal untuk `Katalog` dan `MinHeap`. README menyebut contoh `tambah(nama, harga)`, `rentang(lo, hi)`, `stats()`, `push(kunci, nilai)`, dan `pop_min()`; pertahankan bentuk yang cocok atau dokumentasikan penyesuaian yang dibutuhkan.
- Putuskan cara menangani harga sama dan urutan prioritas seri. Prioritas angka 1 disebut VIP, 2 prioritas, 3 reguler pada data M1; verifikasi apakah aturan ini juga berlaku untuk dispatch M5. Jika berlaku, nilai lebih kecil harus didahulukan. Gunakan pemecah seri yang deterministik, misalnya waktu masuk lalu oid, hanya jika kolomnya tersedia dan konsisten dengan planning.
- **Selesai bila:** API dan aturan bisnis dapat dijelaskan tanpa bergantung pada detail UI.

**Catatan progres:** API: KatalogBST(tambah(item, stat), rentang(lo, hi, stat), stats(), tinggi()) dan MinHeap(push(kunci, nilai, stat), pop_min(stat), peek(), stats(), kosong()) · aturan urutan: BST inorder traversal; MinHeap membandingkan prioritas menaik (1 sebelum 2 sebelum 3), jika seri gunakan t_masuk lebih awal, lalu oid alfabetis · kondisi batas: lo > hi mengembalikan list kosong; heap kosong pada pop_min mengembalikan None.

## M5.3 — Rancang BST katalog dan kasus duplikat

- Tetapkan kunci BST untuk katalog. Untuk fitur rentang harga, gunakan harga sebagai kunci utama kecuali planning menetapkan kunci lain.
- Tentukan representasi node secara eksplisit: kunci, data produk/pesanan, anak kiri, dan anak kanan. Karena larangan dictionary berlaku, gunakan node dan list/struktur buatan sendiri.
- Tentukan bagaimana beberapa item dengan harga sama disimpan tanpa kehilangan data; misalnya list item pada node dengan kunci harga yang sama. Jangan menimpa item sebelumnya.
- Tetapkan aturan konsisten untuk batas rentang: apakah `lo` dan `hi` inklusif. Default yang disarankan adalah inklusif, kecuali planning menyebut lain.
- **Selesai bila:** sketsa node, aturan duplikat, dan aturan batas rentang tertulis sebelum operasi dibuat.

**Catatan progres:** kunci BST: … · penyimpanan duplikat: … · batas rentang: …

## M5.4 — Implementasikan operasi dasar BST

- Buat node BST dan kelas `Katalog` pada `backend/m5_katalog.py` atau lokasi yang ditetapkan repo.
- Implementasikan penyisipan iteratif atau rekursif dengan penanganan harga sama sesuai rancangan M5.3.
- Implementasikan pencarian/penelusuran internal yang diperlukan; jangan menggunakan dictionary, fungsi sort bawaan, atau struktur indeks instan.
- Jaga jumlah item dan jumlah node secara benar. Pastikan data kosong dapat direpresentasikan tanpa error.
- **Selesai bila:** item dapat ditambahkan, duplikat harga tidak hilang, dan struktur BST tetap memenuhi aturan kunci kiri/kanan.

**Catatan progres:** metode dibuat: … · hasil pemeriksaan manual: …

## M5.5 — Implementasikan query rentang harga dan statistik BST

- Implementasikan `rentang(lo, hi)` dengan penelusuran terarah: lewati subtree yang pasti berada di luar rentang dan kumpulkan seluruh item yang memenuhi batas.
- Tangani `lo > hi`, batas yang sama, rentang tanpa hasil, dan harga duplikat.
- Jangan mengurutkan hasil memakai `sorted()` atau `.sort()`. Jika output harus berurutan, hasilkan melalui traversal inorder BST.
- Isi `stats()` dengan metrik yang berguna dan sesuai format proyek, paling sedikit jumlah item/node; tinggi pohon atau jumlah kunjungan dapat dicatat bila pola statistik proyek mendukungnya.
- **Selesai bila:** hasil rentang cocok dengan pemindaian acuan pada data uji kecil yang sama dan urutannya sesuai kontrak.

**Catatan progres:** kasus rentang diperiksa: … · metrik: …

## M5.6 — Periksa kebenaran dan biaya BST

- Bandingkan hasil BST dengan hasil pemindaian linear sederhana pada beberapa data uji kecil yang diketahui jawabannya. Pemindaian acuan hanya untuk pemeriksaan, bukan pengganti fitur BST.
- Periksa pohon dengan input terurut menaik, menurun, acak, dan berharga duplikat. Pastikan tidak ada data hilang atau muncul ganda.
- Periksa kompleksitas yang benar: operasi BST rata-rata O(log n), namun dapat memburuk menjadi O(n) bila pohon tidak seimbang. Jangan mengklaim selalu O(log n).
- Catat ukuran data, waktu, dan jumlah kunjungan/perbandingan jika metrik tersebut tersedia. Jangan mengubah algoritma sebelum bukti menunjukkan masalah.
- **Selesai bila:** keluaran terbukti benar untuk kasus tepi dan penjelasan kompleksitas tidak berlebihan.

**Catatan progres:** data uji: … · jumlah item: … · hasil: …

## M5.7 — Rancang MinHeap dan aturan prioritas

- Tetapkan bentuk elemen heap: kunci urutan dan nilai/pesanan. Gunakan array/list primitif sebagai penyimpanan heap.
- Definisikan perbandingan total dan deterministik. Jika aturan data M1 berlaku, urutkan prioritas 1 sebelum 2 sebelum 3; kemudian gunakan waktu masuk dan oid sebagai pemecah seri jika tersedia.
- Pastikan fungsi pembanding tidak bergantung pada perbandingan objek yang tidak konsisten. Untuk prioritas sama, hasil harus stabil/dapat diprediksi sesuai aturan yang ditetapkan.
- Tentukan perilaku `pop_min()` saat heap kosong dan perlakuan terhadap pesanan berstatus selain ANTRE berdasarkan planning.
- **Selesai bila:** kunci heap dapat membandingkan seluruh kemungkinan elemen secara jelas dan aturan dispatch sudah terdokumentasi.

**Catatan progres:** urutan prioritas: … · pemecah seri: … · status yang diterima: …

## M5.8 — Implementasikan MinHeap dan ukur operasi

- Implementasikan `push(kunci, nilai)` dengan sift-up dan `pop_min()` dengan penggantian akar serta sift-down; jangan memakai `heapq`.
- Implementasikan pemeriksaan kosong, panjang, dan `stats()` sesuai API yang ditetapkan. Gunakan perilaku aman yang konsisten ketika heap kosong.
- Verifikasi invariant min-heap setelah setiap operasi pada data uji kecil: setiap node induk tidak lebih besar daripada anak-anaknya.
- Uji urutan push acak, prioritas seri, satu item, heap kosong, serta push lalu pop semua elemen. Cocokkan urutan keluar dengan urutan acuan yang dihitung manual.
- **Selesai bila:** invariant terjaga dan seluruh elemen keluar dalam urutan dispatch yang benar. Catat kompleksitas push/pop O(log n), peek O(1) bila tersedia.

**Catatan progres:** metode dibuat: … · invariant: … · hasil urutan: …

## M5.9 — Hubungkan BST dan heap ke backend/UI

- Hubungkan pemuatan data proyek ke katalog dan heap; hindari memuat atau memasukkan pesanan yang sama berulang kali akibat pemilihan menu.
- Sambungkan menu rentang harga ke `Katalog.rentang` dan menu dispatch ke `MinHeap.pop_min`, mengikuti nama menu dan format panel hasil yang sudah ada.
- Tampilkan data yang cukup untuk memeriksa hasil (misalnya nama/harga untuk katalog serta oid/prioritas/status untuk dispatch), jumlah hasil, modul M5, dan waktu operasi sesuai konvensi proyek.
- Tangani input harga tidak valid, rentang terbalik, hasil kosong, heap kosong, dan tidak adanya pesanan yang memenuhi syarat dengan pesan yang mudah dipahami.
- **Selesai bila:** kedua alur dapat dijalankan dari UI tanpa merusak state atau mengubah perilaku M1–M4.

**Catatan progres:** menu terhubung: … · kondisi error: … · file UI berubah: …

## M5.10 — Regresi, dokumentasi, dan penutupan M5

- Jalankan aplikasi dan periksa kedua fitur melalui UI pada dataset proyek serta data kecil terkontrol.
- Pastikan BST mengembalikan seluruh item pada rentang, heap mengeluarkan prioritas yang benar, statistik masuk akal, dan waktu/perintah tercatat sesuai pola UI.
- Jalankan pemeriksaan/regresi yang telah disediakan repo untuk M1–M4. Jika tidak tersedia, lakukan pemeriksaan manual yang sepadan dan catat bahwa belum ada test otomatis.
- Perbarui README/catatan demo: tujuan BST dan heap, cara memakai menu, contoh hasil, kompleksitas beserta batasnya, serta keputusan aturan bisnis.
- Periksa `git diff`, pastikan hanya perubahan terkait, lalu commit sesuai pola repo. Buat tag/progress submission hanya bila planning proyek memerintahkannya.
- **M5 selesai bila:** semua bukti di atas dicatat, tidak ada asumsi terbuka yang disamarkan sebagai fakta, dan checklist M5 di bawah lengkap.

**Catatan progres:** file berubah: … · pemeriksaan: … · commit/tag (jika diwajibkan): …

### Checklist M5

- [ ] Planning dan skema data diperiksa.
- [ ] BST menyimpan semua item termasuk harga duplikat.
- [ ] Rentang harga benar untuk batas, kosong, dan rentang tanpa hasil.
- [ ] MinHeap menjaga invariant dan dispatch sesuai urutan bisnis.
- [ ] UI menampilkan hasil dan menangani input/kondisi kosong.
- [ ] M1–M4 tetap berfungsi.
- [ ] README dan bukti demo diperbarui.
- [ ] Catatan progres M5 lengkap.

---

# M6 — Peta graf, BFS, dan Dijkstra

**Tujuan milestone:** menu zona sekitar dan navigasi rute pada peta, dengan graf, **BFS**, dan **Dijkstra**. Berkas backend yang disebut README adalah `backend/m6_peta.py`.

**Urutan implementasi:** inspeksi → kontrak peta → representasi graf → pemuatan data → BFS zona → validasi BFS → Dijkstra → rekonstruksi rute → integrasi UI dan statistik → regresi dan dokumentasi.

## M6.1 — Periksa repo, planning, dan skema peta

- Baca semua instruksi M6 yang tersedia, stub `backend/m6_peta.py`, cara kerja UI, dan implementasi heap dari M5.
- Periksa `data/peta.csv`: nama kolom, format ID lokasi, pasangan titik, arah jalan, bobot/jarak/waktu, nilai kosong, dan apakah ruas jalan dua arah atau satu arah.
- Periksa contoh baris nyata dan jumlah lokasi/ruas tanpa mengasumsikan nama kolom tertentu.
- Cari aturan bisnis untuk titik awal/tujuan, zona berdasarkan jumlah hop, arti bobot rute, dan perilaku jika lokasi tidak dikenal.
- **Selesai bila:** skema graf dan aturan rute berasal dari data/planning yang nyata. Jika tidak ada skema atau aturan tertentu, catat asumsi yang paling kecil dan jangan mengarang kolom CSV.

**Catatan progres:** skema CSV: … · arah ruas: … · arti bobot: … · asumsi: …

## M6.2 — Tetapkan kontrak API dan hasil navigasi

- Cocokkan menu M6 yang disebut README: peta/zona dan navigasi rute. README memberi contoh `Peta.zona(a, hops)` serta `Peta.rute(a, b)`; sesuaikan hanya bila kontrak repo menyatakan lain.
- Definisikan keluaran `zona(a, hops)`: lokasi yang terjangkau sampai jumlah hop yang diminta, termasuk atau tidak termasuk titik awal sesuai kontrak yang dicatat.
- Definisikan keluaran `rute(a, b)`: urutan lokasi, total bobot, dan status ditemukan/tidak ditemukan; pertahankan informasi sisi/jarak jika UI membutuhkannya.
- Putuskan perlakuan lokasi tak dikenal, `hops < 0`, sumber sama dengan tujuan, graf kosong, serta tujuan tak terjangkau.
- Tetapkan arti bobot yang dipakai Dijkstra dan syarat semua bobot tidak negatif. Bila bobot negatif ditemukan, hentikan pemakaian Dijkstra pada data itu dan laporkan konflik terhadap spesifikasi.
- **Selesai bila:** bentuk input/output dan kasus batas tertulis sebelum algoritma diimplementasikan.

**Catatan progres:** kontrak zona: … · kontrak rute: … · kasus batas: …

## M6.3 — Rancang representasi graf tanpa struktur terlarang

- Gunakan graf adjacency list buatan sendiri berbasis list/larik primitif; tetapkan cara menyimpan ID lokasi dan tetangga tanpa dictionary atau set.
- Pilih representasi yang sesuai dengan ukuran data dan pola repo: misalnya larik lokasi dengan pencarian indeks, lalu setiap lokasi memiliki list sisi. Jangan memilih representasi yang mengasumsikan ID numerik rapat sebelum memeriksa CSV.
- Tentukan struktur sisi: indeks/ID tujuan dan bobot numerik; pertahankan label nama lokasi bila disediakan.
- Tentukan bagaimana duplikat ruas, ruas dua arah, self-loop, dan ID tidak valid diperlakukan. Ikuti data/planning; jangan diam-diam menggandakan ruas.
- **Selesai bila:** rancangan dapat memetakan setiap ID nyata ke tetangga dan bobotnya tanpa operasi terlarang.

**Catatan progres:** representasi: … · pencarian lokasi: … · kebijakan ruas: …

## M6.4 — Bangun graf dari data peta

- Implementasikan pemuatan dan validasi `peta.csv` sesuai parser/konvensi yang telah ada.
- Buat lokasi dan sisi dalam representasi graf; untuk jalan dua arah, tambahkan kedua arah hanya bila data atau spesifikasi menyatakan begitu.
- Validasi kolom wajib, angka bobot, endpoint yang merujuk ke lokasi valid, baris kosong, dan duplikat ruas. Berikan pesan yang menunjuk baris/field bermasalah bila format tidak sah.
- Sediakan fungsi internal untuk mengambil tetangga sebuah titik dan mencari lokasi; jangan duplikasi logika pencarian ID di BFS dan Dijkstra.
- **Selesai bila:** jumlah lokasi dan sisi yang dimuat sesuai data, dan sampel adjacency list cocok dengan baris CSV yang diperiksa.

**Catatan progres:** lokasi dimuat: … · sisi: … · baris tidak valid: … · hasil sampel: …

## M6.5 — Implementasikan BFS untuk zona/hop

- Implementasikan antrean buatan sendiri atau gunakan struktur antrean buatan proyek bila dapat dipakai tanpa mengubah kontrak dan bebas dari dependensi terlarang.
- Jalankan BFS dari titik awal, simpan jarak dalam jumlah hop/level, dan tandai lokasi yang sudah dikunjungi tanpa set/dictionary. Gunakan larik penanda atau struktur buatan sendiri yang sesuai.
- Batasi penjelajahan hingga `hops`; jangan memasukkan lokasi di level yang lebih jauh. Hindari mengunjungi ulang node pada graf bersiklus.
- Kembalikan hasil sesuai kontrak M6.2 dengan urutan deterministik bila UI membutuhkan hasil yang konsisten.
- **Selesai bila:** BFS menangani titik awal, hops nol, cabang, siklus, lokasi terisolasi, dan titik tak dikenal dengan benar.

**Catatan progres:** antrean/penanda: … · urutan hasil: … · kasus BFS: …

## M6.6 — Verifikasi BFS dan jelaskan biayanya

- Uji graf buatan kecil yang jawabannya dapat dihitung manual: garis, cabang, siklus, komponen terpisah, dan titik tunggal.
- Bandingkan keluaran tiap nilai hop dengan hasil manual; pastikan node pada hop k tidak tercampur dengan hop k+1.
- Uji `hops = 0`, `hops < 0`, titik tidak ada, dan peta kosong sesuai kontrak.
- Catat jumlah node/sisi yang dikunjungi atau waktu bila pola statistik UI mendukungnya. Kompleksitas BFS adalah O(V + E) dengan adjacency list.
- **Selesai bila:** seluruh keluaran cocok dan tidak ada pengulangan tak berujung pada siklus.

**Catatan progres:** contoh graf: … · hasil pemeriksaan: … · metrik: …

## M6.7 — Implementasikan Dijkstra untuk rute berbobot

- Implementasikan Dijkstra hanya setelah validasi memastikan bobot sisi tidak negatif.
- Gunakan MinHeap buatan sendiri dari M5 bila API dan aturan kuncinya bisa mendukung jarak sementara dengan benar. Jika tidak, implementasikan struktur prioritas khusus di modul M6 dan jelaskan alasannya; jangan memakai `heapq`.
- Simpan jarak terbaik, predecessor, dan status yang diperlukan pada larik/struktur buatan sendiri. Hindari dictionary/set.
- Tangani entri heap lama dengan membandingkan jarak yang keluar terhadap jarak terbaik terkini, atau gunakan strategi decrease-key buatan sendiri yang benar.
- Berhenti saat tujuan diproses dengan jarak minimum yang valid. Untuk graf tak terhubung, kembalikan status tidak ada rute.
- **Selesai bila:** jarak minimum benar pada graf kecil berbobot, termasuk ketika rute dengan hop lebih banyak memiliki bobot total lebih rendah.

**Catatan progres:** heap yang dipakai: … · strategi jarak: … · bobot nonnegatif diverifikasi: …

## M6.8 — Rekonstruksi dan validasi rute

- Rekonstruksi rute dari tujuan ke sumber menggunakan predecessor, lalu balik urutannya dengan operasi larik buatan sendiri; jangan memakai fungsi reverse instan bila larangan proyek mencakupnya.
- Pastikan setiap pasangan lokasi berurutan benar-benar terhubung oleh sisi yang ada.
- Hitung/ambil total bobot rute dan cocokkan dengan jarak final Dijkstra. Jika ada beberapa rute dengan bobot sama, hasil harus deterministik sesuai aturan yang terdokumentasi.
- Tangani sumber sama dengan tujuan sebagai rute nol bobot, lokasi tidak dikenal, dan tujuan tak terjangkau.
- **Selesai bila:** jalur yang ditampilkan valid dan total bobotnya sama dengan hasil algoritma.

**Catatan progres:** rute uji: … · total bobot: … · kasus tak terjangkau: …

## M6.9 — Hubungkan peta ke UI dan statistik

- Sambungkan menu zona dan pencarian rute ke API `Peta` dengan input sesuai kolom lokasi yang ada.
- Tampilkan jalur berurutan, total jarak/waktu/bobot dengan satuan yang benar, atau daftar zona beserta hop jika datanya mendukung.
- Tangani titik awal/tujuan kosong atau tidak dikenal, input hop tidak valid, dan tidak ada rute dengan pesan yang jelas.
- Ikuti gaya pencatatan COMMAND: nama fitur/modul M6, waktu eksekusi, hasil ringkas, dan statistik node/sisi yang diperiksa jika tersedia.
- Pastikan pemuatan peta dilakukan dengan efisien dan tidak membangun ulang graf pada setiap klik kecuali memang dibutuhkan.
- **Selesai bila:** kedua menu bisa dijalankan dari UI dan hasilnya dapat ditelusuri kembali ke data peta.

**Catatan progres:** menu terhubung: … · format bobot/satuan: … · statistik: …

## M6.10 — Regresi, dokumentasi, dan penutupan M6

- Jalankan aplikasi pada data peta proyek dan periksa beberapa pasangan lokasi yang hasilnya dapat divalidasi.
- Pastikan BFS zona, Dijkstra, rekonstruksi rute, kondisi gagal, dan statistik tampil benar.
- Jalankan regresi M1–M5 untuk memastikan integrasi M6 tidak mengubah fitur lama. Jika repo tidak memiliki pemeriksaan otomatis, lakukan pemeriksaan manual yang setara dan catat keterbatasannya.
- Perbarui README/catatan demo dengan skema peta, representasi graf, contoh zona/rute, arti bobot dan satuannya, kompleksitas, asumsi, serta cara menjalankan menu.
- Periksa `git diff`, pastikan file data tidak ikut berubah, lalu commit sesuai pola repo. Buat tag/progress submission hanya bila planning proyek memerintahkannya.
- **M6 selesai bila:** bukti pemeriksaan dicatat, semua asumsi terselesaikan atau dinyatakan terbuka secara eksplisit, dan checklist M6 lengkap.

**Catatan progres:** file berubah: … · pemeriksaan: … · commit/tag (jika diwajibkan): …

### Checklist M6

- [ ] Planning dan skema nyata `peta.csv` diperiksa.
- [ ] Graf terbentuk dengan arah sisi dan bobot yang benar.
- [ ] BFS zona benar untuk hop, siklus, dan lokasi tidak dikenal.
- [ ] Dijkstra hanya berjalan pada bobot nonnegatif dan menghasilkan jarak minimum.
- [ ] Rekonstruksi jalur valid dan total bobot cocok.
- [ ] UI menangani input salah dan rute yang tidak tersedia.
- [ ] M1–M5 tetap berfungsi.
- [ ] README dan bukti demo diperbarui.
- [ ] Catatan progres M6 lengkap.

---

## Ringkasan status

| Milestone | Status | Langkah terakhir | Hambatan/asumsi |
|---|---|---:|---|
| M5 — BST + MinHeap | Sedang berjalan | 2/10 | M5.2 selesai |
| M6 — Graf + BFS + Dijkstra | Menunggu M5 selesai | 0/10 | … |

