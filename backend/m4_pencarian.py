import os
import time

from backend.m3_urut_cari import Statistik, merge_sort, muat_pesanan, salin


class NodeHash:
    __slots__ = ("k", "v", "berikut")

    def __init__(self, k, v, berikut=None):
        self.k = k
        self.v = v
        self.berikut = berikut


class PetaHash:
    def __init__(self, kapasitas_awal=16, faktor_beban=0.75):
        if kapasitas_awal < 4:
            kapasitas_awal = 4
        self._kapasitas = kapasitas_awal
        self._faktor_beban = faktor_beban
        self._ukuran = 0
        self._tabel = [None] * self._kapasitas

    @property
    def ukuran(self):
        return self._ukuran

    @property
    def kapasitas(self):
        return self._kapasitas

    def __len__(self):
        return self._ukuran

    def __contains__(self, k):
        return self.contains(k)

    def __getitem__(self, k):
        v, _ = self.get(k)
        if v is None and not self.contains(k):
            raise KeyError(k)
        return v

    def __setitem__(self, k, v):
        self.put(k, v)

    def __delitem__(self, k):
        if not self.contains(k):
            raise KeyError(k)
        self.remove(k)

    def hash_teks(self, s):
        teks = str(s)
        h = 5381
        i = 0
        n = len(teks)
        while i < n:
            h = (((h << 5) + h) + ord(teks[i])) & 0x7FFFFFFF
            i += 1
        return h % self._kapasitas

    def _rehash(self):
        tabel_lama = self._tabel
        self._kapasitas *= 2
        self._tabel = [None] * self._kapasitas
        i = 0
        n = len(tabel_lama)
        while i < n:
            simpul = tabel_lama[i]
            while simpul is not None:
                berikut = simpul.berikut
                idx = self.hash_teks(simpul.k)
                simpul.berikut = self._tabel[idx]
                self._tabel[idx] = simpul
                simpul = berikut
            i += 1

    def put(self, k, v):
        idx = self.hash_teks(k)
        simpul = self._tabel[idx]
        while simpul is not None:
            if simpul.k == k:
                simpul.v = v
                return
            simpul = simpul.berikut
        baru = NodeHash(k, v, self._tabel[idx])
        self._tabel[idx] = baru
        self._ukuran += 1
        if self._ukuran > self._kapasitas * self._faktor_beban:
            self._rehash()

    def get(self, k, stat=None):
        if stat is None:
            stat = Statistik()
        mulai = time.perf_counter()
        idx = self.hash_teks(k)
        simpul = self._tabel[idx]
        hasil = None
        while simpul is not None:
            stat.perbandingan += 1
            if simpul.k == k:
                hasil = simpul.v
                break
            simpul = simpul.berikut
        stat.waktu_ms = (time.perf_counter() - mulai) * 1000.0
        return hasil, stat

    def contains(self, k):
        idx = self.hash_teks(k)
        simpul = self._tabel[idx]
        while simpul is not None:
            if simpul.k == k:
                return True
            simpul = simpul.berikut
        return False

    def remove(self, k):
        idx = self.hash_teks(k)
        simpul = self._tabel[idx]
        sebelum = None
        while simpul is not None:
            if simpul.k == k:
                if sebelum is None:
                    self._tabel[idx] = simpul.berikut
                else:
                    sebelum.berikut = simpul.berikut
                self._ukuran -= 1
                return simpul.v
            sebelum = simpul
            simpul = simpul.berikut
        return None

    def clear(self):
        self._tabel = [None] * self._kapasitas
        self._ukuran = 0

    def keys(self):
        hasil = [None] * self._ukuran
        pos = 0
        i = 0
        while i < self._kapasitas:
            simpul = self._tabel[i]
            while simpul is not None:
                hasil[pos] = simpul.k
                pos += 1
                simpul = simpul.berikut
            i += 1
        return hasil

    def values(self):
        hasil = [None] * self._ukuran
        pos = 0
        i = 0
        while i < self._kapasitas:
            simpul = self._tabel[i]
            while simpul is not None:
                hasil[pos] = simpul.v
                pos += 1
                simpul = simpul.berikut
            i += 1
        return hasil

    def items(self):
        hasil = [None] * self._ukuran
        pos = 0
        i = 0
        while i < self._kapasitas:
            simpul = self._tabel[i]
            while simpul is not None:
                hasil[pos] = (simpul.k, simpul.v)
                pos += 1
                simpul = simpul.berikut
            i += 1
        return hasil

    def stats(self):
        maks_rantai = 0
        ember_terisi = 0
        total_panjang_rantai = 0
        i = 0
        while i < self._kapasitas:
            simpul = self._tabel[i]
            if simpul is not None:
                ember_terisi += 1
                pjg = 0
                while simpul is not None:
                    pjg += 1
                    simpul = simpul.berikut
                total_panjang_rantai += pjg
                if pjg > maks_rantai:
                    maks_rantai = pjg
            i += 1
        beban = self._ukuran / self._kapasitas if self._kapasitas > 0 else 0.0
        rata_rantai = total_panjang_rantai / ember_terisi if ember_terisi > 0 else 0.0
        return self._ukuran, self._kapasitas, ember_terisi, maks_rantai, rata_rantai, beban


