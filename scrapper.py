# Here using chrome driver we are trying to search a image by clicking search button
# post entering text in the text box by finding the text box in image search and then from that we
# go into it's xpath and try to findout it's ID or URL. Once done then we load the image. If we need multiple images
# of same type then we also look for the id to scroll and do the same using chrome driver.


# Here we will be having 3 methods, method1 will be fetching the image URL
# second method is once image url is fetched we try to download and store in a folder
# Third method is  search the image by entering text and clicking search

import os
import pandas as pd
import numpy as np
import time
import requests
from selenium import webdriver
import io
from PIL import Image

DRIVER_PATH = r'E:/Shubhashish/Image_scrapper/chromedriver.exe'

# Now let's initialize the driver to start executing

wd = webdriver.Chrome(DRIVER_PATH)

# Now let's check for one image

image_url = "https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_square.jpg"

# Now let's write a function to download and save the image



def fetch_image_details(query:str, max_links_to_fetch:int, wd, sleep_between_interactions:float = 1.0):
    """
    This function is used to extract the images from the url through web scrapping
    :param query: search term need to pass in search box
    :param max_links_to_fetch: Max. no of image urls to fetch
    :param wd: chrome webdriver
    :param sleep_between_interactions: wait time to allow the download happen successfully
    :return: image urls
    """

    def scroll_to_end(wd):
        """
        This method is used to scroll till the end to get all the images with scroll
        :param wd: crome web driver
        :return: scrolling object
        """
        wd.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        time.sleep(sleep_between_interactions)

    search_url = f"https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={query}&oq={query}&gs_l=img"

    # Now let's load the image
    wd.get(search_url)

    image_urls = set() # We are creating a set with the name image_url to avoid any duplicate url to be copied
    image_count = 0
    results_start = 0

    # Now let's fetch the urls till the time we hit the max links we need to fetch
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # Now we have reached the search page with the images list. Now we need to click on individual image to select
        select_image = wd.find_elements_by_css_selector('img.rg_i.Q4LuWd')
        # Now let's check the select_image result
        number_result = len(select_image)
        print(f"Found {number_result} search results. Extracting links from {results_start}:{max_links_to_fetch}")

        # Now let's click each image to get their url to download
        for img in select_image[results_start:max_links_to_fetch]:
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

        # Now let's fetch the urls of individually clicked images
        actual_images = wd.find_elements_by_css_selector('img.r48jcc.pT0Scc.iPVvYb')
        # So with this classname we have multiple images and we need to fetch them one by one
        for actual_image in actual_images:
            if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                image_urls.add(actual_image.get_attribute('src'))
                print(len(image_urls))

        image_count = len(image_urls)

        if image_count >= int(max_links_to_fetch):
            print(f"Found the actual no of images which is {len(image_urls)}")
            break
        else:
            print(f"Still looking for images as the threshold {max_links_to_fetch} is not met yet")
        results_start = len(select_image)
    return image_urls

def download_images(folder_path:str,url:str,counter:int):
    try:
        image_content = requests.get(url).content
    except Exception as e:
        print(f"Could not download {url} due to {str(e)}")

    # Now let's save the file

    try:
        f = open(os.path.join(folder_path,'jpg' + "_"+str(counter)+".jpg"),'wb')
        f.write(image_content)
        f.close()
        print(f"Success saved the url {url} as folder_path {folder_path}")
    except Exception as e:
        print(f"Error as could not save {url} in {folder_path}")

def search_and_download(search_term:str,driver_path:str,target_path = './images',no_of_images=10):
    """
    This function is used to get the image and save it from chrome scrapper
    :param search_term: subject name we need to download
    :param driver_path: chrome driver path
    :param target_path: where to save the image file downloaded
    :param no_of_images: The no. of images to download
    :return: img_url
    """
    target_folder = os.path.join(target_path,'_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = fetch_image_details(search_term,no_of_images,wd=wd,sleep_between_interactions=1.0)

    counter = 0
    for i in res:
        download_images(target_folder,i,counter)
        counter += 1


# TESTING THE METHODS

search_term = 'elon musk'
# num of images you can pass it from here  by default it's 10 if you are not passing
#number_images = 50
search_and_download(search_term=search_term, driver_path=DRIVER_PATH, no_of_images=25)