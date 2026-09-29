import csv
import os
import time


class Pesanan:
    def __init__(self, oid, pelanggan, resto, menu, harga, prioritas,
                 t_masuk, t_selesai, status):
        self.oid = oid
        self.pelanggan = pelanggan
        self.resto = resto
        self.menu = menu
        self.harga = harga
        self.prioritas = prioritas
        self.t_masuk = t_masuk
        self.t_selesai = t_selesai
        self.status = status

    def ringkas(self):
        return (self.oid + " | " + self.menu + " | " + self.resto +
                " | P" + str(self.prioritas) + " | " + self.status)


def _angka(value, kosong=-1):
    if value is None or value == "":
        return kosong
    return int(value)


def pesanan_dari_baris(row):
    return Pesanan(row[0], row[1], row[2], row[3], int(row[4]), int(row[5]),
                   int(row[6]), _angka(row[7]), row[8])


class ArrayPesanan:
    def __init__(self, kapasitas_awal=4):
        if kapasitas_awal < 1:
            kapasitas_awal = 1
        self._data = [None] * kapasitas_awal
        self._ukuran = 0
        self._kapasitas = kapasitas_awal

    @property
    def ukuran(self):
        return self._ukuran

    @property
    def kapasitas(self):
        return self._kapasitas

    def append(self, nilai):
        if self._ukuran == self._kapasitas:
            baru = [None] * (self._kapasitas * 2)
            i = 0
            while i < self._ukuran:
                baru[i] = self._data[i]
                i += 1
            self._data = baru
            self._kapasitas *= 2
        self._data[self._ukuran] = nilai
        self._ukuran += 1

    def insert(self, indeks, nilai):
        if indeks < 0 or indeks > self._ukuran:
            raise IndexError("indeks sisip di luar antrean")
        if indeks == self._ukuran:
            self.append(nilai)
            return
        if self._ukuran == self._kapasitas:
            baru = [None] * (self._kapasitas * 2)
            i = 0
            while i < self._ukuran:
                baru[i] = self._data[i]
                i += 1
            self._data = baru
            self._kapasitas *= 2
        i = self._ukuran
        while i > indeks:
            self._data[i] = self._data[i - 1]
            i -= 1
        self._data[indeks] = nilai
        self._ukuran += 1

    def get(self, indeks):
        if indeks < 0 or indeks >= self._ukuran:
            raise IndexError("indeks pesanan tidak tersedia")
        return self._data[indeks]

    def delete(self, indeks):
        nilai = self.get(indeks)
        i = indeks
        while i < self._ukuran - 1:
            self._data[i] = self._data[i + 1]
            i += 1
        self._data[self._ukuran - 1] = None
        self._ukuran -= 1
        return nilai


class Node:
    def __init__(self, nilai):
        self.nilai = nilai
        self.berikutnya = None


class LinkedListPesanan:
    def __init__(self):
        self.head = None
        self.tail = None
        self._ukuran = 0

    @property
    def ukuran(self):
        return self._ukuran

    def append(self, nilai):
        simpul = Node(nilai)
        if self.head is None:
            self.head = simpul
            self.tail = simpul
        else:
            self.tail.berikutnya = simpul
            self.tail = simpul
        self._ukuran += 1

    def prepend(self, nilai):
        simpul = Node(nilai)
        simpul.berikutnya = self.head
        self.head = simpul
        if self.tail is None:
            self.tail = simpul
        self._ukuran += 1

    def insert(self, indeks, nilai):
        if indeks < 0 or indeks > self._ukuran:
            raise IndexError("indeks sisip di luar antrean")
        if indeks == 0:
            self.prepend(nilai)
            return
        if indeks == self._ukuran:
            self.append(nilai)
            return
        sebelum = self.head
        langkah = 1
        while langkah < indeks:
            sebelum = sebelum.berikutnya
            langkah += 1
        simpul = Node(nilai)
        simpul.berikutnya = sebelum.berikutnya
        sebelum.berikutnya = simpul
        self._ukuran += 1

    def get(self, indeks):
        if indeks < 0 or indeks >= self._ukuran:
            raise IndexError("indeks pesanan tidak tersedia")
        simpul = self.head
        langkah = 0
        while langkah < indeks:
            simpul = simpul.berikutnya
            langkah += 1
        return simpul.nilai

    def delete(self, indeks):
        if indeks < 0 or indeks >= self._ukuran:
            raise IndexError("indeks pesanan tidak tersedia")
        if indeks == 0:
            simpul = self.head
            self.head = simpul.berikutnya
            self._ukuran -= 1
            if self._ukuran == 0:
                self.tail = None
            return simpul.nilai
        sebelum = self.head
        langkah = 1
        while langkah < indeks:
            sebelum = sebelum.berikutnya
            langkah += 1
        simpul = sebelum.berikutnya
        sebelum.berikutnya = simpul.berikutnya
        if simpul is self.tail:
            self.tail = sebelum
        self._ukuran -= 1
        return simpul.nilai


