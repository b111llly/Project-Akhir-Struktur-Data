class Tumpukan:
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

    def __len__(self):
        return self._ukuran

    def kosong(self):
        return self._ukuran == 0

    def is_empty(self):
        return self._ukuran == 0

    def push(self, nilai):
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

    def pop(self):
        if self.kosong():
            raise IndexError("tumpukan kosong")
        self._ukuran -= 1
        nilai = self._data[self._ukuran]
        self._data[self._ukuran] = None
        return nilai

    def peek(self):
        if self.kosong():
            raise IndexError("tumpukan kosong")
        return self._data[self._ukuran - 1]


Stack = Tumpukan


def pecah_token(ekspresi):
    tokens = []
    i = 0
    panjang = len(ekspresi)
    while i < panjang:
        karakter = ekspresi[i]
        if karakter in " \t\r\n":
            i += 1
            continue
        if "0" <= karakter <= "9":
            awal = i
            while i < panjang and "0" <= ekspresi[i] <= "9":
                i += 1
            tokens.append(ekspresi[awal:i])
            continue
        if karakter in "+-*/()":
            tokens.append(karakter)
            i += 1
            continue
        i += 1
    return tokens


def presedensi(operator):
    if operator in ("*", "/"):
        return 2
    if operator in ("+", "-"):
        return 1
    return 0


def ke_postfix(ekspresi):
    tokens = pecah_token(ekspresi)
    output = []
    stack = Tumpukan()
    for token in tokens:
        if token[0] in "0123456789":
            output.append(token)
        elif token == "(":
            stack.push(token)
        elif token == ")":
            while not stack.kosong() and stack.peek() != "(":
                output.append(stack.pop())
            if not stack.kosong() and stack.peek() == "(":
                stack.pop()
        elif token in ("+", "-", "*", "/"):
            while (not stack.kosong() and stack.peek() != "(" and
                   presedensi(stack.peek()) >= presedensi(token)):
                output.append(stack.pop())
            stack.push(token)
    while not stack.kosong():
        op = stack.pop()
        if op != "(":
            output.append(op)
    return " ".join(output)


def hitung(postfix):
    tokens = pecah_token(postfix)
    stack = Tumpukan()
    for token in tokens:
        if token[0] in "0123456789":
            stack.push(int(token))
        elif token in ("+", "-", "*", "/"):
            if stack.ukuran < 2:
                raise ValueError("ekspresi tidak valid")
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                hasil = a + b
            elif token == "-":
                hasil = a - b
            elif token == "*":
                hasil = a * b
            elif token == "/":
                if b == 0:
                    raise ZeroDivisionError("pembagian dengan nol")
                hasil = a // b
            stack.push(hasil)
    if stack.ukuran != 1:
        raise ValueError("ekspresi tidak valid")
    return stack.pop()


class AntreanNaif:
    def __init__(self, kapasitas_awal=4):
        if kapasitas_awal < 1:
            kapasitas_awal = 1
        self._data = [None] * kapasitas_awal
        self._ukuran = 0
        self._kapasitas = kapasitas_awal
        self.jumlah_pergeseran = 0

    @property
    def ukuran(self):
        return self._ukuran

    @property
    def kapasitas(self):
        return self._kapasitas

    def __len__(self):
        return self._ukuran

    def kosong(self):
        return self._ukuran == 0

    def is_empty(self):
        return self._ukuran == 0

    def enqueue(self, nilai):
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

    def dequeue(self):
        if self.kosong():
            raise IndexError("antrean kosong")
        nilai = self._data[0]
        i = 0
        while i < self._ukuran - 1:
            self._data[i] = self._data[i + 1]
            i += 1
            self.jumlah_pergeseran += 1
        self._ukuran -= 1
        self._data[self._ukuran] = None
        return nilai

    def peek(self):
        if self.kosong():
            raise IndexError("antrean kosong")
        return self._data[0]


class AntreanMelingkar:
    def __init__(self, kapasitas_awal=4):
        if kapasitas_awal < 1:
            kapasitas_awal = 1
        self._data = [None] * kapasitas_awal
        self._kapasitas = kapasitas_awal
        self._depan = 0
        self._belakang = 0
        self._ukuran = 0

    @property
    def ukuran(self):
        return self._ukuran

    @property
    def kapasitas(self):
        return self._kapasitas

    def __len__(self):
        return self._ukuran

    def kosong(self):
        return self._ukuran == 0

    def is_empty(self):
        return self._ukuran == 0

    def enqueue(self, nilai):
        if self._ukuran == self._kapasitas:
            baru = [None] * (self._kapasitas * 2)
            i = 0
            while i < self._ukuran:
                baru[i] = self._data[(self._depan + i) % self._kapasitas]
                i += 1
            self._data = baru
            self._depan = 0
            self._belakang = self._ukuran
            self._kapasitas *= 2
        self._data[self._belakang] = nilai
        self._belakang = (self._belakang + 1) % self._kapasitas
        self._ukuran += 1

    def dequeue(self):
        if self.kosong():
            raise IndexError("antrean kosong")
        nilai = self._data[self._depan]
        self._data[self._depan] = None
        self._depan = (self._depan + 1) % self._kapasitas
        self._ukuran -= 1
        return nilai

    def peek(self):
        if self.kosong():
            raise IndexError("antrean kosong")
        return self._data[self._depan]

