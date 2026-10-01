from backend.m2_antrean import Tumpukan, Stack


def test_tumpukan_step1():
    # 1. Stack baru harus kosong
    s = Tumpukan()
    assert s.kosong() is True, "Stack baru harus dalam kondisi kosong"
    assert s.ukuran == 0, "Ukuran stack baru harus 0"

    # 2. Push elemen
    s.push(10)
    assert s.kosong() is False, "Stack tidak boleh kosong setelah push"
    assert s.ukuran == 1, "Ukuran stack harus 1 setelah 1 kali push"

    s.push(20)
    assert s.ukuran == 2, "Ukuran stack harus 2 setelah 2 kali push"

    s.push(30)
    assert s.ukuran == 3, "Ukuran stack harus 3 setelah 3 kali push"

    # 3. Peek elemen puncak
    assert s.peek() == 30, "Peek harus menghasilkan elemen teratas (30)"
    assert s.ukuran == 3, "Peek tidak boleh mengurangi ukuran stack"

    # 4. Pop elemen
    teratas = s.pop()
    assert teratas == 30, "Pop pertama harus menghasilkan elemen teratas (30)"
    assert s.ukuran == 2, "Ukuran stack harus berkurang menjadi 2"

    kedua = s.pop()
    assert kedua == 20, "Pop kedua harus menghasilkan 20"
    assert s.ukuran == 1, "Ukuran stack harus berkurang menjadi 1"

    ketiga = s.pop()
    assert ketiga == 10, "Pop ketiga harus menghasilkan 10"
    assert s.ukuran == 0, "Ukuran stack harus kembali menjadi 0"

    # 5. Kondisi kosong bekerja
    assert s.kosong() is True, "Stack harus kembali kosong"

    # 6. Pop stack kosong ditangani dengan aman
    tertangkap_pop = False
    try:
        s.pop()
    except IndexError:
        tertangkap_pop = True
    assert tertangkap_pop is True, "Pop pada stack kosong harus memicu IndexError"

    # 7. Peek stack kosong ditangani dengan aman
    tertangkap_peek = False
    try:
        s.peek()
    except IndexError:
        tertangkap_peek = True
    assert tertangkap_peek is True, "Peek pada stack kosong harus memicu IndexError"

    # 8. Uji penggandaan kapasitas (doubling) primitive array
    t = Stack(kapasitas_awal=2)
    t.push(1)
    t.push(2)
    assert t.kapasitas == 2
    t.push(3)
    assert t.kapasitas == 4, "Kapasitas harus mengganda menjadi 4 saat penuh"
    assert t.ukuran == 3
    assert t.pop() == 3
    assert t.pop() == 2
    assert t.pop() == 1
    assert t.kosong() is True

    print("M2 STEP 1 CHECK OK: Tumpukan (Stack) primitive array lulus semua pengujian.")


if __name__ == "__main__":
    test_tumpukan_step1()
