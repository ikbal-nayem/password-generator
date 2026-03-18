#!/usr/bin/env python3
"""
WiFi Password List Generator (min. 8 chars) for Bangladeshi Networks
Default first names list removed. Uses SSID, username, places, common words, defaults, mobile patterns, years, and random digits.
Usage: python generate_wifi_list.py --ssid <SSID> [--username <USER>] [--max <N>] [--output <FILE>]
"""

import argparse
import itertools
import random
import string
from datetime import datetime

# ------------------- Common Bangladeshi Data (without first names) -------------------
# Get current year for dynamic year-based password generation
CURRENT_YEAR = datetime.now().year

# Year range for password variations (current year ± 5 years forward, ± 3 years backward)
YEARS = [str(y) for y in range(CURRENT_YEAR - 3, CURRENT_YEAR + 6)]

# Major cities, districts, and popular places
PLACES = [
    "Dhaka", "Chittagong", "Khulna", "Rajshahi", "Sylhet", "Barisal", "Rangpur",
    "Mymensingh", "Comilla", "Narayanganj", "Gazipur", "Jessore", "Bogra", "Dinajpur",
    "Pabna", "Tangail", "Faridpur", "Noakhali", "Chandpur", "Coxsbazar", "Brahmanbaria",
    "Sherpur", "Jashore", "Jhalokati", "Madaripur", "Manikganj", "Narail", "Shariatpur",
    "Habiganj", "Moulvibazar", "Sunamganj", "Kushtia", "Meherpur", "Chuadanga",
    "Pirganj", "Natore", "Panchagarh", "Thakurgaon"
]

# Bengali words, cultural terms, and common Bangladeshi references
COMMON_WORDS = [
    # Universal common words
    "love", "baby", "hello", "welcome", "friend", "family", "happy", "smile","friend",
    # Bangladeshi/Bengali words
    "bangla", "desh", "bangladesh", "dhakacity", "rickshaw", "paribari",
    # Cultural/Islamic references
    "bismillah", "islam", "ummah", "prarthana",
    # Sports and entertainment
    "football", "cricket", "tiger", "national", "shakib", "sehwag", "rohit",
    # Nature and places
    "padma", "meghna", "brhamputra", "sundarbans", "teesta", "karnafuli",
    # Colors and materials
    "gold", "silver", "green", "orange", "red", "blue", "pink",
    # Animals - culturally significant
    "tiger", "eagle", "lion", "cobra", "elephant", "peacock", "deer",
    # Positive attributes
    "super", "master", "king", "queen", "prince", "star", "power", "strong",
    # Nature elements
    "sun", "moon", "sky", "fire", "water", "storm", "wind", "earth",
    # Food/Culture
    "rice", "biryani", "puri", "chai", "mango", "hilsa", "roti",
    # Traditional terms
    "zamindar", "jagirdar", "mansab"
]

# Default passwords - common patterns Bangladeshi users try (min length >= 8)
DEFAULT_PASS = [p for p in [
    "12345678", "password", "123456789", "1234567890", "qwertyui", "abc12345",
    "11111111", "12312312", "admin123", "letmein1", "monkey12", "iloveyou",
    "banglades", "dhaka1234", "bismillah", "password1", "123456789", "00000000",
    "password123", "welcome12", "admin1234", "user12345", "guest12345", "test12345",
    "bangladesh", "bangladesx", "dhakacity", "router123", "wifipass1", "networkpass",
    "asdfghjk", "1qaz2wsx", "qwerty123", "123qwerty", "password12", "12345qwerty"
] if len(p) >= 8]

# Bangladeshi mobile operator prefixes (Grameenphone, Robi, Airtel, Banglalink, etc.)
MOBILE_PREFIXES = ["017", "018", "019", "016", "015", "013", "014"]

# Additional common numeric suffixes (dynamically includes recent years)
NUMERIC_SUFFIXES = ["0000", "1111", "2222", "9999"] + YEARS

# Leet substitutions for increased coverage
LEET_MAP = {'a':'4', 'e':'3', 'i':'1', 'o':'0', 's':'5', 't':'7', 'l':'1', 'b':'8', 'g':'9'}

