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
