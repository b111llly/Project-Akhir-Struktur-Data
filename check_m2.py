from backend.m2_antrean import Tumpukan, Stack, pecah_token, ke_postfix, hitung


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


if __name__ == "__main__":
    test_tumpukan_step1()
    test_mesin_kasir_step2()