# ------------------- Helper functions -------------------
def leetify(word):
    """Apply simple leet substitutions to a word."""
    word_low = word.lower()
    return ''.join(LEET_MAP.get(ch, ch) for ch in word_low)

def add_common_variations(base_set, word, max_items):
    """Add word with suffixes, prefixes, and leet versions (min length 8) to base_set until limit."""
    # Build suffixes dynamically based on current year
    year_suffixes = [str(y) for y in range(CURRENT_YEAR - 2, CURRENT_YEAR + 3)]
    suffixes = ["", "123", "1234", "1", "2", "007", "@", "#", "!", "bd", "BD",
                "2020", "2021", "2022", "99", "100", "007bd", "123bd", "!@#", "pass", "wifi", "net"] + year_suffixes
    prefixes = ["", "@", "#", "!", "123", "bd"]

    # Original word (only if length >= 8)
    if len(word) >= 8:
        base_set.add(word)
        if len(base_set) >= max_items:
            return
        base_set.add(word.upper())
        if len(base_set) >= max_items:
            return

    # With suffixes/prefixes
    for p, s in itertools.product(prefixes, suffixes):
        if p == "" and s == "":
            continue
        candidate = p + word + s
        if len(candidate) >= 8 and len(candidate) <= 64:  # Avoid extremely long passwords
            base_set.add(candidate)
            if len(base_set) >= max_items:
                return

    # Leet versions
    leet_word = leetify(word)
    if len(leet_word) >= 8:
        base_set.add(leet_word)
        if len(base_set) >= max_items:
            return
    for p, s in itertools.product(prefixes, suffixes):
        candidate = p + leet_word + s
        if len(candidate) >= 8 and len(candidate) <= 64:
            base_set.add(candidate)
            if len(base_set) >= max_items:
                return

    # Title case variations
    title_word = word.capitalize()
    if len(title_word) >= 8:
        base_set.add(title_word)
        if len(base_set) >= max_items:
            return
        year_suffixes = [str(y) for y in range(CURRENT_YEAR - 1, CURRENT_YEAR + 2)]
        for s in ["123", "1234", "bd"] + year_suffixes:
            candidate = title_word + s
            if len(candidate) >= 8:
                base_set.add(candidate)
                if len(base_set) >= max_items:
                    return

def generate_ssid_variations(ssid, username, max_items):
    """Generate password candidates based on SSID and username (min length 8)."""
    passwords = set()

    # Clean inputs: remove spaces, lowercase
    ssid_clean = ssid.replace(" ", "").lower()
    username_clean = username.replace(" ", "").lower() if username else ""

    # Basic candidates
    candidates = []
    if ssid_clean:
        candidates.append(ssid_clean)
        candidates.append(ssid_clean.capitalize())
        candidates.append(ssid_clean.upper())
    if username_clean:
        candidates.append(username_clean)
        candidates.append(username_clean.capitalize())
        candidates.append(username_clean.upper())

    # Add each candidate with variations
    for cand in candidates:
        add_common_variations(passwords, cand, max_items)
        if len(passwords) >= max_items:
            return passwords

    return passwords

