from selenium import webdriver
from selenium.webdriver.common.by import By
import scrapy
from scrapy_selenium import SeleniumRequest
from time import sleep
from datetime import date, datetime
import pandas as pd

#--Tạo một dataFrame mới
#df = pd.DataFrame(columns=['Name', 'Date', 'Title', 'Category', 'Country', 'Reveneu', 'Cause of Failure', 'Result', 'Link'])

'''#Connect SQL Server
# conn_sqlServer = pyodbc.connect('Driver={SQL Server};'
#                                 'Server=bimcloud.the-bim-factory.com,1433;'
#                                 'Database=failory;'
#                                 'UID=sa;'
#                                 'PWD=tbf@20.07.2022;')
# cursor = conn_sqlServer.cursor()
# cursor.execute('DELETE FROM [dbo].[interViews]')
# print ("Delete all table 'InterViews'")'''

'''
ID              = 'id'
NAME            = 'name'
DATES           = 'dates'
TITLE           = 'title'
CATEGORY        = 'category'
COUNTRY         = 'country'
REVENUE         = 'revenue'
CAUSEofFAILURE  = 'cause_of_failure'
RESULT          = 'result'
URL_LINK        = 'url_link'
'''

#--------- 1. Mở trang web
driver = webdriver.Chrome("D:\Documents\Ty\THE BIM FACTORY 4.7.2022\Code\Python\Data_analyst_BC_TTTN\Failory\crawler\crawler\spiders\chromedriver.exe") #Version 111
url = 'https://www.failory.com/interviews'
driver.get(url)
sleep (1)

#--------- 2. CUỘN xuống trang cuối để load hết item
driver.execute_script("window.scrollTo(0, {});".format(20000))
sleep (1)   
item = driver.find_elements(By.CSS_SELECTOR, 'body > div:nth-child(3) > div:nth-child(2) > div > div._0-padding-mobile.w-col.w-col-9 > div.jetboost-list-wrapper-1jlx.jetboost-list-wrapper-1oex.jetboost-list-wrapper-1qoz.jetboost-list-wrapper-xr72.jetboost-list-wrapper-xkjo.jetboost-list-wrapper-xk4r.jetboost-list-wrapper-179w.w-dyn-list > div.w-dyn-items > div')
print('-----------Item: ',len(item)) 

#Create table of UserId (from startDate to finalDate)
df = pd.DataFrame(columns=['Name', 'Date', 'Title', 'Category', 'Country', 'Reveneu', 'Cause of Failure', 'Result', 'Link'])  
           
