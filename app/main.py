import os
import requests
import base64
import time
from dotenv import load_dotenv

load_dotenv()

SERVER_KEY = os.getenv("MIDTRANS_SERVER_KEY")
CLIENT_KEY = os.getenv("MIDTRANS_CLIENT_KEY") 
CHARGE_URL = os.getenv("MIDTRANS_CHARGE_URL")
TOKEN_URL = os.getenv("MIDTRANS_TOKEN_URL")

# =================================================================
# TAHAP 1: MENDAPATKAN TOKEN ID (GET Request)
# Menukar data kartu mentah menjadi token_id (Aturan Midtrans API)
# =================================================================
print("[INFO] Requesting token_id dari Midtrans...")
token_params = {
    "client_key": CLIENT_KEY,
    "card_number": "4811111111111114",
    "card_exp_month": "12",
    "card_exp_year": "2030",
    "card_cvv": "123"
}

try:
    token_response = requests.get(TOKEN_URL, params=token_params)
    token_data = token_response.json()

    # Perbaikan: Cek status_code dari DALAM JSON response Midtrans
    if token_data.get("status_code") != "200":
        print("[ERROR] Gagal mendapatkan token_id!")
        print("[DETAIL ERROR MIDTRANS]:", token_data) # Ini akan menampilkan alasan aslinya
        exit() # Hentikan program jika token gagal didapat

    token_id = token_data.get("token_id")
    print(f"[SUCCESS] Berhasil mendapatkan token_id: {token_id}\n")

except Exception as e:
    print("[ERROR] Terjadi kesalahan saat request token:", str(e))
    exit()

# =================================================================
# TAHAP 2: CHARGE TRANSACTION (POST Request)
# Mengirimkan payload sesuai urutan rubrik tugas
# =================================================================
encoded_key = base64.b64encode((SERVER_KEY + ":").encode()).decode()

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Basic {encoded_key}"
}

# Membuat Order ID yang dinamis agar tidak error duplicate order id
order_id = f"ORDER-{int(time.time())}"

payload = {
    "payment_type": "credit_card",

    # 1. data transaction details
    "transaction_details": {
        "order_id": order_id,
        "gross_amount": 150000
    },

    # 2. data credit card (MENGGUNAKAN TOKEN_ID)
    "credit_card": {
        "token_id": token_id,
        "authentication": True
    },

    # 3. data item details
    "item_details": [
        {
            "id": "item1",
            "price": 50000,
            "quantity": 1,
            "name": "Produk A"
        },
        {
            "id": "item2",
            "price": 100000,
            "quantity": 1,
            "name": "Produk B"
        }
    ],

    # 4. data customer detail
    "customer_details": {
        "first_name": "Elfan",
        "last_name": "Pradita",
        "email": "elfan@email.com",
        "phone": "08123456789",
        "billing_address": {
            "address": "Jl. Contoh No.1",
            "city": "Jakarta",
            "postal_code": "12345",
            "country_code": "IDN"
        }
    }
}

try:
    print(f"[INFO] Mengirim data transaksi untuk Order ID: {order_id} (POST Charge)...")
    response = requests.post(CHARGE_URL, json=payload, headers=headers)

    print("\nStatus Code:", response.status_code)
    print("Response JSON:")
    print(response.json())

except Exception as e:
    print("Error:", str(e))