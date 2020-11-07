# Web Scrapping Walkthrough - Curating Healthcare Professionals' Information with Python and Selenium

Link to notebook: https://nbviewer.jupyter.org/github/kennethleungty/Web-Scrapper/blob/main/Web-Scrapping-Notebook-Full.ipynb

Link to Medium post: https://kennethleungty.medium.com/web-scrapping-healthcare-professionals-information-1372385d639d

## Motivation
There is no analytics without data, and web scraping is one of the many tools used to curate data. The concept of web scraping has always been fascinating to me, and I felt it would be certainly be interesting to practise my coding chops while exploring the lists of registered healthcare professionals in Singapore. 

The Ministry of Health Professional Registration System webpage grants public access to the general information of healthcare professionals registered in Singapore, allowing the public to readily locate the professional they seek to find. As with most search sites, the records in the system is not available for viewing in its entirety, and that sets up a nice exercise for web scraping practice.

There are different pages for the various categories of healthcare practitioners (e.g. doctors, pharmacists, nurses, dentists etc), and being a pharmacist myself, it was natural for me to first test things out on the Pharmacists dataset.  

___
### Methods
I wrote the web scraping automation script with Python and Selenium.  

The details of my experimentation and implementation are described in the notebook Web-Scrapping-Notebook-Full.ipynb. The clean version (without the details and commentary) can be found in Web-Scrapping-Notebook-Clean.ipynb

To run the script directly, you can use the Web-Scrapping-Script.py file  

___
### Challenges and Solutions
There are multiple challenges to tackle in the process. As a result of this, the Python script had to undergo multiple iterations of adjustments in order to get the web scrapping process done right. The script has been written in a way to overcome these following challenges:

 - As with all web scraping projects, one of the initial challenges is to understand the HTML structure of the website and discover which elements to click or explore. Upon digging deeper, the first step was to get the webdriver to switch to the Frame labelled as 'msg_main'. After that, it was necessary to click Search (without any input for the search bars of 'Name' or 'Name of Place of Practice' to get all records loaded.
 
 - Page loads can be slow, resulting in elements on page not being detected and causing exception to be thrown. It was thus important to place waits (with WebDriverWait, implicit waits and time.sleep) at strategic points to ensure that the loading and scraping process is performed in sequence.

 - When one is on the page with the detailed information of the healthcare professional, clicking the 'Back to Search Results' button at the bottom brings you back all the way to Page 1 of the search results. This means that you could be looking at the information of a pharmacist who was listed on page 50 of the search results, and clicking back brings you all the way to page 1. Thus there is a need to write a function (called locate_target_page) to get the script to navigate to the corresponding pages to scrape the information.

 - The pagination row for each page on the Search Results only show limited number of pages. This makes it difficult to go towards the middle portion of the search results. For example, the first pagination load is 1 2 3 4 5 6 7 8 9 10. Upon clicking the last page option (i.e. page 10), it only loads abit further into 5 6 7 8 9 10 11 12 13 14 on the subsequent page (i.e. loads extra 4 numbers on the pagination row). Therefore, the (click last

 - It will take a ridiculously long amount of time to reach the last result page if we were to start loading from page 1 of the Search Results all the way to the last page. Fortunately there is a 'Last' button that brings you all the way to the final page of the results. With that, the script was written such that for result pages that are more than the half way mark (i.e. pages 101 to 200 from a total of 200 search results pages), the program will go to the last page, and then work backwards in reverse to do the scraping.
 
___
### Comments
Please do let me know your feedback about this repo. I do believe there are still some kinks to resolve, since I still do get thrown an Exception (e.g. stale element reference: element is not attached to the page document) every now and then, despite the strategic placements of wait times.

Please also feel free to share with me ideas to improve the script and details listed in the notebooks. Thanks!
