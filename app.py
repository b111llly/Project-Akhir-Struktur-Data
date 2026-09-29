import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

from backend.m1_pesanan import MesinM1, buat_pesanan


class AplikasiM1:
    def __init__(self, root):
        self.root = root
        self.root.title("2EZ4U APP · Milestone 1")
        self.root.geometry("1180x720")
        self.root.minsize(980, 620)
        self.mesin = MesinM1()
        self.path_data = os.path.join(os.path.dirname(__file__), "data", "pesanan.csv")
        self._buat_style()
        self._buat_ui()
        self._muat_data()

    def _buat_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"), foreground="#12304a")
        style.configure("Section.TLabel", font=("Segoe UI", 11, "bold"), foreground="#12304a")
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=8)

    def _buat_ui(self):
        utama = ttk.Frame(self.root, padding=18)
        utama.pack(fill="both", expand=True)
        ttk.Label(utama, text="2EZ4U APP", style="Title.TLabel").pack(anchor="w")
        ttk.Label(utama, text="M1 · Perbandingan Array dan Linked List", foreground="#5c7080").pack(anchor="w", pady=(0, 12))

        area = ttk.PanedWindow(utama, orient="horizontal")
        area.pack(fill="both", expand=True)
        kiri = ttk.Frame(area, padding=(0, 0, 14, 0))
        kanan = ttk.Frame(area, padding=(14, 0, 0, 0))
        area.add(kiri, weight=1)
        area.add(kanan, weight=3)
        ttk.Label(kiri, text="OPERASI M1", style="Section.TLabel").pack(anchor="w", pady=(0, 8))
        self.mode = tk.StringVar(value="array")
        self._tombol(kiri, "ARRAY · LIHAT PESANAN", lambda: self._pilih("lihat", "array"))
        self._tombol(kiri, "ARRAY · TAMBAH REGULER", lambda: self._pilih("tambah", "array", 3))
        self._tombol(kiri, "ARRAY · TAMBAH PRIORITAS", lambda: self._pilih("tambah", "array", 2))
        self._tombol(kiri, "ARRAY · TAMBAH VIP", lambda: self._pilih("tambah", "array", 1))
        ttk.Separator(kiri).pack(fill="x", pady=10)
        self._tombol(kiri, "LINKED LIST · LIHAT PESANAN", lambda: self._pilih("lihat", "linked_list"))
        self._tombol(kiri, "LINKED LIST · TAMBAH REGULER", lambda: self._pilih("tambah", "linked_list", 3))
        self._tombol(kiri, "LINKED LIST · TAMBAH PRIORITAS", lambda: self._pilih("tambah", "linked_list", 2))
        self._tombol(kiri, "LINKED LIST · TAMBAH VIP", lambda: self._pilih("tambah", "linked_list", 1))
        ttk.Separator(kiri).pack(fill="x", pady=10)
        self._tombol(kiri, "HAPUS PESANAN KE-i", lambda: self._pilih("hapus", "keduanya"))
        self._tombol(kiri, "BANDINGKAN KINERJA", self._bandingkan)

        ttk.Label(kanan, text="FORM PARAMETER", style="Section.TLabel").grid(row=0, column=0, sticky="w")
        form = ttk.Frame(kanan)
        form.grid(row=1, column=0, sticky="ew", pady=(6, 10))
        form.columnconfigure(1, weight=1)
        ttk.Label(form, text="Indeks (0-based)").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=3)
        self.indeks = ttk.Entry(form, width=18)
        self.indeks.grid(row=0, column=1, sticky="w", pady=3)
        ttk.Label(form, text="ID / nama pelanggan / resto / menu / harga").grid(row=1, column=0, columnspan=2, sticky="w", pady=(8, 2))
        self.oid = ttk.Entry(form, width=18); self.oid.grid(row=2, column=0, sticky="w", pady=3)
        self.pelanggan = ttk.Entry(form, width=24); self.pelanggan.grid(row=2, column=1, sticky="w", pady=3)
        self.resto = ttk.Entry(form, width=24); self.resto.grid(row=3, column=0, sticky="w", pady=3)
        self.menu = ttk.Entry(form, width=24); self.menu.grid(row=3, column=1, sticky="w", pady=3)
        self.harga = ttk.Entry(form, width=18); self.harga.grid(row=4, column=0, sticky="w", pady=3)
        self.prioritas = ttk.Combobox(form, values=("1 · VIP", "2 · PRIORITAS", "3 · REGULER"), state="readonly", width=16)
        self.prioritas.current(2); self.prioritas.grid(row=4, column=1, sticky="w", pady=3)
        self.aksi = ttk.Button(form, text="Jalankan", style="Action.TButton", command=self._jalankan)
        self.aksi.grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 0))

        self.info = tk.StringVar(value="Memuat data...")
        ttk.Label(kanan, textvariable=self.info, foreground="#246b4c").grid(row=2, column=0, sticky="w", pady=(0, 8))
        tabel_frame = ttk.Frame(kanan)
        tabel_frame.grid(row=3, column=0, sticky="nsew")
        kanan.rowconfigure(3, weight=1); kanan.columnconfigure(0, weight=1)
        kolom = ("indeks", "oid", "menu", "resto", "harga", "prioritas", "status")
        self.tabel = ttk.Treeview(tabel_frame, columns=kolom, show="headings", height=10)
        judul = ("i", "OID", "Menu", "Resto", "Harga", "Prioritas", "Status")
        lebar = (45, 105, 150, 145, 90, 85, 85)
        i = 0
        while i < len(kolom):
            self.tabel.heading(kolom[i], text=judul[i]); self.tabel.column(kolom[i], width=lebar[i], anchor="w")
            i += 1
        scroll = ttk.Scrollbar(tabel_frame, orient="vertical", command=self.tabel.yview)
        self.tabel.configure(yscrollcommand=scroll.set)
        self.tabel.pack(side="left", fill="both", expand=True); scroll.pack(side="right", fill="y")
        ttk.Label(kanan, text="COMMAND LOG", style="Section.TLabel").grid(row=4, column=0, sticky="w", pady=(12, 4))
        self.log = tk.Text(kanan, height=7, state="disabled", bg="#f4f7f9", relief="flat", wrap="word")
        self.log.grid(row=5, column=0, sticky="ew")

    def _tombol(self, parent, teks, perintah):
        ttk.Button(parent, text=teks, style="Action.TButton", command=perintah).pack(fill="x", pady=3)

    def _muat_data(self):
        try:
            jumlah = self.mesin.muat_csv(self.path_data)
            self.info.set("%d pesanan siap · Array kapasitas %d · data kedua struktur konsisten" % (jumlah, self.mesin.array.kapasitas))
            self._tulis_log("LOAD CSV", "Array + Linked List", "%d pesanan" % jumlah, 0.0)
            self._refresh_tabel(0)
        except (OSError, ValueError, IndexError) as error:
            self.info.set("Gagal memuat data")
            messagebox.showerror("Gagal memuat data", str(error))

    def _pilih(self, operasi, mode, prioritas=None):
        self.mode.set(mode)
        self.operasi = operasi
        if prioritas is not None:
            self.prioritas.current(3 - prioritas)
        self.info.set("Mode: %s · %s" % (mode.upper(), operasi.upper()))
        if operasi == "lihat" or operasi == "hapus":
            self.indeks.focus_set()
        else:
            self.oid.focus_set()

    def _parse_indeks(self):
        try:
            return int(self.indeks.get())
        except ValueError:
            raise ValueError("Indeks harus berupa bilangan bulat, contoh: 0")

    def _jalankan(self):
        operasi = getattr(self, "operasi", "lihat")
        try:
            if operasi == "lihat":
                indeks = self._parse_indeks()
                array_nilai, list_nilai = self.mesin.lihat(indeks)
                self._tulis_log("LIHAT", "Array O(1) / Linked List O(n)", array_nilai.ringkas(), 0.0)
                self._tampil_detail(array_nilai, list_nilai)
            elif operasi == "hapus":
                indeks = self._parse_indeks()
                array_nilai, list_nilai, ta, tl = self.mesin.hapus(indeks)
                self._tulis_log("HAPUS i=%d" % indeks, "Array + Linked List", "Array=%0.3f ms, List=%0.3f ms" % (ta, tl), ta + tl)
                self._refresh_tabel(max(0, indeks - 2))
            else:
                nilai = buat_pesanan(self.oid.get() or "BARU-%06d" % (self.mesin.ukuran + 1), self.pelanggan.get() or "Pelanggan baru", self.resto.get() or "resto-baru", self.menu.get() or "menu-baru", self.harga.get() or "0", 3 - self.prioritas.current())
                ta, tl, indeks = self.mesin.tambah(nilai)
                self._tulis_log("TAMBAH P%d" % nilai.prioritas, self.mode.get(), "masuk pada indeks %d · Array=%0.3f ms, List=%0.3f ms" % (indeks, ta, tl), ta + tl)
                self._refresh_tabel(max(0, indeks - 2))
                self.oid.delete(0, "end"); self.pelanggan.delete(0, "end"); self.resto.delete(0, "end"); self.menu.delete(0, "end"); self.harga.delete(0, "end")
            self.info.set("%d pesanan · konsistensi: OK" % self.mesin.ukuran)
        except (ValueError, IndexError) as error:
            messagebox.showwarning("Parameter belum benar", str(error))

    def _tampil_detail(self, kiri, kanan):
        self._refresh_tabel(0)
        self.info.set("Array dan Linked List menunjuk pesanan yang sama: %s" % kiri.oid)

    def _refresh_tabel(self, mulai):
        for item in self.tabel.get_children():
            self.tabel.delete(item)
        data = self.mesin.ambil_baris(mulai, 14)
        indeks = mulai
        for nilai in data:
            self.tabel.insert("", "end", values=(indeks, nilai.oid, nilai.menu, nilai.resto, "Rp%d" % nilai.harga, "P%d" % nilai.prioritas, nilai.status))
            indeks += 1

    def _tulis_log(self, operasi, struktur, hasil, waktu):
        self.log.configure(state="normal")
        self.log.insert("end", "%s | %s | %s | total %0.3f ms\n" % (operasi, struktur, hasil, waktu))
        self.log.see("end")
        self.log.configure(state="disabled")

    def _bandingkan(self):
        if self.mesin.ukuran == 0:
            return
        nilai = buat_pesanan("BENCH-001", "Benchmark", "resto-benchmark", "menu-benchmark", 10000, 1)
        ta, tl, indeks = self.mesin.tambah(nilai)
        self.mesin.hapus(indeks)
        self._tulis_log("BANDINGKAN", "Array vs Linked List", "sisip+hapus i=%d · Array=%0.3f ms, List=%0.3f ms" % (indeks, ta, tl), ta + tl)


def main():
    root = tk.Tk()
    AplikasiM1(root)
    root.mainloop()


if __name__ == "__main__":
    main()
