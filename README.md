# Instagram Followers Checker

Cek siapa yang tidak follow balik di Instagram.

## Cara Pakai

```bash
pip install instagrapi
python followers.py
```

Masukkan username & password Instagram.

## Jika Gagal Login

- **Password salah** — cek lagi password kamu
- **Minta kode 2FA** — masukkan kode dari email/telepon
- **Minta verifikasi (challenge)** — buka Instagram di browser, selesaikan challenge, lalu coba lagi
- **Tunggu beberapa menit** — Instagram batasi percobaan login, tunggu 15-30 menit

## Session

Session akan disimpan ke `session.json` setelah login pertama. Next time kamu jalankan, cukup pilih `y` untuk pakai session lama.
