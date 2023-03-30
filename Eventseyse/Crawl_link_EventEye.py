from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import NoSuchElementException


f = open('EventsEye.txt', 'w', encoding='UTF-8')

#--------- 1. Mở trang web
driver  = webdriver.Chrome("D:\Documents\Ty\THE BIM FACTORY 4.7.2022\Code\Python\chromedriver (Ver 111 - Check Update)\chromedriver.exe") #Version 111
url     = 'https://www.eventseye.com/fairs/dt1_trade-shows_building-construction-architecture_january_1.html'
driver.get(url)
driver.execute_script("window.scrollTo(0, {});".format(5000))
sleep(0.5)

itemDay = 6
countCheck = 0
for j in range (0,13):
    print (itemDay)
    driver.execute_script("window.scrollTo(0, {});".format(1000))
    sleep(0.5)
    ItemDay_Click = driver.find_element(By.CSS_SELECTOR , 'body > div.monthgraph > div > div > div > svg > a:nth-child('+str(itemDay)+')')
    ItemDay_Click.click()
    print ("Qua tháng")
    sleep (0.5)
    
    
    ItemMonth = driver.find_element(By.CSS_SELECTOR, 'body > div.monthgraph > div > div > div > svg > a:nth-child('+str(itemDay)+') > text:nth-child(3)').text
    itemDay += 1
    print ("Item Month: " ,ItemMonth) 
    #Kiểm tra trong Month đó có bao nhiêu item và lặp trang theo số đó
    for i in range (0, int(ItemMonth) + 1, 50):
        driver.execute_script("window.scrollTo(0, {});".format(1000))
        print ( "Range:  " , i)
        if i == ItemMonth:
            break
        countCheck += 1
        if countCheck == 2:
            driver.refresh()
            #driver.get(driver.current_url)
            print ("CÓ QUẢNG CÁO: Restart lại trang")
        
        ItemPage = driver.find_elements(By.CSS_SELECTOR, 'body > table > tbody > tr')
        print ("Item Page:", len(ItemPage))
        #Lấy item có trong page
        for j in range (1, int(len(ItemPage)) + 1):
            sleep(0.2)
            print ("J: ", j)
            URLlinks        = driver.find_element (By.XPATH, '/html/body/table/tbody/tr['+str(j)+']/td[1]/a').get_attribute("href")
            f.write(URLlinks + '\n')
            print (URLlinks)
            
        #Qua Page
        #Kiểm tra xem đã đến trang cuối chưa (Bằng cách xem có tìm ra được phần tử nút Nextpage nữa hay không)
        try:
            elem = driver.find_element(By.CSS_SELECTOR, 'body > div.pages-links > div:nth-child(2) > a')
            if elem.is_displayed():
                elem.click() # this will click the element if it is there
                print("QUA TRANG!")
            else:
                print ("ĐÃ HẾT TRANG!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        except NoSuchElementException:
            print ("ĐÃ HẾT TRANG!")

