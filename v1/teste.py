from selenium import webdriver
from time import sleep

driver = webdriver.Firefox()

driver.get('https://www.mercadolivre.com.br/')

driver.find_element_by_xpath('/html/body/header/div/form/input').send_keys("Arduino")
driver.find_element_by_xpath('/html/body/header/div/form/button/div').click()
sleep(5)

driver.find_element_by_xpath('//*[@id="root-app"]/div/div[1]/section/ol[1]/li[2]/div/div/a/div/div[1]/div/div/span[1]/span[2]/span[2]').click()