def binary_search_rentang(data, kunci, target, stat=None):
    if stat is None:
        stat = Statistik()
    mulai = time.perf_counter()
    n = len(data)
    lo = 0
    hi = n - 1
    idx_awal = -1
    while lo <= hi:
        tengah = (lo + hi) // 2
        nilai = kunci(data[tengah])
        stat.perbandingan += 1
        if nilai == target:
            idx_awal = tengah
            hi = tengah - 1
        elif nilai < target:
            lo = tengah + 1
        else:
            hi = tengah - 1

    if idx_awal == -1:
        stat.waktu_ms = (time.perf_counter() - mulai) * 1000.0
        return -1, -1, stat

    lo = idx_awal
    hi = n - 1
    idx_akhir = idx_awal
    while lo <= hi:
        tengah = (lo + hi) // 2
        nilai = kunci(data[tengah])
        stat.perbandingan += 1
        if nilai == target:
            idx_akhir = tengah
            lo = tengah + 1
        elif nilai < target:
            lo = tengah + 1
        else:
            hi = tengah - 1

    stat.waktu_ms = (time.perf_counter() - mulai) * 1000.0
    return idx_awal, idx_akhir, stat


def linear_search_semua(data, kunci, target, stat=None):
    if stat is None:
        stat = Statistik()
    mulai = time.perf_counter()
    wadah = [None] * 16
    hitung = 0
    i = 0
    n = len(data)
    while i < n:
        stat.perbandingan += 1
        if kunci(data[i]) == target:
            if hitung == len(wadah):
                baru = [None] * (hitung * 2)
                j = 0
                while j < hitung:
                    baru[j] = wadah[j]
                    j += 1
                wadah = baru
            wadah[hitung] = data[i]
            hitung += 1
        i += 1
    stat.waktu_ms = (time.perf_counter() - mulai) * 1000.0
    return salin(wadah, hitung), stat


def _tambah_ke_indeks_multi(peta, kunci, item):
    simpul_lama, _ = peta.get(kunci)
    if simpul_lama is None:
        wadah = [None] * 4
        wadah[0] = item
        peta.put(kunci, (wadah, 1))
    else:
        wadah, hitung = simpul_lama
        if hitung == len(wadah):
            baru = [None] * (hitung * 2)
            j = 0
            while j < hitung:
                baru[j] = wadah[j]
                j += 1
            wadah = baru
        wadah[hitung] = item
        peta.put(kunci, (wadah, hitung + 1))


