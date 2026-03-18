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
PLACES = [
    "Dhaka", "Chittagong", "Khulna", "Rajshahi", "Sylhet", "Barisal", "Rangpur",
    "Mymensingh", "Comilla", "Narayanganj", "Gazipur", "Jessore", "Bogra", "Dinajpur",
    "Pabna", "Tangail", "Faridpur", "Noakhali", "Chandpur", "Coxsbazar", "Brahmanbaria"
]

COMMON_WORDS = [
    "love", "baby", "hello", "bangla", "desh", "football", "cricket", "tiger",
    "royal", "gold", "silver", "super", "master", "king", "queen", "star",
    "sun", "moon", "sky", "fire", "water", "happy", "smile", "friend"
]

# Default passwords with length >= 8
DEFAULT_PASS = [p for p in [
    "12345678", "password", "123456789", "1234567890", "qwertyui", "abc12345",
    "11111111", "12312312", "admin123", "letmein1", "monkey12", "iloveyou",
    "banglades", "dhaka1234", "bismillah", "password1", "123456789", "00000000"
] if len(p) >= 8]

MOBILE_PREFIXES = ["017", "018", "019", "016", "015", "013", "014"]
YEARS = [str(y) for y in range(datetime.now().year - 2, datetime.now().year + 1)]

# Leet substitutions (optional)
LEET_MAP = {'a':'4', 'e':'3', 'i':'1', 'o':'0', 's':'5', 't':'7'}

# ------------------- Helper functions -------------------
def leetify(word):
    """Apply simple leet substitutions to a word."""
    word_low = word.lower()
    return ''.join(LEET_MAP.get(ch, ch) for ch in word_low)

def add_common_variations(base_set, word, max_items):
    """Add word with suffixes, prefixes, and leet versions (min length 8) to base_set until limit."""
    suffixes = ["", "123", "1234", "1", "2", "007", "@", "#", "!", "2023", "2024", "2025", "bd", "BD"]
    prefixes = ["", "@", "#", "!"]

    # Original word (only if length >= 8)
    if len(word) >= 8:
        base_set.add(word)
        if len(base_set) >= max_items:
            return

    # With suffixes/prefixes
    for p, s in itertools.product(prefixes, suffixes):
        if p == "" and s == "":
            continue
        candidate = p + word + s
        if len(candidate) >= 8:
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
    parser = argparse.ArgumentParser(description="Generate a targeted WiFi password list (min 8 chars, no default first names).")
    parser.add_argument("--ssid", required=True, help="WiFi SSID (network name)")
    parser.add_argument("--username", help="Optional username (e.g., owner's name)")
    parser.add_argument("--max", type=int, default=100000, help="Maximum number of passwords (default: 100000)")
    parser.add_argument("--output", default="default_passwords.txt", help="Output file name")
    args = parser.parse_args()

    max_pass = args.max
    passwords = set()

    # 1. SSID/Username specific variations
    ssid_vars = generate_ssid_variations(args.ssid, args.username, max_pass)
    passwords.update(ssid_vars)
    if len(passwords) >= max_pass:
        passwords = list(passwords)[:max_pass]
        random.shuffle(passwords)
        write_file(passwords, args.output)
        return

    # 2. Add common Bangladeshi default passwords (already filtered for length >=8)
    for pwd in DEFAULT_PASS:
        passwords.add(pwd)
        if len(passwords) >= max_pass:
            break

    # 3. Add places (with min-length enforcement)
    for place in PLACES:
        add_common_variations(passwords, place, max_pass)
        if len(passwords) >= max_pass:
            break

    # 4. Add common words
    for word in COMMON_WORDS:
        add_common_variations(passwords, word, max_pass)
        if len(passwords) >= max_pass:
            break

    # 5. Add mobile number patterns (always 11 digits, so >=8)
    if len(passwords) < max_pass:
        for _ in range(min(10000, max_pass - len(passwords))):
            prefix = random.choice(MOBILE_PREFIXES)
            num = ''.join(random.choices(string.digits, k=8))
            passwords.add(prefix + num)
            if len(passwords) >= max_pass:
                break

    # 6. Add years combined with words (ensuring total length >=8)
    if len(passwords) < max_pass:
        year_combos = []
        for year in YEARS:
            year_combos.append("bangla" + year)      # e.g., bangla2024 (10 chars)
            year_combos.append("dhaka" + year)       # dhaka2024 (9 chars)
            # "ctg" + year is only 7 chars, skip
        for combo in year_combos:
            if len(combo) >= 8:
                passwords.add(combo)
                if len(passwords) >= max_pass:
                    break

    # 7. Pad with random 8-digit numbers if still under limit
    while len(passwords) < max_pass:
        passwords.add(''.join(random.choices(string.digits, k=8)))

    # Shuffle and write
    passwords = list(passwords)
    random.shuffle(passwords)
    passwords = passwords[:max_pass]

    with open(args.output, "w") as f:
        for pwd in passwords:
            f.write(pwd + "\n")

    print(f"[+] Generated {len(passwords)} passwords (min length 8). Saved to {args.output}")

if __name__ == "__main__":
    main()