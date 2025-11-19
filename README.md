# Jiji.ug Data Extraction Tool

> ⚠️ **IMPORTANT LEGAL DISCLAIMER**
> 
> This tool is provided **strictly for educational and personal research purposes only**. By using this software, you acknowledge and agree to the following:
> 
> - **Terms of Service Compliance**: You are solely responsible for ensuring your use complies with Jiji.ug's Terms of Service, robots.txt file, and applicable laws
> - **Data Privacy**: Extracting personal information (including phone numbers) may violate privacy laws such as Uganda's Data Protection and Privacy Act, GDPR, or other regional regulations
> - **Rate Limiting**: Excessive scraping may place undue burden on Jiji.ug's servers and could be considered a denial of service
> - **No Commercial Use**: This tool is NOT intended for commercial purposes, bulk data harvesting, spam, or any activities that could harm individuals or businesses
> - **Ethical Use Only**: Use this tool responsibly and ethically. Do not use extracted data for harassment, unsolicited marketing, fraud, or any malicious purposes
> 
> **THE AUTHORS AND CONTRIBUTORS OF THIS PROJECT ASSUME NO LIABILITY FOR ANY MISUSE OF THIS TOOL. YOU USE IT AT YOUR OWN RISK.**

---

## 📋 Table of Contents

