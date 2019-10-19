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
from flask_ngrok import run_with_ngrok


#options = webdriver.ChromeOptions()#"
#prefs={"profile.managed_default_content_settings.images": 2,'disk-cache-size': 4096 }
#options.add_experimental_option('prefs', prefs)
## options.headless = True
## options.add_argument("--user-data-dir=/home/anurag/.config/google-chrome/")
#options.add_argument('--no-sandbox')
#options.add_argument('--disable-dev-shm-usage')
##    options.add_argument('--headless')
#driver = webdriver.Chrome(executable_path = "/Users/manthan/Documents/GitHub/sih/chromedriver")
#driver = webdriver.Chrome('/Users/manthan/Downloads/chromedriver')

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
    
    
    t_end = time.time() + 50
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
    
def reco_linked(source,base):
    driver = webdriver.Chrome('/Users/manthan/Downloads/chromedriver')
    driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
    time.sleep(5)
    username = driver.find_element_by_id('username')
    username.send_keys('mayankochar@gmail.com')
    password = driver.find_element_by_id('password')
    password.send_keys('airforce27')
    sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
    sign_in_button.click()
    time.sleep(5)
    driver.get("https://www.linkedin.com/in/"+source.split('/')[4]+"/detail/photo")
    time.sleep(5)
    img=driver.get_screenshot_as_file("sih/Samples/main_base.png")

    p1 = face_recognition.load_image_file(base)
    pe1 = face_recognition.face_encodings(p1)[0]

    p2 = face_recognition.load_image_file("sih/Samples/main_base.png")
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
        if True in matches:
            match=True
            break
    if os.path.isfile("sih/Samples/main_base.png"):
        os.remove("sih/Samples/main_base.png")
    driver.quit()
    return match

def linked_in(Query,base):
    driver = webdriver.Chrome('/Users/manthan/Downloads/chromedriver')
    driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
    time.sleep(5)
    username = driver.find_element_by_id('username')
    username.send_keys('mayankochar@gmail.com')
    password = driver.find_element_by_id('password')
    password.send_keys('airforce27')
    sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
    sign_in_button.click()
    time.sleep(5)
    driver.get('https:www.google.com')
    search_query = driver.find_element_by_name('q')
    search_query.send_keys('site:linkedin.com/in/ AND "'+Query+'"')
    search_query.send_keys(Keys.ENTER)
    time.sleep(0.5)
    linkedin_urls = driver.find_elements_by_xpath("//div[@class='r']/a")
    linkedin_urls = [url.get_attribute('href') for url in linkedin_urls]
    time.sleep(0.5)
    global ans2
    for id in linkedin_urls:
        if reco_linked(id,base):
            print(id)
            ans2 = id
            return
        
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

def Instag(Query,base):
    driver = webdriver.Chrome('/Users/manthan/Downloads/chromedriver')
    driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
    time.sleep(5)
    usern = driver.find_element_by_class_name("_2hvTZ.pexuQ.zyHYP")
    pw = driver.find_element_by_xpath("//input[@name='password']")
    usern.send_keys("mayankochar_")
    pw.send_keys("airforce2712")
    driver.find_element_by_class_name("sqdOP.L3NKy.y3zKF").click()
    time.sleep(5)
    driver.find_element_by_xpath("//button[contains(@class,'HoLwm')]").click()
    searc = driver.find_element_by_xpath("//input[contains(@placeholder,'Search')]")
    searc.send_keys(Query)
    time.sleep(8)
    ids = driver.find_elements_by_class_name("yCE8d")
    for ab in ids:
        url_in = ab.get_attribute('href')
        if about_page2(url_in,base) is True:
            break

def about_page2(source,base):
    driver = webdriver.Chrome('/Users/manthan/Downloads/chromedriver')
    driver.get(source)
    time.sleep(5)
#    about_page=driver.page_source
#    abt_soup = bs(about_page, "html.parser")
#    try:
#        user_id= abt_soup.find_all("meta",{"property":"al:android:url"})[0].get("content",None).split('/')[3]
#        print(user_id)
#    except IndexError:
#        user_id = "100004247586903"
    user_id = driver.find_element_by_class_name("_7UhW9.fKFbl.yUEEX.KV-D4.fDxYl").text
#
#    image="https://graph.facebook.com/"+user_id+"/picture?type=large&width=720&height=720"
#    driver.find_element_by_class_name("_4Kbb_._54f4m")
    image = driver.find_element_by_class_name("_6q-tv").get_attribute('href')
    print(image)
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

app = Flask(__name__)
#run_with_ngrok(app)

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
#    WebWork(user_name,destination)
#    linked_in(user_name,destination)
    Instag(user_name,destination)
    try:
        prediction_text='URL Found for ' + user_name + ' is {}'.format(ans)
    except NameError:
        prediction_text = "URL NOT FOUND!! SORRY "
    try:
        prediction_text2='URL Found for ' + user_name + ' is {}'.format(ans2)
    except NameError:
        prediction_text2= "URL NOT FOUND!! SORRY!! "
    

#    return render_template('index.html', prediction_text='URL Found for ' + user_name + ' is {}'.format(ans), prediction_text2='URL Found for ' + user_name + ' is {}'.format(ans2) )

    return render_template('index.html', prediction_text= prediction_text, prediction_text2=prediction_text2 )

#    try:
#        return render_template('index.html', prediction_text=format(ans))
#    except NameError:
#        return render_template('index.html', prediction_text='URL NOT FOUND!! SORRY ')


if __name__ == "__main__":
#    app.run(port = 8010, debug=True)
    app.run()
#    options = Options()
#    #options.add_argument("--headless")
#    driver = webdriver.Firefox(options=options)
#    driver = webdriver.Chrome('/Users/manthan/Downloads/chromedriver')

#    app.run()
