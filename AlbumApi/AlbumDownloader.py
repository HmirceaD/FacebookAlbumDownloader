"""
This module donwloads images from public facebook albums. It uses selenium to do so and
a Chrome webdriver. It was developed on a python 3.6 interpreter and a 78 chrome driver
Requirements: Python 3, Selenium and Chrome webdriver
You can download the chrome webdriver from the following link
(Be sure to select the version that coresponds to your version of chrome):
https://chromedriver.chromium.org/downloads
Check the provided README for instructions
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import shutil
import os
import requests
import sys
import logging
import math
import time

pause = 3 # Best to leave this at 3

def check_if_output_folder_exists(output_folder_path):
    """
    Helper function to check if the output folder exists
    :param output_folder_path: the path to the output folder
    :return: Existance of folder
    """
    if os.path.isdir(output_folder_path):
        return True
    else:
        return False

def get_num_of_scrolls(num_of_images):
    """
    :param num_of_images: number of wanted images
    :return: the number of times the webdriver needs to scroll for the
    desired number of elements to load
    """
    ROWSPERLOAD = 7
    COLSPERROW = 4
    return math.floor(num_of_images / (ROWSPERLOAD * COLSPERROW))

def download_images_from_album(albums_list = [], output_folder_path = "", num_of_images = 10):
    """
    Delegate all of the functions. This is the main function that you should
    interact with.
    Check if the folder exists. If it doesn't, close the script.
    Access each album.
    Compile a list of all the desired urls from the album
    Download to the desired output folder
    :param albums_list: list of the urls for the facebook albums
    :param output_folder_path: path of the desired output folder
    :param num_of_images: How many images should be downloaded
    from each album. If this number is selected as -1 than it download
    all images from the album
    """
    if check_if_output_folder_exists(output_folder_path):
        logging.info("Beginning Download")
    else:
        logging.error("Folder does not exist, please create it and try again")
        sys.exit(0)

    if num_of_images < -1 or num_of_images == 0:
        logging.error("The number of images you want to download must be -1 or greater than 0")
        sys.exit(0)

    num_of_scrolls = get_num_of_scrolls(num_of_images)

    browser = webdriver.Chrome()

    for album in albums_list:
        browser.get(album)
        image_links_list = get_image_links(browser, num_of_images, num_of_scrolls)
        scontent_list = compile_scontent_list(image_links_list, browser)
        download_images_from_scontent(scontent_list, output_folder_path)

def find(driver):
    """
    Helper function for waiting for the fb page to load.
    :param driver: instance of selenium webdriver
    """
    element = driver.find_element_by_class_name("_1ktf") #TODO: _1ktf is the name of the class the images corespond to in the facebook single image page
    if element:
        return element
    else:
        return False

def get_image_links(browser, num_of_images, num_of_scrolls):
    """
    Compile a list of links to the single image facebook pages of an album
    :param browser: Selenium Web Driver instance
    :param num_of_images: number of desired images to download
    :param num_of_scrolls: Number of times the crawler needs to scroll to get to
    the desired number of images
    """
    if int(num_of_scrolls) > 0 and num_of_images != -1:
        for i in range(0, int(num_of_scrolls)):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause)
    elif num_of_images == -1:
        scroll_to_end(browser)

    list_links = browser.find_elements_by_class_name("_2eea") #TODO: _2eea is the name of the class the images corespond to in the facebook album page
    links = []

    for link in list_links[:num_of_images]:
        links.append(link.find_element_by_css_selector('a').get_attribute('href'))

    return links


def scroll_to_end(browser):
    """
    Scroll to the end of a large album.
    Is invoked only if the num_of_images param is -1
    :param browser: instance of selenium webdriver
    """
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def compile_scontent_list(image_links_list, browser):
    """
    Parses through every single image page and extracts the image url
    :param image_links_list: list of links to single image facebook page
    :param browser: instance of selenium webdriver
    :return: list of image urls
    """
    scontent_list = []
    for image_link in image_links_list:

        browser.get(image_link)
        element = WebDriverWait(browser, pause).until(find)
        scontent = element.find_element_by_css_selector('a').get_attribute("data-ploi")
        scontent_list.append(scontent)

    return scontent_list

def get_image_name_from_facebook_url(image_url):
    """
    Extracts the facebook name of the image from the url
    Example: https://scontent.fomr1-1.fna.fbcdn.net/v/t1.0-9/
    79693065_2572106579740383_1796344134244499456_n.jpg?
    _nc_cat=100&_nc_ohc=dNVAkk4hXtMAQkvZ0M_FgvnvfSGkZl6odKnU6Vi0SaOD2vrMF_DQDYpqw
    &_nc_ht=scontent.fomr1-1.fna&oh=a08522f6f29bf5b5faef4ce2e8ee8888&oe=5E3F23A5 -> 79693065_2572106579740383_1796344134244499456_n.jpg
    :param image_url: url of full resolution image
    :return: the facebook name of the image
    """
    return (image_url.split("/")[-1]).split("?")[0]

def download_images_from_scontent(scontent_list=[], output_foler_location=""):
    """
    Create requests to all the full resolution image urls,
    download and save the images in the desired folders.
    If the output folder is left empty than then images
    will be saved in the same directory as the script
    :param scontent_list: list of the jpeg image urls
    :param output_foler_location: the path to the folder where the images will be stored
    """

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

def test_function():
    """
    Use this function to test the module
    """
    album_list = ['https://www.facebook.com/pg/occreamystolenmemes/photos/?tab=album&album_id=1983141641970216',
                  'https://www.facebook.com/pg/occreamystolenmemes/photos/?tab=album&album_id=1983128928638154']

    download_images_from_album(album_list, 'Path/Where/The/Output/Folder/Is', 10)
