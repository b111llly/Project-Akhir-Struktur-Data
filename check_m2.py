from backend.m2_antrean import (
    Tumpukan,
    Stack,
    pecah_token,
    ke_postfix,
    hitung,
    AntreanNaif,
    AntreanMelingkar,
)


def test_tumpukan_step1():
    s = Tumpukan()
    assert s.kosong() is True
    assert s.ukuran == 0

    s.push(10)
    assert s.kosong() is False
    assert s.ukuran == 1

    s.push(20)
    assert s.ukuran == 2

    s.push(30)
    assert s.ukuran == 3

    assert s.peek() == 30
    assert s.ukuran == 3

    teratas = s.pop()
    assert teratas == 30
    assert s.ukuran == 2

    kedua = s.pop()
    assert kedua == 20
    assert s.ukuran == 1

    ketiga = s.pop()
    assert ketiga == 10
    assert s.ukuran == 0

    assert s.kosong() is True

    tertangkap_pop = False
    try:
        s.pop()
    except IndexError:
        tertangkap_pop = True
    assert tertangkap_pop is True

    tertangkap_peek = False
    try:
        s.peek()
    except IndexError:
        tertangkap_peek = True
    assert tertangkap_peek is True

    t = Stack(kapasitas_awal=2)
    t.push(1)
    t.push(2)
    assert t.kapasitas == 2
    t.push(3)
    assert t.kapasitas == 4
    assert t.ukuran == 3
    assert t.pop() == 3
    assert t.pop() == 2
    assert t.pop() == 1
    assert t.kosong() is True


def test_mesin_kasir_step2():
    expr_spec = "( 3 * 12000 ) + ( 2 * 8500 ) - 5000"
    post_spec = ke_postfix(expr_spec)
    assert post_spec == "3 12000 * 2 8500 * + 5000 -", f"Hasil postfix salah: {post_spec}"
    total_spec = hitung(post_spec)
    assert total_spec == 48000, f"Hasil evaluasi salah: {total_spec}"

    expr1 = "10 + 20 * 3"
    post1 = ke_postfix(expr1)
    assert post1 == "10 20 3 * +"
    assert hitung(post1) == 70

    expr2 = "( 10 + 20 ) * 3"
    post2 = ke_postfix(expr2)
    assert post2 == "10 20 + 3 *"
    assert hitung(post2) == 90

    expr3 = "100 - 20 - 10"
    post3 = ke_postfix(expr3)
    assert post3 == "100 20 - 10 -"
    assert hitung(post3) == 70

    expr4 = "( ( 50 - ( 10 + 5 ) ) * 2 ) / 7"
    post4 = ke_postfix(expr4)
    assert post4 == "50 10 5 + - 2 * 7 /"
    assert hitung(post4) == 10

    div_expr = "100 / 4 / 5"
    post_div = ke_postfix(div_expr)
    assert post_div == "100 4 / 5 /"
    assert hitung(post_div) == 5

    print("M2 STEP 1 & 2 CHECK OK: Tumpukan dan Mesin Kasir Postfix lulus semua pengujian.")


def test_antrean_step3():
    q_naif = AntreanNaif(kapasitas_awal=2)
    assert q_naif.kosong() is True
    assert q_naif.ukuran == 0
    assert q_naif.jumlah_pergeseran == 0

    q_naif.enqueue("A")
    q_naif.enqueue("B")
    assert q_naif.kapasitas == 2
    q_naif.enqueue("C")
    assert q_naif.kapasitas == 4
    assert q_naif.ukuran == 3
    assert q_naif.peek() == "A"

    val_a = q_naif.dequeue()
    assert val_a == "A"
    assert q_naif.ukuran == 2
    assert q_naif.jumlah_pergeseran == 2
    assert q_naif.peek() == "B"

    val_b = q_naif.dequeue()
    assert val_b == "B"
    assert q_naif.ukuran == 1
    assert q_naif.jumlah_pergeseran == 3

    val_c = q_naif.dequeue()
    assert val_c == "C"
    assert q_naif.ukuran == 0
    assert q_naif.kosong() is True

    tertangkap_naif = False
    try:
        q_naif.dequeue()
    except IndexError:
        tertangkap_naif = True
    assert tertangkap_naif is True

    q_ring = AntreanMelingkar(kapasitas_awal=3)
    assert q_ring.kosong() is True
    assert q_ring.ukuran == 0

    q_ring.enqueue(10)
    q_ring.enqueue(20)
    q_ring.enqueue(30)
    assert q_ring.kapasitas == 3
    assert q_ring.ukuran == 3
    assert q_ring.peek() == 10

    assert q_ring.dequeue() == 10
    assert q_ring.dequeue() == 20
    assert q_ring.ukuran == 1
    assert q_ring.peek() == 30

    q_ring.enqueue(40)
    q_ring.enqueue(50)
    assert q_ring.ukuran == 3
    assert q_ring.kapasitas == 3

    q_ring.enqueue(60)
    assert q_ring.kapasitas == 6
    assert q_ring.ukuran == 4

    assert q_ring.dequeue() == 30
    assert q_ring.dequeue() == 40
    assert q_ring.dequeue() == 50
    assert q_ring.dequeue() == 60
    assert q_ring.kosong() is True

    tertangkap_ring = False
    try:
        q_ring.dequeue()
    except IndexError:
        tertangkap_ring = True
    assert tertangkap_ring is True

    print("M2 STEP 3 CHECK OK: AntreanNaif dan AntreanMelingkar lulus semua pengujian.")


if __name__ == "__main__":
    test_tumpukan_step1()
    test_mesin_kasir_step2()
    test_antrean_step3()

