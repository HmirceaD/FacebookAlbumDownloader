Interact with download_images_from_album(param1,param2,param3) function in order to begin downloading.
Description of the parameters:
    - param1: python list containing links to the facebook albums
    - param2: the path of the folder where you want the photos to be downloaded
    - param3: Number of images that you want to download from the albums.
              Leave it empty and it will download 10 images per album.
              Set it to -1 to download the whole album.

Requirements:
    - Python 3 (The project was developed on the python 3.6 interpreter)
    - Selenium
    - Google Chrome
    - A chrome webdriver. You can donwload one that coresponds to your chrome webdriver here:
      https://chromedriver.chromium.org/downloads