- [Overview](#overview)
- [⚖️ Legal & Ethical Considerations](#️-legal--ethical-considerations)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This is a web scraping tool built with Playwright that demonstrates automated data extraction techniques from Jiji.ug, a popular Ugandan classifieds platform. It extracts phone numbers from product advertisements and category listings for research and educational purposes.

**Intended Use Cases:**
- Learning web scraping techniques and browser automation
- Personal research on market trends (small-scale, ethical use)
- Understanding dynamic content handling and infinite scroll implementations
- Educational demonstrations of data extraction methodologies

---

## ⚖️ Legal & Ethical Considerations

### Before Using This Tool

1. **Review Jiji.ug's Terms of Service**: Visit [Jiji.ug](https://jiji.ug/) and carefully read their terms of service and acceptable use policy

2. **Check robots.txt**: Review `https://jiji.ug/robots.txt` to understand which pages are permitted for automated access

3. **Respect Rate Limits**: Implement reasonable delays between requests to avoid overwhelming the server

4. **Data Privacy Compliance**:
   - Do NOT use extracted data for unsolicited communications
   - Do NOT share, sell, or distribute personal information
   - Ensure compliance with applicable data protection laws
   - Consider data minimization principles

5. **Obtain Consent**: If using extracted data to contact individuals, ensure you have proper legal basis under applicable law

### Recommendations for Responsible Use

- **Limit scope**: Only scrape small amounts of data for personal research
- **Add delays**: Implement reasonable wait times between page loads
- **Use sparingly**: Don't run the scraper continuously or repeatedly
- **Respect opt-outs**: If someone asks not to be contacted, honor that immediately
- **Secure storage**: Protect any extracted data with appropriate security measures
- **Delete when done**: Remove extracted data when your research is complete

---

## Features

- **Playwright-Powered Automation**: Uses Playwright's asynchronous API with Chromium for reliable browser automation
- **Dynamic Content Handling**: 
  - Automatically clicks "Show contact" buttons to reveal phone numbers
  - Dismisses language preference popups
  - Handles both category listings and single advert pages
- **Comprehensive Number Extraction**:
  - Scans `__NUXT_DATA__` script content
  - Extracts from contacts popover DOM elements
  - Parses full HTML and rendered text including comments
- **Strict Mobile Number Normalization**:
  - Validates Ugandan mobile numbers (07XXXXXXXX format)
  - Normalizes all numbers to international format (+2567XXXXXXXX)
  - Deduplicates results using sets
- **Cookie-Based Session Management**: Maintains authenticated sessions to avoid login popups
- **Intelligent Infinite Scrolling**: Automatically loads all content with configurable limits
- **Personal Number Exclusion**: Filter out your own phone numbers from results
- **Robust Error Handling**: Continues operation despite individual page failures

---

## Prerequisites

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** (Python package installer)
- **Basic command line knowledge**

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/jiji-scraper.git
cd jiji-scraper
```

### 2. Create a Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
playwright
beautifulsoup4
```

### 4. Install Playwright Browsers

```bash
playwright install chromium
```

This downloads the Chromium browser that Playwright will use for automation.

---

## Configuration

### 1. Obtain Cookies File

The scraper requires authentication cookies to function properly.

**Using a Browser Extension:**

1. Install a "cookies.txt" extension for your browser:
   - **Chrome**: Search "Get cookies.txt" in Chrome Web Store
   - **Firefox**: Search "cookies.txt" in Firefox Add-ons

2. Visit [jiji.ug](https://jiji.ug/) and log in (optional but recommended)

3. Click the extension icon and export cookies in **Netscape HTTP Cookie File** format

4. Save as `jiji.ug_cookies.txt` in the project directory

**Expected Format:**
```
# Netscape HTTP Cookie File
.jiji.ug	TRUE	/	TRUE	1795071664	uid	68dc4d849277aa826d69a67fd826f0da4e5dd0f1
jiji.ug	FALSE	/	FALSE	1790804228	lang	en
```

### 2. Configure the Script

Open `jiji_scraper.py` and modify the configuration section:

```python
# URLs to scrape (can be category pages or individual adverts)
jiji_category_urls = [
    "https://jiji.ug/tv-dvd-equipment",
    # Add more URLs here
]

# Path to your cookies file
cookie_file = "jiji.ug_cookies.txt"

# Your own numbers to exclude from results (optional)
my_numbers_to_exclude = [
    "0700000000",  # Replace with your actual number
]
```

### 3. Configure Scrolling Behavior

**Option A: Scroll until all content is loaded (Recommended)**
```python
asyncio.run(
    main_scraper(
        jiji_category_urls,
        cookie_file,
        scroll_until_done=True,
        max_scroll_actions_per_category=10,  # Safety limit
    )
)
```

**Option B: Fixed number of scrolls**
```python
asyncio.run(
    main_scraper(
        jiji_category_urls,
        cookie_file,
        scroll_until_done=False,
        max_scroll_actions_per_category=5,
    )
)
```

---

## Usage

Run the scraper from your terminal:

```bash
python jiji_scraper.py
```

The script will:
1. Load your cookies to maintain session state
2. Visit each specified URL
3. Scroll through category pages to load all adverts
4. Click "Show contact" buttons on advert pages
5. Extract and normalize phone numbers
6. Save unique numbers to `jiji_phone_numbers.txt`

**Output:**
```
Starting Jiji.ug scraper (Playwright)...
Loaded 15 cookies from jiji.ug_cookies.txt
Processing: https://jiji.ug/tv-dvd-equipment
Detected category page. Scrolling to load all adverts...
Scroll 1/10: Found 24 total ads so far...
Extracted 47 unique phone numbers.
Results saved to jiji_phone_numbers.txt
```

---

## How It Works

1. **Cookie Authentication**: Injects browser cookies to maintain logged-in state
2. **Page Type Detection**: Identifies whether URL is a category listing or single advert
3. **Dynamic Loading**: For categories, scrolls until all adverts are loaded
4. **Advert Processing**: Visits each unique advert page
5. **Contact Revelation**: Clicks buttons to reveal hidden phone numbers
6. **Multi-Source Extraction**: Scans JavaScript data, HTML, and visible text
7. **Validation & Normalization**: Ensures all numbers are valid Ugandan mobile numbers
8. **Deduplication**: Stores only unique numbers in international format
9. **Filtering**: Removes any personal numbers you've configured to exclude

---

## Troubleshooting

### Browser Closes Immediately
- Jiji.ug may detect headless browsers. The script runs in headed mode by default
- Ensure your cookies file is up to date

### No Phone Numbers Found
- Verify your cookies file is properly formatted and not expired
- Check that you're logged in to Jiji.ug in your browser before exporting cookies
- Some ads may not display contact information

### Script Hangs During Scrolling
- Reduce `max_scroll_actions_per_category` value
- Check your internet connection
- Some pages may have loading issues

### Permission Errors
- Ensure you have write permissions in the project directory
- Check that `jiji_phone_numbers.txt` isn't open in another program

---

## Contributing

This is an educational project. If you have improvements or bug fixes:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

**Please ensure all contributions maintain the educational and ethical focus of this project.**

---

## License

This project is provided for educational purposes only. See [LICENSE](LICENSE) for more information.

**Disclaimer**: This software is provided "as is" without warranty of any kind. The authors are not responsible for any damages or legal issues arising from its use.

---

## Contact & Support

For questions about web scraping ethics, legal compliance, or technical issues, please open an issue on GitHub.

**Remember**: Always prioritize ethical behavior, respect privacy, and comply with applicable laws and terms of service.

---

*Last Updated: November 2025*
