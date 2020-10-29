# Web Scrapper - Healthcare Professionals in Singapore

### Introduction
I felt it would be interesting to consolidate a dataset comprising the full list of licensed healthcare professionals in Singapore, and then run some analysis on it. To gather this dataset in the first place, I had to perform web scrapping on the Ministry of Health (MOH) Healthcare Professionals page to retrieve this publicly available information. This is because the entire list is not readily available for download in its entirety. 

The healthcare professional search page is meant for the public to readily locate healthcare professionals in Singapore, and this includes doctors, nurses, pharmacists, dentists, and other practitioners.

Being a pharmacist myself, it was natural to first test things out on the Pharmacists dataset.

### Methods
I wrote the web scraping automation script with Python and Selenium.  

Selenium allows you to define tests and automatically detect results of these tests on a pre-decided browser (I used ChromeDriver of Chromium). The Google Chrome we are familiar with is actually built on Chromium. For more info, do check this article out: https://www.howtogeek.com/202825/what%E2%80%99s-the-difference-between-chromium-and-chrome  

Before downloading the Chromium ChromeDriver, do check your Chrome version here: https://www.whatismybrowser.com/detect/what-version-of-chrome-do-i-have  
Once done, proceed over to this link to download the corresponding ChromeDriver version for your Chrome: https://chromedriver.chromium.org/downloads

A host of Selenium functions allows for step-by-step interactions with a webpage and assess the response of a browser to various changes. This is exceptionally useful since the MOH website can be tricky to navigate if we are to scrape the contents.  

The details of my experimentation and implementation are described in the Jupyter notebook.   

To run the script directly, you can use the .py file  

### Challenges and Solutions
There are multiple challenges to tackle when scrapping from the MOH website. As a result of this, the Python script had to undergo multiple iterations of adjustments in order to get the web scrapping process done right. The script has been written in a way to overcome these following challenges:

 - As with all web scraping projects, one of the initial challenges is to understand the HTML/JS structure of the website and discover which elements to click or explore. Upon digging deeper, the first step was to get the webdriver to switch to the Frame labelled as 'msg_main'. After that, it was necessary to click Search (without any input for the search bars of 'Name' or 'Name of Place of Practice' to get all records loaded.
 
 - Page loads can be slow, resulting in elements on page not being detected and causing exception to be thrown. It was thus important to place waits (with WebDriverWait, implicit waits and time.sleep) at strategic points to ensure that the loading and scraping process is performed in sequence.

 - When one is on the page with the detailed information of the healthcare professional, clicking the 'Back to Search Results' button at the bottom brings you back all the way to Page 1 of the search results. This means that you could be looking at the information of a pharmacist who was listed on page 50 of the search results, and clicking back brings you all the way to page 1. Thus there is a need to write a function (called locate_target_page) to get the script to navigate to the corresponding pages to scrape the information.

 - The pagination row for each page on the Search Results only show limited number of pages. This makes it difficult to go towards the middle portion of the search results. For example, the first pagination load is 1 2 3 4 5 6 7 8 9 10. Upon clicking the last page option (i.e. page 10), it only loads abit further into 5 6 7 8 9 10 11 12 13 14 on the subsequent page (i.e. loads extra 4 numbers on the pagination row). Therefore, the (click last

 - It will take a ridiculously long amount of time to reach the last result page if we were to start loading from page 1 of the Search Results all the way to the last page. Fortunately there is a 'Last' button that brings you all the way to the final page of the results. With that, the script was written such that for result pages that are more than the half way mark (i.e. pages 101 to 200 from a total of 200 search results pages), the program will go to the last page, and then work backwards in reverse to do the scraping.
 
 
### Comments
Please do let me know your feedback about this repo. I do believe there are still some kinks to resolve, since I still do get thrown an Exception (e.g. stale element reference: element is not attached to the page document) every now and then. Also, feel free to tell me how I can better improve the script, as well as the information listed in this README. Thanks!
