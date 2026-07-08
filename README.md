# Instagram Followers Checker

Tools Python untuk cek siapa aja yang **tidak follow balik** di Instagram.

## Fitur

- Login via **sessionid** (cookie) — lebih aman, tanpa password
- Login via **username & password** (dengan dukungan 2FA)
- Session tersimpan otomatis untuk penggunaan selanjutnya
- Lihat daftar yang **tidak follow balik**
- Lihat daftar yang **kamu tidak follow**
- **Unfollow otomatis** — pilih manual akun yang mau dikecualikan
- Batas jumlah cek bisa diatur

## Persiapan

```bash
pip install instagrapi
```

Disarankan pakai virtual environment:

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # Linux/Mac
pip install instagrapi
```

## Cara Pakai

### 1. Login via Session (Rekomendasi)

Ambil `sessionid` dari cookie Instagram di browser:
1. Buka [instagram.com](https://instagram.com) dan login
2. Buka Developer Tools (`F12`) → **Application** → **Cookies** → `instagram.com`
3. Cari cookie bernama `sessionid`, salin value-nya
4. Buka `session.json` dan tempel:

```json
{"cookies": {"sessionid": "sessionid-kamu-disini"}}
```

Jalankan:

```bash
python followers.py
```

Pilih `y` saat ditanya "Pakai session tersimpan?"

### 2. Login via Username & Password

```bash
python followers.py
```

Masukkan username dan password saat diminta. Session akan otomatis tersimpan ke `session.json` untuk dipakai nanti.

> **Catatan:** Login via password rawan kena blokir/challenge oleh Instagram. Metode session lebih direkomendasikan.

## Struktur File

```
followers/
├── followers.py       # Script utama
├── session.json       # Session (ada di .gitignore, aman)
├── .gitignore         # File yang diabaikan git
└── README.md          # Dokumentasi ini
```

## Troubleshooting

| Masalah | Solusi |
|---|---|
| `sessionid` tidak valid / expired | Ambil ulang `sessionid` dari browser |
| Kena `FeedbackRequired` | Buka Instagram di browser, selesaikan konfirmasi |
| Kena `ChallengeRequired` | Buka Instagram di browser, selesaikan challenge |
| Kena `PleaseWaitFewMinutes` | Tunggu 15-30 menit sebelum coba lagi |
| Kena `SentryBlock` | Coba ganti IP (VPN/koneksi lain) |

## Disclaimer

Tools ini menggunakan [instagrapi](https://github.com/adw0rd/instagrapi) (unofficial Instagram API). Gunakan dengan bijak. Instagram bisa membatasi atau memblokir akun jika mendeteksi aktivitas mencurigakan.

## Lisensi

MIT
