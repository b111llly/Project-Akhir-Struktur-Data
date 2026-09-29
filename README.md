# 2EZ4U APP — Milestone 1

Engine backend layanan antar makanan mini untuk proyek Struktur Data & Analisa Algoritma. Versi ini mengerjakan M1 saja: data pesanan disimpan bersamaan dalam Array dinamis dan Singly Linked List, lalu keduanya melayani operasi yang sama.

## Fitur M1

- Lihat pesanan ke-i (indeks dimulai dari 0).
- Tambah pesanan REGULER (prioritas 3) ke belakang.
- Tambah pesanan PRIORITAS (prioritas 2) ke tengah antrean.
- Tambah pesanan VIP (prioritas 1) ke paling depan.
- Hapus pesanan ke-i dari kedua struktur.
- Memuat 200.000 baris `data/pesanan.csv`.
- UI Tkinter menampilkan antrean, detail ringkas, command log, ukuran, kapasitas Array, dan waktu operasi.

## Struktur

```text
2ez4u/
├── app.py
├── check.py
├── data/
│   ├── pesanan.csv
│   └── peta.csv
├── backend/
│   └── m1_pesanan.py
└── frontend/
```

Array menyimpan referensi dalam `list` primitif dan menggandakan kapasitas saat penuh. Linked List memiliki `head`, `tail`, dan simpul dengan pointer `berikutnya`. Tidak digunakan `dict`, `set`, `sorted`, `.sort()`, `heapq`, atau `collections` pada implementasi struktur data.

## Kompleksitas

| Operasi | Array | Linked List |
|---|---:|---:|
| Lihat indeks ke-i | O(1) | O(n) |
| Tambah Reguler | O(1) amortized | O(1) |
| Tambah Prioritas | O(n) | O(n) telusur |
| Tambah VIP | O(n) geser | O(1) |
| Hapus indeks ke-i | O(n) | O(n) telusur |

## Menjalankan

Gunakan Python 3.11 atau lebih baru dari folder proyek:

```bash
python run.py
```

Launcher utama yang direkomendasikan adalah `run.py`; file tersebut otomatis
mencari folder proyek dan membuka aplikasi. Alternatif langsung:

```bash
python app.py
```

Untuk pemeriksaan backend tanpa GUI:

```bash
python check.py
```

Masukkan indeks pada form untuk melihat atau menghapus. Untuk menambah, isi ID, pelanggan, resto, menu, harga, lalu pilih prioritas. Jika kolom teks kosong, aplikasi memakai nilai contoh; harga kosong menjadi 0.
