from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os



def login():
    username_field=driver.find_element(By.ID,"email")
    password_field=driver.find_element(By.ID,"pass")
    login_btn=driver.find_element(By.ID,"loginbutton")

    username_field.click()
    username_field.send_keys(username)
    time.sleep(0.5)

    password_field.click()
    password_field.send_keys(password)
    time.sleep(0.5)

    login_btn.click()

def search_marketplace(value):
    
    market_place=driver.find_element(By.XPATH,"//a[contains(@aria-label,'Marketplace')]")
    market_place.click()
    driver.implicitly_wait(10)
    search_product=driver.find_element(By.XPATH,"//input[@placeholder='Search Marketplace']")
    search_product.click()
    time.sleep(0.5)
    search_product.send_keys(value)
    search_product.send_keys(Keys.ENTER)
    driver.implicitly_wait(10)

    filter_dropdown=driver.find_element(By.XPATH,"//span[text()='Date listed']")
    filter_dropdown.click()
    driver.implicitly_wait(10)
    hours_24_btn=driver.find_element(By.XPATH,"//span[text()='Last 24 hours']")
    hours_24_btn.click()

def send_messages():
    current_hight=driver.execute_script("return document.body.scrollHeight")
   
    links=set()
    records="adds_records.txt"
    if os.path.exists(records):
        mode="r+"
    else:
        mode="w+" 
    
    
    while(1):
        new_adds = driver.find_elements(By.XPATH, "//a[contains(@href, '/marketplace/item/')]")
        file=open(records,mode=mode)
        ls=file.readlines()
        for i in range(0,len(ls)):
            ls[i]=ls[i].split("\n")[0]
        for add in new_adds:
            links.add(add.get_attribute("href"))
            if (add.get_attribute("href").split("?")[0]) in ls:
                print("already exists")
            else:    
                
                driver.execute_script("window.open(arguments[0], '_blank');", add.get_attribute('href'))
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[-1])
                
                driver.implicitly_wait(20)
                msg_btn=driver.find_element(By.XPATH,"//div[contains(@aria-label, 'Message')]")
                msg_btn.click()
                driver.implicitly_wait(20)
                time.sleep(3)
                msg=driver.find_element(By.XPATH,"//label[contains(@aria-label, 'Please type your message to the seller')]")
                    
                msg.send_keys("Hi is this still available")
                
                send_btn=driver.find_element(By.XPATH,"//div[contains(@aria-label, 'Send message')]")
                send_btn.click()
                driver.implicitly_wait(20)
                time.sleep(12)
               
                limit=None    
               
                try:
                    driver.switch_to.active_element.text
                    print(driver.switch_to.active_element.text)
                    limit=driver.switch_to.active_element.find_element(By.XPATH,"//span[text()='You've Reached Your Limit']")
                    print(limit)
                    if limit in None:
                        print("limit i not found")
                    #limit=driver.find_element(By.XPATH,"//span[text()='You've Reached Your Limit']")
                except:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(2)
                    print("explored")
                    file.write(add.get_attribute("href").split("?")[0]);file.write("\n")
                if limit:
                    print("Message limit has reached bot will now sleep for 24 hours")
                    time.sleep(12*60*60)
                    explore_adds()      

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(50)
        time.sleep(5)
        new_hight=driver.execute_script("return document.body.scrollHeight")
        
        if new_hight==current_hight:
            break
        current_hight=new_hight
    
    print("len of links: ",len(links))

def explore_adds():
    search_keywords=["Toyota","chelsea boots","nokia","apple phone"]
    while(1):
        for value in search_keywords:
            time.sleep(3)
            search_marketplace(value)
            time.sleep(3)
            send_messages()
        print("next refresh in 30 minutes")
        time.sleep(30*60)
        driver.refresh()
        time.sleep(3)
        print("refreshed")


        

url="https://www.facebook.com/login.php/"
username="username"
password="password"
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.page_load_strategy = 'eager'

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
driver.maximize_window()

login()
driver.implicitly_wait(10)

time.sleep(2)
driver.implicitly_wait(10)

explore_adds()

