__author__ = 'Administrator'
import sys   #读参数
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
import pyexcel

if __name__ == '__main__':
    rows = []
    keyword = 'iphone'
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
    option = Options()
    #option.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=option)
    driver.get('https://global.jd.com/')
    time.sleep(3)

    kw = driver.find_element_by_id('key')
    kw.send_keys(keyword)
    kw.send_keys(Keys.ENTER)


    has_next = True
    while has_next:
        time.sleep(20)

        #点击按销量排序
        sort_btn = driver.find_element_by_xpath('.//div[@class="f-sort"]/a[2]')
        sort_btn.click()
        time.sleep(15)
        #先获取整个商品区域的尺寸、坐标,根据区域的大小决定往下滑动多少
        goods_list = driver.find_element_by_id('J_goodsList')
        y = goods_list.rect['y'] + goods_list.rect['height']
        driver.execute_script('window.scrollTo(0, %s)' % y)
        time.sleep(10)
        try:
            curr_page = driver.find_element_by_xpath('.//div[@id="J_bottomPage"]//a[@class="curr"]').text
        except:
            driver.refresh()
            time.sleep(10)
            curr_page = driver.find_element_by_xpath('.//div[@id="J_bottomPage"]//a[@class="curr"]').text
        if curr_page == '1':
            time.sleep(30)
        else:
            continue
        print('-----------------current page is %s-------------------------' % curr_page)

        products = driver.find_elements_by_class_name('gl-item')
        print('&&&****'*10,products,len(products))
        print('this page have %s goods' %len(products))
        for p in products:
            row = {}
            print('店名：'*5, p.find_element_by_xpath('//span[@class="J_im_icon"]/a').text)
            row['sku'] = p.get_attribute('data-sku')
            row['price'] = p.find_element_by_css_selector('strong.J_%s' % row['sku']).text
            row['desc'] = p.find_element_by_css_selector('div.p-name>a>em').text
            row['comments'] = p.find_element_by_id('J_comment_%s' % row['sku']).text
            try:
                row['shop'] = p.find_element_by_css_selector('div.p-shop>span>a').text
            except:
                row['shop'] = '无'
            print(row)
            rows.append(row)

        #取下一页
        next_page = driver.find_element_by_css_selector('a.pn-next')
        if 'disabled' in next_page.get_attribute('class'):
            has_next = False
        else:
            next_page.click()

    pyexcel.save_as(records=rows, dest_file_name='%s.xls' % keyword)

    driver.quit()






