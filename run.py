import os
import sys
import glob
import subprocess


def _runtime_kompatibel():
    try:
        import tkinter
        return sys.version_info >= (3, 11) and (
            sys.platform != "darwin" or tkinter.TkVersion >= 8.6
        )
    except ImportError:
        return False


def _pilih_python(folder_proyek):
    if _runtime_kompatibel():
        return True
    if sys.platform == "darwin":
        kandidat = [os.path.join(folder_proyek, ".venv", "bin", "python3")]
        kandidat += sorted(glob.glob(
            "/Library/Frameworks/Python.framework/Versions/3.*/bin/python3"
        ), reverse=True)
        kandidat += ["/opt/homebrew/bin/python3", "/usr/local/bin/python3"]
        probe = (
            "import sys, tkinter; sys.exit(0 if "
            "sys.version_info >= (3, 11) and tkinter.TkVersion >= 8.6 else 1)"
        )
        for python in kandidat:
            if not os.path.isfile(python):
                continue
            if os.path.realpath(python) == os.path.realpath(sys.executable):
                continue
            try:
                hasil = subprocess.run([python, "-c", probe],
                                       capture_output=True, timeout=10)
            except (OSError, subprocess.TimeoutExpired):
                continue
            if hasil.returncode == 0:
                print("Menjalankan dengan Python kompatibel: " + python, flush=True)
                os.execv(python, [python, os.path.join(folder_proyek, "run.py")] + sys.argv[1:])
    print("ERROR: aplikasi membutuhkan Python 3.11+ dengan Tk 8.6+ di macOS.")
    print("Python aktif: " + sys.executable)
    print("Instal Python dari https://www.python.org/downloads/macos/ lalu jalankan kembali run.py.")
    return False


def main():
    folder_proyek = os.path.dirname(os.path.abspath(__file__))
    if folder_proyek not in sys.path:
        sys.path.insert(0, folder_proyek)

    if not _pilih_python(folder_proyek):
        return 1

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