class MesinM4:
    def __init__(self):
        self.data = [None] * 0
        self.peta_oid = PetaHash()
        self.peta_resto = PetaHash()
        self.peta_pelanggan = PetaHash()
        self.peta_menu = PetaHash()
        self._cache_terurut = [None] * 4

    @property
    def ukuran(self):
        return len(self.data)

    def muat_csv(self, path, batas=None):
        self.data = muat_pesanan(path, batas)
        self._cache_terurut = [None] * 4
        self.bangun_hash()
        return len(self.data)

    def bangun_hash(self):
        mulai = time.perf_counter()
        stat = Statistik()
        n = len(self.data)
        kapasitas_awal = 16
        while kapasitas_awal * 0.75 < n:
            kapasitas_awal *= 2

        peta_oid = PetaHash(kapasitas_awal)
        peta_resto = PetaHash(kapasitas_awal)
        peta_pelanggan = PetaHash(kapasitas_awal)
        peta_menu = PetaHash(kapasitas_awal)

        i = 0
        while i < n:
            p = self.data[i]
            peta_oid.put(p.oid, p)
            _tambah_ke_indeks_multi(peta_resto, p.resto, p)
            _tambah_ke_indeks_multi(peta_pelanggan, p.pelanggan, p)
            _tambah_ke_indeks_multi(peta_menu, p.menu, p)
            i += 1

        self.peta_oid = peta_oid
        self.peta_resto = peta_resto
        self.peta_pelanggan = peta_pelanggan
        self.peta_menu = peta_menu
        stat.waktu_ms = (time.perf_counter() - mulai) * 1000.0
        return stat

    def _ekstraktor_kunci(self, mode):
        mode_u = mode.upper()
        if mode_u == "OID":
            return lambda p: p.oid
        if mode_u == "RESTO":
            return lambda p: p.resto
        if mode_u == "PELANGGAN":
            return lambda p: p.pelanggan
        if mode_u == "MENU":
            return lambda p: p.menu
        raise ValueError("Mode tidak didukung: " + str(mode))

    def _slot_indeks(self, mode):
        mode_u = mode.upper()
        if mode_u == "OID":
            return 0
        if mode_u == "RESTO":
            return 1
        if mode_u == "PELANGGAN":
            return 2
        if mode_u == "MENU":
            return 3
        raise ValueError("Mode tidak didukung: " + str(mode))

    def urutkan_merge(self, kunci, jumlah=None):
        data = salin(self.data, jumlah)
        stat = merge_sort(data, kunci)
        return data, stat

    def dapatkan_data_terurut(self, mode):
        slot = self._slot_indeks(mode)
        tersimpan = self._cache_terurut[slot]
        if tersimpan is not None:
            return tersimpan[0], tersimpan[1], False
        fn_kunci = self._ekstraktor_kunci(mode)
        data_baru, stat_sort = self.urutkan_merge(fn_kunci)
        self._cache_terurut[slot] = (data_baru, stat_sort)
        return data_baru, stat_sort, True

    def cari_hash(self, mode, target):
        mode_u = mode.upper()
        if mode_u == "OID":
            p, stat = self.peta_oid.get(target)
            if p is None:
                return [None] * 0, stat
            wadah = [None] * 1
            wadah[0] = p
            return wadah, stat
        if mode_u == "RESTO":
            return self.cari_hash_resto(target)
        if mode_u == "PELANGGAN":
            wadah_tuple, stat = self.peta_pelanggan.get(target)
            if wadah_tuple is None:
                return [None] * 0, stat
            wadah, hitung = wadah_tuple
            return salin(wadah, hitung), stat
        if mode_u == "MENU":
            wadah_tuple, stat = self.peta_menu.get(target)
            if wadah_tuple is None:
                return [None] * 0, stat
            wadah, hitung = wadah_tuple
            return salin(wadah, hitung), stat
        raise ValueError("Mode tidak didukung: " + str(mode))

    def cari_hash_oid(self, oid):
        return self.peta_oid.get(oid)

    def cari_hash_resto(self, resto):
        wadah_tuple, stat = self.peta_resto.get(resto)
        if wadah_tuple is None:
            return [None] * 0, stat
        wadah, hitung = wadah_tuple
        return salin(wadah, hitung), stat

    def cari_binary(self, mode, target):
        data_terurut, stat_sort, _ = self.dapatkan_data_terurut(mode)
        fn_kunci = self._ekstraktor_kunci(mode)
        idx_awal, idx_akhir, stat_search = binary_search_rentang(data_terurut, fn_kunci, target)
        if idx_awal == -1:
            return [None] * 0, stat_search, stat_sort
        panjang = idx_akhir - idx_awal + 1
        hasil = [None] * panjang
        i = 0
        while i < panjang:
            hasil[i] = data_terurut[idx_awal + i]
            i += 1
        return hasil, stat_search, stat_sort

    def cari_linear(self, mode, target):
        fn_kunci = self._ekstraktor_kunci(mode)
        return linear_search_semua(self.data, fn_kunci, target)
