import csv
from selenium import webdriver
from time import sleep


driver = webdriver.Chrome('/home/krptic_07/Documents/chromedriver')
writer = csv.writer(open('intershala_companies', 'w'))
writer.writerow(['Intern Profile', 'Company'])


def validate_field(field):

    if field:
        field = field.strip()
    if type(field) is None:
        field = 'No results'
    return field


def scrapper():
    internship_containers = driver.find_elements_by_css_selector('div.container-fluid.individual_internship')
    companies = [internship.find_element_by_class_name('company').find_elements_by_tag_name('a') for internship in internship_containers[1::]]
    internships = [[company[0].get_attribute("text"), company[1].get_attribute("text")] for company in companies]
    for internship_c in internships:
        internship = validate_field(internship_c[0])
        company = validate_field(internship_c[1])
        writer.writerow([internship, company])
    sleep(3)


for i in range(1, 330):
    driver.get('https://internshala.com/internships/page-{}'.format(str(i)))
    driver.maximize_window()
    scrapper()


driver.quit()
