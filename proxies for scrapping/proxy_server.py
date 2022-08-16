from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import warnings
warnings.filterwarnings("ignore")

driver=webdriver.Chrome(executable_path="C:\Program Files\Google\Chrome\Application\chromedriver")


driver.get("https://free-proxy-list.net/")

rows=driver.find_elements(By.XPATH,'//*[@id="list"]/div/div[2]/div/table/tbody/tr')
number_row=len(rows)
headers=["Server","HTTPS"]
with open("proxies.csv","w",encoding="UTF8",newline="") as file:
    writer=csv.writer(file)
    writer.writerow(headers)
    for i in range(1,number_row):
        server=driver.find_element(By.XPATH,f'//*[@id="list"]/div/div[2]/div/table/tbody/tr[{i}]/td[1]').text
        http=driver.find_element(By.XPATH,f'//*[@id="list"]/div/div[2]/div/table/tbody/tr[{i}]/td[7]').text
        port=driver.find_element(By.XPATH,f'//*[@id="list"]/div/div[2]/div/table/tbody/tr[{i}]/td[2]').text
        writer.writerow((server+":"+port,http))
driver.close()


