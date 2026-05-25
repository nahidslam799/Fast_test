import os
import pickle
import sys
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import phonenumbers
from phonenumbers import geocoder, region_code_for_number
import json
from collections import deque

import uuid
import sys
import platform
import hashlib
NSTEAM = "https://opensheet.elk.sh/1NIZJbaTIOojml2T0xkuDhYVU8rpptKoRY2M2_EmN6qQ/BOTACC"

def get_device_id():
    raw = (
        platform.system() +
        platform.node() +
        platform.machine()
    )
    return hashlib.md5(raw.encode()).hexdigest()

def check_license():
    device_id = get_device_id()

    try:
        res = requests.get(NSTEAM)
        data = res.json()

        for row in data:
            if row.get("device_id") == device_id:
                if row.get("status") == "active":
                    return True
                else:
                    print("❌ License inactive!")
                    return False

        print("❌ Device not registered!")
        print(f"👉 Your Device ID: {device_id}")
        print("📞 Contact admin to activate")
        return False

    except Exception as e:
        print("⚠️ Error:", e)
        return False

if not check_license():
    sys.exit()

# --- Configuration ---
# ===== USER CONFIG =====

print("\n========== BOT SETUP ==========\n")

BOT_TOKEN = input("Enter Bot Token: ").strip()

if not BOT_TOKEN:
    print("❌ Bot Token Required!")
    sys.exit()

chat_input = input("Enter Chat ID (comma separated): ").strip()

if not chat_input:
    print("❌ Chat ID Required!")
    sys.exit()

CHAT_IDS = [x.strip() for x in chat_input.split(",")]

CHANNEL_URL = input("Enter Telegram Channel URL: ").strip()

if not CHANNEL_URL:
    print("❌ Channel URL Required!")
    sys.exit()

NUMBER_BOT_URL = input("Enter Number Bot URL: ").strip()

if not NUMBER_BOT_URL:
    print("❌ Number Bot URL Required!")
    sys.exit()

BASE_URL = input("Enter Website URL: ").strip()

if not BASE_URL:
    print("❌ Website URL Required!")
    sys.exit()

template_path = input(
    "Enter TXT Template Path (optional): "
).strip()

CUSTOM_TEMPLATE = None

if template_path:
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            CUSTOM_TEMPLATE = f.read()

        print("[✅] Custom template loaded")

    except Exception as e:
        print(f"[❌] Failed to load template: {e}")
        print("[⚠️] Using default template")
        
LOGIN_URL = f"{BASE_URL}/login"
SMS_URL = f"{BASE_URL}/client/SMSCDRStats"

SERVICE_EMOJIS = {
    "FB": "5323261730283863478", "FACEBOOK": "5323261730283863478",
    "INSTAGRAM": "5319160079465857105", "IG": "5319160079465857105",
    "MESSENGER": "5323687726615119535",
    "TG": "5330237710655306682", "TELEGRAM": "5330237710655306682",
    "WA": "5334998226636390258", "WHATSAPP": "5334998226636390258",
    "SNAPCHAT": "5330248916224983855",
    "DISCORD": "5325612636467903082",
    "LINE": "5323608076446613036",
    "STEAM": "5373144051690258848", "STREAM": "5373144051690258848",
    "GOOGLE": "5337276985959784779",
    "YOUTUBE": "5334681713316479679",
    "TIKTOK": "5327982530702359565",
    "NETFLIX": "5318911503938634641",
    "CHATGPT": "5359726582447487916", "OPENAI": "5359726582447487916",
    "TWITTER": "5330337435500951363", "X": "5330337435500951363",
    "BIGO": "5334954057192719331",
    "MICROSOFT": "5370857634440170316",
    "DEFAULT": "5372878077250519677"
}

