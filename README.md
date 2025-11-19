# Web Scraping Education Project - Playwright Automation Demo

> 🛑 **CRITICAL WARNING - DO NOT USE ON JIJI.UG**
> 
> **This project violates Jiji.ug's Terms of Service and should NOT be used on their platform.**
>
> After thorough review of Jiji.ug's Terms of Service, this tool explicitly violates their policies:
> - **Prohibited Activity**: Jiji's Terms explicitly state: *"You will not harvest or otherwise collect information about users, including email addresses, phone numbers, without their consent"*
> - **Automated Access**: Their Terms prohibit: *"software and pursue any other actions aimed to interference with the normal operation of the Platform"*
> - **Legal Consequences**: Violating these terms may result in account termination, legal action, and liability for damages
>
> **THIS IS A TECHNICAL DEMONSTRATION ONLY** - The code showcases web scraping techniques, browser automation, and data extraction methodologies for **educational purposes**. It should **NEVER** be executed against Jiji.ug or any platform without explicit written permission.

---

## 📋 Table of Contents

- [Purpose of This Project](#purpose-of-this-project)
- [⚖️ Legal & Ethical Disclaimer](#️-legal--ethical-disclaimer)
- [What This Project Demonstrates](#what-this-project-demonstrates)
- [Technical Features](#technical-features)
- [Prerequisites](#prerequisites)
- [Installation (For Learning Only)](#installation-for-learning-only)
- [Legitimate Use Cases](#legitimate-use-cases)
- [How the Code Works](#how-the-code-works)
- [Learning Resources](#learning-resources)
- [Contributing](#contributing)
- [License](#license)

---

## Purpose of This Project

This repository is a **technical portfolio piece** and **educational resource** that demonstrates:

- Advanced Playwright automation techniques
- Dynamic content handling (infinite scroll, popup dismissal, button clicks)
- Cookie-based session management
- Data extraction from multiple sources (DOM, scripts, HTML)
- Regular expression pattern matching for phone numbers
- Robust error handling in web scraping

**What this project is:**
- ✅ A learning tool for web automation concepts
- ✅ A code example for portfolio/resume purposes
- ✅ A demonstration of Python + Playwright capabilities
- ✅ A reference for ethical scraping considerations

**What this project is NOT:**
- ❌ A tool to be used on Jiji.ug or any live platform
- ❌ A commercial data harvesting solution
- ❌ Legal or compliant with most websites' Terms of Service
- ❌ Intended for actual deployment or production use

---

## ⚖️ Legal & Ethical Disclaimer

### Terms of Service Violations

**This scraper violates the following provisions in Jiji.ug's Terms of Service:**

1. **Data Harvesting Prohibition** (Direct Quote):
   > "You will not harvest or otherwise collect information about users, including email addresses, phone numbers, without their consent or otherwise violate the privacy of another person"

2. **Automated Access Prohibition** (Direct Quote):
   > "You will not use software and pursue any other actions aimed to interference with the normal operation of the Platform"

3. **Privacy Violations**: Extracting phone numbers without consent violates privacy rights

### Legal Risks

Using this tool on Jiji.ug or similar platforms may result in:

- **Account Termination**: Immediate suspension and permanent ban
- **Legal Action**: Civil lawsuits for breach of contract and terms violations
- **Criminal Charges**: Potential violations of computer fraud and abuse laws
- **Data Protection Violations**: Uganda Data Protection and Privacy Act, GDPR, or similar regulations
- **Financial Liability**: Damages, legal fees, and potential fines

### Data Protection Laws

Extracting personal data (phone numbers) without consent likely violates:
- 🇺🇬 Uganda's Data Protection and Privacy Act (2019)
- 🇪🇺 GDPR (if any EU residents' data is involved)
- 🇺🇸 Various US state privacy laws (CCPA, etc.)
- 🌍 Other regional data protection regulations

### Ethical Considerations

**Why this matters:**
- Phone numbers are **personal information** that people expect to be protected
- Bulk extraction enables **spam, fraud, and harassment**
- Violates user expectations and **consent principles**
- Places undue burden on website infrastructure
- Undermines trust in online marketplaces

---

## What This Project Demonstrates

### Technical Skills Showcased

1. **Browser Automation**
   - Playwright async API with Python
   - Headed vs headless browser modes
   - Cookie injection for session management

2. **Dynamic Content Handling**
   - Clicking dynamically loaded elements
   - Dismissing popups automatically
   - Infinite scroll detection and processing

3. **Data Extraction Techniques**
   - DOM element scraping
   - JavaScript data extraction (`__NUXT_DATA__`)
   - HTML parsing with BeautifulSoup
   - Regular expression pattern matching

4. **Data Processing**
   - Phone number normalization (Ugandan format)
   - Deduplication using sets
   - Data filtering and exclusion lists

5. **Error Handling**
   - Timeout management
   - Graceful failure recovery
   - Logging and debugging

---

## Technical Features

### Core Capabilities (For Educational Reference)

- **Playwright-Powered**: Asynchronous browser automation with Chromium
- **Cookie Management**: Netscape HTTP Cookie File parsing and injection
- **Smart Page Detection**: Differentiates between category pages and single adverts
- **Infinite Scroll Handling**: Loads all content with configurable limits
- **Multi-Source Extraction**: Scans DOM, scripts, and HTML
- **Pattern Matching**: Validates and normalizes Ugandan phone numbers (07XXXXXXXX → +2567XXXXXXXX)
- **Global Deduplication**: Tracks visited URLs to prevent duplicate processing
- **Exclusion Lists**: Filters out specified numbers
- **Robust Error Handling**: Continues operation despite individual page failures

### Architecture Highlights

```
┌─────────────────┐
│  Cookie Loader  │ → Maintains session state
└────────┬────────┘
         ↓
┌─────────────────┐
│  Page Navigator │ → Handles URLs, detects page types
└────────┬────────┘
         ↓
┌─────────────────┐
│ Scroll Manager  │ → Loads infinite scroll content
└────────┬────────┘
         ↓
┌─────────────────┐
│ Data Extractor  │ → Multi-source phone number extraction
└────────┬────────┘
         ↓
┌─────────────────┐
│  Normalizer     │ → Validates, formats, deduplicates
└────────┬────────┘
         ↓
┌─────────────────┐
│  File Output    │ → Saves unique results
└─────────────────┘
```

---

## Prerequisites

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **pip** (Python package installer)
- **Basic understanding of web scraping ethics and laws**

---

## Installation (For Learning Only)

### ⚠️ Installation Does NOT Grant Permission to Use

Installing this code does **not** give you permission to scrape any website. Review each target site's Terms of Service and robots.txt before even considering use.

```bash
# Clone the repository
git clone https://github.com/yourusername/jiji-scraper.git
cd jiji-scraper

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

**requirements.txt:**
```
playwright
beautifulsoup4
```

---

## Legitimate Use Cases

### Where You CAN Use Similar Techniques

✅ **Your own websites** - Scrape sites you own or operate
✅ **With explicit permission** - Written authorization from website owners
✅ **Public APIs** - Use official APIs instead of scraping (Jiji.ug may offer APIs)
✅ **Academic research** - With IRB approval and proper consent mechanisms
✅ **Open data sources** - Government databases, public records with explicit scraping permissions
✅ **Test environments** - Practice sites designed for scraping education (e.g., books.toscrape.com)

### Recommended Learning Alternatives

Instead of scraping Jiji.ug, practice on:

1. **http://books.toscrape.com** - Specifically designed for scraping practice
2. **https://quotes.toscrape.com** - Quote scraping sandbox
3. **Your own local test server** - Build a dummy site to practice on
4. **Jiji.ug's API** (if available) - Contact them about legitimate data access

### How to Do This Legally

If you need real marketplace data:

1. **Contact Jiji Support**: Email support@jiji.ug requesting:
   - Research partnership opportunities
   - Official API access
   - Data licensing agreements
   
2. **Academic Research Protocol**:
   - Get IRB (Institutional Review Board) approval
   - Request formal permission from Jiji
   - Implement proper consent mechanisms
   - Limit scope and ensure data protection

3. **Commercial Licensing**:
   - Negotiate data licensing agreements
   - Pay for official data access
   - Sign proper legal contracts

---

## How the Code Works

### (Technical Documentation for Learning)

#### 1. Cookie Management

```python
# Loads Netscape format cookies
cookies = load_cookies_from_netscape_file("jiji.ug_cookies.txt")
await context.add_cookies(cookies)
```

Maintains authenticated sessions to avoid login prompts and access restrictions.

#### 2. Page Type Detection

```python
if "/tv-dvd-equipment" in url and not url.endswith(".html"):
    # Category page - use infinite scroll
    await handle_category_page(page, url)
else:
    # Single advert page - extract directly
    await extract_from_advert(page, url)
```

#### 3. Infinite Scroll Implementation

```python
while scroll_count < max_scrolls:
    previous_ads = current_ad_count
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    await page.wait_for_timeout(2000)
    current_ad_count = await page.locator(".ad-selector").count()
    
    if current_ad_count == previous_ads:
        break  # No new content
```

#### 4. Phone Number Extraction

```python
# Pattern matches Ugandan numbers: 07XXXXXXXX
pattern = r'\b(0[7][0-9]{8})\b'
matches = re.findall(pattern, text)

# Normalize to international format
normalized = [f"+256{num[1:]}" for num in matches]
```

#### 5. Multi-Source Scanning

- **DOM Elements**: `.b-show-contacts-popover-item__phone`
- **Script Content**: `__NUXT_DATA__` JSON parsing
- **Full HTML**: BeautifulSoup text extraction
- **Visible Text**: Page content including comments

---

## Learning Resources

### Web Scraping Ethics & Law

- [Web Scraping Best Practices](https://www.scrapinghub.com/guides/web-scraping-best-practices/)
- [Legal Risks of Web Scraping (2024)](https://blog.apify.com/is-web-scraping-legal/)
- [GDPR and Web Scraping](https://gdpr.eu/data-scraping/)

### Playwright Documentation

- [Official Playwright Docs](https://playwright.dev/python/)
- [Playwright Authentication Guide](https://playwright.dev/python/docs/auth)
- [Handling Dynamic Content](https://playwright.dev/python/docs/navigations)

### Python Web Scraping

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Regular Expressions in Python](https://docs.python.org/3/howto/regex.html)
- [Async/Await in Python](https://realpython.com/async-io-python/)

### Ethical Alternatives

- [Public APIs List](https://github.com/public-apis/public-apis)
- [Practice Scraping Sites](http://toscrape.com/)
- [Web Scraping Sandbox](https://www.scrapethissite.com/)

---

## Contributing

This is an educational project demonstrating web scraping techniques. Contributions are welcome that:

- ✅ Improve code quality and documentation
- ✅ Add ethical considerations and warnings
- ✅ Enhance error handling and robustness
- ✅ Demonstrate alternative, legal approaches
- ✅ Add educational comments and explanations

**We will NOT accept:**
- ❌ Features that facilitate Terms of Service violations
- ❌ Removal of warnings or ethical disclaimers
- ❌ Guides for bypassing security measures
- ❌ Anything that encourages misuse

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/educational-improvement`)
3. Commit your changes (`git commit -am 'Add educational content'`)
4. Push to the branch (`git push origin feature/educational-improvement`)
5. Open a Pull Request

---

## License

See [LICENSE](LICENSE) file for details.

**Additional Restrictions:**
- This code may NOT be used to violate any website's Terms of Service
- Commercial use for data harvesting is prohibited
- Users must obtain explicit permission before scraping any platform
- This code is provided for educational demonstration only

---

## Final Warning

**TO USERS**: Do not use this tool on Jiji.ug or any other platform without:
1. ✅ Reading and understanding their Terms of Service
2. ✅ Obtaining explicit written permission
3. ✅ Ensuring compliance with all applicable laws
4. ✅ Implementing proper consent and data protection measures

**TO RECRUITERS/EMPLOYERS**: This repository demonstrates technical proficiency in web automation, not actual deployment. It showcases understanding of:
- Browser automation with Playwright
- Asynchronous Python programming
- Data extraction and processing
- Legal and ethical considerations in software development

**THE AUTHOR ASSUMES NO LIABILITY FOR MISUSE OF THIS CODE.**

---

## Contact & Support

For questions about:
- **Technical implementation**: Open a GitHub issue
- **Legal compliance**: Consult a qualified attorney
- **Ethical considerations**: Review provided resources above
- **Jiji.ug data access**: Contact support@jiji.ug directly

**Remember**: The best scraping is the scraping you don't have to do. Always check for official APIs first.

---

*This project is maintained for educational purposes only. Last Updated: November 2025*
