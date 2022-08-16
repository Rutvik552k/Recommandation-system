from logging import warning
import threading
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import requests
import csv
import warnings
warnings.filterwarnings("ignore")
def count_list(driver):
    number_list=driver.find_elements(By.XPATH,'//*[@id="content"]/div/div[1]/div/div[4]/div[5]/div[3]/div[10]/div/div/div[1]/ul/li')
    return len(number_list)




def Total_sale_function(driver):

    try:
        sale_price=driver.find_element(By.XPATH,f"//*[@id='listing-page-cart']/div[1]/div[2]/div/span[2]").text
    except:
        sale_price="None"
    return sale_price


def Badge_fucntion(driver):
    try:
        badge=driver.find_element(By.XPATH,'//*[@id="listing-page-cart"]/div[2]/div/button/span/div/span')
    except:
        badge="None"
    return badge

def move_to_next_page(driver,i):
    button=driver.find_element(By.XPATH,f"//*[@id='content']/div/div[1]/div/div[4]/div[5]/div[3]/div[13]/div/div/div/div[2]/nav/ul/li[{i}]/a")
    button.click()
    print(f"{i+1} Next Page\n")




def find_button(driver):
    tag_list=driver.find_elements(By.XPATH,"//*[@id='content']/div/div[1]/div/div[4]/div[5]/div[3]/div[13]/div/div/div/div[2]/nav/ul/li")
    return len(tag_list)
    
def image_capture(driver,headers,img_link,i,j):
    page=requests.get(img_link,headers=headers)
    WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,"/html/body/img")))
    if page.status_code==200:
        with open(f"image/page{j}_{i}.jpg","wb") as file:
            var=f"page{j}_image/{i}.jpg"
            file.write(page.content)
            print(f"{i} image printed")
    
    else:
        var="None"
        print("fail")
    return var


def img_load(driver,handle):
    i=0
    while True:
        i=i+1
        try:
            img=driver.find_element(By.XPATH,"//*[@id='listing-right-column']/div/div[1]/div[1]/div/div/div[2]/div/div[1]/ul/li[1]/img")
            return img
        except:
            driver.refresh()
            img_load(driver,handle)
        if i==2:
            break

    
    

def input_file(value_dict):
    with open("etsy_product.csv","a",encoding="UTf8",newline="") as file:
        writer=csv.writer(file)
        for i in value_dict:
        
            writer.writerow(value_dict)

def scrape_page(driver,headers,j):
    main_list=[]
    
    t1=threading.Thread(target=count_list,args=(driver,))
    t2=threading.Thread(target=Total_sale_function,args=(driver,))
    t3=threading.Thread(target=Badge_fucntion,args=(driver,))
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
#     
    number_product=count_list(driver)
    for i in range(1,number_product):
        
        img_button=driver.find_element(By.XPATH,f"//*[@id='content']/div/div[1]/div/div[4]/div[5]/div[3]/div[10]/div[1]/div/div/ul/li[{i}]/div/div/a/div[1]/div/div/div/div/div/img")
        time.sleep(1)
        img_button.click()


        
        
        
        handle=driver.window_handles

        driver.switch_to.window(handle[1])
       
        img=img_load(driver,handle=handle)
        
        head=driver.find_element(By.XPATH,f"//*[@id='listing-page-cart']/div[2]/h1").text
        shop_name=driver.find_element(By.XPATH,f"//*[@id='listing-page-cart']/div[1]/div[1]/div/p/a").text
        sales=Total_sale_function(driver)
        price=driver.find_element(By.XPATH,f'//*[@id="listing-page-cart"]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/p').text
        badge=Badge_fucntion(driver)
        

        
        

        img_link=img.get_attribute("src")

        time.sleep(2)
        
        var=image_capture(driver,headers,img_link,i,j)

        main_list.append([head,shop_name,sales,price,badge,var])
        

        driver.close()
        driver.switch_to.window(handle[0])
        print(main_list)
    

    input_file(main_list)
    return 0






def main(start,end,product_name):
    start_time=time.time()
    # proxy_ip_port="8.219.97.248:80"
    # proxy=Proxy()
    # proxy.proxytype=ProxyType.MANUAL
    # proxy.http_proxy=proxy_ip_port
    # proxy.ssl_proxy=proxy_ip_port
    
    # capability=webdriver.DesiredCapabilities.CHROME
    # proxy.add_to_capabilities(capability)
    
    # Item=item

    header = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})
    
    
    i=1

    for page in range(start,end+1):
        driver=webdriver.Chrome(executable_path="C:\Program Files\Google\Chrome\Application\chromedriver")
        driver.get(f"https://www.etsy.com/in-en/search?q={product_name}&ref=pagination&page={page}")

        scrape_page(driver,header,page)
        time.sleep(2)
        print(time.time()-start_time)
        print(f"---------------------------------------- page {page} scraped-----------------------------")
        i=i+1
        
        driver.close()