PREMIUM_EMOJIS = {
    "Afghanistan": "5222096009009575868", "Albania": "5224312057515486246", "Algeria": "5224260376174015500",
    "Andorra": "5221987861733061751", "Angola": "5224379767674907895", "Argentina": "5221980461504411710",
    "Armenia": "5224369957969603463", "Australia": "5224659803837574114", "Austria": "5224520754271366661",
    "Azerbaijan": "5224426544163728284", "Bahamas": "5224504167107668172", "Bahrain": "5224492892818518587",
    "Bangladesh": "5224407289825340729", "Barbados": "5222156533688712094", "Belarus": "5222398507851199882",
    "Belgium": "5224513182244024630", "Belize": "5224316292353241916", "Benin": "5222024115552009151",
    "Bhutan": "5224541065171710147", "Bolivia": "5224675484763170798", "Bosnia and Herzegovina": "5224496092569155254",
    "Botswana": "5224288456670196085", "Brazil": "5224688610183228070", "Brunei": "5224435958732042406",
    "Bulgaria": "5222092074819530668", "Burkina Faso": "5222356541725749790", "Burundi": "5224490444687158452",
    "Cambodia": "5224189882875785448", "Cameroon": "5222270788408717651", "Canada": "5222001124592071204",
    "Cape Verde": "5222347737042792258", "Central African Republic": "5222073662294733523", "Chad": "5222060468155204001",
    "Chile": "5222350726340032308", "China": "5224435456220868088", "Colombia": "5224455152940886669",
    "Comoros": "5222398735484466247", "DR Congo": "5224398158724871677", "Republic of the Congo": "5222104268231684600",
    "Costa Rica": "5222453801260168022", "Croatia": "5221967765581085099", "Cuba": "5357035553508308603",
    "Cyprus": "5222431454545327055", "Czech Republic": "5222073533445714675", "Denmark": "5222297215342490217",
    "Djibouti": "5224203012590810589", "Dominica": "5222337489250824921", "Dominican Republic": "5224286412265763450",
    "Ecuador": "5224191188545840926", "Egypt": "5222161185138292290", "El Salvador": "5224337131534559907",
    "Equatorial Guinea": "5222172811614762423", "Eritrea": "5420548035232937623", "Estonia": "5222195463272281351",
    "Eswatini": "5224269666188274723", "Ethiopia": "5224467805914542024", "Fiji": "5221962676044838178",
    "Finland": "5224282903277482188", "France": "5222029789203804982", "Gabon": "5224669733801963467",
    "Gambia": "5221949872747330159", "Georgia": "5222152195771742239", "Germany": "5222165617544542414",
    "Ghana": "5224511339703056124", "Greece": "5222463490706389920", "Grenada": "5222234560359577687",
    "Guatemala": "5222128302868672826", "Guinea": "5222337588035073000", "Guinea-Bissau": "5224705704153066489",
    "Guyana": "5224570532942329532", "Haiti": "5224683146984831315", "Honduras": "5222229234600130045",
    "Hungary": "5224691998912427164", "Iceland": "5222063229819172521", "India": "5222300011366200403",
    "Indonesia": "5224405893960969756", "Iran": "5224374154152653367", "Iraq": "5221980268230882832",
    "Ireland": "5222233374948602940", "Israel": "5371035398841571673", "Italy": "5222460101977190141",
    "Jamaica": "5222007034467074185", "Japan": "5222390089715299207", "Jordan": "5222292177345853436",
    "Kazakhstan": "5222276376161171525", "Kenya": "5222279743415531561", "Kiribati": "5224652244695134610",
    "North Korea": "5341271404329317987", "South Korea": "5222345550904439270", "Kuwait": "5221949726718442491",
    "Kyrgyzstan": "5224388147156102493", "Laos": "5224200843632324642", "Latvia": "5224401229626484931",
    "Lebanon": "5222244425899455269", "Lesotho": "5224245850594619415", "Liberia": "5221998371518034740",
    "Libya": "5222194286451242896", "Liechtenstein": "5226703795953612903", "Lithuania": "5224245902134226386",
    "Luxembourg": "5224499567197700690", "Madagascar": "5222042605386217334", "Malawi": "5341341330691863561",
    "Malaysia": "5224312886444174057", "Maldives": "5224393700548814960", "Mali": "5224322352552096671",
    "Malta": "5224731388057497620", "Marshall Islands": "5224538449536624503", "Mauritania": "5422465115360345921",
    "Mauritius": "5224238347286752315", "Mexico": "5221971386238514431", "Micronesia": "5222280486444873367",
    "Moldova": "5224216473018314447", "Monaco": "5221937224068640464", "Mongolia": "5224192257992701543",
    "Montenegro": "5224463399278096980", "Morocco": "5224530035695693965", "Mozambique": "5222470388423864826",
    "Myanmar": "5188162778073935826", "Namibia": "5224690826386351746", "Nauru": "5233464284930915439",
    "Nepal": "5222444378101925267", "Netherlands": "5224516489368841614", "New Zealand": "5224573595254009705",
    "Nicaragua": "5426842228200847679", "Niger": "5222099049846420864", "Nigeria": "5224723614166691638",
    "North Macedonia": "5222470435668505656", "Norway": "5224465228934163949", "Oman": "5222396686785066306",
    "Pakistan": "5224637061985742245", "Palau": "5222244507503833341", "Panama": "5222111719999945107",
    "Papua Guina": "5224500164198149905", "Paraguay": "5222152565138929235", "Peru": "5224482026551258766",
    "Philippines": "5222065042295376892", "Poland": "5224670399521892983", "Portugal": "5224404094369672274",
    "Qatar": "5222225596762830469", "Romania": "5222273794885826118", "Russia": "5449408995691341691",
    "Rwanda": "5222449197055227754", "Saint Kitts and Nevis": "5231087492978982103", "Saint Lucia": "5222000927023577045",
    "Saint Vincent and the Grenadines": "5224541228380467535", "Samoa": "5224660353593387686", "San Marino": "5228954998766843234",
    "Sao Tome and Principe": "5221953304426198315", "Saudi Arabia": "5224698145010624573", "Senegal": "5224358988623130949",
    "Serbia": "5222145396838512729", "Seychelles": "5224467496676896871", "Sierra Leone": "5224420995065983217",
    "Singapore": "5224194023224257181", "Slovakia": "5222401879400528047", "Slovenia": "5224660718665607511",
    "Solomon Islands": "5222290588207954120", "Somalia": "5222370504664428325", "South Africa": "5224696216570309138",
    "South Sudan": "5224618146949773268", "Spain": "5222024776976970940", "Sri Lanka": "5224277294050192388",
    "Sudan": "5224372990216514135", "Suriname": "5224567367551428669", "Sweden": "5222201098269373561",
    "Switzerland": "5224707263226194753", "Syria": "5308002793812955097", "Tajikistan": "5222217865821696536",
    "Tanzania": "5224397364155923150", "Thailand": "5224638530864556281", "Timor-Leste": "5224515905253291409",
    "Togo": "5222408051268532030", "Tonga": "5467490150877508877", "Trinidad and Tobago": "5224391883777651050",
    "Tunisia": "5221991375016310330", "Turkey": "5224601903383457698", "Turkmenistan": "5224256935905208951",
    "Tuvalu": "5454304115947487098", "Uganda": "5222464040462200940", "Ukraine": "5222250679371839695",
    "UAE": "5224565851427976312", "United Kingdom": "5224518800061245598", "United States": "5224321781321442532",
    "Uruguay": "5222466849370813232", "Uzbekistan": "5222404546575219535", "Vanuatu": "5222126748090512778",
    "Vatican City": "5222420266155520507", "Venezuela": "5228751795274136090", "Vietnam": "5222359651282071925",
    "Yemen": "5222300655611294950", "Zambia": "5224646626877911277", "Zimbabwe": "5222060442385397848",
    "Palestine": "5222370620628546719", 
    "DEFAULT": "6188045471118790922"
}


