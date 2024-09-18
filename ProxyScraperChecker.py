import re
import requests
import time
import os
from datetime import datetime
import random
from bs4 import BeautifulSoup

# ANSI escape kodları
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
PINK = "\033[95m"
PURPLE = "\033[95m"
RESET = "\033[0m"

# Dil seçenekleri ve mesajlar
languages = {
    'en': {
        'choose_language': "Please choose your language:",
        'telegram_question': "Do you want to connect the proxy scraper to Telegram? (Y/N): ",
        'geoip_question': "Do you want to use MaxMind GeoIP to detect proxy locations? (Y/N): ",
        'enter_bot_token': "Please enter your Telegram bot token: ",
        'enter_channel_id': "Please enter your Telegram channel ID: ",
        'proxy_site_question': "Which site should the proxies be checked on? (e.g., https://google.com): ",
        'fetching_proxies': "Fetching proxies...",
        'invalid_proxy_format': "Proxy {} is in an invalid format!",
        'telegram_message_sent': "Message sent to Telegram channel!",
        'telegram_message_failed': "Failed to send message to Telegram!",
        'proxy_check_success': "Proxy {} is working!",
        'proxy_check_fail': "Proxy {} is not working!",
    },
    'tr': {
        'choose_language': "Lütfen dilinizi seçin:",
        'telegram_question': "Proxy scraper'ı Telegram'a bağlamak ister misiniz? (Y/N): ",
        'geoip_question': "Proxy konumlarını tespit etmek için MaxMind GeoIP kullanmak ister misiniz? (Y/N): ",
        'enter_bot_token': "Lütfen Telegram bot token'ınızı girin: ",
        'enter_channel_id': "Lütfen Telegram kanal ID'sini girin: ",
        'proxy_site_question': "Proxyler hangi sitede kontrol edilsin? (örn: https://google.com): ",
        'fetching_proxies': "Proxyler çekiliyor...",
        'invalid_proxy_format': "Proxy {} geçersiz formatta!",
        'telegram_message_sent': "Mesaj Telegram kanalına gönderildi!",
        'telegram_message_failed': "Mesaj gönderilemedi!",
        'proxy_check_success': "Proxy {} çalışıyor!",
        'proxy_check_fail': "Proxy {} çalışmıyor!",
    },
    'jp': {
        'choose_language': "言語を選択してください:",
        'telegram_question': "プロキシスクレーパーをTelegramに接続しますか？ (Y/N): ",
        'geoip_question': "MaxMind GeoIPを使用してプロキシの場所を検出しますか？ (Y/N): ",
        'enter_bot_token': "Telegramボットトークンを入力してください: ",
        'enter_channel_id': "TelegramチャンネルIDを入力してください: ",
        'proxy_site_question': "どのサイトでプロキシをチェックしますか？ (例： https://google.com): ",
        'fetching_proxies': "プロキシを取得しています...",
        'invalid_proxy_format': "プロキシ{}は無効な形式です！",
        'telegram_message_sent': "メッセージがTelegramチャンネルに送信されました！",
        'telegram_message_failed': "メッセージの送信に失敗しました！",
        'proxy_check_success': "プロキシ{}は動作しています！",
        'proxy_check_fail': "プロキシ{}は動作していません！",
    },
    'ar': {
        'choose_language': "يرجى اختيار لغتك:",
        'telegram_question': "هل تريد توصيل كاشف البروكسي بتليجرام؟ (Y/N): ",
        'geoip_question': "هل تريد استخدام MaxMind GeoIP لتحديد مواقع البروكسي؟ (Y/N): ",
        'enter_bot_token': "يرجى إدخال رمز Telegram bot الخاص بك: ",
        'enter_channel_id': "يرجى إدخال معرف قناة Telegram الخاص بك: ",
        'proxy_site_question': "على أي موقع يجب فحص البروكسي؟ (مثال: https://google.com): ",
        'fetching_proxies': "جارٍ جلب البروكسيات...",
        'invalid_proxy_format': "البروكسي {} بتنسيق غير صالح!",
        'telegram_message_sent': "تم إرسال الرسالة إلى قناة تليجرام!",
        'telegram_message_failed': "فشل في إرسال الرسالة إلى تليجرام!",
        'proxy_check_success': "البروكسي {} يعمل!",
        'proxy_check_fail': "البروكسي {} لا يعمل!",
    }
}

