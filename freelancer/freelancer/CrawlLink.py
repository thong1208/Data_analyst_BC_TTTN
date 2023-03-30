from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

f = open('D:/Documents/Ty/THE BIM FACTORY 4.7.2022/Code/Python/freelancer/freelancer/LinkProfile.txt', 'w', encoding='UTF-8')
input_page = input('How many pages do you want to collect: ')

class getLink():
    #--------- 1. Mở trang web và click vào tắt chế độ online
    driver = webdriver.Chrome("D:\Documents\Ty\THE BIM FACTORY 4.7.2022\Code\Python\Data_analyst_BC_TTTN\freelancer\freelancer\chromedriver.exe")
    url = 'https://www.freelancer.com/freelancers/skills/autodesk-revit-revit-revit-architecture'
    driver.get(url)

    online_click = driver.find_element(By.ID, 'online_only')
    sleep (0.5)
    online_click.click()
    #sleep (0.5)
    #online_click.click()
    print ('------ Click online user successfully! --------')
    
    link_trung = []

    #--------- 2. Lấy link của 10 itemlist trong 1 trang và qua trang tiếp theo (VÀ LẶP LẠI THAO TÁC NÀY cho đến khi đạt yêu cầu)
    def GetURL():
        all_profile_URL = []
        for i in range(1,11):
            print(i)
            sleep(0.2)
            href_link = getLink.driver.find_element(By.CSS_SELECTOR, '#freelancer_list > div:nth-child('+str(i)+') > li > div > div.freelancer-details-header > h3 > a.find-freelancer-username-mobile').get_attribute("href")
            
            if href_link not in all_profile_URL:
                all_profile_URL.append(href_link)
                f.write('\n' + href_link)
            else: 
                getLink.link_trung.append(href_link)
        return all_profile_URL


    def GetURLs_onPages():
        URLs_all_page = []
        number_of_page = int(input_page) + 1
        for page in range (1, number_of_page):
            
            print ('Đang crawl trang: ' + str(page))
            URLs_one_page = getLink.GetURL()
            next_page = getLink.driver.find_element(By.CSS_SELECTOR, '#display_div > div:nth-child(1) > div.ns_pagination.is-desktop-only > ul > li:nth-child(7) > a')
            next_page.click()
            URLs_all_page = URLs_all_page + URLs_one_page
            sleep(2)
            
        getLink.driver.close()
        print('Crawl link successful! CLOSE CHROME!')
        return URLs_all_page
    
    
    
#--------- Truyền all link lấy được vào profile[]
profile = []
profile = getLink.GetURLs_onPages()
print('Total link: ' + str(len(profile)))
print('The number of links is duplicate: ' + str(getLink.link_trung))
