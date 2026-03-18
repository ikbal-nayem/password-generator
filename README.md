# Bangladeshi WiFi Password Generator

A targeted WiFi password list generator optimized for Bangladeshi networks. This tool generates common password candidates based on network-specific information and Bangladeshi cultural patterns.

## Features

✨ **Intelligent Password Generation**
- Generates passwords with minimum 8 characters (WiFi standard)
- Uses SSID and username as primary password candidates
- Incorporates Bangladeshi-specific cultural references
- Dynamic year-based variations (automatically updates each year)

🌍 **Bangladeshi Content Library**
- **37 Districts & Cities**: All major Bangladeshi locations
- **50+ Cultural Words**: Bengali terms, Islamic references, local food, sports, traditions
- **Mobile Patterns**: All 7 Bangladeshi mobile operator prefixes (Grameenphone, Robi, Airtel, Banglalink, etc.)
- **Default Passwords**: 30+ common patterns users typically set
- **Leet Substitutions**: Enhanced character replacements for pattern coverage

⚡ **Multiple Generation Strategies**
1. SSID and username variations (case, leet, prefixes, suffixes)
2. Common Bangladeshi default passwords
3. Place names with variants (Dhaka, Chittagong, etc.)
4. Cultural words and common bengali terms
5. Place + Year combinations (e.g., Dhaka2026)
6. Mobile number patterns (11 digits: 017/018/019/016/015/013/014 + 8 digits)
7. Word + Year combinations
8. Numeric repetition patterns
9. Random padding to reach target count

## Installation

### Requirements
- Python 3.8+
- No external dependencies

### Setup
```bash
git clone <repository>
cd password-generator
```

## Usage

### Basic Usage
```bash
python main.py --ssid "MyWiFiNetwork"
```

### With Username
```bash
python main.py --ssid "MyWiFiNetwork" --username "admin"
```

### Custom Output Size
```bash
python main.py --ssid "HomeWiFi" --max 50000 --output passwords.txt
```

### All Options
```bash
python main.py --ssid <SSID> [--username <USERNAME>] [--max <COUNT>] [--output <FILE>]
```

**Arguments:**
- `--ssid` (required): WiFi network name
- `--username` (optional): Owner's name or username for additional variations
- `--max` (optional): Maximum passwords to generate (default: 100,000)
- `--output` (optional): Output filename (default: `default_passwords.txt`)

## Examples

### Example 1: Generate 10,000 passwords for a home network
```bash
python main.py --ssid "Home_Network" --max 10000 --output home_passwords.txt
```

Output:
```
[+] Generated 10000 passwords (min length 8). Saved to home_passwords.txt
[+] Password list includes: SSID variations, places, words, mobile numbers, year combos, and random patterns
```

### Example 2: Generate passwords with owner information
```bash
python main.py --ssid "DhakaCafe_WiFi" --username "karim" --max 5000 --output cafe_passwords.txt
```

## Password Generation Strategy

### Generation Priority
The tool generates passwords in a structured order to maximize likelihood:

1. **SSID Variations** (Highest Priority)
   - Original, capitalized, uppercase versions
   - With suffixes: 123, 1234, @, #, !, bd, wifi, pass, net
   - With prefixes: @, #, !, 123, bd
   - Leet versions (a→4, e→3, i→1, etc.)

2. **Default Passwords**
   - Common patterns like "password123", "admin1234", "router123"
   - Bangladeshi-specific: "banglades", "dhaka1234", "bismillah"

3. **Places** (37 major cities and districts)
   - All variations with suffixes/prefixes
   - Year combinations (Dhaka2026, Chittagong2025, etc.)

4. **Common Words** (50+ Bangladeshi cultural terms)
   - Sports: "football", "cricket", "shakib"
   - Food: "biryani", "chai", "mango", "hilsa"
   - Culture: "rickshaw", "zamindar", "bismillah"
   - Nature: "padma", "sundarbans", "meghna"

5. **Mobile Patterns** (5,000 variations)
   - Format: PREFIX + 8 random digits
   - Prefixes: 017, 018, 019, 016, 015, 013, 014

6. **Year Combinations**
   - Place + Year: "Dhaka2026", "chittagong2025"
   - Word + Year: "bangla2026", "cricket2024"
   - Range: Current Year ± 5 years

7. **Numeric Patterns**
   - Repetitions: 11111111, 22222222, etc.
   - Sequences: 10101010, 12121212
   - Recent years with suffixes

8. **Random Padding**
   - Pure digits: 8 random numbers
   - Mixed: Random letters + digits
   - Word-based: Short word + random digits

### Dynamic Year Handling
The tool automatically updates year variations based on the current date:
- **Backwards**: Includes previous 3 years
- **Forwards**: Includes next 5 years
- **No manual updates needed** - stays current forever

Example (as of March 2026):
- Year range: 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031

## Output

Each generated password:
- Is minimum 8 characters (meets WiFi minimum requirement)
- Is maximum 64 characters (memory safe)
- Is on a separate line in the output file
- Is unique (uses set-based generation)
- Is randomly shuffled for distribution

### Sample Output (first 10 lines)
```
MyWiFiNetwork123
mywifinework@123
mywifinework2026
Mywifinework1234
4yw1f1n37w0r#
17043892145b123
dhaka2026
cricket1234
Bangladesh123
bismillah2025
```

## Performance

Generation speed depends on target count:
- **10,000 passwords**: < 1 second
- **100,000 passwords**: 1-3 seconds
- **1,000,000 passwords**: 10-30 seconds

Memory usage remains efficient due to set-based duplicate elimination.

## Customization

### Add Custom Words
Edit the `COMMON_WORDS` list in `main.py`:
```python
COMMON_WORDS = [
    # ... existing words ...
    "yourword", "customterm"
]
```

### Add Custom Places
Edit the `PLACES` list:
```python
PLACES = [
    # ... existing places ...
    "YourLocation", "YourCity"
]
```

### Adjust Year Range
Modify the `YEARS` calculation:
```python
# Current: CURRENT_YEAR - 3 to CURRENT_YEAR + 5
YEARS = [str(y) for y in range(CURRENT_YEAR - 5, CURRENT_YEAR + 10)]
```

### Change Leet Substitutions
Edit the `LEET_MAP`:
```python
LEET_MAP = {
    'a':'4', 'e':'3', 'i':'1', 'o':'0', 's':'5', 
    't':'7', 'l':'1', 'b':'8', 'g':'9',
    # Add more mappings
}
```

## Technical Details

### Dependencies
- Python Standard Library only:
  - `argparse` - Command line argument parsing
  - `itertools` - Efficient iteration
  - `random` - Randomization
  - `string` - Character sets
  - `datetime` - Current year calculation

### File Size Reference
- 10,000 passwords ≈ 100 KB
- 100,000 passwords ≈ 1 MB
- 1,000,000 passwords ≈ 10 MB

### Algorithm Complexity
- Time: O(n) where n = target password count
- Space: O(n) for set storage

## Ethical Use

⚠️ **DISCLAIMER**

This tool is designed for:
- **Authorized security testing** of your own networks
- **Penetration testing** with explicit permission
- **Educational purposes** to understand password patterns
- **Incident response** on networks you own or manage

**Unauthorized access to networks is illegal.** Always obtain proper authorization before testing any network.

## Contributing

Suggestions welcome for:
- Additional Bangladeshi cultural references
- New password patterns
- Performance optimizations
- Bug fixes

## License

This project is provided as-is for educational and authorized testing purposes.

## Author

Created for Bangladeshi network security testing and education.

---

**Last Updated**: March 2026
**Current Year**: 2026 (Years: 2023-2031)
