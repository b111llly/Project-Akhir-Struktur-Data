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

    def stats(self):
        maks_rantai = 0
        ember_terisi = 0
        i = 0
        while i < self._kapasitas:
            simpul = self._tabel[i]
            if simpul is not None:
                ember_terisi += 1
                pjg = 0
                while simpul is not None:
                    pjg += 1
                    simpul = simpul.berikut
                if pjg > maks_rantai:
                    maks_rantai = pjg
            i += 1
        beban = self._ukuran / self._kapasitas if self._kapasitas > 0 else 0.0
        return self._ukuran, self._kapasitas, ember_terisi, maks_rantai, beban


class MesinM4:
    def __init__(self):
        self.data = [None] * 0
        self.peta_oid = PetaHash()
        self.peta_resto = PetaHash()
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

        i = 0
        while i < n:
            p = self.data[i]
            peta_oid.put(p.oid, p)
            simpul_lama, _ = peta_resto.get(p.resto)
            if simpul_lama is None:
                wadah = [None] * 4
                wadah[0] = p
                peta_resto.put(p.resto, (wadah, 1))
            else:
                wadah, hitung = simpul_lama
                if hitung == len(wadah):
                    baru = [None] * (hitung * 2)
                    j = 0
                    while j < hitung:
                        baru[j] = wadah[j]
                        j += 1
                    wadah = baru
                wadah[hitung] = p
                peta_resto.put(p.resto, (wadah, hitung + 1))
            i += 1

        self.peta_oid = peta_oid
        self.peta_resto = peta_resto
        stat.waktu_ms = (time.perf_counter() - mulai) * 1000.0
        return stat

    def urutkan_merge(self, kunci, jumlah=None):
        data = salin(self.data, jumlah)
        stat = merge_sort(data, kunci)
        return data, stat

    def cari_hash_oid(self, oid):
        return self.peta_oid.get(oid)

    def cari_hash_resto(self, resto):
        wadah_tuple, stat = self.peta_resto.get(resto)
        if wadah_tuple is None:
            return [None] * 0, stat
        wadah, hitung = wadah_tuple
        return salin(wadah, hitung), stat
