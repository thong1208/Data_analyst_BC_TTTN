import scrapy
from time import sleep
from scrapy_selenium import SeleniumRequest

#Đọc file để crawl những link trong đó
with open('Autodesk.txt', 'r') as f:
    link_list = f.readlines()
    print ('---------- TOTAL LINK: ' + str(len(link_list)) + ' link')
    
    input_from = input('Muốn crawl từ link nào: ')
    input_to = input('Đến link thứ: ')
    
    list_link_rutgon = link_list[int(input_from):int(input_to)]
    print (list_link_rutgon)
    print ('---------- CRAWL: ' + str(len(list_link_rutgon)) + ' link')

class AutodeskSpider(scrapy.Spider):
    name = 'autodesk'
    allowed_domains = ['apps.autodesk.com']
    
    def start_requests(self):
        for link in list_link_rutgon:
            print (link)
            sleep(0.5)
            yield SeleniumRequest ( url = link ,
                                    wait_time = 3,
                                    callback = self.parse,
                                    )

    def parse(self, response):
        sleep(0.1)
        ProductName = response.css('#detail-title ::text').get()
        ProductLink = response.url
        Rating = response.css('#rating').attrib['value']
        Review = response.css('#detail-rating > a > span ::text').get()
        
        Price = response.css('#purchase > h4 ::text').get()
        
        #Giá của sản phẩm tính theo NĂM
        Price2 = response.css('#price-options > button.flat-button.toggle-btn-item.selected.flat-button-normal ::text').get()
        P2 = Price2
        #Giá của sản phẩm tính theo THÁNG 
        Price3 = response.css('#price-options > button:nth-child(2) ::text').get()
        P3 = Price3 
        
        ReleaseDate = response.css('#right-wrapper > div:nth-child(1) > div.download-info-wrapper > div:nth-child(2) > div.value ::text').get()
        LastUpdated = response.css('#right-wrapper > div:nth-child(1) > div.download-info-wrapper > div:nth-child(3) > div.value ::text').get()
        PublishingCompany = response.css('#detail-info > div.app-details__app-info-top > div.app-details__publisher-link-wrapper > a > span::text').get() 
        LinkCompany = response.css('#detail-info > div.app-details__app-info-top > div.app-details__publisher-link-wrapper > a ::attr(href)').get()
        LinkCompany = 'https://apps.autodesk.com' + LinkCompany
        Review = Review.replace("reviews", "")
        Review = Review.replace("review", "")
        print('--------1: ' ,Price)
        print('--------2: ' ,Price2)
        print('--------3: ' ,Price3)
        
        if str(Price) == 'Free':
            print ('----------------------------1')
            Free = Price
            Price = ''
            Price2 = ''
            Price3 = ''
            Trial = ''
        elif str(Price) == 'Trial':
            print ('----------------------------2')
            Trial = Price
            Free = ''
            Price = ''
            Price2 = ''
            Price3 = ''
        elif str(Price2) == 'None' and str(Price3) == 'None':
            if Price.find('/Year') == -1:
                print ('----------------------------3.1')
                Price = Price.replace("USD", "")
                Free = ''
                Trial = ''
                Price2 = ''
                Price3 = ''
            else:
                print ('----------------------------3.2')
                Price2 = Price.replace("USD", "")
                Price2 = Price2.replace("/Year", "")
                Free = ''
                Trial = ''
                Price = ''
                Price3 = ''

        else:
            if Price2.find('/Month') == -1:
                print ('----------------------------4.1')
                Price2 = Price2.replace('\r\n', "")
                Price2 = Price2.strip('" "')
                Price2 = Price2.replace("USD", "")
                Price2 = Price2.replace("/Year", "")
                
                Price3 = Price3.replace('\r\n', "")
                Price3 = Price3.strip('" "')
                Price3 = Price3.replace("USD", "")
                Price3 = Price3.replace("/Month", "")
            else:
                print ('----------------------------4.2')
                Price2 = P3
                Price3 = P2
                Price2 = Price2.replace('\r\n', "")
                Price2 = Price2.strip('" "')
                Price2 = Price2.replace("USD", "")
                Price2 = Price2.replace("/Year", "")
                
                Price3 = Price3.replace('\r\n', "")
                Price3 = Price3.strip('" "')
                Price3 = Price3.replace("USD", "")
                Price3 = Price3.replace("/Month", "")
            
            Free = ''
            Trial = ''
            Price = ''
            
            
        yield {
            #.strip ('@'): dùng để xóa kí tự @ đầu và cuối chuỗi string
            'Product Name' : ProductName,
            'Product Link' : ProductLink,
            'Rating' : Rating,
            'Review' : Review,
            
            'Free' : Free,
            'Trial' : Trial,
            'Price (USD)' : Price,
            'USD/Year' : Price2,
            'USD/Month' : Price3,
            
            'Release Date' : ReleaseDate,
            'Last Updated' : LastUpdated,
            'Publishing Company' : PublishingCompany,
            'Link Company' : LinkCompany,
        }