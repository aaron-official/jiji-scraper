import asyncio
import re
import json
from playwright.async_api import async_playwright, Playwright, Page
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def load_cookies_from_txt_for_playwright(filepath):
    """
    Loads cookies from a Netscape HTTP Cookie File, filtering for 'Include Subdomains = TRUE' and 'Path = /',
    and formats them for Playwright.
    """
    cookies_list = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split('\t')
                if len(parts) >= 7:
                    domain, include_subdomains_flag, path, secure, expiry, name, value = parts[:7]
                    
                    # Load all cookies from the Netscape file as-is into Playwright
                    is_secure = secure.lower() == 'true'

                    expires_timestamp = int(expiry) if expiry.isdigit() else -1
                    if expires_timestamp == 0:
                        expires_timestamp = -1

                    cookies_list.append({
                        'name': name,
                        'value': value,
                        'domain': domain,
                        'path': path,
                        'secure': is_secure,
                        'expires': expires_timestamp,
                        'sameSite': 'Lax'
                    })
        return cookies_list
    except FileNotFoundError:
        print(f"Error: Cookie file not found at {filepath}. Please ensure it exists.")
        return None
    except Exception as e:
        print(f"Error loading cookies for Playwright: {e}")
        return None

def normalize_phone_number(number_str):
    """Normalizes a Ugandan phone number to +256 format."""
    cleaned_number = re.sub(r'\D', '', number_str)
    
    # Only accept local Ugandan mobile numbers in the form 07XXXXXXXX (exactly 10 digits).
    if not re.fullmatch(r'07\d{8}', cleaned_number):
        return cleaned_number

    # 07XXXXXXXX (10 digits) -> +2567XXXXXXXX
    return '+256' + cleaned_number[1:]

