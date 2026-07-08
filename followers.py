import sys
import os
import json
import time
from instagrapi import Client
from instagrapi.exceptions import (
    BadPassword,
    ChallengeRequired,
    PleaseWaitFewMinutes,
    TwoFactorRequired,
    FeedbackRequired,
    LoginRequired,
    SentryBlock,
    AccountContactPointRequired,
    ReloginAttemptExceeded,
)


def login_with_credentials(cl):
    username = input(">> Username Instagram: ").strip()
    password = input(">> Password Instagram: ").strip()
    if not username or not password:
        print("[!] Username dan password wajib diisi.")
        return None

    print("\n[*] Sedang login...")
    try:
        cl.login(username, password)
        cl.dump_settings("session.json")
        print("[*] Login berhasil, session tersimpan.\n")
        return cl.user_id
    except BadPassword:
        print("[!] Password salah.")
        print("    Tapi bisa juga Instagram blokir login dari aplikasi tidak resmi.")
        print("    Coba login di browser dulu, lalu ambil sessionid untuk login via session.")
    except TwoFactorRequired:
        code = input(">> Kode 2FA dari email/telepon: ").strip()
        cl.login(username, password, verification_code=code)
        cl.dump_settings("session.json")
        return cl.user_id
    except ChallengeRequired:
        print("[!] Instagram minta verifikasi (challenge).")
        print("    Buka Instagram di browser, selesaikan challenge, lalu coba lagi.")
    except FeedbackRequired:
        msg = cl.last_json.get("feedback_message", cl.last_json.get("message", ""))
        print(f"[!] Instagram minta konfirmasi: {msg}")
        print("    Buka Instagram di browser dan selesaikan.")
    except PleaseWaitFewMinutes:
        print("[!] Harap tunggu beberapa menit sebelum coba lagi.")
    except SentryBlock:
        print("[!] Login diblokir Instagram. Coba pakai VPN atau koneksi lain.")
    except AccountContactPointRequired:
        print("[!] Instagram minta verifikasi nomor telepon/email.")
        print("    Buka Instagram di browser dan selesaikan.")
    except ReloginAttemptExceeded:
        print("[!] Terlalu banyak percobaan login. Tunggu beberapa saat.")
    except Exception as e:
        last_json = getattr(cl, "last_json", {})
        msg = last_json.get("message", str(e))
        print(f"[!] Gagal login: {msg}")
        if "challenge" in str(last_json).lower():
            print("    Kemungkinan Instagram minta challenge. Selesaikan di browser.")
    return None


def login_with_session_from_file(cl):
    with open("session.json") as f:
        data = json.load(f)
    sessionid = data["cookies"]["sessionid"]
    cl.login_by_sessionid(sessionid)
    return cl.user_id


def main():
    print("=" * 60)
    print("   INSTAGRAM FOLLOWERS CHECKER")
    print("=" * 60)

    cl = Client()
    cl.delay_range = [2, 5]
    cl.set_user_agent()
    cl.set_device()

    if os.path.exists("session.json"):
        load = input("\n>> Pakai session tersimpan? (y/n): ").strip().lower()
        if load == "y":
            try:
                user_id = login_with_session_from_file(cl)
                print("[*] Login dengan session tersimpan berhasil!\n")
            except Exception as e:
                print(f"[!] Session expired: {e}")
                os.remove("session.json")
                return
        else:
            os.remove("session.json")
            user_id = login_with_credentials(cl)
            if user_id is None:
                return
    else:
        user_id = login_with_credentials(cl)
        if user_id is None:
            return

    max_input = input("Jumlah maksimal yang dicek (kosongkan untuk semua): ").strip()
    max_count = int(max_input) if max_input.isdigit() else 0

    print("\n[*] Mengambil daftar following...")
    following = cl.user_following(user_id, amount=max_count)
    print(f"    -> {len(following)} following")
    following_map = {str(pk): info.username for pk, info in following.items()}

    print("[*] Mengambil daftar followers...")
    followers = cl.user_followers(user_id, amount=max_count)
    print(f"    -> {len(followers)} followers")
    follower_map = {str(pk): info.username for pk, info in followers.items()}

    not_follow_back = [(pk, uname) for pk, uname in following_map.items() if pk not in follower_map]
    not_followed_by_me = [(pk, uname) for pk, uname in follower_map.items() if pk not in following_map]

    mutual = len(following_map) - len(not_follow_back)

    print("\n" + "=" * 60)
    print("   HASIL ANALISIS FOLLOWERS")
    print("=" * 60)
    print(f"\n>> Statistik:")
    print(f"   Following            : {len(following_map)}")
    print(f"   Followers            : {len(follower_map)}")
    print(f"   Mutual               : {mutual}")
    print(f"   Tidak follow balik   : {len(not_follow_back)}")
    print(f"   Tidak kamu follow    : {len(not_followed_by_me)}")

    if not_follow_back:
        print(f"\n[X] TIDAK FOLLOW BALIK ({len(not_follow_back)}):")
        for i, (_, uname) in enumerate(not_follow_back, 1):
            print(f"   {i:3d}. @{uname}")

    if not_followed_by_me:
        print(f"\n[!] KAMU TIDAK FOLLOW MEREKA ({len(not_followed_by_me)}):")
        for i, (_, uname) in enumerate(not_followed_by_me, 1):
            print(f"   {i:3d}. @{uname}")

    if not_follow_back:
        print("\n" + "=" * 60)
        print("   UNFOLLOW OTOMATIS")
        print("=" * 60)
        q = input("\n>> Mau unfollow yang tidak follow balik? (y/n): ").strip().lower()
        if q == "y":
            print("\n[*] Ketik nomor yang ingin DIKECUALIKAN (dipisah koma).")
            print("    Contoh: 1,5,10,23")
            print("    Enter langsung = unfollow semua.\n")
            skip_input = input(">> Nomor yang dilewati: ").strip()
            skip_set = set()
            if skip_input:
                for part in skip_input.split(","):
                    part = part.strip()
                    if part.isdigit():
                        idx = int(part)
                        if 1 <= idx <= len(not_follow_back):
                            skip_set.add(idx)

            print(f"\n[*] Mulai unfollow {len(not_follow_back) - len(skip_set)} akun...\n")
            for i, (pk, uname) in enumerate(not_follow_back, 1):
                if i in skip_set:
                    print(f"   [-] {i}. @{uname} dilewati")
                    continue
                try:
                    cl.user_unfollow(int(pk))
                    print(f"   [{i}] @{uname} berhasil diunfollow")
                    time.sleep(10)
                except Exception as e:
                    print(f"   [!] Gagal unfollow @{uname}: {e}")
                    time.sleep(30)
            print("\n[*] Selesai!")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Dibatalkan oleh user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        sys.exit(1)
