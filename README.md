# Naukri Job Scraper

A Python-based web scraping application using Playwright to collect job listings from Naukri.com and store them in an Excel file.

## Project Objective

The purpose of this project is to scrape Python Developer job listings from Naukri.com for Chennai and save the job information into an Excel file.

The scraper also checks the existing Excel file on every run and adds only new jobs. Previously scraped jobs are preserved.

## Technologies Used

- Python
- Playwright
- Pandas
- OpenPyXL
- Microsoft Excel

## Job Details Scraped

The application collects the following information:

- Job Title
- Company
- Location
- Experience
- Skills
- Posted Date
- Job URL

## Project Structure

```text
naukri-job-scraper/
│
├── scraper.py
├── requirements.txt
├── README.md
├── scraper.log
├── naukri_jobs.xlsx
└── venv/