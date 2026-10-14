# 2EZ4U APP

Engine backend layanan antar makanan untuk proyek Struktur Data dan Analisa Algoritma. Proyek ini mengimplementasikan struktur data secara mandiri tanpa menggunakan struktur bawaan tingkat tinggi (seperti dict, set, heapq, collections, atau fungsi sort bawaan).

## Fitur Utama

### Milestone 1 (M1)
- Data pesanan disimpan bersamaan dalam Array dinamis dan Singly Linked List untuk melayani operasi yang sama.
- Lihat pesanan ke-i (indeks dimulai dari 0).
- Tambah pesanan REGULER (prioritas 3) ke posisi belakang antrean.
- Tambah pesanan PRIORITAS (prioritas 2) ke posisi tengah antrean.
- Tambah pesanan VIP (prioritas 1) ke posisi paling depan antrean.
- Hapus pesanan ke-i dari kedua struktur data.
- Memuat 200.000 baris data/pesanan.csv.
- Antarmuka GUI Tkinter menampilkan antrean, detail ringkas, command log, ukuran, kapasitas Array, dan waktu eksekusi operasi.

### Milestone 2 (M2)
- Struktur data Tumpukan (Stack) dengan alokasi array primitif tetap dan mekanisme penggandaan kapasitas (doubling).
- Operasi dasar LIFO: push, pop, peek, kosong, dan pengecekan ukuran.
- Penanganan underflow pada operasi pop dan peek ketika tumpukan kosong.
- Mesin kasir nota: pemecah token multi-digit, konversi ekspresi infix ke postfix berbasis stack operator, serta evaluasi postfix berbasis stack operand.
- Antrean pesanan dapur: AntreanNaif (pergeseran elemen O(n)) dan AntreanMelingkar (circular array O(1)).
- Sistem pengelola riwayat tindakan Undo dan Redo berbasis dua tumpukan.

### Milestone 3 (M3)
- Pengurutan data pesanan stabil berbasis kunci (harga, prioritas, t_masuk, oid, pelanggan, resto, menu):
  - Insertion Sort: in-place, stabil, O(n^2), dengan penolakan data lebih dari 20.000 baris.
  - Merge Sort: stabil, rekursif pembagian dua, alokasi buffer tunggal, O(n log n) untuk data penuh 200.000 baris.
- Pencarian data pesanan:
  - Linear Search: O(n) pada data acak tanpa syarat terurut.
  - Binary Search: O(log n) leftmost match pada data terurut berdasarkan kunci, disertai pelaporan ongkos pengurutan indeks awal.
- Antarmuka visual M3 Tkinter untuk komparasi jumlah perbandingan operasi dan waktu eksekusi secara empiris.

## Struktur Direktori

```text
2ez4u/
├── app.py
├── run.py
├── check.py
├── check_m2.py
├── check_m3.py
├── README.md
├── data/
│   ├── pesanan.csv
│   └── peta.csv
├── backend/
│   ├── __init__.py
│   ├── m1_pesanan.py
│   ├── m2_antrean.py
│   └── m3_urut_cari.py
└── frontend/
    ├── __init__.py
    └── m3_view.py
```

## Karakteristik dan Kompleksitas Struktur Data

Array dinamis menyimpan referensi dalam list primitif dan menggandakan kapasitasnya saat penuh. Singly Linked List memiliki penunjuk head, tail, serta simpul dengan penunjuk berikutnya.

### Kompleksitas Waktu Milestone 1:

- Lihat indeks ke-i:
  Array: O(1)
  Linked List: O(n)
- Tambah Reguler:
  Array: O(1) amortized
  Linked List: O(1)
- Tambah Prioritas:
  Array: O(n)
  Linked List: O(n) penelusuran
- Tambah VIP:
  Array: O(n) pergeseran
  Linked List: O(1)
- Hapus indeks ke-i:
  Array: O(n)
  Linked List: O(n) penelusuran

### Kompleksitas Waktu Milestone 2:

- Tumpukan (Stack):
  - Operasi push: O(1) amortized
  - Operasi pop: O(1)
  - Operasi peek: O(1)
  - Pengecekan kosong: O(1)
- Antrean Naif:
  - Enqueue: O(1) amortized
  - Dequeue: O(n) pergeseran elemen
- Antrean Melingkar:
  - Enqueue: O(1) amortized
  - Dequeue: O(1) tanpa pergeseran elemen
- Undo dan Redo: O(1) per operasi tumpukan

### Kompleksitas Waktu Milestone 3:

- Insertion Sort: O(n^2) waktu terburuk dan rata-rata, O(n) waktu terbaik, memori O(1)
- Merge Sort: O(n log n) pada seluruh kasus, memori tambahan O(n) buffer tunggal
- Linear Search: O(n) pencarian sekuensial
- Binary Search: O(log n) pencarian biner pada data terurut

## Menjalankan Aplikasi

Gunakan Python 3.11 atau lebih baru dari direktori proyek:

```bash
python run.py
```

Di macOS, gunakan `python3 run.py`. Python bawaan Apple dengan Tk 8.5 tidak kompatibel dan dapat menampilkan jendela kosong. Gunakan Python 3.11 atau lebih baru yang sudah menyertakan Tk modern. Launcher otomatis mendeteksi instalasi Python yang kompatibel dari sistem, Homebrew, atau virtual environment (.venv).

Alternatif menjalankan GUI secara langsung:

```bash
python app.py
```

Pemeriksaan backend dan pengujian unit tanpa GUI:

- Menjalankan uji Milestone 1:
```bash
python check.py
```

- Menjalankan uji Milestone 2 (Stack, Kasir, Queue, Undo/Redo):
```bash
python check_m2.py
```

- Menjalankan uji Milestone 3 (Sort & Search):
```bash
python check_m3.py
```

## Penggunaan Form GUI

Masukkan indeks pada form untuk melihat atau menghapus pesanan. Untuk menambah pesanan, isi ID, pelanggan, restoran, menu, harga, lalu pilih tingkat prioritas. Jika kolom teks kosong, aplikasi akan memakai nilai contoh bawaan. Untuk modul pengurutan dan pencarian M3, klik tombol M3 · SORT & SEARCH pada panel samping.
