# Job scrapper

## Overview

This Python script scrapes job details from the **CHwapi job portal**, extracting titles, URLs, phone numbers, and email addresses. It stores the data in an Excel file.

## Requirements

- python 3.8
- BeautifulSoup
- requests
- xlsxwriter
- phonenumbers


## Important note
During phone number extraction, the script excludes the phone number associated with the job portal.

## Usage

1. Clone the repository.
2. Install the required packages using `pip install -r requirements.txt`.
3. Run the script: `python job_scraper.py`.
4. Check the generated Excel file `job_offers.xlsx` for job details.

## Job Data

The script extracts job details such as title, URL, phone numbers, and email addresses. Here is a preview of the extracted data. **The job link, phone numbers and email addresses in this table are not real**:

| Title                                         | URL                                                      | Phone Numbers                  | Email Addresses                                     |
|-----------------------------------------------|----------------------------------------------------------|--------------------------------|-----------------------------------------------------|
| Employé enregistrement médical RCM (F/H/X)     | [Link](https://exemple-link.com/job1)                    | +32 123 456 789                | job1@example.com                                    |
| Sage-femme (H/F/X) - temps plein - Contrat...  | [Link](https://exemple-link.com/job2)                    | +32 987 654 321                | job2@example.com                                    |
| ...                                           | ...                                                      | ...                            | ...                                                 |
