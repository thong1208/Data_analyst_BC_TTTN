import scrapy
from time import sleep
from scrapy_selenium import SeleniumRequest

#Đọc file (LinkProfile.txt) để crawl những link trong đó
with open('D:\Documents\Ty\THE BIM FACTORY 4.7.2022\EventsEye.txt', 'r') as f:
    link_list = f.readlines()
    print ('---------- TOTAL LINK: ' + str(len(link_list)) + ' link')
    
    input_from = input('Muốn crawl từ link nào: ')
    input_to = input('Đến link thứ: ')
    
    list_link_rutgon = link_list[int(input_from):int(input_to)]
    print ('---------- CRAWL: ' + str(len(list_link_rutgon)) + ' link')


class EventseyeSpider(scrapy.Spider):
    name = 'eventseye'
    allowed_domains = ['www.eventseye.com']

    def start_requests(self):
        for link in list_link_rutgon:
            sleep(1)
            yield SeleniumRequest ( url = link ,
                                    wait_time = 3,
                                    callback = self.parse,
                                    )
    def parse(self, response):
        sleep(0.2)
        Name_Event  = response.css ('body > div.title-line > div:nth-child(2) > h1 ::text').get()
        Description = response.css ('body > div.drac-group > div.description ::text').getall()
        Date        = response.xpath('/html/body/table/tbody/tr/td[1]/text()').get()
        Audience    = response.css ('body > div.drac-group > div.ac-group > div.audience ::text').getall()
        Industries  = response.css ('body > div.drac-group > div.industries ::text').getall()
        Cycle       = response.css ('body > div.drac-group > div.ac-group > div.cycle ::text').getall()
        Veneu       = response.xpath('/html/body/table/tbody/tr/td[3]/text()').get()
        Address     = response.css ('body > div.venues > div > div > div.info > div ::text').getall()
        City        = response.xpath('/html/body/table/tbody/tr/td[2]/a/text()').get()
        Country     = response.css ('body > div.venues > div > div > div.info > div > a.countrylink ::text').get()
        Website     = response.css ('body > div.me-group > div.more-info > a.ev-web ::attr(href)').get()
        Link        = response.url
        
        Description = Description[2]
        Audience    = Audience[2]
        Cycle       = Cycle[2]
        Address     = Address[3] + " " + Address[4]
        
        #Làm sạch chuỗi
        Audience    = Audience.replace("\n", " ")
        Veneu       = Veneu.replace("\n", " ")
        Description = Description.replace("\n", " ")
        Cycle       = Cycle.replace("\n", " ")
        Address     = Address.replace("\n", " ")
        
        
        yield {
            #.strip ('@'): dùng để xóa kí tự @ đầu và cuối chuỗi string
            'Name Event'    : Name_Event,
            'Description'   : Description.strip("' '"),
            'Date'          : Date,
            'Audience'      : Audience.strip("' '"),
            'Industries'    : Industries,
            'Cycle'         : Cycle.strip("' '"),
            'Veneu'         : Veneu.strip("' '"),
            'Address'       : Address.strip("' '"),
            'City '         : City,
            'Country'       : Country,
            'Website'       : Website,
            'Link'          : Link
        }

