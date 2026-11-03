import os
import time

from backend.m1_pesanan import buat_pesanan
from backend.m3_urut_cari import (
    merge_sort,
    salin,
    stabil,
)
from backend.m4_pencarian import (
    MesinM4,
    NodeHash,
    PetaHash,
    binary_search_rentang,
    linear_search_semua,
)

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

    assert peta["k2"] == 200
    assert "k1" in peta
    assert "k4" not in peta

    peta["k4"] = 400
    assert peta.ukuran == 4
    assert peta.kapasitas == 8
    assert peta["k4"] == 400

    peta["k2"] = 250
    assert peta.ukuran == 4
    assert peta["k2"] == 250

    k_list = peta.keys()
    v_list = peta.values()
    it_list = peta.items()
    assert len(k_list) == 4
    assert len(v_list) == 4
    assert len(it_list) == 4

    del peta["k3"]
    assert peta.ukuran == 3
    assert not peta.contains("k3")
    v, _ = peta.get("k3")
    assert v is None

    peta.clear()
    assert peta.ukuran == 0
    assert len(peta.keys()) == 0


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
    uk, kap, terisi, maks_rantai, rata_rantai, beban = peta.stats()
    assert uk == 20 and kap >= 20 and maks_rantai >= 1
    assert rata_rantai >= 1.0


def test_binary_search_rentang_dan_linear():
    larik = (
        buat_pesanan("O-000001", "A", "R1", "M1", 1000, 3),
        buat_pesanan("O-000002", "B", "R2", "M1", 2000, 3),
        buat_pesanan("O-000003", "C", "R2", "M2", 3000, 3),
        buat_pesanan("O-000004", "D", "R2", "M2", 4000, 3),
        buat_pesanan("O-000005", "E", "R3", "M3", 5000, 3),
    )
    lo, hi, stat_bin = binary_search_rentang(larik, lambda p: p.resto, "R2")
    assert lo == 1 and hi == 3
    assert stat_bin.perbandingan > 0

    hasil_lin, stat_lin = linear_search_semua(larik, lambda p: p.resto, "R2")
    assert len(hasil_lin) == 3
    assert hasil_lin[0].oid == "O-000002"
    assert hasil_lin[2].oid == "O-000004"
    assert stat_lin.perbandingan == 5


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

    uk, kap, terisi, maks_r, rata_r, beban = mesin.peta_oid.stats()
    print("PetaHash OID stats: ukuran=%d, kapasitas=%d, terisi=%d, maks_rantai=%d, rata_rantai=%.2f, load=%.2f" % (
        uk, kap, terisi, maks_r, rata_r, beban
    ))
    assert uk == 200000
    assert maks_r <= 10

    p_hash_list, s_hash = mesin.cari_hash("OID", "O-150000")
    assert len(p_hash_list) == 1 and p_hash_list[0].oid == "O-150000"
    print("PetaHash get O-150000: %d perbandingan, %.4f ms" % (s_hash.perbandingan, s_hash.waktu_ms))

    p_bin_list, s_bin, s_sort = mesin.cari_binary("OID", "O-150000")
    assert len(p_bin_list) == 1 and p_bin_list[0].oid == "O-150000"
    print("Binary Search O-150000: %d perbandingan, %.4f ms (indeks sort: %d cmp)" % (
        s_bin.perbandingan, s_bin.waktu_ms, s_sort.perbandingan
    ))

    p_lin_list, s_lin = mesin.cari_linear("OID", "O-150000")
    assert len(p_lin_list) == 1 and p_lin_list[0].oid == "O-150000"
    print("Linear Search O-150000: %d perbandingan, %.4f ms" % (s_lin.perbandingan, s_lin.waktu_ms))

    assert s_hash.perbandingan < s_bin.perbandingan
    assert s_bin.perbandingan < s_lin.perbandingan

    resto_target = "kafe-teknik"
    h_resto, s_hr = mesin.cari_hash("RESTO", resto_target)
    b_resto, s_br, _ = mesin.cari_binary("RESTO", resto_target)
    l_resto, s_lr = mesin.cari_linear("RESTO", resto_target)
    assert len(h_resto) > 0
    assert len(h_resto) == len(b_resto) == len(l_resto)
    print("Multi-match Resto '%s': %d pesanan cocok." % (resto_target, len(h_resto)))
    print("Resto comparison: Hash %d cmp vs Binary %d cmp vs Linear %d cmp" % (
        s_hr.perbandingan, s_br.perbandingan, s_lr.perbandingan
    ))
    assert s_hr.perbandingan < s_br.perbandingan < s_lr.perbandingan


if __name__ == "__main__":
    test_peta_hash_dasar()
    test_peta_hash_kolisi()
    test_binary_search_rentang_dan_linear()
    test_merge_sort_m4()
    test_data_penuh_m4()
    print("check_m4: PASS")
