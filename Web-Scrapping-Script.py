# ===================================================================
#   Web Scrapping Script (for MOH Healthcare Professionals Page)
# ===================================================================

# ---------------------
#  Import dependencies
# ---------------------
import urllib
import re
import time
import pandas as pd
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# --------------------------
#  Initial Web Driver Setup
# --------------------------
# Define healthcare professional (HCP) body
# e.g. SPC for Singapore Pharmacy Council, SDC for Singapore Dentist Council, SMC for Singapore Medical Council etc
hcp_body = 'SPC'

# Set wait times
waittime = 20
sleeptime = 2

# Initiate web driver
try:
    driver.close() # Close any existing windows from drivers
except Exception:
    pass

# Access the professional registration system (PRS) homepage for the specified healthcare professional body
home_page = f"https://prs.moh.gov.sg/prs/internet/profSearch/main.action?hpe={hcp_body}"

# Set webdriver options
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('ignore-certificate-errors')

# Initiate webdriver
driver = webdriver.Chrome(options=options)

# Get driver to retrieve homepage
driver.get(home_page)

# Switch to frame which contains the HTML for the search section
driver.switch_to.frame(driver.find_element_by_name('msg_main'))

# Click Search button to load all results
WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, "//input[@name='btnSearch']"))).click()

# Sleep a short while for page loading to be fully completed
time.sleep(sleeptime)

# --------------------------
#  Setting up Key Functions
# --------------------------
file_name = 'master_list_test.csv' # Change this based on your preference

if os.path.isfile(f'./{file_name}'):
    print(f'Filename {file_name} already exists')
else:
    column_names = ['name','reg_number','reg_date','reg_end_date','reg_type','practice_status','cert_start_date',
                    'cert_end_date','qualification','practice_place_name','practice_place_address','practice_place_phone']
    df_template = pd.DataFrame(columns = column_names)
    df_template.to_csv(f'{file_name}', header=True)
    print('Created new master list file')

# Get current page number
def get_current_page():
    current_page_elem = WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, "//label[@class='pagination_selected_page']"))).text
    current_page_num = int(current_page_elem)
    return current_page_num

def get_absolute_last_page():
    # Find all elements with pagination class (since it contains page numbers)
    WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, "//a[@class='pagination']")))
    all_pages = driver.find_elements_by_xpath("//a[@class='pagination']")

    # Get the final element, which corresponds to 'Last' hyperlink (which will go to the last page number)
    last_elem = all_pages[-1].get_attribute('href')

    # Keep only the number of last page
    last_page_num = int(re.sub("[^0-9]", "", last_elem))
    return last_page_num

def gen_hcp_dict():
    WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, "//div[@class='table-head']")))
    hcp_name =  driver.find_element_by_xpath("//div[@class='table-head']").text
    all_fields = driver.find_elements_by_xpath("//td[@class='no-border table-data']") # Using find elementS since there are multiple elements
    hcp_data = []

    for field in all_fields:
        hcp_data.append(field.text)

    hcp_dict = {}
    hcp_dict['name'] = hcp_name
    hcp_dict['reg_number'] = hcp_data[0]
    # hcp_data[1] is just a blank space, so it can be ignored
    hcp_dict['reg_date'] = hcp_data[2]
    hcp_dict['reg_end_date'] = hcp_data[3]
    hcp_dict['reg_type'] = hcp_data[4]
    hcp_dict['practice_status'] = hcp_data[5]
    hcp_dict['cert_start_date'] = hcp_data[6]
    hcp_dict['cert_end_date'] = hcp_data[7]
    hcp_dict['qualification'] = hcp_data[8]
    hcp_dict['practice_place_name'] = hcp_data[9]
    hcp_dict['practice_place_address'] = hcp_data[10]
    hcp_dict['practice_place_phone'] = hcp_data[11]

    return hcp_dict

def get_current_pagination_range():
    WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, "//a[@class='pagination']")))
    all_pages = driver.find_elements_by_xpath("//a[@class='pagination']")
    driver.implicitly_wait(1)
    pagination_range_on_page = []
    for elem in all_pages:
        if elem.text.isnumeric():
            pagination_range_on_page.append(int(elem.text))
            driver.implicitly_wait(1)
        else:
            pass
    driver.implicitly_wait(1)
    return pagination_range_on_page


def click_last_pagination_num(pagination_range):
    last_pagination_num = pagination_range[-1]
    driver.implicitly_wait(1)
    WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.LINK_TEXT, f'{last_pagination_num}'))).click()
    driver.implicitly_wait(1)


