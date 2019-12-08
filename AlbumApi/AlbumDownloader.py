from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import shutil
import os
import requests
pause = 0
ROWSPERLOAD=7

def download_images_from_album():
    browser = webdriver.Chrome()
    browser.get('https://www.facebook.com/pg/occreamystolenmemes/photos/?tab=album&album_id=1983128928638154&ref=page_internal')

    image_links_list = get_image_links(browser)
    scontent_list = compile_scontent_list(image_links_list, browser)
    download_images_from_scontent(scontent_list)

def find(driver):
    element = driver.find_element_by_class_name("_1ktf")
    if element:
        return element
    else:
        return False

def get_image_links(browser):
    list_links = browser.find_elements_by_class_name("_2eea")
    links = []
    for link in list_links:
        links.append(link.find_element_by_css_selector('a').get_attribute('href'))

    return links

def compile_scontent_list(image_links_list, browser):
    scontent_list = []
    for image_link in image_links_list:

        browser.get(image_link)
        element = WebDriverWait(browser, 3).until(find)
        scontent = element.find_element_by_css_selector('a').get_attribute("data-ploi")
        scontent_list.append(scontent)

    return scontent_list

def get_image_name_from_facebook_url(image_url):
    return (image_url.split("/")[-1]).split("?")[0]

def download_images_from_scontent(scontent_list=[], output_foler_location=""):

    for image_url in scontent_list:
        image_name = get_image_name_from_facebook_url(image_url)

        if output_foler_location:
            image_file_path = os.path.join(output_foler_location, image_name)
        else:
            image_file_path = image_name

        resp = requests.get(image_url, stream=True)
        with open(image_file_path, 'wb') as local_file:
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, local_file)

        del resp

'''
startTime = time.time()
for i in range(0,65):
	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(3)'''


'''
elems = browser.find_elements_by_class_name("_2eea")
for elem in elems:
    print(elem)'''

'''lastHeight = browser.execute_script("return document.body.scrollHeight")
while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause)
    newHeight = browser.execute_script("return document.body.scrollHeight")
    if newHeight == lastHeight:
        break
    lastHeight = newHeight'''
