Deskripsi Aplikasi:
Aplikasi ini adalah sistem manajemen untuk mengelola produk dan transaksi di toko mamat. Aplikasi ini dibangun menggunakan Python dengan framework Tkinter untuk tampilan antarmuka pengguna dan MySQL untuk penyimpanan data. Fungsionalitas aplikasi meliputi dua tab utama:
1. Manajemen Produk: Memungkinkan pengguna untuk menambah, memperbarui, dan menghapus produk. Pengguna dapat menginput nama dan harga produk, serta melihat daftar produk dalam tabel.
2. Transaksi: Pengguna dapat melakukan transaksi dengan memilih produk dan memasukkan jumlah yang dibeli. Transaksi akan disimpan dalam tabel transaksi dengan harga total dan tanggal transaksi.
Aplikasi ini juga melakukan validasi input untuk memastikan data yang dimasukkan valid, serta menampilkan notifikasi melalui message box jika ada kesalahan.

Cara Menjalankan Aplikasi:
Persiapkan Database:
Pastikan MySQL sudah terinstal di sistem.
Buat database toko_mamat dengan dua tabel: product dan transaction.
Struktur tabel adalah sebagai berikut:
1. 1Tabel product:
id_product (INT, PRIMARY KEY, AUTO_INCREMENT)
name_product (VARCHAR)
price_product (FLOAT)
2. Tabel transaction:
id_transaction (INT, PRIMARY KEY, AUTO_INCREMENT)
id_product (INT, FOREIGN KEY ke product.id_product)
total_product (INT)
total_price (FLOAT)
transaction_date (DATE)
Instalasi Library:

Instal library yang diperlukan dengan perintah berikut:
pip install mysql-connector-python

Cara menjalankan aplikasi:
1. Menajemen produk
a. Untuk menambahkan produk, masukkan nama produk dan harga nya pada messagebox kemudian click button tambah produk
b. Untuk mengupdate produk, double click data yang ingin di update kemudian ubah nama atau harga produk kemudian click button update produk maka produk akan terupdate
c. Untuk Menghapus produk, click data yang ingin di hapus, kemudian click button hapus produk
2. Transaksi Produk
a. Pilih produk melalui dropdown nama produk kemudian click masukkan jumlah yang ingin dibeli, dan kemudian click button tambah transasksi dan transaksi berhasil di tambahkan
b. untuk produk yang di update atau baru ditambahkan pada menajemen produk, akan dimuat ketika user keluar dari program kemudian masuk lagi maka barang yang baru ditambah, edit, atau hapus akan diperbarui pada dropdown nama produk


Struktur Tabel Database:
1. Tabel product:
CREATE TABLE product (
    id_product INT AUTO_INCREMENT PRIMARY KEY,
    name_product VARCHAR(255) NOT NULL,
    price_product FLOAT NOT NULL
);
2. Tabel transaction:
CREATE TABLE transaction (
    id_transaction INT AUTO_INCREMENT PRIMARY KEY,
    id_product INT,
    total_product INT NOT NULL,
    total_price FLOAT NOT NULL,
    transaction_date DATE NOT NULL,
    FOREIGN KEY (id_product) REFERENCES product(id_product)
);
