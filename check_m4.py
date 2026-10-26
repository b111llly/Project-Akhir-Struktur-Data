import os
import time

from backend.m1_pesanan import buat_pesanan
from backend.m3_urut_cari import (
    binary_search,
    linear_search,
    merge_sort,
    salin,
    stabil,
)
from backend.m4_pencarian import MesinM4, NodeHash, PetaHash

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "pesanan.csv")


def _urutan(p):
    return int(p.oid[2:])


def test_peta_hash_dasar():
    peta = PetaHash(kapasitas_awal=4, faktor_beban=0.75)
    assert peta.ukuran == 0
    assert peta.kapasitas == 4

    peta.put("k1", 100)
    peta.put("k2", 200)
    peta.put("k3", 300)
    assert peta.ukuran == 3
    assert peta.kapasitas == 4

    v, s = peta.get("k2")
    assert v == 200 and s.perbandingan >= 1
    assert peta.contains("k1")
    assert not peta.contains("k4")

    peta.put("k4", 400)
    assert peta.ukuran == 4
    assert peta.kapasitas == 8
    v, _ = peta.get("k4")
    assert v == 400

    peta.put("k2", 250)
    assert peta.ukuran == 4
    v, _ = peta.get("k2")
    assert v == 250

    terhapus = peta.remove("k3")
    assert terhapus == 300
    assert peta.ukuran == 3
    assert not peta.contains("k3")
    v, _ = peta.get("k3")
    assert v is None


def test_peta_hash_kolisi():
    peta = PetaHash(kapasitas_awal=4, faktor_beban=1.0)
    i = 0
    while i < 20:
        peta.put("kunci_%d" % i, i * 10)
        i += 1
    assert peta.ukuran == 20
    i = 0
    while i < 20:
        v, s = peta.get("kunci_%d" % i)
        assert v == i * 10
        i += 1
    uk, kap, terisi, maks_rantai, beban = peta.stats()
    assert uk == 20 and kap >= 20 and maks_rantai >= 1


def test_merge_sort_m4():
    harga = (7000, 3000, 7000, 1000, 3000, 9000, 2000, 1000)
    data = [None] * len(harga)
    i = 0
    while i < len(harga):
        data[i] = buat_pesanan("O-%06d" % (i + 1), "p", "r", "m", harga[i], 3)
        i += 1
    stat = merge_sort(data, lambda p: p.harga)
    assert stabil(data, lambda p: p.harga, _urutan)
    assert stat.perbandingan > 0


def test_data_penuh_m4():
    mesin = MesinM4()
    n = mesin.muat_csv(PATH)
    assert n == 200000
    print("CSV loaded 200.000 data ke MesinM4.")

    uk, kap, terisi, maks_r, beban = mesin.peta_oid.stats()
    print("PetaHash OID stats: ukuran=%d, kapasitas=%d, terisi=%d, maks_rantai=%d, load=%.2f" % (uk, kap, terisi, maks_r, beban))
    assert uk == 200000
    assert maks_r <= 10

    p1, s_hash = mesin.cari_hash_oid("O-150000")
    assert p1 is not None and p1.oid == "O-150000"
    print("PetaHash get O-150000: %d perbandingan, %.4f ms" % (s_hash.perbandingan, s_hash.waktu_ms))
    assert s_hash.perbandingan <= 5

    data_sorted, s_sort = mesin.urutkan_merge(lambda p: p.oid)
    assert stabil(data_sorted, lambda p: p.oid, _urutan)
    idx_bin, s_bin = binary_search(data_sorted, lambda p: p.oid, "O-150000")
    assert idx_bin >= 0 and data_sorted[idx_bin].oid == "O-150000"
    print("Binary Search O-150000: %d perbandingan, %.4f ms" % (s_bin.perbandingan, s_bin.waktu_ms))

    idx_lin, s_lin = linear_search(mesin.data, lambda p: p.oid, "O-150000")
    assert idx_lin == 149999
    print("Linear Search O-150000: %d perbandingan, %.4f ms" % (s_lin.perbandingan, s_lin.waktu_ms))

    assert s_hash.perbandingan < s_bin.perbandingan
    assert s_bin.perbandingan < s_lin.perbandingan

    hasil_resto, s_resto = mesin.cari_hash_resto("kafe-teknik")
    assert len(hasil_resto) > 0
    print("PetaHash get resto 'kafe-teknik': %d pesanan ditemukan, %d perbandingan, %.4f ms" % (len(hasil_resto), s_resto.perbandingan, s_resto.waktu_ms))


if __name__ == "__main__":
    test_peta_hash_dasar()
    test_peta_hash_kolisi()
    test_merge_sort_m4()
    test_data_penuh_m4()
    print("check_m4: PASS")