processed_messages = deque(maxlen=500)

# --- Helper Functions ---
def get_country_flag(country_code):

    if not country_code or len(country_code) != 2:
        return "🌐"
    return "".join(chr(ord(c) + 127397) for c in country_code.upper())

def save_cookies(driver):
    """
    Selenium WebDriver থেকে কুকিজ সেভ করে।
    n
    
    
    SVRYSDRSQlV-
    boRyRXZyU4KTc3xWZ3WCQ09hzbsjbHhH1XIBmj3Via1aC
    R1N3SU5PSDRSQnJVaXhmSHeMiEGHlItBVId7i19YZVVU
    mFVpbmdheIKD
    
    
   
    """
    try:
        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
        print("[🍪] কুকিজ সেভ করা হয়েছে")
    except Exception as e:
        print(f"[❌] কুকিজ সেভ করতে ব্যর্থ: {e}")

def load_cookies(driver):
    """
    সেভ করা কুকিজ লোড করে এবং WebDriver এ যোগ করে।
    """
    if not os.path.exists("cookies.pkl"):
        return False
    try:
        driver.get(LOGIN_URL) # কুকিজ যোগ করার আগে একই ডোমেইনে থাকতে হবে
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            # ডোমেন চেক করে কুকি যোগ করা
            if 'domain' in cookie and driver.current_url.split('/')[2] in cookie['domain']:
                driver.add_cookie(cookie)
            elif 'domain' not in cookie: # ডোমেন না থাকলে যোগ করার চেষ্টা করুন
                 driver.add_cookie(cookie)
        driver.refresh()
        time.sleep(5) # কুকিজ লোড হওয়ার জন্য অপেক্ষা
        print("[🍪] কুকিজ লোড করা হয়েছে")
        return True
    except Exception as e:
        print(f"[❌] কুকিজ লোড করতে ব্যর্থ: {e}")
        return False

