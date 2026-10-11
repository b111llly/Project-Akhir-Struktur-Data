import os
import time

from backend.m1_pesanan import buat_pesanan
from backend.m3_urut_cari import (
    BATAS_INSERTION,
    MesinM3,
    insertion_sort,
    merge_sort,
    linear_search,
    binary_search,
    stabil,
    salin,
)

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "pesanan.csv")


def _sampel():
    harga = (5000, 3000, 5000, 1000, 3000, 5000, 2000, 1000)
    data = [None] * len(harga)
    i = 0
    while i < len(harga):
        data[i] = buat_pesanan("O-%06d" % (i + 1), "p", "r", "m", harga[i], 3)
        i += 1
    return data


def _urutan(p):
    return int(p.oid[2:])


def test_insertion():
    data = _sampel()
    stat = insertion_sort(data, lambda p: p.harga)
    assert stabil(data, lambda p: p.harga, _urutan)
    assert stat.perbandingan > 0
    besar = [None] * (BATAS_INSERTION + 1)
    try:
        insertion_sort(besar, lambda p: p)
        assert False
    except ValueError:
        pass


def test_merge():
    data = _sampel()
    stat = merge_sort(data, lambda p: p.harga)
    assert stabil(data, lambda p: p.harga, _urutan)
    assert stat.perbandingan > 0
    kosong = [None] * 0
    merge_sort(kosong, lambda p: p)


def test_search():
    data = _sampel()
    i, s = linear_search(data, lambda p: p.harga, 1000)
    assert i == 3 and s.perbandingan == 4
    i, s = linear_search(data, lambda p: p.harga, 999)
    assert i == -1 and s.perbandingan == len(data)
    merge_sort(data, lambda p: p.harga)
    i, s = binary_search(data, lambda p: p.harga, 3000)
    assert data[i].harga == 3000 and data[i - 1].harga < 3000
    i, s = binary_search(data, lambda p: p.harga, 4000)
    assert i == -1


def test_data_penuh():
    mesin = MesinM3()
    n = mesin.muat_csv(PATH)
    assert n == 200000
    data, stat = mesin.urutkan("merge", "harga")
    assert stabil(data, lambda p: p.harga, _urutan)
    print("Merge Sort 200000: %d perbandingan, %.1f ms" % (stat.perbandingan, stat.waktu_ms))
    data, stat = mesin.urutkan("insertion", "harga", 5000)
    assert stabil(data, lambda p: p.harga, _urutan)
    print("Insertion Sort 5000: %d perbandingan, %.1f ms" % (stat.perbandingan, stat.waktu_ms))
    try:
        mesin.urutkan("insertion", "harga")
        assert False
    except ValueError:
        pass
    i, sl = mesin.cari_linear("oid", "O-150000")
    assert mesin.data[i].oid == "O-150000"
    j, sb, ongkos = mesin.cari_binary("oid", "O-150000")
    assert mesin.hasil_binary(j).oid == "O-150000"
    assert ongkos is not None and sb.perbandingan <= 20
    print("Linear: %d perbandingan | Binary: %d perbandingan + indeks %d perbandingan" % (sl.perbandingan, sb.perbandingan, ongkos.perbandingan))
    j, sb, ongkos = mesin.cari_binary("oid", "O-000001")
    assert ongkos is None


if __name__ == "__main__":
    test_insertion()
    test_merge()
    test_search()
    test_data_penuh()
    print("check_m3: PASS")
