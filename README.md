```markdown
# Dokumentasi Integrasi Midtrans API - Tugas Sesi 5
**Mata Kuliah:** Arsitektur Berbasis Layanan  
**Topik:** HTTP Header & Method POST (Credit Card Payment)

## 📌 Deskripsi Proyek
Proyek ini adalah implementasi pengiriman data transaksi ke payment gateway **Midtrans (Sandbox)** menggunakan bahasa pemrograman Python dan Docker. Program ini melakukan integrasi API untuk memproses pembayaran kartu kredit dengan mengikuti standar keamanan Midtrans (Tokenization).

## 🛠️ Arsitektur & Teknologi
- **Bahasa:** Python 3.11
- **Library:** `requests` (HTTP Client), `python-dotenv` (Environment Variables)
- **Containerization:** Docker & Docker Compose
- **Gateway:** Midtrans API (Sandbox)

## 📂 Struktur File
```text
.
├── Dockerfile              # Konfigurasi image Python
├── docker-compose.yml      # Konfigurasi orkestrasi container
├── .env                    # Variabel sensitif (Server Key & Client Key)
└── app/
    ├── main.py             # Script utama (Logika bisnis)
    └── requirements.txt    # Dependency Python
```

## 🚀 Alur Kerja Program
Sesuai dengan dokumentasi resmi Midtrans, pengiriman data kartu kredit dilakukan dalam dua tahap untuk menjaga keamanan data (PCI-DSS):
1. **GET Token:** Menukarkan data kartu mentah (*card number, exp, cvv*) menjadi `token_id` melalui endpoint `/v2/token`.
2. **POST Charge:** Mengirimkan `token_id` beserta detail transaksi lainnya ke endpoint `/v2/charge`.

## 📋 Struktur Payload (Sesuai Rubrik)
Berdasarkan rubrik penilaian, data diinputkan dengan urutan sebagai berikut:
1. **transaction_details:** Berisi `order_id` dan `gross_amount`.
2. **credit_card:** Berisi `token_id` yang didapat dari tahap tokenisasi.
3. **item_details:** Daftar barang yang dibeli (ID, harga, jumlah, nama).
4. **customer_details:** Informasi identitas pembeli dan alamat penagihan.

## ⚙️ Cara Menjalankan
1. Pastikan file `.env` sudah terisi dengan `MIDTRANS_SERVER_KEY` dan `MIDTRANS_CLIENT_KEY` yang valid dari dashboard Sandbox.
2. Jalankan perintah Docker:
   ```bash
   docker-compose up --build
   ```
3. Perhatikan log di terminal. Jika berhasil, akan muncul `status_code: 201` dan `status_message: Success`.

## 📊 Hasil Eksekusi (Output)
Program berhasil dijalankan dengan respons sebagai berikut:
- **HTTP Status Code:** 200 OK
- **Midtrans Status Code:** 201 (Created/Success)
- **Transaction Status:** Pending (Menunggu verifikasi 3DS)

---
**Dibuat oleh:** ELFAN PRADITA RUSMIN 20230801068
**Status Tugas:** Selesai
```