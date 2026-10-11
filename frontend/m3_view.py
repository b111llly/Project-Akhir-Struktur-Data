import threading
import tkinter as tk
from tkinter import messagebox, ttk

from backend.m3_urut_cari import BATAS_INSERTION, MesinM3, nama_kunci


class JendelaM3:
    def __init__(self, root, path_data):
        self.win = tk.Toplevel(root)
        self.win.title("2EZ4U APP · M3 Sort & Search")
        self.win.geometry("1100x680")
        self.win.configure(bg="#ffffff")
        self.mesin = MesinM3()
        self.path_data = path_data
        self.siap = False
        self._hasil = None
        self._buat_ui()
        threading.Thread(target=self._muat, daemon=True).start()
        self.win.after(50, self._cek_muat)

    def _buat_ui(self):
        utama = ttk.Frame(self.win, padding=18)
        utama.pack(fill="both", expand=True)
        ttk.Label(utama, text="M3 · Pengurutan dan Pencarian", style="Title.TLabel").pack(anchor="w", pady=(0, 12))

        form = ttk.Frame(utama)
        form.pack(fill="x")
        ttk.Label(form, text="Kunci").grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.kunci = ttk.Combobox(form, values=nama_kunci(), state="readonly", width=12)
        self.kunci.current(0)
        self.kunci.grid(row=0, column=1, sticky="w", padx=(0, 16))
        ttk.Label(form, text="Jumlah data").grid(row=0, column=2, sticky="w", padx=(0, 6))
        self.jumlah = ttk.Entry(form, width=10)
        self.jumlah.insert(0, "5000")
        self.jumlah.grid(row=0, column=3, sticky="w", padx=(0, 16))
        ttk.Label(form, text="Target cari").grid(row=0, column=4, sticky="w", padx=(0, 6))
        self.target = ttk.Entry(form, width=16)
        self.target.insert(0, "12000")
        self.target.grid(row=0, column=5, sticky="w")

        tombol = ttk.Frame(utama)
        tombol.pack(fill="x", pady=10)
        self.tombol = (
            ttk.Button(tombol, text="INSERTION SORT", style="Action.TButton", command=lambda: self._urut("insertion")),
            ttk.Button(tombol, text="MERGE SORT", style="Action.TButton", command=lambda: self._urut("merge")),
            ttk.Button(tombol, text="BANDINGKAN SORT", style="Action.TButton", command=self._banding_sort),
            ttk.Button(tombol, text="LINEAR SEARCH", style="Action.TButton", command=self._linear),
            ttk.Button(tombol, text="BINARY SEARCH", style="Action.TButton", command=self._binary),
        )
        for b in self.tombol:
            b.pack(side="left", padx=(0, 6))
            b.state(["disabled"])

        self.info = tk.StringVar(value="Memuat data...")
        ttk.Label(utama, textvariable=self.info, style="Status.TLabel").pack(anchor="w", pady=(0, 6))

        frame = ttk.Frame(utama)
        frame.pack(fill="both", expand=True)
        kolom = ("indeks", "oid", "pelanggan", "menu", "resto", "harga", "prioritas", "t_masuk")
        judul = ("i", "OID", "Pelanggan", "Menu", "Resto", "Harga", "Prio", "t_masuk")
        lebar = (55, 95, 160, 130, 130, 80, 50, 80)
        self.tabel = ttk.Treeview(frame, columns=kolom, show="headings", height=12)
        i = 0
        while i < len(kolom):
            self.tabel.heading(kolom[i], text=judul[i])
            self.tabel.column(kolom[i], width=lebar[i], anchor="w")
            i += 1
        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.tabel.yview)
        self.tabel.configure(yscrollcommand=scroll.set)
        self.tabel.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        ttk.Label(utama, text="COMMAND LOG", style="Section.TLabel").pack(anchor="w", pady=(10, 4))
        self.log = tk.Text(utama, height=8, state="disabled", bg="#f8fafc", fg="#0f172a", relief="solid", bd=1, wrap="word", padx=8, pady=6)
        self.log.pack(fill="x")

    def _muat(self):
        try:
            self._hasil = (self.mesin.muat_csv(self.path_data), None)
        except Exception as error:
            self._hasil = (0, error)

    def _cek_muat(self):
        if self._hasil is None:
            self.win.after(50, self._cek_muat)
            return
        jumlah, error = self._hasil
        if error is not None:
            self.info.set("Gagal memuat data")
            messagebox.showerror("Gagal memuat data", str(error), parent=self.win)
            return
        self.siap = True
        for b in self.tombol:
            b.state(["!disabled"])
        self.info.set("%d pesanan siap · batas Insertion Sort %d data" % (jumlah, BATAS_INSERTION))
        self._tampil(self.mesin.data, 0, 15)

    def _n(self):
        teks = self.jumlah.get().strip()
        if teks == "":
            return self.mesin.ukuran
        try:
            n = int(teks)
        except ValueError:
            raise ValueError("Jumlah data harus bilangan bulat")
        if n < 1:
            raise ValueError("Jumlah data minimal 1")
        if n > self.mesin.ukuran:
            n = self.mesin.ukuran
        return n

    def _urut(self, algoritma):
        try:
            n = self._n()
            kunci = self.kunci.get()
            data, stat = self.mesin.urutkan(algoritma, kunci, n)
        except ValueError as error:
            messagebox.showwarning("Ditolak", str(error), parent=self.win)
            self._tulis("%s DITOLAK | %s" % (algoritma.upper(), error))
            return
        nama = "INSERTION SORT O(n^2)" if algoritma == "insertion" else "MERGE SORT O(n log n)"
        self._tulis("%s | kunci=%s n=%d | %d perbandingan, %d pergeseran | %.3f ms" % (nama, kunci, n, stat.perbandingan, stat.pergeseran, stat.waktu_ms))
        self.info.set("%s selesai: %d data terurut stabil berdasarkan %s" % (nama, n, kunci))
        self._tampil(data, 0, 15)

    def _banding_sort(self):
        try:
            n = self._n()
        except ValueError as error:
            messagebox.showwarning("Parameter", str(error), parent=self.win)
            return
        if n > BATAS_INSERTION:
            n = BATAS_INSERTION
        kunci = self.kunci.get()
        _, si = self.mesin.urutkan("insertion", kunci, n)
        _, sm = self.mesin.urutkan("merge", kunci, n)
        self._tulis("BANDINGKAN n=%d kunci=%s | Insertion %d cmp %.3f ms | Merge %d cmp %.3f ms" % (n, kunci, si.perbandingan, si.waktu_ms, sm.perbandingan, sm.waktu_ms))

    def _linear(self):
        kunci = self.kunci.get()
        try:
            indeks, stat = self.mesin.cari_linear(kunci, self.target.get().strip())
        except ValueError as error:
            messagebox.showwarning("Parameter", str(error), parent=self.win)
            return
        if indeks < 0:
            self._tulis("LINEAR O(n) | %s=%s tidak ditemukan | %d perbandingan | %.3f ms" % (kunci, self.target.get(), stat.perbandingan, stat.waktu_ms))
            return
        self._tulis("LINEAR O(n) | %s ditemukan di indeks asli %d | %d perbandingan | %.3f ms" % (self.mesin.data[indeks].oid, indeks, stat.perbandingan, stat.waktu_ms))
        self._tampil(self.mesin.data, max(0, indeks - 2), 15)

    def _binary(self):
        kunci = self.kunci.get()
        try:
            indeks, stat, ongkos = self.mesin.cari_binary(kunci, self.target.get().strip())
        except ValueError as error:
            messagebox.showwarning("Parameter", str(error), parent=self.win)
            return
        if ongkos is not None:
            self._tulis("INDEKS TERURUT dibangun (Merge Sort, kunci=%s) | %d perbandingan | %.3f ms" % (kunci, ongkos.perbandingan, ongkos.waktu_ms))
        if indeks < 0:
            self._tulis("BINARY O(log n) | %s=%s tidak ditemukan | %d perbandingan | %.3f ms" % (kunci, self.target.get(), stat.perbandingan, stat.waktu_ms))
            return
        self._tulis("BINARY O(log n) | %s ditemukan di indeks terurut %d | %d perbandingan | %.3f ms" % (self.mesin.hasil_binary(indeks).oid, indeks, stat.perbandingan, stat.waktu_ms))
        self._tampil(self.mesin.terurut, indeks, 15)

    def _tampil(self, data, mulai, jumlah):
        for item in self.tabel.get_children():
            self.tabel.delete(item)
        i = mulai
        while i < len(data) and i < mulai + jumlah:
            p = data[i]
            self.tabel.insert("", "end", values=(i, p.oid, p.pelanggan, p.menu, p.resto, "Rp%d" % p.harga, "P%d" % p.prioritas, p.t_masuk))
            i += 1

    def _tulis(self, teks):
        self.log.configure(state="normal")
        self.log.insert("end", teks + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")