# ASCII Art ve Bilgilendirme
def display_startup_message():
    os.system('cls' if os.name == 'nt' else 'clear')  # Ekranı temizle

    print(f"{PURPLE}__   __    _             _            _    {RESET}")
    print(f"{YELLOW}\ \ / /   | |           | |          | |   {RESET}")
    print(f"{PURPLE} \ V /   _| | _____  ___| | ___  __ _| | __{RESET}")
    print(f"{YELLOW}  \ / | | | |/ / __|/ _ \ |/ _ \/ _` | |/ /{RESET}")
    print(f"{PURPLE}  | | |_| |   <\__ \  __/ |  __/ (_| |   < {RESET}")
    print(f"{YELLOW}  \_/\__,_|_|\_\___/\___|_|\___|\__,_|_|\_\{RESET}")

    print(f"{GREEN}Discord : Yukseleak   Telegram Yukseleak BEST PROXYSCRAPER {RESET}")

def choose_language():
    print(f"{YELLOW} Please choose your language: {RESET}")
    print(f"{YELLOW} 1. English{RESET}")
    print(f"{YELLOW} 2.Türkçe {RESET}")
    print(f"{YELLOW}3.日本語 {RESET}")
    print(f"4. {YELLOW}العربية{RESET}")
    while True:
        choice = input("Enter choice (1-4): ")
        if choice == '1':
            return 'en'
        elif choice == '2':
            return 'tr'
        elif choice == '3':
            return 'jp'
        elif choice == '4':
            return 'ar'
        else:
            print("Invalid choice. Please choose a valid option.")

# Proxy kaynaklarını içeren URL'ler
proxy_sources = [
    'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt',
    'https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt',
    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
    'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt',
    'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt',
    'https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt',
    'https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt',
    'https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt',
    'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
    'https://raw.githubusercontent.com/themiralay/Proxy-List-World/master/data.txt',
    'https://raw.githubusercontent.com/r00tee/Proxy-List/main/Https.txt',
    'https://raw.githubusercontent.com/im-razvan/proxy_list/main/http.txt',
    'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt'
]

# Çalışan proxylerin tutulacağı liste
working_proxies = []

# Proxy formatı doğrulama fonksiyonu
def is_valid_proxy_format(proxy):
    host_port_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$')
    auth_host_port_pattern = re.compile(r'^\w+:\w+@\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$')
    return bool(host_port_pattern.match(proxy) or auth_host_port_pattern.match(proxy))

# Proxy'leri kontrol etmek için güncellenmiş fonksiyon
def check_proxy(proxy, check_url):
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}',
    }

    try:
        response = requests.get(check_url, proxies=proxies, timeout=8)
        if response.status_code == 200:
            print(f"{GREEN}{messages['proxy_check_success'].format(proxy)}{RESET}")
            return True
        else:
            print(f"{RED}{messages['proxy_check_fail'].format(proxy)}{RESET}")
            return False
    except requests.exceptions.RequestException:
        print(f"{RED}{messages['proxy_check_fail'].format(proxy)}{RESET}")
        return False

# Proxy kaynaklarından veri çekme fonksiyonu
def fetch_proxies_from_source(url):
    try:
        response = requests.get(url)
        proxies = response.text.splitlines()
        return proxies
    except Exception as e:
        print(f"{RED}{messages['fetching_proxies']} {e}{RESET}")
        return []

# Telegram kanalına mesaj gönderme fonksiyonu
def send_to_telegram(bot_token, channel_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {'chat_id': channel_id, 'text': message}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"{GREEN}{messages['telegram_message_sent']}{RESET}")
        else:
            print(f"{RED}{messages['telegram_message_failed']}{RESET}")
    except Exception as e:
        print(f"{RED}{messages['telegram_message_failed']} {e}{RESET}")

def main():
    # Dil seçimini yap
    lang = choose_language()
    global messages
    messages = languages[lang]

    display_startup_message()

    # Telegram kullanıp kullanmama seçimi
    use_telegram = input(messages['telegram_question']).lower()
    if use_telegram == 'y':
        bot_token = input(messages['enter_bot_token'])
        channel_id = input(messages['enter_channel_id'])
    else:
        bot_token, channel_id = None, None

    # Proxy kontrol edilecek siteyi kullanıcıdan al
    check_url = input(messages['proxy_site_question'])

    print(f"{YELLOW}{messages['fetching_proxies']}{RESET}")

    # Proxy'leri random sırayla çekme ve kontrol etme
    random.shuffle(proxy_sources)
    for source in proxy_sources:
        proxies = fetch_proxies_from_source(source)
        for proxy in proxies:
            if is_valid_proxy_format(proxy) and check_proxy(proxy, check_url):
                working_proxies.append(proxy)

            # Telegram'a mesaj gönderme seçilmişse
            if len(working_proxies) % 300 == 0 and bot_token and channel_id:
                send_to_telegram(bot_token, channel_id, f"300 working proxies found! {datetime.now()}")

# Program başlatılıyor
if __name__ == "__main__":
    main()
