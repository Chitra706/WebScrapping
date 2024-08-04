import os
import csv
import time
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime

headers = {
    "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
}

# Skills and Place of Work
skill = input('Enter your Skill: ').strip()
place = input('Enter the location: ').strip()
no_of_pages = int(input('Enter the #pages to scrape: '))
min_salary = input('Enter minimum salary (optional): ').strip()

# Creating the Main Directory
main_dir = os.path.join(os.getcwd(), 'IndeedJobScraperResults')
if not os.path.exists(main_dir):
    os.mkdir(main_dir)
    print('Results Directory Created Successfully.')

# Name of the CSV File
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name = f"{skill.title()}_{place.title()}_{timestamp}_Jobs.csv"
# Path of the CSV File
file_path = os.path.join(main_dir, file_name)

# Writing to the CSV File
with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Adding the Column Names to the CSV File
    writer.writerow(
        ['JOB_NAME', 'COMPANY', 'LOCATION', 'POSTED', 'SALARY', 'DESCRIPTION', 'APPLY_LINK'])

    # Requesting and getting the webpage using requests
    print(f'\nScraping in progress...\n')
    for page in range(no_of_pages):
        url = f'https://www.indeed.co.in/jobs?q={skill}&l={place}&start={page * 10}'
        if min_salary:
            url += f'&salary={min_salary}'
        
        response = requests.get(url, headers=headers)
        html = response.text

        # Scrapping the Web
        soup = BeautifulSoup(html, 'lxml')
        jobs = soup.find_all('a', class_='tapItem')

        for job in jobs:
            job_id = job['id'].split('_')[-1]
            job_title = job.find('span', title=True).text.strip()
            company = job.find('span', class_='companyName').text.strip()
            location = job.find('div', class_='companyLocation').text.strip()
            posted = job.find('span', class_='date').text.strip()
            job_link = f'https://in.indeed.com/viewjob?jk={job_id}'
            
            salary = job.find('div', class_='salary-snippet')
            salary = salary.text.strip() if salary else 'Not specified'

            job_description = job.find('div', class_='job-snippet')
            job_description = job_description.text.strip() if job_description else 'Not available'

            # Writing to CSV File
            writer.writerow(
                [job_title, company, location.title(), posted, salary, job_description, job_link])

        print(f'Page {page + 1} scraped.')
        time.sleep(random.uniform(1, 3))  # Random delay between requests

print(f'Jobs data written to <{file_name}> successfully.')
print(f'Results saved in: {main_dir}')