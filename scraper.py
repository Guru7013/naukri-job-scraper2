import logging
from pathlib import Path
import pandas as pd
from playwright.sync_api import sync_playwright

SEARCH_URL = (
    "https://www.naukri.com/python-developer-jobs-in-chennai"
    "?k=python%20developer&l=chennai&experience=0"
)

EXCEL_FILE = Path("naukri_jobs.xlsx")

COLUMNS = [
    "Title",
    "Company",
    "Location",
    "Experience",
    "Skills",
    "Posted Date",
    "Job URL",
]

logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def clean_text(text):
    if not text:
        return ""
    return " ".join(text.split())


def load_existing_jobs():
    if not EXCEL_FILE.exists():
        return pd.DataFrame(columns=COLUMNS)

    try:
        df = pd.read_excel(EXCEL_FILE)

        for column in COLUMNS:
            if column not in df.columns:
                df[column] = ""

        return df[COLUMNS]

    except Exception as e:
        logging.error("Excel read error: %s", e)
        return pd.DataFrame(columns=COLUMNS)


def scrape_jobs(page):
    jobs = []

    print("Opening Naukri page...")

    try:
        page.goto(
            SEARCH_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        print("Naukri page opened...")
        page.wait_for_timeout(5000)

        # Close popup if present
        for selector in [
            "button[aria-label='Close']",
            ".crossIcon",
            ".close"
        ]:
            try:
                page.locator(selector).first.click(timeout=1500)
                break
            except Exception:
                pass

        print("Checking job listings...")

        # Wait for job cards
        try:
            page.wait_for_selector(
                "article.jobTuple, .srp-jobtuple-wrapper",
                timeout=15000
            )
        except Exception:
            print("Job cards were not found immediately.")

        # Scroll to load more jobs
        for _ in range(3):
            page.mouse.wheel(0, 2500)
            page.wait_for_timeout(2000)

        cards = page.locator(
            "article.jobTuple, .srp-jobtuple-wrapper"
        )

        count = cards.count()

        print(f"Job cards found: {count}")

        for i in range(count):

            try:
                card = cards.nth(i)

                title = ""
                company = ""
                location = ""
                experience = ""
                skills = ""
                posted_date = ""
                job_url = ""

                # Title + URL
                try:
                    title_locator = card.locator(
                        "a.title, a[href*='/job-listings/']"
                    ).first

                    title = clean_text(
                        title_locator.inner_text()
                    )

                    job_url = (
                        title_locator.get_attribute("href")
                        or ""
                    )

                except Exception:
                    pass

                # Company
                for selector in [
                    ".comp-name",
                    ".companyInfo a",
                    "a.subTitle"
                ]:
                    try:
                        company = clean_text(
                            card.locator(
                                selector
                            ).first.inner_text()
                        )

                        if company:
                            break

                    except Exception:
                        pass

                # Location
                for selector in [
                    ".locWdth",
                    ".location",
                    ".job-location"
                ]:
                    try:
                        location = clean_text(
                            card.locator(
                                selector
                            ).first.inner_text()
                        )

                        if location:
                            break

                    except Exception:
                        pass

                # Experience
                for selector in [
                    ".expwdth",
                    ".experience"
                ]:
                    try:
                        experience = clean_text(
                            card.locator(
                                selector
                            ).first.inner_text()
                        )

                        if experience:
                            break

                    except Exception:
                        pass

                # Skills
                try:
                    skill_nodes = card.locator(
                        ".tags-gt, .skills, .skill"
                    )

                    skill_list = []

                    for j in range(skill_nodes.count()):

                        text = clean_text(
                            skill_nodes.nth(j).inner_text()
                        )

                        if text:
                            skill_list.append(text)

                    skills = ", ".join(skill_list)

                except Exception:
                    pass

                # Posted date
                for selector in [
                    ".job-post-day",
                    ".job-post-date"
                ]:
                    try:
                        posted_date = clean_text(
                            card.locator(
                                selector
                            ).first.inner_text()
                        )

                        if posted_date:
                            break

                    except Exception:
                        pass

                # Convert relative URL to full URL
                if job_url.startswith("/"):
                    job_url = (
                        "https://www.naukri.com"
                        + job_url
                    )

                # Save only valid jobs
                if title and job_url:

                    jobs.append({
                        "Title": title,
                        "Company": company,
                        "Location": location,
                        "Experience": experience,
                        "Skills": skills,
                        "Posted Date": posted_date,
                        "Job URL": job_url,
                    })

                    print(f"Scraped: {title}")

            except Exception as e:

                logging.error(
                    "Error scraping card %s: %s",
                    i,
                    e
                )

        print(f"Total jobs scraped: {len(jobs)}")

    except Exception as e:

        logging.error(
            "Scraping failed: %s",
            e
        )

        print("Scraping error:", e)

    return jobs


def save_jobs(new_jobs):

    existing_df = load_existing_jobs()

    if not new_jobs:

        print("No jobs scraped.")
        return

    new_df = pd.DataFrame(
        new_jobs,
        columns=COLUMNS
    )

    # Remove duplicates from current scraping
    new_df = new_df.drop_duplicates(
        subset=["Job URL"]
    )

    # Existing URLs
    existing_urls = set(
        existing_df["Job URL"]
        .dropna()
        .astype(str)
    )

    # Keep only NEW jobs
    new_df = new_df[
        ~new_df["Job URL"]
        .astype(str)
        .isin(existing_urls)
    ]

    if new_df.empty:

        print(
            "No NEW jobs found. "
            "Excel file is unchanged."
        )

        return

    # Add new jobs to old jobs
    final_df = pd.concat(
        [
            existing_df,
            new_df
        ],
        ignore_index=True
    )

    # Final duplicate protection
    final_df = final_df.drop_duplicates(
        subset=["Job URL"],
        keep="first"
    )

    # Save Excel
    final_df.to_excel(
        EXCEL_FILE,
        index=False,
        engine="openpyxl"
    )

    print(
        f"Added {len(new_df)} new jobs."
    )

    print(
        f"Total jobs in Excel: {len(final_df)}"
    )


def main():

    print("=" * 50)
    print("Starting Naukri Job Scraper...")
    print("=" * 50)

    logging.info("Scraper started.")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page(
            viewport={
                "width": 1366,
                "height": 768
            }
        )

        try:

            jobs = scrape_jobs(page)

            print(
                f"Scraped {len(jobs)} jobs."
            )

            save_jobs(jobs)

        except Exception as e:

            logging.error(
                "Main error: %s",
                e
            )

            print(
                "An error occurred."
            )

            print(
                "Check scraper.log"
            )

        finally:

            browser.close()

    logging.info("Scraper finished.")

    print("=" * 50)
    print("Scraper finished.")
    print("=" * 50)


if __name__ == "__main__":
    main()