async def scrape_jiji_category_for_numbers(
    page: Page,
    category_url: str,
    all_phone_numbers_set: set,
    visited_ad_urls_set: set, # Now explicitly passed and used to track visited ads
    scroll_until_done: bool = True, # New option to control scrolling behavior
    max_scroll_actions_per_category: int = None, # Optional limit for scroll actions
    base_domain: str = "",
    excluded_numbers_normalized: set | None = None,
):
    """
    Scrapes phone numbers from a single Jiji.ug category URL using an existing Playwright Page
    and handling infinite scrolling until no new ads are loaded or a max scroll limit is reached.
    """
    # Restrict regex scanning strictly to local 07XXXXXXXX numbers (10 digits starting with 07)
    ugandan_phone_regex = r'(?<!\d)07\d{8}(?!\d)'

    print(f"\nStarting scraping for category: {category_url}")

    try:
        await page.goto(category_url, wait_until="domcontentloaded")

        # Dismiss language selection popup if it appears
        try:
            language_save_button = page.locator('text=Save').first
            await language_save_button.click(timeout=3000)
            await asyncio.sleep(0.5)
        except Exception:
            pass

        # Detect whether this URL is a category listing (with advert list) or a direct advert page.
        is_category_page = True
        try:
            await page.wait_for_selector('div.qa-advert-listing', timeout=20000)
        except Exception:
            is_category_page = False

        if is_category_page:
            await asyncio.sleep(3) # Initial pause for content to settle

        previous_ad_count = 0
        scroll_count = 0

        while True:
            # Get current visible ad links before scrolling
            if is_category_page:
                current_ad_elements = await page.locator('div.qa-advert-listing a.qa-advert-list-item').all()
                current_visible_ad_links = set()
                for ad in current_ad_elements:
                    href = await ad.get_attribute('href')
                    if not href:
                        continue
                    full_url = f"{base_domain}{href}" if href.startswith('/') else href
                    # Canonicalize ad URL by stripping query and fragment so the same ad
                    # is not revisited just because tracking parameters changed.
                    parsed = urlparse(full_url)
                    canonical_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                    current_visible_ad_links.add(canonical_url)
            else:
                # If this is a direct advert URL, just process this single page as an ad.
                current_visible_ad_links = {category_url}

            # Check if any new ads were loaded in the previous scroll or initial load
            if len(current_visible_ad_links) == previous_ad_count and scroll_count > 0:
                print(f"  No new unique ads detected after scroll {scroll_count}. Ending infinite scroll for this category.")
                break

            # Process newly found ads
            newly_found_ad_links = []
            for ad_url in current_visible_ad_links:
                if ad_url not in visited_ad_urls_set:
                    newly_found_ad_links.append(ad_url)
            
            print(f"  Found {len(newly_found_ad_links)} new unique ads on this step. Total ads visible: {len(current_visible_ad_links)}")

            # Visit and scrape each newly found ad
            for full_ad_url in newly_found_ad_links:
                print(f"    Visiting ad: {full_ad_url}")
                visited_ad_urls_set.add(full_ad_url) # Mark as visited to prevent future re-processing

                try:
                    await page.goto(full_ad_url, wait_until="domcontentloaded")
                    await page.wait_for_selector('h1.qa-advert-title', timeout=15000) # Increased wait
                    await asyncio.sleep(1)

                    # --- Extract numbers from __NUXT_DATA__ script tag ---
                    nuxt_data_script = None
                    try:
                        nuxt_data_script = await page.locator('script[id="__NUXT_DATA__"]').first.text_content(timeout=2000)
                    except Exception:
                        nuxt_data_script = None
                    if nuxt_data_script:
                        try:
                            # Treat the script content as plain text and run the 07-number regex on it directly
                            found_numbers_nuxt = re.findall(ugandan_phone_regex, nuxt_data_script)
                            for match_str in found_numbers_nuxt:
                                raw_str = match_str.strip()
                                full_number = normalize_phone_number(raw_str)
                                if len(full_number) >= 10:
                                    if excluded_numbers_normalized and full_number in excluded_numbers_normalized:
                                        continue
                                    if full_number not in all_phone_numbers_set:
                                        all_phone_numbers_set.add(full_number)
                                        print(f"      Phone: {raw_str} -> {full_number}")
                        except Exception as e:
                            print(f"    Error processing __NUXT_DATA__ for {full_ad_url}: {e}")

                    # --- Handle "Show contact" button ---
                    try:
                        # Match any element (div or a) with the Show contact classes
                        show_contact_button_locator = page.locator(
                            '.qa-show-contact.cy-show-contact.js-show-contact.b-show-contact'
                        )
                        show_btn_count = await show_contact_button_locator.count()
                        print(f"      Show contact buttons matched: {show_btn_count}")
                        if show_btn_count > 0:
                            # Click the last Show contact button (seller block) which typically opens the popover
                            target_btn = show_contact_button_locator.nth(show_btn_count - 1)
                            await target_btn.click(timeout=8000)
                            # Give the popover a moment to render
                            await asyncio.sleep(2)
                    except Exception:
                        pass # Suppress frequent "no button" or popover errors

                    # --- Extract numbers from contacts popover (primary source) ---
                    try:
                        phone_locator = page.locator('div.b-show-contacts-popover-item__phone')
                        phone_texts = await phone_locator.all_text_contents()
                        print(f"      Popover phone elements found: {len(phone_texts)}")
                        for raw_str in (t.strip() for t in phone_texts):
                            if not raw_str:
                                continue
                            full_number = normalize_phone_number(raw_str)
                            if len(full_number) >= 10:
                                if excluded_numbers_normalized and full_number in excluded_numbers_normalized:
                                    continue
                                if full_number not in all_phone_numbers_set:
                                    all_phone_numbers_set.add(full_number)
                                    print(f"      Phone: {raw_str} -> {full_number}")
                    except Exception:
                        pass

                    # --- Extract numbers from current page source (including revealed numbers) ---
                    ad_html_content = await page.content()

                    # First, scan the full HTML markup (including attributes like tel: links).
                    found_numbers_in_html = re.findall(ugandan_phone_regex, ad_html_content)
                    for match_str in found_numbers_in_html:
                        raw_str = match_str.strip()
                        full_number = normalize_phone_number(raw_str)
                        if len(full_number) >= 10:
                            if excluded_numbers_normalized and full_number in excluded_numbers_normalized:
                                continue
                            if full_number not in all_phone_numbers_set:
                                all_phone_numbers_set.add(full_number)
                                print(f"      Phone: {raw_str} -> {full_number}")

                    # Then, parse the rendered HTML and scan only visible text content.
                    ad_soup = BeautifulSoup(ad_html_content, 'html.parser')
                    page_text = ad_soup.get_text()

                    found_numbers_on_page = re.findall(ugandan_phone_regex, page_text)
                    for match_str in found_numbers_on_page:
                        raw_str = match_str.strip()
                        full_number = normalize_phone_number(raw_str)
                        if len(full_number) >= 10:
                            if excluded_numbers_normalized and full_number in excluded_numbers_normalized:
                                continue
                            if full_number not in all_phone_numbers_set:
                                all_phone_numbers_set.add(full_number)
                                print(f"      Phone: {raw_str} -> {full_number}")

                    # --- Extract numbers from comments section (if identifiable) ---
                    comment_sections = ad_soup.select('div.b-comments, ul.b-comments__list, div[data-qa-comments-section]')
                    for comment_section in comment_sections:
                        comment_text = comment_section.get_text()
                        found_numbers_in_comments = re.findall(ugandan_phone_regex, comment_text)
                        for match_str in found_numbers_in_comments:
                            raw_str = match_str.strip()
                            full_number = normalize_phone_number(raw_str)
                            if len(full_number) >= 10:
                                if excluded_numbers_normalized and full_number in excluded_numbers_normalized:
                                    continue
                                if full_number not in all_phone_numbers_set:
                                    all_phone_numbers_set.add(full_number)
                                    print(f"      Phone: {raw_str} -> {full_number}")

                except Exception as e:
                    print(f"    Error processing ad page {full_ad_url}: {e}")
                finally:
                    # After processing an ad, navigate back to the category listing page
                    # to continue scrolling or visiting other ads in the current view.
                    # This is crucial to keep the infinite scroll context.
                    if is_category_page:
                        await page.goto(category_url, wait_until="domcontentloaded")
                        await page.wait_for_selector('div.qa-advert-listing', timeout=10000)
                        await asyncio.sleep(2)
            
            # Update previous_ad_count for the next iteration's comparison
            previous_ad_count = len(current_visible_ad_links)

            # For direct advert pages, do not attempt infinite scrolling; process once and exit.
            if not is_category_page:
                break

            # Perform scroll only if 'scroll_until_done' is True OR if we have a max_scroll_actions_per_category limit
            if scroll_until_done or (max_scroll_actions_per_category is not None and scroll_count < max_scroll_actions_per_category):
                scroll_count += 1
                if max_scroll_actions_per_category is not None and scroll_count > max_scroll_actions_per_category:
                    print(f"  Reached maximum scroll actions ({max_scroll_actions_per_category}). Ending scroll for this category.")
                    break
                
                print(f"  Scrolling down (scroll attempt {scroll_count})...")
                last_height = await page.evaluate('document.body.scrollHeight')
                await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                await asyncio.sleep(3) # Give time for new content to load

                new_height = await page.evaluate('document.body.scrollHeight')

                # Check if the page actually scrolled or new content loaded (height increased)
                if new_height == last_height:
                    print("  No new content loaded after scrolling (page height did not change). Ending infinite scroll for this category.")
                    break
            else:
                break # Exit if not scrolling until done and no max scroll is set

    except Exception as e:
        print(f"  An error occurred while processing category '{category_url}': {e}")
            
    print(f"Finished scraping category: {category_url}")