def indeks_sisip(prioritas, ukuran):
    if prioritas == 1:
        return 0
    if prioritas == 2:
        return ukuran // 2
    if prioritas == 3:
        return ukuran
    raise ValueError("prioritas harus 1 (VIP), 2 (Prioritas), atau 3 (Reguler)")


class MesinM1:
    def __init__(self):
        self.array = ArrayPesanan()
        self.linked_list = LinkedListPesanan()

    @property
    def ukuran(self):
        return self.array.ukuran

    def muat_csv(self, path, batas=None):
        if not os.path.isfile(path):
            raise FileNotFoundError("File data tidak ditemukan: " + path)
        self.array = ArrayPesanan()
        self.linked_list = LinkedListPesanan()
        with open(path, "r", encoding="utf-8", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)
            jumlah = 0
            for row in reader:
                if len(row) < 9:
                    continue
                nilai = pesanan_dari_baris(row)
                self.array.append(nilai)
                self.linked_list.append(nilai)
                jumlah += 1
                if batas is not None and jumlah >= batas:
                    break
        return jumlah

    def tambah(self, pesanan):
        indeks_array = indeks_sisip(pesanan.prioritas, self.array.ukuran)
        indeks_list = indeks_sisip(pesanan.prioritas, self.linked_list.ukuran)
        mulai_array = time.perf_counter_ns()
        self.array.insert(indeks_array, pesanan)
        waktu_array = time.perf_counter_ns() - mulai_array
        mulai_list = time.perf_counter_ns()
        self.linked_list.insert(indeks_list, pesanan)
        waktu_list = time.perf_counter_ns() - mulai_list
        return (waktu_array / 1000000.0, waktu_list / 1000000.0, indeks_array)

    def lihat(self, indeks):
        return self.array.get(indeks), self.linked_list.get(indeks)

    def hapus(self, indeks):
        mulai_array = time.perf_counter_ns()
        array_nilai = self.array.delete(indeks)
        waktu_array = time.perf_counter_ns() - mulai_array
        mulai_list = time.perf_counter_ns()
        list_nilai = self.linked_list.delete(indeks)
        waktu_list = time.perf_counter_ns() - mulai_list
        return (array_nilai, list_nilai, waktu_array / 1000000.0,
                waktu_list / 1000000.0)

    def ambil_baris(self, mulai, jumlah):
        hasil = []
        akhir = mulai + jumlah
        if mulai < 0:
            mulai = 0
        if akhir > self.ukuran:
            akhir = self.ukuran
        indeks = mulai
        while indeks < akhir:
            hasil.append(self.array.get(indeks))
            indeks += 1
        return hasil

    def konsisten(self, batas=None):
        jumlah = self.ukuran
        if self.linked_list.ukuran != jumlah:
            return False
        if batas is not None and jumlah > batas:
            jumlah = batas
        indeks = 0
        simpul = self.linked_list.head
        while indeks < jumlah:
            if self.array._data[indeks] is not simpul.nilai:
                return False
            simpul = simpul.berikutnya
            indeks += 1
        return True


def buat_pesanan(oid, pelanggan, resto, menu, harga, prioritas,
                 status="ANTRE"):
    return Pesanan(oid, pelanggan, resto, menu, int(harga), int(prioritas),
                   0, -1, status)