def click_first_pagination_num(pagination_range):
    first_pagination_num = pagination_range[0]
    driver.implicitly_wait(1)
    WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.LINK_TEXT, f'{first_pagination_num}'))).click()
    driver.implicitly_wait(1)


def locate_target_page(target_page):
    last_page_num = get_absolute_last_page()
    midway_point = last_page_num/2

    if target_page < midway_point: # If target page is in the first half, then start clicking from the start
        current_page_num = get_current_page()

        if current_page_num == target_page:
            pass
        else:
            pagination_range = get_current_pagination_range()

            while target_page not in pagination_range:
                driver.implicitly_wait(1)
                click_last_pagination_num(pagination_range) # If target page is not in pagination range, keep clicking last pagination number to go further down the list
                current_page_num = get_current_page()
                pagination_range = get_current_pagination_range()
                driver.implicitly_wait(1)
            else:
                WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.LINK_TEXT, f"{target_page}"))).click() # Once target page is in pagination page, go to the target page

    else: # If target page is in later half of list, then go to Last page and move backwards (This saves alot of time)
        WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.LINK_TEXT, 'Last'))).click()  # Go to last page
        time.sleep(sleeptime)
        current_page_num = get_current_page()

        if current_page_num == target_page:
            pass
        else:
            pagination_range = get_current_pagination_range()

            while target_page not in pagination_range:
                driver.implicitly_wait(2)
                click_first_pagination_num(pagination_range)
                current_page_num = get_current_page()
                pagination_range = get_current_pagination_range()
            else:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, f"{target_page}"))).click() # Once target page is in pagination page, go to the target page

def full_scrape(target_page):

    last_page_num = get_absolute_last_page()
    driver.implicitly_wait(1)

    while target_page != last_page_num:
        locate_target_page(target_page)
        print('Starting with target page ' + str(target_page))

        # Retrieve the HTML from that search page
        target_page_html = driver.find_element_by_xpath("//body").get_attribute('outerHTML')
        driver.implicitly_wait(1)

        # Find the list of IDs on that page, and keep the unique IDs
        all_ids = re.findall("P[0-9]{5}[A-Z]{1}", target_page_html)
        id_list = list(dict.fromkeys(all_ids))

        for index, hcp_id in enumerate(id_list): # Tracking the healthcare professional (HCP)'s ID
            # Click 'View More Details' link to access the info page for that professional with the specific ID
            WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, f"//a[contains(@onclick,'{hcp_id}')]"))).click()

            # Scrape the relevant data from the pharmacist info page into a dictionary
            hcp_dict = gen_hcp_dict()

            # Convert dict to pandas dataframe (Need to pass an index since we are passing scalar values)
            df_hcp_dict = pd.DataFrame(hcp_dict, index=[0])

            # Append df to existing master list csv
            df_hcp_dict.to_csv(f'{file_name}', mode='a', header=False)

            # Print the row that has been scraped (To track progress)
            print(f'Scraped row {index+1} of page {target_page}')

            # After scrapping all records on that page, update (+1) the next target page to go to
            if index == len(id_list):
                print(f'Completed scraping for page {target_page}')
                target_page += 1
                print('Updated target page ' + str(target_page))
            else:
                pass

            # Head back to home page by clicking the Back to Search Results link
            WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.LINK_TEXT, 'Back to Search Results'))).click()

            # Go to the latest target page
            locate_target_page(target_page)

    else:
        locate_target_page(target_page)
        print('Working on last page')
        target_page_html = driver.find_element_by_xpath("//body").get_attribute('outerHTML')
        driver.implicitly_wait(1)
        all_ids = re.findall("P[0-9]{5}[A-Z]{1}", target_page_html)
        id_list = list(dict.fromkeys(all_ids))

        for index, hcp_id in enumerate(id_list):
            WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, f"//a[contains(@onclick,'{hcp_id}')]"))).click()
            hcp_dict = gen_hcp_dict()
            df_hcp_dict = pd.DataFrame(hcp_dict, index=[0])
            df_hcp_dict.to_csv('master_list.csv', mode='a', header=False)
            print(f'Scraped row {index+1} of {target_page}')

            if index == len(id_list)-1:
                print(f'Completed scraping for page {target_page}')
                print('Mission Complete')
            else:
                pass

            WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.LINK_TEXT, 'Back to Search Results'))).click()
            locate_target_page(target_page)


# --------------------------
#  Kickstart Web scraping
# --------------------------
# Start off with selected target page. target_page = 1 if starting from the beginning
target_page = 1

# Run web scraping
full_scrape(target_page)
