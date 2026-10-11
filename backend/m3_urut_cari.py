import csv
import os
import time

from backend.m1_pesanan import pesanan_dari_baris

BATAS_INSERTION = 20000

KUNCI = (
    ("harga", lambda p: p.harga),
    ("prioritas", lambda p: p.prioritas),
    ("t_masuk", lambda p: p.t_masuk),
    ("oid", lambda p: p.oid),
    ("pelanggan", lambda p: p.pelanggan),
    ("resto", lambda p: p.resto),
    ("menu", lambda p: p.menu),
)


def ambil_kunci(nama):
    i = 0
    while i < len(KUNCI):
        if KUNCI[i][0] == nama:
            return KUNCI[i][1]
        i += 1
    raise ValueError("kunci tidak dikenal: " + str(nama))


def nama_kunci():
    hasil = [None] * len(KUNCI)
    i = 0
    while i < len(KUNCI):
        hasil[i] = KUNCI[i][0]
        i += 1
    return tuple(hasil)


class Statistik:
    def __init__(self):
        self.perbandingan = 0
        self.pergeseran = 0
        self.waktu_ms = 0.0


def salin(data, n=None):
    if n is None or n > len(data):
        n = len(data)
    hasil = [None] * n
    i = 0
    while i < n:
        hasil[i] = data[i]
        i += 1
    return hasil


def insertion_sort(data, kunci, stat=None):
    if stat is None:
        stat = Statistik()
    n = len(data)
    if n > BATAS_INSERTION:
        raise ValueError("Insertion Sort ditolak: %d data melebihi batas %d" % (n, BATAS_INSERTION))
    mulai = time.perf_counter()
    i = 1
    while i < n:
        x = data[i]
        kx = kunci(x)
        j = i - 1
        while j >= 0:
            stat.perbandingan += 1
            if kunci(data[j]) > kx:
                data[j + 1] = data[j]
                stat.pergeseran += 1
                j -= 1
            else:
                break
        data[j + 1] = x
        i += 1
    stat.waktu_ms = (time.perf_counter() - mulai) * 1000.0
    return stat


def _gabung(data, buffer, kiri, tengah, kanan, kunci, stat):
    i = kiri
    j = tengah
    k = kiri
    while i < tengah and j < kanan:
        stat.perbandingan += 1
        if kunci(data[j]) < kunci(data[i]):
            buffer[k] = data[j]
            j += 1
        else:
            buffer[k] = data[i]
            i += 1
        k += 1
    while i < tengah:
        buffer[k] = data[i]
        i += 1
        k += 1
    while j < kanan:
        buffer[k] = data[j]
        j += 1
        k += 1
    k = kiri
    while k < kanan:
        data[k] = buffer[k]
        k += 1


def _merge_rekursif(data, buffer, kiri, kanan, kunci, stat):
    if kanan - kiri < 2:
        return
    tengah = (kiri + kanan) // 2
    _merge_rekursif(data, buffer, kiri, tengah, kunci, stat)
    _merge_rekursif(data, buffer, tengah, kanan, kunci, stat)
    _gabung(data, buffer, kiri, tengah, kanan, kunci, stat)


def merge_sort(data, kunci, stat=None):
    if stat is None:
        stat = Statistik()
    mulai = time.perf_counter()
    buffer = [None] * len(data)
    _merge_rekursif(data, buffer, 0, len(data), kunci, stat)
    stat.waktu_ms = (time.perf_counter() - mulai) * 1000.0
    return stat


def stabil(data, kunci, urutan_asal):
    i = 1
    while i < len(data):
        a = data[i - 1]
        b = data[i]
        if kunci(a) > kunci(b):
            return False
        if kunci(a) == kunci(b) and urutan_asal(a) > urutan_asal(b):
            return False
        i += 1
    return True


def linear_search(data, kunci, target, stat=None):
    if stat is None:
        stat = Statistik()
    mulai = time.perf_counter()
    hasil = -1
    i = 0
    n = len(data)
    while i < n:
        stat.perbandingan += 1
        if kunci(data[i]) == target:
            hasil = i
            break
        i += 1
    stat.waktu_ms = (time.perf_counter() - mulai) * 1000.0
    return hasil, stat


def binary_search(data, kunci, target, stat=None):
    if stat is None:
        stat = Statistik()
    mulai = time.perf_counter()
    kiri = 0
    kanan = len(data) - 1
    hasil = -1
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        nilai = kunci(data[tengah])
        stat.perbandingan += 1
        if nilai == target:
            hasil = tengah
            kanan = tengah - 1
        elif nilai < target:
            kiri = tengah + 1
        else:
            kanan = tengah - 1
    stat.waktu_ms = (time.perf_counter() - mulai) * 1000.0
    return hasil, stat


def muat_pesanan(path, batas=None):
    if not os.path.isfile(path):
        raise FileNotFoundError("File data tidak ditemukan: " + path)
    data = [None] * 1024
    n = 0
    with open(path, "r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if len(row) < 9:
                continue
            if n == len(data):
                data = salin_kapasitas(data, n * 2)
            data[n] = pesanan_dari_baris(row)
            n += 1
            if batas is not None and n >= batas:
                break
    return salin(data, n)


def salin_kapasitas(data, kapasitas):
    baru = [None] * kapasitas
    i = 0
    while i < len(data):
        baru[i] = data[i]
        i += 1
    return baru


def ubah_target(nama, teks):
    if nama in ("harga", "prioritas", "t_masuk"):
        try:
            return int(teks)
        except ValueError:
            raise ValueError("Target untuk kunci %s harus bilangan bulat" % nama)
    return teks


class MesinM3:
    def __init__(self):
        self.data = [None] * 0
        self.terurut = None
        self.kunci_terurut = None
        self.ongkos_indeks = None

    @property
    def ukuran(self):
        return len(self.data)

    def muat_csv(self, path, batas=None):
        self.data = muat_pesanan(path, batas)
        self.terurut = None
        self.kunci_terurut = None
        self.ongkos_indeks = None
        return len(self.data)

    def urutkan(self, algoritma, nama, jumlah=None):
        kunci = ambil_kunci(nama)
        data = salin(self.data, jumlah)
        if algoritma == "insertion":
            stat = insertion_sort(data, kunci)
        elif algoritma == "merge":
            stat = merge_sort(data, kunci)
        else:
            raise ValueError("algoritma tidak dikenal: " + str(algoritma))
        return data, stat

    def bangun_indeks(self, nama):
        data, stat = self.urutkan("merge", nama)
        self.terurut = data
        self.kunci_terurut = nama
        self.ongkos_indeks = stat
        return stat

    def cari_linear(self, nama, target):
        return linear_search(self.data, ambil_kunci(nama), ubah_target(nama, target))

    def cari_binary(self, nama, target):
        baru = None
        if self.kunci_terurut != nama:
            baru = self.bangun_indeks(nama)
        indeks, stat = binary_search(self.terurut, ambil_kunci(nama), ubah_target(nama, target))
        return indeks, stat, baru

    def hasil_binary(self, indeks):
        return self.terurut[indeks]
