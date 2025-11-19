# Jiji.ug Phone Number Scraper (Playwright)

## Overview

This is an advanced, robust web scraping tool designed to extract Ugandan phone numbers from product advert pages and category listings on Jiji.ug. It leverages Playwright for efficient browser automation, handling dynamic content, interacting with elements like "Show contact" buttons, and navigating category pages that use infinite scrolling.

The tool uses pre-obtained cookies to maintain your logged-in Jiji session (avoiding sign-in popups and language prompts). It extracts phone numbers from:

* The contacts popover opened via the "Show contact" button.
* Jiji's embedded `__NUXT_DATA__` script content (treated as plain text).
* The full HTML and visible text of each advert page, including comments.

## Features

*   **Playwright-Powered Automation:** Uses Playwright's asynchronous API with Chromium. By default, the script runs in *headed* mode (`headless=False`) because Jiji may hide contacts when running fully headless. You can change this in `main_scraper` if desired.
*   **Dynamic Content Handling:**
*   *   Automatically clicks the "Show contact" button (using Jiji's CSS classes) on product detail pages to reveal dynamically loaded phone numbers.
*   *   Automatically dismisses the "Which language do you prefer?" popup by clicking **Save** if it appears.
*   *   Detects whether a URL is a **category listing** (with many adverts) or a **single advert page**, and handles each appropriately.
*   **Comprehensive Number Extraction:**
*   *   Scans the `__NUXT_DATA__` script content as plain text for any matching phone patterns.
*   *   Reads numbers from the contacts popover DOM (`div.b-show-contacts-popover-item__phone`).
*   *   Scans the full HTML and rendered text (including comments) for extra occurrences of valid numbers.
*   **Strict Mobile Number Normalization:**
*   *   Only accepts *local* Ugandan mobile numbers in the form `07XXXXXXXX` (exactly 10 digits starting with `07`).
*   *   Every valid match is normalized to `+2567XXXXXXXX`.
*   *   All numbers are stored in a Python `set` so only **unique** values are written to the output file.
*   **Cookie-Based Session Management:**
*   *   Injects pre-obtained cookies (from a `Netscape HTTP Cookie File`) to maintain session state, including authentication.
*   *   All cookies from `jiji.ug_cookies.txt` are loaded into the Playwright context; no filtering by subdomain or path is applied.
*   **Multi-Category & Single-Ad Scraping:** Accepts a list of Jiji URLs that can be:
*   *   Category pages (e.g., `https://jiji.ug/tv-dvd-equipment`).
*   *   Direct advert pages (e.g., a single product URL).
*   **Intelligent Infinite Scrolling:**
*   *   Supports infinite scrolling until no new ads are detected, with an optional maximum scroll limit per category.
*   *   Canonicalizes advert URLs (stripping query parameters like `?page=...`) and tracks them globally so the same ad is never revisited due to tracking parameters.
*   **Exclude Your Own Numbers:** Allows you to configure a list of your own `07XXXXXXXX` numbers to be excluded from all results.
*   **Robust Error Handling:** Catches and logs common scraping issues (timeouts, selector failures, closed browser) while allowing the process to continue and shut down cleanly.

## Prerequisites

Before running the scraper, ensure you have the following installed:

1.  **Python 3.8+**:
    Download and install Python from [python.org](https://www.python.org/downloads/).

2.  **Playwright Browser Binaries**:
    Playwright requires browser engines to operate. After installing the Python library, you'll need to install these executables.

## Setup

1.  **Save the Script:**
    Save the provided Python code as `jiji_scraper.py` in your desired project directory.

2.  **Create `requirements.txt`:**
    Create a file named `requirements.txt` in the same directory as your `jiji_scraper.py` file and add the following content:

    ```
    playwright
    beautifulsoup4
    ```

3.  **Install Python Dependencies:**
    Open your terminal or command prompt, navigate to the directory where you saved the files, and run:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright Browser Drivers:**
    Playwright manages its browser binaries automatically. Install them by running:

    ```bash
    playwright install
    ```
    This command will download and set up Chromium, Firefox, and WebKit browsers that Playwright uses. You do *not* need to download separate `chromedriver` or `geckodriver` files.

## Obtaining `jiji.ug_cookies.txt`

The scraper relies on pre-obtained cookies to function effectively. You'll need to export your Jiji.ug cookies from your web browser.

**Recommended Method (using a browser extension):**

1.  **Install a "Cookies.txt" Extension:**
    *   **For Chrome:** Search for "Cookies.txt" or "Netscape format cookies" extensions in the Chrome Web Store (e.g., "Get cookies.txt").
    *   **For Firefox:** Search for similar extensions in the Firefox Add-ons store.
2.  **Log in to Jiji.ug (optional, but recommended):**
    Open your browser, navigate to [jiji.ug](https://www.jiji.ug/), and log in to your account. This ensures you obtain any authentication-related cookies. Even if not logged in, visit a few pages to gather general session cookies.
3.  **Export Cookies:**
    Click on the installed extension's icon. It should provide an option to "Export" or "Save" cookies. **Ensure you select an option that saves them in the "Netscape HTTP Cookie File" format.**
4.  **Save the File:**
    Save the exported file as `jiji.ug_cookies.txt` in the same directory as your `jiji_scraper.py` script (or update `cookie_file` accordingly).

**Expected `jiji.ug_cookies.txt` Format (Netscape HTTP Cookie File):**

The scraper is specifically designed to parse this format. Each relevant line in the file should be tab-separated, similar to this example:

Netscape HTTP Cookie File
(header lines)
jiji.ug FALSE /central-division/video-games-and-consoles FALSE 1790804244 change-language-popup 1
.jiji.ug TRUE / TRUE 1795071664 uid 68dc4d849277aa826d69a67fd826f0da4e5dd0f1
jiji.ug FALSE / FALSE 1790804228 lang en
... other cookie entries

All cookies from this file are loaded into Playwright as-is. For best results, export cookies from a browser session where you are already logged in to Jiji.ug.

## Configuration

Open `jiji_scraper.py` and modify the `if __name__ == "__main__":` block to suit your needs:

*   **`jiji_category_urls`**:
    This list contains the starting URLs you wish to scrape. You can add or remove URLs here. Each URL can be either a **category** page or a **single advert** page.

    ```python
    jiji_category_urls = [
        "https://jiji.ug/tv-dvd-equipment",  # Category URL
        # "https://jiji.ug/central-division/tv-dvd-equipment/...ad.html",  # Optional: direct advert URL
        # Add more URLs as needed
    ]
    ```

*   **`cookie_file`**:
    The path to your `jiji.ug_cookies.txt` file. Ensure it matches the location where you saved your cookies.

    ```python
    cookie_file = "jiji.ug_cookies.txt"
    ```

*   **`output_filename`** (parameter of `main_scraper`):
    The name of the text file where the extracted unique phone numbers will be saved. By default this is `jiji_phone_numbers.txt`.

*   **`scroll_until_done`**:
    A boolean (`True`/`False`) to control the infinite scrolling behavior within each category.
*   *   Set to `True` (recommended for comprehensive scraping) to make the scraper continuously scroll down until no more **new** ads are detected on the page.
*   *   Set to `False` if you only want to scroll a fixed number of times, controlled by `max_scroll_actions_per_category`.

    ```python
    # OPTION 1 (Recommended): Scroll until all ads are loaded (with an optional safety limit)
    asyncio.run(
        main_scraper(
            jiji_category_urls,
            cookie_file,
            scroll_until_done=True,
            max_scroll_actions_per_category=10,
        )
    )
    ```

*   **`max_scroll_actions_per_category`**:
    An optional integer.
*   *   If `scroll_until_done` is `True`, this acts as a hard limit on the number of scroll actions to prevent endless loops on problematic pages. The scraper will stop after this many scrolls *or* when no new content is detected, whichever comes first.
*   *   If `scroll_until_done` is `False`, this explicitly defines the fixed number of times the scraper will scroll down within each category.

    ```python
    # OPTION 2: Scroll a maximum number of times (e.g., 5 scroll actions)
    asyncio.run(
        main_scraper(
            jiji_category_urls,
            cookie_file,
            scroll_until_done=False,
            max_scroll_actions_per_category=5,
        )
    )
    ```

*   **`exclude_numbers_local` / `my_numbers_to_exclude`**:
    A list of your own `07XXXXXXXX` numbers (local format) that should be **excluded** from all results.

    ```python
    my_numbers_to_exclude = [
        "0700000000",  # Example: your personal number
        # Add more of your own 07XXXXXXXX numbers here
    ]

    asyncio.run(
        main_scraper(
            jiji_category_urls,
            cookie_file,
            scroll_until_done=False,
            max_scroll_actions_per_category=5,
            exclude_numbers_local=my_numbers_to_exclude,
        )
    )
    ```

## How to Run

After configuring the script and ensuring all prerequisites are met, run the Python script from your terminal:

```bash
python jiji_scraper.py
