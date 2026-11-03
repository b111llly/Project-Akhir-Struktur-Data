import threading
import tkinter as tk
from tkinter import messagebox, ttk

from backend.m4_pencarian import MesinM4


class JendelaM4:
    def __init__(self, root, path_data):
        self.win = tk.Toplevel(root)
        self.win.title("2EZ4U APP · M4 Peta Hash & Search")
        self.win.geometry("1120x700")
        self.win.configure(bg="#ffffff")
        self.mesin = MesinM4()
        self.path_data = path_data
        self.siap = False
        self._hasil = None
        self._buat_ui()
        threading.Thread(target=self._muat, daemon=True).start()
        self.win.after(50, self._cek_muat)

    def _buat_ui(self):
        utama = ttk.Frame(self.win, padding=18)
        utama.pack(fill="both", expand=True)
        ttk.Label(utama, text="M4 · Peta Hash O(1) vs Binary Search O(log n) vs Linear Search O(n)", style="Title.TLabel").pack(anchor="w", pady=(0, 12))

        form = ttk.Frame(utama)
        form.pack(fill="x")
        ttk.Label(form, text="Kunci Cari").grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.mode_cari = ttk.Combobox(form, values=("OID", "RESTO", "PELANGGAN", "MENU"), state="readonly", width=12)
        self.mode_cari.current(0)
        self.mode_cari.grid(row=0, column=1, sticky="w", padx=(0, 16))
        self.mode_cari.bind("<<ComboboxSelected>>", self._ganti_mode)

        ttk.Label(form, text="Target").grid(row=0, column=2, sticky="w", padx=(0, 6))
        self.target = ttk.Entry(form, width=26)
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

        self.info = tk.StringVar(value="Memuat data dan membangun PetaHash mandiri...")
        ttk.Label(utama, textvariable=self.info, style="Status.TLabel").pack(anchor="w", pady=(0, 6))

        frame = ttk.Frame(utama)
        frame.pack(fill="both", expand=True)
        kolom = ("indeks", "oid", "pelanggan", "menu", "resto", "harga", "prioritas", "t_masuk", "status")
        judul = ("i", "OID", "Pelanggan", "Menu", "Resto", "Harga", "Prio", "t_masuk", "Status")
        lebar = (50, 95, 170, 130, 130, 80, 50, 75, 75)
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

    def _ganti_mode(self, event=None):
        mode = self.mode_cari.get()
        self.target.delete(0, "end")
        if mode == "OID":
            self.target.insert(0, "O-150000")
        elif mode == "RESTO":
            self.target.insert(0, "kafe-teknik")
        elif mode == "PELANGGAN":
            self.target.insert(0, "Rahmi Simanjuntak")
        elif mode == "MENU":
            self.target.insert(0, "roti-bakar")

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
        uk, kap, terisi, maks_r, rata_r, beban = self.mesin.peta_oid.stats()
        self.info.set("%d pesanan siap · PetaHash kapasitas %d · maks rantai %d" % (jumlah, kap, maks_r))
        self._tampil(self.mesin.data, 0, 15)

    def _cari_hash(self):
        mode = self.mode_cari.get()
        target = self.target.get().strip()
        if target == "":
            messagebox.showwarning("Target Kosong", "Masukkan target pencarian.", parent=self.win)
            return
        hasil, stat = self.mesin.cari_hash(mode, target)
        n = len(hasil)
        if n == 0:
            self._tulis("PETA HASH O(1) | %s '%s' tidak ditemukan | %d perbandingan | %.4f ms" % (mode, target, stat.perbandingan, stat.waktu_ms))
            self._tampil(hasil, 0, 0)
            return
        self._tulis("PETA HASH O(1) | %s '%s': %d ditemukan | %d perbandingan | %.4f ms" % (mode, target, n, stat.perbandingan, stat.waktu_ms))
        self._tampil(hasil, 0, 20)

    def _cari_binary(self):
        mode = self.mode_cari.get()
        target = self.target.get().strip()
        if target == "":
            messagebox.showwarning("Target Kosong", "Masukkan target pencarian.", parent=self.win)
            return
        _, _, apakah_baru = self.mesin.dapatkan_data_terurut(mode)
        hasil, stat_search, stat_sort = self.mesin.cari_binary(mode, target)
        if apakah_baru:
            self._tulis("MERGE SORT INDEKS %s dibangun | %d perbandingan | %.3f ms" % (mode, stat_sort.perbandingan, stat_sort.waktu_ms))
        n = len(hasil)
        if n == 0:
            self._tulis("BINARY SEARCH O(log n) | %s '%s' tidak ditemukan | %d perbandingan | %.4f ms" % (mode, target, stat_search.perbandingan, stat_search.waktu_ms))
            self._tampil(hasil, 0, 0)
            return
        self._tulis("BINARY SEARCH O(log n) | %s '%s': %d ditemukan | %d perbandingan | %.4f ms" % (mode, target, n, stat_search.perbandingan, stat_search.waktu_ms))
        self._tampil(hasil, 0, 20)

    def _cari_linear(self):
        mode = self.mode_cari.get()
        target = self.target.get().strip()
        if target == "":
            messagebox.showwarning("Target Kosong", "Masukkan target pencarian.", parent=self.win)
            return
        hasil, stat = self.mesin.cari_linear(mode, target)
        n = len(hasil)
        if n == 0:
            self._tulis("LINEAR SEARCH O(n) | %s '%s' tidak ditemukan | %d perbandingan | %.4f ms" % (mode, target, stat.perbandingan, stat.waktu_ms))
            self._tampil(hasil, 0, 0)
            return
        self._tulis("LINEAR SEARCH O(n) | %s '%s': %d ditemukan | %d perbandingan | %.4f ms" % (mode, target, n, stat.perbandingan, stat.waktu_ms))
        self._tampil(hasil, 0, 20)

    def _bandingkan_tiga(self):
        mode = self.mode_cari.get()
        target = self.target.get().strip()
        if target == "":
            messagebox.showwarning("Target Kosong", "Masukkan target pencarian.", parent=self.win)
            return
        _, s_hash = self.mesin.cari_hash(mode, target)
        _, s_bin, _ = self.mesin.cari_binary(mode, target)
        _, s_lin = self.mesin.cari_linear(mode, target)
        self._tulis("PERBANDINGAN %s '%s': Hash %d cmp (%.4f ms) vs Binary %d cmp (%.4f ms) vs Linear %d cmp (%.4f ms)" % (
            mode, target, s_hash.perbandingan, s_hash.waktu_ms, s_bin.perbandingan, s_bin.waktu_ms, s_lin.perbandingan, s_lin.waktu_ms
        ))

    def _tampil_stats(self):
        peta_daftar = (
            ("OID", self.mesin.peta_oid),
            ("RESTO", self.mesin.peta_resto),
            ("PELANGGAN", self.mesin.peta_pelanggan),
            ("MENU", self.mesin.peta_menu),
        )
        i = 0
        while i < len(peta_daftar):
            nama, peta = peta_daftar[i]
            uk, kap, terisi, maks_r, rata_r, beban = peta.stats()
            pct_terisi = (terisi / kap * 100.0) if kap > 0 else 0.0
            self._tulis("STATISTIK PETA HASH %s: %d kunci | %d ember | %d terisi (%.1f%%) | maks rantai %d | rata rantai %.2f | load factor %.2f" % (
                nama, uk, kap, terisi, pct_terisi, maks_r, rata_r, beban
            ))
            i += 1

    def _tampil(self, data, mulai, jumlah):
        for item in self.tabel.get_children():
            self.tabel.delete(item)
        i = mulai
        n = len(data)
        while i < n and i < mulai + jumlah:
            p = data[i]
            self.tabel.insert("", "end", values=(i, p.oid, p.pelanggan, p.menu, p.resto, "Rp%d" % p.harga, "P%d" % p.prioritas, p.t_masuk, p.status))
            i += 1

    def _tulis(self, teks):
        self.log.configure(state="normal")
        self.log.insert("end", teks + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")
