# Project UAS Visual 3 - Data Management Application

Repositori ini berisi project akhir (UAS) untuk mata kuliah Visual 3, yang dikembangkan menggunakan Python. Aplikasi ini adalah sistem manajemen data untuk mata kuliah universitas menggunakan PyQt5 untuk antarmuka GUI dan MySQL untuk basis data.

## Fitur

- **CRUD Operations**: Membuat, Membaca, Memperbarui, dan Menghapus data mata kuliah.
- **Fungsi Pencarian**: Mencari mata kuliah berdasarkan ID.
- **UI Responsif**: Menyesuaikan tata letak dan ukuran jendela untuk pengalaman pengguna yang lebih baik.

## Prasyarat

- Python 3.x
- PyQt5
- MySQL Server

## Instalasi

1. **Clone repositori**:
    ```bash
    git clone https://github.com/ayawae123/dbkampus_mariyani2210010095
    cd dbkampus_mariyani2210010095
    ```

2. **Instal paket Python yang dibutuhkan**:
    ```bash
    pip install PyQt5 mysql-connector-python
    ```

3. **Konfigurasi Basis Data**:
    - Pastikan server MySQL berjalan.
    - Buat basis data dengan nama `db_kampus`.
    - Perbarui konfigurasi basis data di `matkul.py` jika diperlukan.

## Penggunaan

1. **Jalankan aplikasi**:
    ```bash
    python matkul.py
    ```

2. **Gunakan antarmuka**:
    - **Insert**: Tambahkan data mata kuliah baru.
    - **Update**: Modifikasi data mata kuliah yang ada.
    - **Delete**: Hapus data mata kuliah.
    - **Search**: Temukan data mata kuliah berdasarkan ID.
    - **Table**: Lihat semua data mata kuliah dalam format tabel.

## Struktur File

- `matkul.py`: File aplikasi utama yang berisi logika antarmuka dan interaksi basis data.

## Berkontribusi

Jika Anda ingin berkontribusi pada proyek ini, silakan fork repositori ini dan ajukan pull request.

## Lisensi

Proyek ini dilisensikan di bawah MIT License.
