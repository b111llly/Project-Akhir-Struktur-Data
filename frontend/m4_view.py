import threading
import tkinter as tk
from tkinter import messagebox, ttk

from backend.m3_urut_cari import binary_search, linear_search
from backend.m4_pencarian import MesinM4


class JendelaM4:
    def __init__(self, root, path_data):
        self.win = tk.Toplevel(root)
        self.win.title("2EZ4U APP · M4 Peta Hash & Search")
        self.win.geometry("1100x680")
        self.win.configure(bg="#ffffff")
        self.mesin = MesinM4()
        self.path_data = path_data
        self.siap = False
        self._hasil = None
        self._data_terurut_oid = None
        self._buat_ui()
        threading.Thread(target=self._muat, daemon=True).start()
        self.win.after(50, self._cek_muat)

    def _buat_ui(self):
        utama = ttk.Frame(self.win, padding=18)
        utama.pack(fill="both", expand=True)
        ttk.Label(utama, text="M4 · Peta Hash & Pencarian O(1) vs Binary vs Linear", style="Title.TLabel").pack(anchor="w", pady=(0, 12))

        form = ttk.Frame(utama)
        form.pack(fill="x")
        ttk.Label(form, text="Mode Cari").grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.mode_cari = ttk.Combobox(form, values=("OID", "RESTO"), state="readonly", width=10)
        self.mode_cari.current(0)
        self.mode_cari.grid(row=0, column=1, sticky="w", padx=(0, 16))

        ttk.Label(form, text="Target").grid(row=0, column=2, sticky="w", padx=(0, 6))
        self.target = ttk.Entry(form, width=22)
        self.target.insert(0, "O-150000")
        self.target.grid(row=0, column=3, sticky="w", padx=(0, 16))

        tombol = ttk.Frame(utama)
        tombol.pack(fill="x", pady=10)
        self.tombol = (
            ttk.Button(tombol, text="CARI HASH (O(1))", style="Action.TButton", command=self._cari_hash),
            ttk.Button(tombol, text="CARI BINARY (O(log n))", style="Action.TButton", command=self._cari_binary),
            ttk.Button(tombol, text="CARI LINEAR (O(n))", style="Action.TButton", command=self._cari_linear),
            ttk.Button(tombol, text="BANDINGKAN KETIGANYA", style="Action.TButton", command=self._bandingkan_tiga),
            ttk.Button(tombol, text="STATISTIK PETA HASH", style="Action.TButton", command=self._tampil_stats),
        )
        for b in self.tombol:
            b.pack(side="left", padx=(0, 6))
            b.state(["disabled"])

        self.info = tk.StringVar(value="Memuat data dan membangun PetaHash...")
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
            jumlah = self.mesin.muat_csv(self.path_data)
            self._hasil = (jumlah, None)
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
        uk, kap, terisi, maks_r, beban = self.mesin.peta_oid.stats()
        self.info.set("%d pesanan siap · PetaHash kapasitas %d · maks rantai %d" % (jumlah, kap, maks_r))
        self._tampil(self.mesin.data, 0, 15)

    def _cari_hash(self):
        mode = self.mode_cari.get()
        target = self.target.get().strip()
        if target == "":
            messagebox.showwarning("Target Kosong", "Masukkan target pencarian.", parent=self.win)
            return
        if mode == "OID":
            p, stat = self.mesin.cari_hash_oid(target)
            if p is None:
                self._tulis("PETA HASH O(1) | OID %s tidak ditemukan | %d perbandingan | %.4f ms" % (target, stat.perbandingan, stat.waktu_ms))
                return
            self._tulis("PETA HASH O(1) | OID %s ditemukan | %s - %s - Rp%d | %d perbandingan | %.4f ms" % (p.oid, p.pelanggan, p.menu, p.harga, stat.perbandingan, stat.waktu_ms))
            wadah = [p]
            self._tampil(wadah, 0, 1)
        else:
            daftar, stat = self.mesin.cari_hash_resto(target)
            self._tulis("PETA HASH O(1) | Resto '%s': %d pesanan | %d perbandingan | %.4f ms" % (target, len(daftar), stat.perbandingan, stat.waktu_ms))
            self._tampil(daftar, 0, 15)

    def _cari_binary(self):
        target = self.target.get().strip()
        if target == "":
            messagebox.showwarning("Target Kosong", "Masukkan target pencarian OID.", parent=self.win)
            return
        if self._data_terurut_oid is None:
            data, stat_sort = self.mesin.urutkan_merge(lambda p: p.oid)
            self._data_terurut_oid = data
            self._tulis("MERGE SORT INDEKS OID dibangun | %d perbandingan | %.3f ms" % (stat_sort.perbandingan, stat_sort.waktu_ms))
        idx, stat = binary_search(self._data_terurut_oid, lambda p: p.oid, target)
        if idx < 0:
            self._tulis("BINARY SEARCH O(log n) | OID %s tidak ditemukan | %d perbandingan | %.4f ms" % (target, stat.perbandingan, stat.waktu_ms))
            return
        p = self._data_terurut_oid[idx]
        self._tulis("BINARY SEARCH O(log n) | OID %s ditemukan pada indeks terurut %d | %d perbandingan | %.4f ms" % (p.oid, idx, stat.perbandingan, stat.waktu_ms))
        self._tampil(self._data_terurut_oid, idx, 15)

    def _cari_linear(self):
        target = self.target.get().strip()
        if target == "":
            messagebox.showwarning("Target Kosong", "Masukkan target pencarian OID.", parent=self.win)
            return
        idx, stat = linear_search(self.mesin.data, lambda p: p.oid, target)
        if idx < 0:
            self._tulis("LINEAR SEARCH O(n) | OID %s tidak ditemukan | %d perbandingan | %.4f ms" % (target, stat.perbandingan, stat.waktu_ms))
            return
        p = self.mesin.data[idx]
        self._tulis("LINEAR SEARCH O(n) | OID %s ditemukan pada indeks asal %d | %d perbandingan | %.4f ms" % (p.oid, idx, stat.perbandingan, stat.waktu_ms))
        self._tampil(self.mesin.data, max(0, idx - 2), 15)

    def _bandingkan_tiga(self):
        target = self.target.get().strip()
        if target == "":
            messagebox.showwarning("Target Kosong", "Masukkan target pencarian OID.", parent=self.win)
            return
        _, s_hash = self.mesin.cari_hash_oid(target)
        if self._data_terurut_oid is None:
            data, _ = self.mesin.urutkan_merge(lambda p: p.oid)
            self._data_terurut_oid = data
        _, s_bin = binary_search(self._data_terurut_oid, lambda p: p.oid, target)
        _, s_lin = linear_search(self.mesin.data, lambda p: p.oid, target)
        self._tulis("PERBANDINGAN TARGET OID %s: Hash %d cmp (%.4f ms) vs Binary %d cmp (%.4f ms) vs Linear %d cmp (%.4f ms)" % (target, s_hash.perbandingan, s_hash.waktu_ms, s_bin.perbandingan, s_bin.waktu_ms, s_lin.perbandingan, s_lin.waktu_ms))

    def _tampil_stats(self):
        uk, kap, terisi, maks_r, beban = self.mesin.peta_oid.stats()
        self._tulis("STATISTIK PETA HASH OID: %d data | kapasitas %d ember | ember terisi %d (%.1f%%) | rantai terpanjang %d | load factor %.2f" % (uk, kap, terisi, (terisi / kap) * 100.0, maks_r, beban))

    def _tampil(self, data, mulai, jumlah):
        for item in self.tabel.get_children():
            self.tabel.delete(item)
        i = mulai
        n = len(data)
        while i < n and i < mulai + jumlah:
            p = data[i]
            self.tabel.insert("", "end", values=(i, p.oid, p.pelanggan, p.menu, p.resto, "Rp%d" % p.harga, "P%d" % p.prioritas, p.t_masuk))
            i += 1

    def _tulis(self, teks):
        self.log.configure(state="normal")
        self.log.insert("end", teks + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")
