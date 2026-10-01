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

## Struktur Direktori

```text
2ez4u/
├── app.py
├── run.py
├── check.py
├── check_m2.py
├── README.md
├── data/
│   ├── pesanan.csv
│   └── peta.csv
├── backend/
│   ├── __init__.py
│   ├── m1_pesanan.py
│   └── m2_antrean.py
└── frontend/
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

### Kompleksitas Waktu Tumpukan (Stack) Milestone 2:

- Operasi push: O(1) amortized
- Operasi pop: O(1)
- Operasi peek: O(1)
- Pengecekan kosong (is_empty): O(1)

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

- Menjalankan uji Milestone 2 (Stack):
```bash
python check_m2.py
```

## Penggunaan Form GUI

Masukkan indeks pada form untuk melihat atau menghapus pesanan. Untuk menambah pesanan, isi ID, pelanggan, restoran, menu, harga, lalu pilih tingkat prioritas. Jika kolom teks kosong, aplikasi akan memakai nilai contoh bawaan.
