import numpy as np
from flask import Flask, request, jsonify, render_template,redirect, url_for
#from werkzeug.utils import secure_filename
import pickle
import os
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup as bs
#import urlparse
import urllib.parse
#import urllib
#from urllib2 import urlopen
#from urllib import urlretrieve
from urllib.request import urlretrieve
import sys
import requests
from PIL import Image, ImageTk
import numpy as np
import cv2
import time
import face_recognition
from skimage import io
import sys
from twitter import *
from selenium.webdriver.firefox.options import Options


#options = webdriver.ChromeOptions()#"
#prefs={"profile.managed_default_content_settings.images": 2,'disk-cache-size': 4096 }
#options.add_experimental_option('prefs', prefs)
## options.headless = True
## options.add_argument("--user-data-dir=/home/anurag/.config/google-chrome/")
#options.add_argument('--no-sandbox')
#options.add_argument('--disable-dev-shm-usage')
##    options.add_argument('--headless')
#driver = webdriver.Chrome(executable_path = "/Users/manthan/Documents/GitHub/sih/chromedriver")


def WebWork(Query,base):
    # print "Open the website"
#    driver.get('https://www.facebook.com/public/'+Query)
#    options = Options()
#    driver = webdriver.Firefox(options=options)
    driver = webdriver.Chrome('/Users/manthan/Downloads/chromedriver')
    driver.get("https://www.facebook.com/login")
    username_box = driver.find_element_by_id('email')
    password_box = driver.find_element_by_id('pass')
    
    
    
    
    username_box.send_keys('manthankeim@icloud.com')
    password_box.send_keys('iCloud!1')
    
    
    
    password_box.send_keys(Keys.ENTER)
    
    #    login_button = driver.find_element_by_id('u_0_2')
    
    print("Logged in...")
#    search_b = driver.find_element_by_class_name("_1frb")
#    search_b.send_keys(Query)
#  driver.find_element_by_xpath("//button[@class='_42ft._4jy0._4w98._4jy3._517h._51sy']").click()
    url="https://www.facebook.com/search/people/?q="+Query
#    url = "https://www.facebook.com/search/top/?q=" + Query
    driver.get(url)
    
    
    t_end = time.time() + 10
    html = driver.find_element_by_tag_name('html')
    while time.time() <= t_end:
        html.send_keys(Keys.END)
    
    
    
    page_source=driver.page_source
    soup = bs(page_source, "html.parser")
    
    for link in soup.findAll("a", {"class": "_2ial"}):
        dp_link=link.get('href')
        # print dp_link
        # print link.get('href')
        # print  " "
        # about_page(dp_link)
        if about_page(dp_link,base) is True:
            break
    driver.quit()
    
def about_page(source,base):
    driver = webdriver.Chrome('/Users/manthan/Downloads/chromedriver')
    driver.get(source)
    about_page=driver.page_source
    abt_soup = bs(about_page, "html.parser")
    try:
        user_id= abt_soup.find_all("meta",{"property":"al:android:url"})[0].get("content",None).split('/')[3]
        print(user_id)
    except IndexError:
        user_id = "100004247586903"

    image="https://graph.facebook.com/"+user_id+"/picture?type=large&width=720&height=720"
    
    urlretrieve(image, "sih/Samples/"+user_id+".jpg")
    if reco("sih/Samples/"+user_id+".jpg",base) is True:
        # ans.append(source)
        global ans
        ans=source
        print(source)
        driver.quit()
        if os.path.isfile("sih/Samples/"+user_id+".jpg"):
            os.remove("sih/Samples/"+user_id+".jpg")
        return True
    
    if os.path.isfile("sih/Samples/"+user_id+".jpg"):
        os.remove("sih/Samples/"+user_id+".jpg")
    return False

def reco(u2,base):
    # '/home/anurag/Desktop/Py/sih/Samples/base_photo.jpg'
    p1 = face_recognition.load_image_file(base)
    pe1 = face_recognition.face_encodings(p1)[0]
    print(pe1)
    
    # urlretrieve(u2, "/home/anurag/Desktop/Py/sih/Samples/main_base.jpg")
    # p2 = face_recognition.load_image_file("/home/anurag/Desktop/Py/sih/Samples/main_base.jpg")
    p2 = face_recognition.load_image_file(u2)
    
    pe2 = face_recognition.face_encodings(p2)
    if len(pe2)>0:
        pe2=face_recognition.face_encodings(p2)[0]
    else:
        return False
    face_locations = face_recognition.face_locations(p2)
    face_encodings = face_recognition.face_encodings(p2, face_locations)
    match=False
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces([pe1], face_encoding, tolerance=0.50)
        # print face_recognition.face_distance([pe1], face_encoding)
        if True in matches:
            match=True
            break

    if os.path.isfile("/home/anurag/Desktop/Py/sih/Samples/main_base.jpg"):
        os.remove("/home/anurag/Desktop/Py/sih/Samples/main_base.jpg")
    return match


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    user_name = request.form['user_name']
    print(user_name)
    driver = webdriver.Chrome('/Users/manthan/Downloads/chromedriver')
#    options = Options()
#    driver = webdriver.Firefox(options=options)
    target = os.path.join(APP_ROOT, 'images/')
#    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)
    
    for file in request.files.getlist("file"):
#        print(file)
        filename = file.filename
        destination = "".join([target, filename])
        print(destination)
        file.save(destination)
    WebWork(user_name,destination)
    try:
        return render_template('index.html', prediction_text='URL Found for ' + user_name + ' is {}'.format(ans))
    except NameError:
        return render_template('index.html', prediction_text='URL NOT FOUND!! SORRY ')


if __name__ == "__main__":
    app.run(port = 8000, debug=True)
#    options = Options()
#    #options.add_argument("--headless")
#    driver = webdriver.Firefox(options=options)
#    driver = webdriver.Chrome('/Users/manthan/Downloads/chromedriver')

#    app.run()
