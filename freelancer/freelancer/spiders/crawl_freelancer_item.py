import scrapy
from time import sleep
from scrapy_selenium import SeleniumRequest

#Đọc file (LinkProfile.txt) để crawl những link trong đó
with open("D:/Documents/Ty/THE BIM FACTORY 4.7.2022/Code/Python/freelancer/freelancer/LinkProfile.txt", 'r') as f:
    link_list = f.readlines()
    print ('---------- TOTAL LINK: ' + str(len(link_list)) + ' link')
    
    input_from = input('Muốn crawl từ link nào: ')
    input_to = input('Đến link thứ: ')
    
    list_link_rutgon = link_list[int(input_from):int(input_to)]
    print ('---------- CRAWL: ' + str(len(list_link_rutgon)) + ' link')

class CrawlFreelancerItemSpider(scrapy.Spider):
    name = 'crawl_freelancer_item'
    allowed_domains = ['www.freelancer.com']

    def start_requests(self):
        for link in list_link_rutgon:
            sleep(2.5)
            yield SeleniumRequest ( url = link ,
                                    wait_time = 3,
                                    callback = self.parse,
                                    )
            
    def parse(self, response):
        sleep(0.2)
        Name = response.css('body > app-root > app-logged-out-shell > app-user-profile > fl-bit.Page > fl-bit.PageContent > fl-container > fl-grid > fl-col:nth-child(2) > app-user-profile-summary > fl-card > fl-bit > fl-bit > fl-grid > fl-col:nth-child(3) > fl-grid > fl-col.SummaryHeader > app-user-profile-summary-name > fl-bit > fl-username > fl-bit:nth-child(2) > fl-heading > h3 ::text').get()
        Location = response.css('body > app-root > app-logged-out-shell > app-user-profile > fl-bit.Page > fl-bit.PageContent > fl-container > fl-grid > fl-col:nth-child(2) > app-user-profile-summary > fl-card > fl-bit > fl-bit > fl-grid > fl-col:nth-child(2) > fl-grid > fl-col:nth-child(2) > app-user-profile-summary-information > fl-grid > fl-col > fl-bit > fl-link > a > fl-flag > img').attrib['title']
        Link = response.url #Lấy link hiện tại được gửi qua từ SeleniumRequest
        
        Average_Rating = response.css('body > app-root > app-logged-out-shell > app-user-profile > fl-bit.Page > fl-bit.PageContent > fl-container > fl-grid > fl-col:nth-child(2) > app-user-profile-summary > fl-card > fl-bit > fl-bit > fl-grid > fl-col:nth-child(3) > fl-grid > fl-col:nth-child(2) > app-user-profile-summary-rating > fl-bit > fl-tooltip:nth-child(1) > fl-bit > span > span > fl-rating > fl-bit > fl-bit.ValueBlock.ng-star-inserted ::text').get()
        Review = response.css('body > app-root > app-logged-out-shell > app-user-profile > fl-bit.Page > fl-bit.PageContent > fl-container > fl-grid > fl-col:nth-child(2) > app-user-profile-summary > fl-card > fl-bit > fl-bit > fl-grid > fl-col:nth-child(3) > fl-grid > fl-col:nth-child(2) > app-user-profile-summary-rating > fl-bit > fl-tooltip:nth-child(1) > fl-bit > span > span > fl-rating > fl-bit > fl-bit.ReviewCount.ng-star-inserted ::text').get()
        
        Earnings = response.css('body > app-root > app-logged-out-shell > app-user-profile > fl-bit.Page > fl-bit.PageContent > fl-container > fl-grid > fl-col:nth-child(2) > app-user-profile-summary > fl-card > fl-bit > fl-bit > fl-grid > fl-col:nth-child(3) > fl-grid > fl-col:nth-child(2) > app-user-profile-summary-rating > fl-bit > fl-tooltip.ng-star-inserted > fl-bit > span > span > fl-earnings > fl-bit:nth-child(1) > fl-bit.RightEarningsText.ng-star-inserted > fl-text > div ::text').get()
        
        Jobs_Completed = response.css('body > app-root > app-logged-out-shell > app-user-profile > fl-bit.Page > fl-bit.PageContent > fl-container > fl-grid > fl-col:nth-child(2) > app-user-profile-summary > fl-card > fl-bit > fl-bit > fl-grid > fl-col:nth-child(3) > fl-grid > fl-col:nth-child(4) > app-user-profile-summary-reputation > fl-bit > fl-bit > fl-grid > fl-col:nth-child(1) > app-user-profile-summary-reputation-item > fl-bit > fl-tooltip > fl-bit > span > span > fl-bit > fl-text.ReputationItemAmount > div ::text').get()
        On_Budget = response.css('body > app-root > app-logged-out-shell > app-user-profile > fl-bit.Page > fl-bit.PageContent > fl-container > fl-grid > fl-col:nth-child(2) > app-user-profile-summary > fl-card > fl-bit > fl-bit > fl-grid > fl-col:nth-child(3) > fl-grid > fl-col:nth-child(4) > app-user-profile-summary-reputation > fl-bit > fl-bit > fl-grid > fl-col:nth-child(2) > app-user-profile-summary-reputation-item > fl-bit > fl-tooltip > fl-bit > span > span > fl-bit > fl-text.ReputationItemAmount > div ::text').get()
        On_Time = response.css('body > app-root > app-logged-out-shell > app-user-profile > fl-bit.Page > fl-bit.PageContent > fl-container > fl-grid > fl-col:nth-child(2) > app-user-profile-summary > fl-card > fl-bit > fl-bit > fl-grid > fl-col:nth-child(3) > fl-grid > fl-col:nth-child(4) > app-user-profile-summary-reputation > fl-bit > fl-bit > fl-grid > fl-col:nth-child(3) > app-user-profile-summary-reputation-item > fl-bit > fl-tooltip > fl-bit > span > span > fl-bit > fl-text.ReputationItemAmount > div ::text').get()
        Repeat_Hire_Rate = response.css('body > app-root > app-logged-out-shell > app-user-profile > fl-bit.Page > fl-bit.PageContent > fl-container > fl-grid > fl-col:nth-child(2) > app-user-profile-summary > fl-card > fl-bit > fl-bit > fl-grid > fl-col:nth-child(3) > fl-grid > fl-col:nth-child(4) > app-user-profile-summary-reputation > fl-bit > fl-bit > fl-grid > fl-col:nth-child(4) > app-user-profile-summary-reputation-item > fl-bit > fl-tooltip > fl-bit > span > span > fl-bit > fl-text.ReputationItemAmount > div ::text').get()
        
        Join_Date = response.css('body > app-root > app-logged-out-shell > app-user-profile > fl-bit.Page > fl-bit.PageContent > fl-container > fl-grid > fl-col:nth-child(2) > app-user-profile-summary > fl-card > fl-bit > fl-bit > fl-grid > fl-col:nth-child(2) > fl-grid > fl-col:nth-child(3) > app-user-profile-summary-extra-info > fl-grid:nth-child(2) > fl-col:nth-child(2) > fl-text > div ::text').get()
          
        
        print (Name)
        print (Location)
        print (Link)
        print (Average_Rating)
        print (Review)
        print (Earnings)
        print (Jobs_Completed)
        print (On_Budget)
        print (On_Time)
        print (Repeat_Hire_Rate)
        print (Join_Date)
        #Làm sạch chuỗi
        Review = Review.replace("reviews", "")
        Review = Review.replace("review", "")
        Join_Date = Join_Date.replace("Joined", "")
        Jobs_Completed = Jobs_Completed.replace("N/A" , '0%')
        On_Budget = On_Budget.replace("N/A" , '0%')
        On_Time = On_Time.replace("N/A" , '0%')
        Repeat_Hire_Rate = Repeat_Hire_Rate.replace("N/A" , '0%')
        
        
        yield {
            #.strip ('@'): dùng để xóa kí tự @ đầu và cuối chuỗi string
            'Name' : Name.strip('@'),
            'Location' : Location,
            'Link' : Link,
            
            'Average Rating' : Average_Rating.strip('" "'),
            'Review' : Review.strip('() " "'),
       
            'Earnings' : Earnings.strip('" "'),
            
            'Jobs Completed' : Jobs_Completed.strip('" "'),
            'On Budget' : On_Budget.strip('" "'),
            'On Time' : On_Time.strip('" "'),
            'Repeat Hire Rate' : Repeat_Hire_Rate.strip('" "'),
            
            'Join Date' : Join_Date.strip('" "'),
        
        }