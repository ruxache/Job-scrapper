from bs4 import BeautifulSoup
import requests
import xlsxwriter
import phonenumbers
import re

def url(index):
    '''
    Returns the URL of the job offers page
    '''
    return 'https://emploi.chwapi.be/fr/vacatures/p/' + str(index) + '/index.aspx'

def get_last_index():
    '''
    Returns the last index of the job offers
    '''
    index = 1
    while True:
        response = requests.get(url(index))
        soup = BeautifulSoup(response.text, 'html.parser')
        page_number_span = soup.find('span', {'class': 'pageNumDisabled'})
        if not page_number_span:
            break
        index += 1
    return index

def extract_phone_numbers(text):
    phone_numbers = []
    
    # define the job website's phone number to exclude
    job_website_phone_number = "+32 (0)69 333 111"
    
    for match in phonenumbers.PhoneNumberMatcher(text, "BE"):
        formatted_number = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)
        
        # exclude the job website's phone number
        if formatted_number != phonenumbers.format_number(phonenumbers.parse(job_website_phone_number, "BE"), phonenumbers.PhoneNumberFormat.E164):
            phone_numbers.append(formatted_number)
    
    return phone_numbers

def extract_email_addresses(text):
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    return re.findall(email_pattern, text)

def get_job_details(title, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # extract contact information from entire page content
    page_content = soup.get_text()

    # check if there are phone numbers before extracting
    phone_numbers = extract_phone_numbers(page_content)
    phone_numbers = phone_numbers if phone_numbers else None

    email_addresses = extract_email_addresses(page_content)

    return {
        'title': title,
        'url': url,
        'phone_numbers': phone_numbers,
        'email_addresses': email_addresses,
    }

def get_job_offers():
    '''
    Returns a list of dictionaries containing the job title and URL
    '''
    job_data = []
    number_of_pages = get_last_index()
    for i in range(0, number_of_pages):
        print(f'Scrapping page {i+1} of {number_of_pages+1}')
        page_to_scrape = requests.get(url(i))
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")

        job_links = soup.find_all("a", attrs={"class": "title-overflow"})

        # Extract job titles and URLs
        for link in job_links:
            title = link.text.strip()
            job_url = 'https://emploi.chwapi.be' + link.get('href')
            # job_data.append({'title': title, 'url': job_url})
            job_data.append(get_job_details(title, job_url))

    return job_data
    

job_data = get_job_offers()

print('Writing to excel file...')

# create and write to excel file
workbook = xlsxwriter.Workbook('job_offers.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'Title')
worksheet.write('B1', 'URL')
worksheet.write('C1', 'Phone Numbers')
worksheet.write('D1', 'Email Addresses')
# worksheet.write('E1', 'Status')

for row_num, job in enumerate(job_data, start=2):
    worksheet.write(f'A{row_num}', job['title'])
    worksheet.write(f'B{row_num}', job['url'])
    
    # Check if there are phone numbers before writing
    if job['phone_numbers']:
        if isinstance(job['phone_numbers'], list):
            worksheet.write(f'C{row_num}', ', '.join(job['phone_numbers']))
        else:
            worksheet.write(f'C{row_num}', job['phone_numbers'])
    worksheet.write(f'D{row_num}', ', '.join(job['email_addresses']))


workbook.close()

print('Done!')