for i in range(1, len(item) + 1):
    URLlinks        = driver.find_element (By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div[1]/div['+str(i)+']/a').get_attribute("href")
    Titles          = driver.find_element (By.XPATH ,'/html/body/div[3]/div[2]/div/div[2]/div[1]/div[1]/div['+str(i)+']/a/div[1]').text 
    Categorys       = driver.find_element (By.XPATH ,'/html/body/div[3]/div[2]/div/div[2]/div[1]/div[1]/div['+str(i)+']/a/div[2]/div[1]').text
    Countrys        = driver.find_element (By.XPATH ,'/html/body/div[3]/div[2]/div/div[2]/div[1]/div[1]/div['+str(i)+']/a/div[2]/div[2]').text
    Cause_of_Fail   = driver.find_element (By.XPATH ,'/html/body/div[3]/div[2]/div/div[2]/div[1]/div[1]/div['+str(i)+']/a/div[2]/div[3]').text
    Revenues        = driver.find_element (By.XPATH ,'/html/body/div[3]/div[2]/div/div[2]/div[1]/div[1]/div['+str(i)+']/a/div[2]/div[4]').text 
    
    Names           = driver.find_element (By.XPATH ,'/html/body/div[3]/div[2]/div/div[2]/div[1]/div[1]/div['+str(i)+']/a/div[3]/div/div[1]').text 
    Dates           = driver.find_element (By.XPATH ,'/html/body/div[3]/div[2]/div/div[2]/div[1]/div[1]/div['+str(i)+']/a/div[3]/div/div[2]').text   

    Dates = datetime.strptime(Dates, "%B %d, %Y")
    
    #Làm sạch chuỗi
    Titles          = Titles.replace("'", '"')
    Categorys       = Categorys.replace("'", '"')
    Countrys        = Countrys.replace("'", '"')
    Cause_of_Fail   = Cause_of_Fail.replace("'", '"')
    Revenues        = Revenues.replace("'", '"')
    Names           = Names.replace("'", '"')
    
    print('\n', i)
    sleep(0.5)
    print(URLlinks,'\n', Titles ,'\n', Categorys,' ', Countrys,' ', Cause_of_Fail,' ', Revenues,'\n',  Names , Dates.date())
    # if THÀNH CÔNG & THẤT BẠI
    if Cause_of_Fail == "":
        print ('Successful Startup!')
        Results = "Succsess"       
            
        '''                                                                          ---INSERT DATA TO SQL SERVER---
        # cursor.execute (f"INSERT INTO [dbo].[interViews] (["+NAME+"], ["+DATES+"], ["+TITLE+"], ["+CATEGORY+"], ["+COUNTRY+"], ["+REVENUE+"], ["+CAUSEofFAILURE+"], ["+RESULT+"], ["+URL_LINK+"])"
        #                 "VALUES                       ( '"+Names+"',  '"+Datess+"' ,   '"+Titles+"',  '"+Categorys+"',  '"+Countrys+"',   '"+Revenues+"',   '"+Cause_of_Fail+"',   '"+Results+"',  '"+URLlinks+"') ")
        # conn_sqlServer.commit()
        '''
   
    else:
        Results = "Fail"
        print ('Failed Startup!')
        
    df = pd.concat([df, pd.DataFrame.from_records([{'Name':                 Names,
                                                    'Date':                 Dates.date(),
                                                    'Title':                Titles,
                                                    'Category':             Categorys,
                                                    'Country':              Countrys,
                                                    'Reveneu':              Revenues,
                                                    'Cause of Failure':     Cause_of_Fail,
                                                    'Result':               Results,
                                                    'Link':                 URLlinks}])])
    
    '''                                                                             ---INSERT DATA TO SQL SERVER---
    # cursor.execute (f"INSERT INTO [dbo].[interViews] (["+NAME+"], ["+DATES+"],   ["+TITLE+"],   ["+CATEGORY+"],   ["+COUNTRY+"],     ["+REVENUE+"],  ["+CAUSEofFAILURE+"],    ["+RESULT+"],   ["+URL_LINK+"])"
    #                 "VALUES                       ( '"+Names+"', '"+Datess+"',   '"+Titles+"',  '"+Categorys+"',  '"+Countrys+"',   '"+Revenues+"',   '"+Cause_of_Fail+"',   '"+Results+"',  '"+URLlinks+"') ")
    # conn_sqlServer.commit()'''

driver.close()       
with pd.ExcelWriter('Failory.xlsx', engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Sheet1')

#--------- 3. In ra tổng số lượng item có là bao nhiêu

# class ItemFailorySpider(scrapy.Spider):
#     name = 'item_failory'
#     allowed_domains = ['www.failory.com']
#     start_urls = ['http://www.failory.com/']

#     def start_requests(self):
#         #Vòng lặp lấy dữ liệu từng item
#         for i in range(1, len(item) + 1):
#             print(i)
#             sleep(0.5)
#             href_link = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[1]/div[1]/div['+str(i)+']/a').get_attribute("href")
#             sleep(0.5)
            
#             yield SeleniumRequest ( url         = href_link,
#                                     wait_time   = 3,
#                                     callback    = self.parse,
#                                     )
            
#     def parse(self, response):
#         sleep(0.1)
#         PostLink = response.url
        
#         Category = response.card1
#         Country = response.CountryX
#         Revenue = response.RevenueX
#         Cause_of_Falure = response.Cause_of_FalureX
        
#         yield {
#             #.strip ('@'): dùng để xóa kí tự @ đầu và cuối chuỗi string
#             'Post Link' : PostLink,
#             'Category' : Category,
#             'Country' : Country,
#             'Revenue' : Revenue,
#             'Cause_of_Falure' : Cause_of_Falure,
#         }


    
    