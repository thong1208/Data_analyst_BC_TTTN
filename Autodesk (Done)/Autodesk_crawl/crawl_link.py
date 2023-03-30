from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

f = open('Autodesk.txt', 'w', encoding='UTF-8')
input_page = input('How many pages do you want to collect: ')
inputpage =  int(input_page) + 1
class getLink():
    #--------- 1. Mở trang web
    driver = webdriver.Chrome("D:\Documents\Ty\THE BIM FACTORY 4.7.2022\Code\Python\chromedriver (Ver 111 - Check Update)\chromedriver.exe")
    url = 'https://apps.autodesk.com/RVT/en/List/Search?&page=1'
    driver.get(url)

    #--------- 2. Lấy link của 10 itemlist trong 1 trang và qua trang tiếp theo (VÀ LẶP LẠI THAO TÁC NÀY cho đến khi đạt yêu cầu)
    def GetURL():
        all_profile_URL = []
        for i in range(1,25):
            sleep(0.1)
            href_link = getLink.driver.find_element(By.CSS_SELECTOR, '#result-list > li:nth-child('+str(i)+') > a').get_attribute("href")
            print(i , ": ", href_link)
            if href_link not in all_profile_URL:
                all_profile_URL.append(href_link)
                f.write('\n' + href_link)
            
        return all_profile_URL


    def GetURLs_onPages():
        URLs_all_page = []
        for page in range (1, inputpage):
            
            print ('Đang crawl trang: ' + str(page))
            URLs_one_page = getLink.GetURL()
            next_page = getLink.driver.find_element(By.CSS_SELECTOR, '#main > div.main-middle-content > div.right-mainmiddlecontent > div.list-header > div.list-display-options.horizontal-container > div.page-navi > ul > li.next.last.leftborder-pageitem > a')
            next_page.click()
            URLs_all_page = URLs_all_page + URLs_one_page
            sleep(1)
            
        getLink.driver.close()
        print('Crawl link successful! CLOSE CHROME!')
        return URLs_all_page
    
    
    
#--------- Truyền all link lấy được vào profile[]
url_item = []
url_item = getLink.GetURLs_onPages()
print('Total link: ' + str(len(url_item)))