# ------------------- Main generator -------------------
def main():
    parser = argparse.ArgumentParser(description="Generate a targeted WiFi password list (min 8 chars) for Bangladeshi networks.")
    parser.add_argument("--ssid", required=True, help="WiFi SSID (network name)")
    parser.add_argument("--username", help="Optional username (e.g., owner's name)")
    parser.add_argument("--max", type=int, default=100000, help="Maximum number of passwords (default: 100000)")
    parser.add_argument("--output", default="default_passwords.txt", help="Output file name")
    args = parser.parse_args()

    max_pass = args.max
    passwords = set()

    # 1. SSID/Username specific variations (highest priority)
    ssid_vars = generate_ssid_variations(args.ssid, args.username, max_pass)
    passwords.update(ssid_vars)
    if len(passwords) >= max_pass:
        passwords = list(passwords)[:max_pass]
        random.shuffle(passwords)
        with open(args.output, "w") as f:
            for pwd in passwords:
                f.write(pwd + "\n")
        print(f"[+] Generated {len(passwords)} passwords (min length 8). Saved to {args.output}")
        return

    # 2. Add common Bangladeshi default passwords
    for pwd in DEFAULT_PASS:
        passwords.add(pwd)
        if len(passwords) >= max_pass:
            break

    # 3. Add places with variations (major password source)
    for place in PLACES:
        add_common_variations(passwords, place, max_pass)
        if len(passwords) >= max_pass:
            break

    # 4. Add common words with variations
    for word in COMMON_WORDS:
        add_common_variations(passwords, word, max_pass)
        if len(passwords) >= max_pass:
            break

    # 5. Add combinations of place + year (e.g., Dhaka2024)
    if len(passwords) < max_pass:
        for place in PLACES[:10]:  # Top 10 places
            for year in YEARS:
                combo = place.lower() + year
                if len(combo) >= 8:
                    passwords.add(combo)
                    passwords.add(place + year)
                    if len(passwords) >= max_pass:
                        break
            if len(passwords) >= max_pass:
                break

    # 6. Add mobile number patterns (Bangladeshi format: 11 digits)
    if len(passwords) < max_pass:
        mobile_count = min(5000, max_pass - len(passwords))
        for _ in range(mobile_count):
            prefix = random.choice(MOBILE_PREFIXES)
            num = ''.join(random.choices(string.digits, k=8))
            mobile = prefix + num
            passwords.add(mobile)
            # Also try variations
            passwords.add(mobile + "bd")
            passwords.add(mobile + "123")
            if len(passwords) >= max_pass:
                break

    # 7. Add word + year combinations
    if len(passwords) < max_pass:
        sample_words = random.sample(COMMON_WORDS, min(10, len(COMMON_WORDS)))
        for word in sample_words:
            for year in YEARS:
                combo = (word + year).lower()
                if len(combo) >= 8 and len(combo) <= 64:
                    passwords.add(combo)
                    passwords.add(word.capitalize() + year)
                    if len(passwords) >= max_pass:
                        break
            if len(passwords) >= max_pass:
                break

    # 8. Add numeric patterns (repetitions and ranges - very common)
    if len(passwords) < max_pass:
        # Build recent years dynamically
        recent_years = [str(y) for y in range(CURRENT_YEAR - 3, CURRENT_YEAR + 1)]
        digit_patterns = ["00000000", "11111111", "22222222", "33333333", "99999999",
                          "10101010", "12121212"] + recent_years
        for digits in digit_patterns:
            if len(digits) >= 8:
                passwords.add(digits)
                for suffix in ["bd", "@", "#", "123"]:
                    candidates = [
                        digits + suffix,
                        suffix + digits,
                    ]
                    for c in candidates:
                        if len(c) >= 8 and len(c) <= 64:
                            passwords.add(c)
                    if len(passwords) >= max_pass:
                        break
            if len(passwords) >= max_pass:
                break

    # 9. Pad with random 8-character combinations if still under limit
    if len(passwords) < max_pass:
        random_count = max_pass - len(passwords)
        for _ in range(random_count):
            # Mix of digits, letters, and common patterns
            choice_type = random.choice([1, 2, 3])
            if choice_type == 1:
                # Random 8 digits
                passwords.add(''.join(random.choices(string.digits, k=8)))
            elif choice_type == 2:
                # Random letters + digits
                pwd = ''.join(random.choices(string.ascii_lowercase, k=4)) + \
                      ''.join(random.choices(string.digits, k=4))
                random.shuffle(list(pwd))
                passwords.add(pwd)
            else:
                # Word + random digit suffix
                word = random.choice(COMMON_WORDS + PLACES)
                pwd = word.lower()[:4] + ''.join(random.choices(string.digits, k=4))
                if len(pwd) >= 8:
                    passwords.add(pwd)

    # Shuffle and write
    passwords = list(passwords)
    random.shuffle(passwords)
    passwords = passwords[:max_pass]

    with open(args.output, "w") as f:
        for pwd in passwords:
            f.write(pwd + "\n")

    print(f"[+] Generated {len(passwords)} passwords (min length 8). Saved to {args.output}")
    print(f"[+] Password list includes: SSID variations, places, words, mobile numbers, year combos, and random patterns")

if __name__ == "__main__":
    main()