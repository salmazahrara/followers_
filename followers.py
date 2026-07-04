import sys
import os
from instagrapi import Client
from instagrapi.exceptions import BadPassword, ChallengeRequired, PleaseWaitFewMinutes, TwoFactorRequired


def main():
    print("=" * 60)
    print("   INSTAGRAM FOLLOWERS CHECKER")
    print("=" * 60)

    # Cek session tersimpan
    cl = Client()
    cl.delay_range = [2, 5]

    if os.path.exists("session.json"):
        load = input("\n>> Pakai session tersimpan? (y/n): ").strip().lower()
        if load == "y":
            try:
                cl.load_settings("session.json")
                cl.login_by_sessionid(cl.get_settings()["cookies"]["sessionid"])
                print("[*] Login dengan session tersimpan berhasil!\n")
                user_id = cl.user_id
            except Exception as e:
                print(f"[!] Session expired: {e}")
                os.remove("session.json")
                return
        else:
            os.remove("session.json")
            username = input(">> Username Instagram: ").strip()
            password = input(">> Password Instagram: ").strip()
            if not username or not password:
                print("[!] Username dan password wajib diisi.")
                return
            print("\n[*] Sedang login...")
            try:
                cl.login(username, password)
                cl.dump_settings("session.json")
                print("[*] Session tersimpan.\n")
                user_id = cl.user_id
            except BadPassword:
                print("[!] Password salah.")
                return
            except TwoFactorRequired:
                code = input(">> Kode 2FA dari email/telepon: ").strip()
                cl.login(username, password, verification_code=code)
                cl.dump_settings("session.json")
                user_id = cl.user_id
            except ChallengeRequired:
                print("[!] Instagram minta verifikasi. Coba buka Instagram di browser dan selesaikan challenge.")
                return
            except PleaseWaitFewMinutes:
                print("[!] Harap tunggu beberapa menit sebelum coba lagi.")
                return
            except Exception as e:
                print(f"[!] Gagal login: {e}")
                return
    else:
        username = input(">> Username Instagram: ").strip()
        password = input(">> Password Instagram: ").strip()
        if not username or not password:
            print("[!] Username dan password wajib diisi.")
            return
        print("\n[*] Sedang login...")
        try:
            cl.login(username, password)
            cl.dump_settings("session.json")
            print("[*] Session tersimpan.\n")
            user_id = cl.user_id
        except BadPassword:
            print("[!] Password salah.")
            return
        except TwoFactorRequired:
            code = input(">> Kode 2FA dari email/telepon: ").strip()
            cl.login(username, password, verification_code=code)
            cl.dump_settings("session.json")
            user_id = cl.user_id
        except ChallengeRequired:
            print("[!] Instagram minta verifikasi. Coba buka Instagram di browser dan selesaikan challenge.")
            return
        except PleaseWaitFewMinutes:
            print("[!] Harap tunggu beberapa menit sebelum coba lagi.")
            return
        except Exception as e:
            print(f"[!] Gagal login: {e}")
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
