import os
import sys
import instaloader
import getpass
from instaloader import Instaloader

def banner():
    print("""
\033[32m██\033[0m╗ \033[32m██████\033[0m╗      \033[32m██████\033[0m╗ \033[32m███████\033[0m╗\033[32m██\033[0m╗\033[32m███\033[0m╗   \033[32m██\033[0m╗\033[32m████████\033[0m╗
\033[32m██\033[0m║\033[32m██\033[0m╔════╝     \033[32m██\033[0m╔═══\033[32m██\033[0m╗\033[32m██\033[0m╔════╝\033[32m██\033[0m║\033[32m████\033[0m╗  \033[32m██\033[0m║╚══\033[32m██\033[0m╔══╝
\033[32m██\033[0m║\033[32m██\033[0m║  \033[32m███\033[0m╗    \033[32m██\033[0m║   \033[32m██\033[0m║\033[32m███████\033[0m╗\033[32m██\033[0m║\033[32m██\033[0m╔\033[32m██\033[0m╗ \033[32m██\033[0m║   \033[32m██\033[0m║
\033[32m██\033[0m║\033[32m██\033[0m║   \033[32m██\033[0m║    \033[32m██\033[0m║   \033[32m██\033[0m║╚════\033[32m██\033[0m║\033[32m██\033[0m║\033[32m██\033[0m║╚\033[32m██\033[0m╗\033[32m██\033[0m║   \033[32m██\033[0m║
\033[32m██\033[0m║╚\033[32m██████\033[0m╔╝    ╚\033[32m██████\033[0m╔╝\033[32m███████\033[0m║\033[32m██\033[0m║\033[32m██\033[0m║ ╚\033[32m████\033[0m║   \033[32m██\033[0m║
\033[0m╚═╝ ╚═════╝      ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝\033[0m\033[41mV2\033[0m
\033[41mCoded By Achik | www.termuxcommands.com\033[0m
""")

def login_instaloader():
    loader = instaloader.Instaloader()
    print("\n\033[36mLogin Required for full access\033[0m")
    username = input("Enter your Instagram login username: ")
    password = getpass.getpass("Enter password: ")
    try:
        loader.login(username, password)
        return loader
    except Exception as e:
        print("Login failed:", e)
        sys.exit()

def profile_information(loader, username):
    try:
        print("\033[33mProfile Information...\033[0m\n")
        profile = instaloader.Profile.from_username(loader.context, username)

        print("\033[32mUsername\033[0m :", profile.username)
        print("\033[32mID\033[0m :", profile.userid)
        print("\033[32mFull Name\033[0m :", profile.full_name)
        print("\033[32mBiography\033[0m :", profile.biography)
        print("\033[32mBusiness Category\033[0m :", profile.business_category_name)
        print("\033[32mExternal URL\033[0m :", profile.external_url)
        print("\033[32mFollowers\033[0m :", profile.followers)
        print("\033[32mFollowees\033[0m :", profile.followees)
        print("\033[32mIs Private\033[0m :", profile.is_private)
        print("\033[32mIs Verified\033[0m :", profile.is_verified)
        print("\033[32mMedia Count\033[0m :", profile.mediacount)
        print("\033[32mProfile Pic URL\033[0m :", profile.profile_pic_url)

    except Exception as e:
        print("Error fetching profile info:", e)

def fetch_post_info(loader, username):
    print("\n\033[33mPost Information...\033[0m\n")
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        posts = profile.get_posts()

        post_info = []
        for i, post in enumerate(posts, start=1):
            caption = post.caption or "No caption"
            date = post.date.strftime("%Y-%m-%d")
            time = post.date.strftime("%I:%M %p")
            post_info.append((f"POST {i}", date, time, caption, post.url))

        return post_info

    except instaloader.exceptions.PrivateProfileNotFollowedException:
        print("This is a private profile. You must follow it to access posts.")
        return []
    except Exception as e:
        print("Error fetching posts:", e)
        return []

def download_posts(loader, username):
    print("\n\033[33mDownloading all posts & profile picture...\033[0m\n")
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        posts = profile.get_posts()

        download_path = os.path.join(os.getcwd(), "IG_OSINT", username)
        os.makedirs(download_path, exist_ok=True)

        # Download profile picture
        loader.download_profile(username, profile_pic_only=True, fast_update=True, filename_target=download_path)

        # Download all posts
        for i, post in enumerate(posts, start=1):
            loader.download_post(post, target=download_path)
            print(f"\033[41mPOST {i}\033[0m downloaded to {download_path}")

    except instaloader.exceptions.PrivateProfileNotFollowedException:
        print("This profile is private. You need to follow it to download posts.")
    except Exception as e:
        print("Download error:", e)

def print_post_info(post_info):
    if post_info:
        for info in post_info:
            print(f"\n\033[41m{info[0]}\033[0m")
            print(f"Posted Date: {info[1]}")
            print(f"Posted Time: {info[2]}")
            print(f"Caption: {info[3]}")
            print(f"Post URL: \033[32m{info[4]}\033[0m")
            print("-" * 50)
    else:
        print("No post info available.")

def options_menu(loader, username):
    while True:
        print("\n\033[1;34mOptions:\033[0m")
        print("\033[1;33m[1]\033[0m \033[1;32mProfile Information\033[0m")
        print("\033[1;33m[2]\033[0m \033[1;32mPost Information\033[0m")
        print("\033[1;33m[3]\033[0m \033[1;32mDownload all Posts & DP\033[0m")
        print("\033[1;33m[4]\033[0m \033[1;32mChange Username\033[0m")
        print("\033[1;33m[5]\033[0m \033[1;32mExit\033[0m")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            profile_information(loader, username)
        elif choice == "2":
            post_info = fetch_post_info(loader, username)
            print_post_info(post_info)
        elif choice == "3":
            download_posts(loader, username)
        elif choice == "4":
            username = input("Enter new Instagram username: ")
        elif choice == "5":
            print("\033[1;31mExiting...\033[0m")
            sys.exit()
        else:
            print("Invalid choice.")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    loader = login_instaloader()
    username = input("\n\033[36mEnter Instagram username to inspect: \033[0m")
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    options_menu(loader, username)

if __name__ == "__main__":
    main()