async def main_scraper(
    category_urls: list[str],
    cookies_filepath: str,
    output_filename: str = "jiji_phone_numbers.txt",
    scroll_until_done: bool = True, # Default to scroll until all ads are loaded
    max_scroll_actions_per_category: int = None, # Optional maximum scroll actions
    exclude_numbers_local: list[str] | None = None,
):
    """
    Main function to orchestrate scraping across multiple Jiji categories,
    handling infinite scrolling until all ads are loaded or a max limit is reached.
    """
    all_phone_numbers = set()
    visited_ad_urls_set = set() # Dedicated set to track ALL visited ad URLs across categories

    excluded_numbers_normalized = set()
    if exclude_numbers_local:
        for raw in exclude_numbers_local:
            normalized = normalize_phone_number(raw)
            if normalized and len(normalized) >= 10:
                excluded_numbers_normalized.add(normalized)

    if not category_urls:
        print("No category URLs provided. Exiting.")
        return
    parsed_first_url = urlparse(category_urls[0])
    base_domain = f"{parsed_first_url.scheme}://{parsed_first_url.netloc}"

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        
        cookies = load_cookies_from_txt_for_playwright(cookies_filepath)
        if not cookies:
            try:
                await browser.close()
            except Exception:
                pass
            return

        context = await browser.new_context()
        await context.add_cookies(cookies)
        print("Filtered cookies injected successfully into Playwright context.")

        page = await context.new_page()
        page.set_default_timeout(60000)
        
        for category_url in category_urls:
            await scrape_jiji_category_for_numbers(
                page,
                category_url,
                all_phone_numbers,
                visited_ad_urls_set, # Pass the global visited_ad_urls_set
                scroll_until_done,
                max_scroll_actions_per_category,
                base_domain,
                excluded_numbers_normalized
            )
        
        try:
            await browser.close()
        except Exception as e:
            print(f"Error while closing browser: {e}")

    with open(output_filename, 'w') as f:
        for number in sorted(list(all_phone_numbers)):
            f.write(number + '\n')
    print(f"\nTotal scraping complete. Found {len(all_phone_numbers)} unique phone numbers across all categories.")
    print(f"Numbers saved to {output_filename}")


# --- How to run the tool ---
if __name__ == "__main__":
    jiji_category_urls = [
        "https://jiji.ug/tv-dvd-equipment",
        # Add more category URLs as needed
    ]
    
    cookie_file = "jiji.ug_cookies.txt" 

    # List any of your own numbers here (local 07XXXXXXXX format) to exclude them from results.
    my_numbers_to_exclude = [
        "0780363182",  # Example: your personal number
        # Add more 07XXXXXXXX numbers here if needed
    ]
    
    # OPTION 1: Scroll until all ads are loaded (recommended for comprehensive scraping)
    # asyncio.run(main_scraper(jiji_category_urls, cookie_file, scroll_until_done=True, exclude_numbers_local=my_numbers_to_exclude))

    # OPTION 2: Scroll a maximum number of times (e.g., 5 scroll actions)
    # This acts as a safety limit or for quick testing.
    asyncio.run(main_scraper(
        jiji_category_urls,
        cookie_file,
        scroll_until_done=False,
        max_scroll_actions_per_category=5,
        exclude_numbers_local=my_numbers_to_exclude,
    ))

    # OPTION 3: To scroll until done, but with a hard limit in case of issues (e.g., max 10 scrolls)
    # asyncio.run(main_scraper(jiji_category_urls, cookie_file, scroll_until_done=True, max_scroll_actions_per_category=10, exclude_numbers_local=my_numbers_to_exclude))