def send_to_telegram(text: str, otp_code: str = None):
    """
    টেলিগ্রাম API ব্যবহার করে বার্তা পাঠায়, সাথে ইনলাইন কিবোর্ড বাটন।
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    payload_template = {
        "text": text,
        "parse_mode": "HTML",
    }
    
    all_sent = True
    for chat_id in CHAT_IDS:
        inline_keyboard_buttons = []
        
        if otp_code and otp_code != "N/A":
            inline_keyboard_buttons.append([
                {"text": f" {otp_code}", "copy_text": {"text": otp_code}, "style": "success", "icon_custom_emoji_id": "5449419131973682976"}
            ])

        inline_keyboard_buttons.append([
            {"text": "Channel", "url": CHANNEL_URL, "style": "primary", "icon_custom_emoji_id": "5316594137154200720"},
            {"text": "NUMBER BOT", "url": NUMBER_BOT_URL, "style": "primary", "icon_custom_emoji_id": "5323523560080158541"}
        ])

        keyboard = {"inline_keyboard": inline_keyboard_buttons}
        
        payload = payload_template.copy()
        payload["chat_id"] = chat_id
        payload["reply_markup"] = json.dumps(keyboard)
        
        try:
            res = requests.post(url, data=payload, timeout=10)
            if res.status_code == 200:
                print(f"[✅] বার্তা {chat_id} তে পাঠানো হয়েছে")
            else:
                print(f"[❌] টেলিগ্রামে বার্তা {chat_id} তে পাঠাতে ব্যর্থ: {res.status_code} - {res.text}")
                all_sent = False
        except Exception as e:
            print(f"[❌] টেলিগ্রামে বার্তা {chat_id} তে পাঠাতে ব্যর্থ: {e}")
            all_sent = False
    return all_sent

def format_phone_number(number):
    """
    ফোন নম্বরের মাঝের অংশ গোপন করে ফরম্যাট করে।
    """
    if len(number) >= 6:
        return number[:3] + '★★★' + number[-4:]
    return number

def escape_markdown_v2(text):
    """
    MarkdownV2-এর জন্য বিশেষ ক্যারেক্টারগুলো এস্কেপ করে।
    
    
    
    
    
    """
    # টেলিগ্রাম MarkdownV2 দ্বারা ব্যবহৃত বিশেষ ক্যারেক্টারগুলি
    chars_to_escape = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    escaped_text = ""
    for char in text:
        if char in chars_to_escape:
            escaped_text += '\\' + char
        else:
            escaped_text += char
    return escaped_text


def detect_service_from_message(message):
    """
    মেসেজ টেক্সট থেকে সার্ভিস সনাক্ত করে এবং তার নাম রিটার্ন করে।
    """
    message_lower = message.lower()
    service_patterns = {
        'Facebook': ['facebook', 'fb'], 'WhatsApp': ['whatsapp', 'wa'],
        'Telegram': ['telegram', 'tg'], 'Google': ['google', 'g-'],
        'TikTok': ['tiktok'], 'Instagram': ['instagram', 'ig'],
        'Imo': ['imo'], 'Viber': ['viber'], 'Snapchat': ['snapchat'],
        'Microsoft': ['microsoft'], 'Apple': ['apple', 'icloud'],
        'Discord': ['discord'], 'Twitter': ['twitter', 'x.com'],
        'Amazon': ['amazon'], 'PayPal': ['paypal'], 'Steam': ['steam'],
        'Netflix': ['netflix'], 'YouTube': ['youtube'], 'Bigo': ['bigo'],
        'Line': ['line'], 'ChatGPT': ['chatgpt', 'openai'], 'Messenger': ['messenger']
    }
    
    for service, keywords in service_patterns.items():
        if any(kw in message_lower for kw in keywords):
            return service
            
    if "otp" in message_lower:
        return "Generic OTP"

    return "Unknown"

def extract_sms(driver, first_run=False):
    """
    SMSCDRStats পৃষ্ঠা থেকে SMS এক্সট্র্যাক্ট করে এবং টেলিগ্রামে পাঠায়।
    
    
    
    
    """
    global processed_messages
    try:
        driver.get(SMS_URL)
        time.sleep(3) # পৃষ্ঠা লোড হওয়ার জন্য অপেক্ষা
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        headers = soup.find_all('th')

        # টেবিল হেডার ইনডেক্স খুঁজে বের করুন
        number_idx = service_idx = sms_idx = None
        for idx, th in enumerate(headers):
            label = th.get('aria-label', '').lower()
            if 'number' in label: number_idx = idx
            elif 'cli' in label or 'service' in label: service_idx = idx
            elif 'sms' in label: sms_idx = idx

        if None in (number_idx, service_idx, sms_idx): 
            print("[⚠️] টেবিল হেডার সনাক্ত করা যায়নি। পৃষ্ঠার কাঠামো পরিবর্তিত হতে পারে।")
            return False

        rows = soup.find_all('tr')[1:] # প্রথম সারি (হেডার) বাদ দিন
        
        for row in reversed(rows): # নতুন মেসেজগুলো আগে প্রসেস করার জন্য রিভার্স করা হয়েছে
            cols = row.find_all('td')
            if len(cols) <= max(number_idx, service_idx, sms_idx): 
                continue # অপর্যাপ্ত কলাম থাকলে এড়িয়ে যান
            
            raw_number = cols[number_idx].get_text(strip=True) or "Unknown"
            service_col = cols[service_idx].get_text(strip=True) or "0"
            message = cols[sms_idx].get_text(strip=True)
            
            if not message: continue # খালি মেসেজ এড়িয়ে যান
            
            msg_id = f"{raw_number}_{message}" # মেসেজ ট্র্যাক করার জন্য ইউনিক আইডি

            if msg_id in processed_messages:
                continue # ইতিমধ্যে প্রসেস করা মেসেজ এড়িয়ে যান
            
            processed_messages.append(msg_id) # নতুন মেসেজ যোগ করুন

            if first_run:
                continue # প্রথম রানে শুধু সিঙ্ক করে, পাঠায় না

            # ফোন নম্বর থেকে দেশের তথ্য বের করুন
            country_name = "Unknown"
            flag = "🏳️"
            try:
                phone_val = raw_number if raw_number.startswith('+') else "+" + raw_number
                parsed_number = phonenumbers.parse(phone_val, None)
                if phonenumbers.is_valid_number(parsed_number):
                    country_name = geocoder.description_for_number(parsed_number, "en")
                    region_code = region_code_for_number(parsed_number)
                    flag = get_country_flag(region_code)
            except Exception as e:
                pass # ফোন নম্বর পার্স করতে ব্যর্থ হলে ডিফল্ট ব্যবহার করুন



            # --- OTP এক্সট্র্যাকশন লজিক (বিভিন্ন প্যাটার্ন) ---
            otp_code = "N/A"
            message_lower = message.lower()

            # প্যাটার্ন 1: 4 থেকে 8 ডিজিটের সংখ্যা যা একটি শব্দ সীমানার মধ্যে আছে
            match1 = re.search(r'\b(\d{4,8})\b', message)
            if match1:
                otp_code = match1.group(1)
            else:
                # প্যাটার্ন 2: "OTP", "Code", "PIN" ইত্যাদি শব্দের পর 4 থেকে 8 ডিজিটের সংখ্যা
                # বাংলা এবং আরবী কিওয়ার্ডও যোগ করা হয়েছে
                match2 = re.search(r'(?:otp|code|pin|verification|رمز|কোড)\D*(\d{4,8})', message_lower, re.IGNORECASE)
                if match2:
                    otp_code = match2.group(1)
                else:
                    # প্যাটার্ন 3: শুধু 4 থেকে 8 ডিজিটের সংখ্যা (ফলব্যাক)
                    match3 = re.search(r'(\d{4,8})', message)
                    if match3:
                        otp_code = match3.group(1)
            # --- OTP এক্সট্র্যাকশন লজিক শেষ ---
            
            # সার্ভিস ডিটেকশন (ইমোজি ছাড়া)
            detected_service_name = detect_service_from_message(message)
            
            # service_col থেকে পাওয়া তথ্য ব্যবহার করে ডিটেকশন উন্নত করুন
            if detected_service_name == "Unknown" and service_col != "0":
                detected_service_name = service_col.capitalize()
            # যদি এখনও Unknown থাকে এবং OTP থাকে তবে Generic OTP ব্যবহার করুন
            elif detected_service_name == "Unknown" and "OTP" in message.upper():
                 detected_service_name = "Generic OTP"

            # --- Formatted টেক্সট স্টাইলিং ---
            # HTML ফরম্যাটিং ব্যবহার করে টেক্সট স্টাইলিশ করা হয়েছে
            
            #
            
            
            # বিশেষ ক্যারেক্টারগুলো এস্কেপ করার প্রয়োজন নেই HTML এ শুধুমাত্র < > & এস্কেপ করতে হয় (যদি থাকে)
            
            # HTML Escape
            def escape_html(text):
                return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

            escaped_message = escape_html(message)
            escaped_country_name = escape_html(country_name)
            escaped_phone_number = escape_html(format_phone_number(raw_number))
            
            service_display = detected_service_name if detected_service_name != "Unknown" else "Service"
            escaped_service_name = escape_html(service_display)

            # প্রিমিয়াম ইমোজি আইডি বের করুন
            country_emoji_id = PREMIUM_EMOJIS.get(country_name, PREMIUM_EMOJIS["DEFAULT"])
            premium_flagHTML = f'<tg-emoji emoji-id="{country_emoji_id}">{flag}</tg-emoji>'

            # সার্ভিস ইমোজি আইডি বের করুন
            service_emoji_id = SERVICE_EMOJIS.get(detected_service_name.upper(), SERVICE_EMOJIS["DEFAULT"])
            premium_serviceHTML = f'<tg-emoji emoji-id="{service_emoji_id}">🟢</tg-emoji>'

            if CUSTOM_TEMPLATE:

                formatted_text = CUSTOM_TEMPLATE.format(
                    premium_flagHTML=premium_flagHTML,
                    escaped_service_name=escaped_service_name,
                    premium_serviceHTML=premium_serviceHTML,
                    escaped_country_name=escaped_country_name,
                    escaped_phone_number=escaped_phone_number,
                    otp_code=escape_html(otp_code),
                    escaped_message=escaped_message,
                )

            else:

                formatted_text = f"""
