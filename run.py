import os
import sys


def main():
    folder_proyek = os.path.dirname(os.path.abspath(__file__))
    if folder_proyek not in sys.path:
        sys.path.insert(0, folder_proyek)

    file_data = os.path.join(folder_proyek, "data", "pesanan.csv")
    if not os.path.isfile(file_data):
        print("ERROR: data/pesanan.csv tidak ditemukan.")
        print("Pastikan file run.py berada di folder utama proyek 2EZ4U APP.")
        return 1

    try:
        from app import main as jalankan_aplikasi
        jalankan_aplikasi()
    except ImportError as error:
        print("ERROR: modul aplikasi tidak dapat dimuat: " + str(error))
        print("Pastikan menggunakan Python 3.11 atau lebih baru.")
        return 1
    except KeyboardInterrupt:
        print("Aplikasi dihentikan.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
