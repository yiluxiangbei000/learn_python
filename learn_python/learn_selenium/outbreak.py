__author__ = 'Administrator'


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options

option = Options()
option.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=option)
driver.get('https://www.outbreak.my/')
time.sleep(5)

confirmed = driver.find_element_by_id('cases-my-confirmed').text
active = driver.find_element_by_id('cases-my-active').text
death = driver.find_element_by_id('cases-my-death').text

cofirmed_changes = driver.find_element_by_id('cases-my-confirmed-changes').text[2:]
death_changes = driver.find_element_by_id('cases-my-death-changes').text

states = driver.find_elements_by_xpath('//div[@class="card-body o-auto"]//tr')
date = driver.find_element_by_xpath('//span[@id="last-update"]').text[:9]
for state in states[1:]:
    if state.find_element_by_css_selector('td.text-value').text == 'Melaka':
        melaka_confirmed = state.find_element_by_css_selector('td.text-right.text-value-total').text
        melaka_death = state.find_element_by_css_selector('td.text-right.text-value-black').text
        try:
            melaka_changes = state.find_element_by_css_selector('td.fe.fe-arrow-up.float-center').text
        except:
            melaka_changes = 0
        break



print('疫情报告：截止到{}，马来西亚全国单日新增确诊{}例，累计确诊{}例，现存病例{}例，累计死亡{}例；项目部所在地马六甲州新增{}例，累计确诊{}例，累计死亡{}例。'.
      format(date, cofirmed_changes, confirmed, active, death, melaka_changes, melaka_confirmed, melaka_death ))



driver.quit()