<b>𓆩𓆩.{premium_flagHTML}{escaped_service_name}  {premium_serviceHTML}𝚁𝙴𝙲𝙴𝙸𝚅𝙴𝙳 .𓆪𓆪</b>
﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌
<blockquote>{premium_flagHTML} ᯓ𝙲𝚘𝚞𝚗𝚝𝚛𝚢 » {escaped_country_name}
☎️ ᯓ𝗡𝘂𝗺𝗯𝗲𝗿 » {escaped_phone_number}</blockquote>
<blockquote>🔐ᯓ𝙾𝚃𝙿 » <code>{escape_html(otp_code)}</code></blockquote>
<blockquote>{escaped_message}</blockquote>
"""
            
            # টেলিগ্রামে বার্তা পাঠান
            if send_to_telegram(formatted_text, otp_code):
                print(f"[✅] পাঠানো হয়েছে: {raw_number} - {otp_code}")
            else:
                print(f"[❌] টেলিগ্রামে পাঠাতে ব্যর্থ: {raw_number} - {otp_code}")
            
        return True

    except Exception as e:
        print(f"[❌] SMS এক্সট্র্যাক্ট করতে ত্রুটি: {e}")
        return True

def wait_for_manual_login(driver):
    """
    ইউজারকে ম্যানুয়ালি ওয়েবসাইটে লগইন করার জন্য অপেক্ষা করে।
    """
    print("\n[👉] অনুগ্রহ করে ম্যানুয়ালি লগইন করুন...")
    login_start_time = time.time() 

    while True:
        try:
            current_url_lower = driver.current_url.lower()
            # login, signin, home, dashboard, agent এইগুলি লগইন করার পরের URL হতে পারে
            if "signin" not in current_url_lower and "login" not in current_url_lower:
                print("[✅] লগইন সনাক্ত হয়েছে!")
                return True
            
            remaining_time = int(60 - (time.time() - login_start_time))
            if remaining_time <= 0:
                print("[⏳] ম্যানুয়াল লগইনের জন্য ১ মিনিট সময় শেষ হয়েছে। এগিয়ে যাচ্ছি...")
                return True 

            print(f"ম্যানুয়াল লগইনের জন্য অপেক্ষা করা হচ্ছে... ({remaining_time} সেকেন্ড বাকি)")
            time.sleep(5) 
        except Exception as e:
            print(f"[❌] ম্যানুয়াল লগইন অপেক্ষার সময় ত্রুটি: {e}")
            return False 

def launch_browser():
    """
    Selenium WebDriver সহ Chrome ব্রাউজার চালু করে।
    """
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # হেডলেস মোড (ব্রাউজার UI দেখা যাবে না) যদি আপনি সার্ভারে চালান
    chrome_options.add_argument("--log-level=3") # কম লগ আউটপুট
    chrome_options.add_argument("--disable-gpu") # GPU ব্যবহার নিষ্ক্রিয় করুন (হেডলেস মোডে দরকারী)
    chrome_options.add_argument("--no-sandbox") # স্যান্ডবক্স নিষ্ক্রিয় করুন (লিনাক্স সার্ভারে প্রায়শই প্রয়োজন)
    chrome_options.add_argument("--disable-dev-shm-usage") # /dev/shm ব্যবহারের অক্ষমতা (ডকার/লারাভেল কন্টেইনারে দরকারী)
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"[❌] ব্রাউজার চালু করতে ব্যর্থ: {e}")
        print("অনুগ্রহ করে নিশ্চিত করুন যে আপনার সিস্টেমে Chrome ব্রাউজার এবং ChromeDriver ইনস্টল করা আছে এবং তাদের সংস্করণ সামঞ্জস্যপূর্ণ।")
        sys.exit(1)

# --- Main Execution ---
def main():
    """
    স্ক্রিপ্টের প্রধান লজিক পরিচালনা করে।
    """
    driver = launch_browser()
    try:
        if not load_cookies(driver):
            print("[👉] কুকিজ পাওয়া যায়নি বা লোড করতে ব্যর্থ, নতুন লগইনের চেষ্টা করা হচ্ছে।")
            driver.get(LOGIN_URL)
        
        # যদি লগইন প্রয়োজন হয়, ব্যবহারকারীকে ম্যানুয়ালি লগইন করতে বলুন
        if "signin" in driver.current_url.lower() or "login" in driver.current_url.lower():
            if wait_for_manual_login(driver):
                save_cookies(driver) # সফল লগইনের পর কুকিজ সেভ করুন
            else:
                print("[🛑] ম্যানুয়াল লগইন সম্পন্ন হয়নি। স্ক্রিপ্ট বন্ধ করা হচ্ছে।")
                driver.quit()
                sys.exit(1)
        
        print("[⏳] প্রাথমিক সিঙ্ক শুরু হচ্ছে...")
        extract_sms(driver, first_run=True) # প্রাথমিক সিঙ্ক: শুধুমাত্র নতুন মেসেজ ট্র্যাক করে, পাঠায় না
        print("[🚀] মনিটরিং শুরু হয়েছে...")
        
        while True:
            # SMS এক্সট্র্যাক্ট করার চেষ্টা করুন
            if not extract_sms(driver):
                # যদি SMS এক্সট্র্যাক্ট করতে সমস্যা হয়, সেশন মেয়াদ উত্তীর্ণ হয়েছে কিনা পরীক্ষা করুন
                current_url_lower = driver.current_url.lower()
                if "signin" in current_url_lower or "login" in current_url_lower:
                    print("[⚠️] সেশন মেয়াদ উত্তীর্ণ হয়েছে বা লগইন প্রয়োজন।")
                    if wait_for_manual_login(driver):
                        save_cookies(driver) # পুনরায় লগইনের পর কুকিজ সেভ করুন
                    else:
                        print("[🛑] পুনরায় লগইন ব্যর্থ। স্ক্রিপ্ট বন্ধ করা হচ্ছে।")
                        driver.quit()
                        sys.exit(1)
                else:
                    print("[⚠️] SMS এক্সট্র্যাক্ট করতে সমস্যা হয়েছে, আবার চেষ্টা করা হচ্ছে...")
            time.sleep(2) 
            
    except KeyboardInterrupt:
        print("\n[🛑] ব্যবহারকারী কর্তৃক বন্ধ করা হয়েছে।")
    except Exception as e:
        print(f"[❌] একটি অপ্রত্যাশিত ত্রুটি ঘটেছে: {e}")
    finally:
        print("[👋] ব্রাউজার বন্ধ করা হচ্ছে।")
        driver.quit()

if __name__ == "__main__":
    main()
    