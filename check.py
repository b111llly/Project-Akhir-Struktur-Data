import os

from backend.m1_pesanan import ArrayPesanan, LinkedListPesanan, MesinM1, buat_pesanan


def check():
    array = ArrayPesanan(2)
    linked = LinkedListPesanan()
    for angka in range(20):
        array.append(angka)
        linked.append(angka)
    if array.kapasitas < 20 or array.get(19) != 19 or linked.get(19) != 19:
        raise AssertionError("append/get gagal")
    array.insert(0, -1); linked.insert(0, -1)
    array.insert(10, -2); linked.insert(10, -2)
    if array.delete(0) != -1 or linked.delete(0) != -1:
        raise AssertionError("delete gagal")
    mesin = MesinM1()
    path = os.path.join(os.path.dirname(__file__), "data", "pesanan.csv")
    jumlah = mesin.muat_csv(path, batas=1000)
    if jumlah != 1000 or not mesin.konsisten():
        raise AssertionError("load CSV atau konsistensi gagal")
    for prioritas in (3, 2, 1):
        mesin.tambah(buat_pesanan("T-%d" % prioritas, "Test", "Resto", "Menu", 1000, prioritas))
    if not mesin.konsisten() or mesin.lihat(0)[0].oid != "T-1":
        raise AssertionError("aturan penyisipan gagal")
    mesin.hapus(0)
    if not mesin.konsisten():
        raise AssertionError("hapus tidak konsisten")
    print("M1 CHECK OK: primitive structures, CSV load, insertion rules, delete, consistency")


if __name__ == "__main__":
    check()
