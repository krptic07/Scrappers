import parameters
import csv
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from parsel import Selector
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException





driver = webdriver.Chrome('/home/krptic_07/Documents/chromedriver')

driver.get(parameters.search_query['website'])
driver.maximize_window()

file_name = 'Nit Warangal'


def validate_field(field):

    if field:
        field = field.strip()
    if type(field) is None:
        field = 'No results'
    return field


def scrapper(college, location):

    writer = csv.writer(open(file_name, 'w'))

    writer.writerow(['Name', 'Headline', 'Education','Linkedin Profile','Email','Phone','Website','Address'])
    username = driver.find_element_by_name('session_key')
    username.send_keys(parameters.linkedin_username)
    sleep(0.5)

    password = driver.find_element_by_name('session_password')
    password.send_keys(parameters.linkedin_password)
    sleep(0.5)

    sign_in = driver.find_element_by_class_name("sign-in-form__submit-button")
    sign_in.click()
    sleep(0.5)

    #to fetch urls from google

    driver.get('https:www.google.com')
    sleep(3)

    search_query_button = driver.find_element_by_name('q')
    search_query = 'LinkedIn Profiles of {coll} {loc} students'.format(coll=college,loc=location)
    search_query_button.send_keys(search_query)
    sleep(0.5)

    search_query_button.send_keys(Keys.RETURN)
    sleep(3)


    linkedin_url = driver.find_elements_by_class_name('yuRUbf')
    linkedin_urls = [url.find_element_by_tag_name('a').get_attribute('href') for url in linkedin_url]
    sleep(0.5)

    for url in linkedin_urls:
        
        driver.get(url)
        sleep(5)

        sel = Selector(text=driver.page_source)
        
        
        name = sel.xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/ul[1]/li[1]/text()').extract_first()
        validate_field(name)

        headline = sel.xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/h2/text()').extract_first()
        validate_field(headline)
        
        education = sel.xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[2]/ul/li/a/span/text()').extract_first()
        validate_field(education)

        
                    
        try:
            
            contact = driver.find_element_by_xpath(" /html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/ul[2]/li[3]/a")
            contact.click()
            sleep(5)
            
            sel = Selector(text=driver.page_source)
            
            
            
            linkedin_profile = sel.xpath('/html/body/div[4]/div/div/div[2]/section/div/div[1]/div/section[1]/div/a/text()').extract_first()
            validate_field(linkedin_profile)

            email = sel.xpath('/html/body/div[4]/div/div/div[2]/section/div/div[1]/div/section[5]/div/a/text()').extract_first()
            validate_field(email)

            phone = sel.xpath('/html/body/div[4]/div/div/div[2]/section/div/div[1]/div/section[3]/ul/li/span[1]/text()').extract_first()
            validate_field(phone)
            
            website = sel.xpath('/html/body/div[4]/div/div/div[2]/section/div/div[1]/div/section[2]/ul/li/div/a/text()[1]').extract_first()
            validate_field(website)

            address  = sel.xpath('/html/body/div[4]/div/div/div[2]/section/div/div[1]/div/section[4]/div/a/text()').extract_first()
            validate_field(address)

            

        except NoSuchElementException:  
            pass
        
        writer.writerow([name,
                        headline,
                        education,
                        linkedin_profile,
                        email,
                        phone,
                        website,
                        address,])


        

        

    driver.quit()



scrapper('nit','warangal')


