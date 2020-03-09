from scrapy import Spider, Request
from chewy_rx.items import ChewyRxItem
import re, time
import math

class ChewyRxSpider(Spider):
    name = 'chewyrx_spider'
    allowed_domains = ['www.chewy.com']
    start_urls = ['https://www.chewy.com/b/pharmacy-2515']
    print ("#"*50,'in the start url',"#"*50)

    def parse(self, response):
        # Find the total number of pages in the result so that we can decide how many urls to scrape next
        text = response.xpath('//div[@class="results-header__title"]/p[@class="results-count"]/text()').extract_first()
        _, per_page, total = map(lambda x: int(x), re.findall('\d+', text))
        number_pages = math.ceil(int(total)/ int(per_page))
        #print(number_pages)

        # List comprehension to construct all the urls
        result_urls = ['https://www.chewy.com/s?rh=c%3A2515&page={}'.format(x) for x in range(1,number_pages+1)]

        # Yield the requests to different search result urls, 
        # using parse_result_page function to parse the response.
        for url in result_urls:
            yield Request(url=url, callback=self.parse_result_page)


    def parse_result_page(self, response):
        # This fucntion parses the search result page.
        
        # We are looking for url of the detail page.
        detail_urls = response.xpath('//article[@class="product-holder js-tracked-product  cw-card cw-card-hover"]/a[@class="product"]/@href').extract()
        #print(len(detail_urls))

        # Yield the requests to the details pages, 
        # using parse_detail_page function to parse the response.
        
        for url in ['https://www.chewy.com{}'.format(x) for x in detail_urls]:
            yield Request(url=url, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        # product name
        product = (response.xpath('//div[@id="product-title"]/h1/text()').extract_first()).strip()
        # brand name
        brand = response.xpath('//div[@id="product-subtitle"]/a/span/text()').extract_first()
        # regular price
        regular = float((response.xpath('//div[@id="pricing"]/ul/li/p[2]/span[1]/text()').extract_first()).strip().split('$')[1])
        # specific categories of each item
        categories = response.xpath('//li[@itemprop="itemListElement"]/a/span/text()').extract()
        # discounted price
        try:
            discount = float((response.xpath('//div[@id="featured-promotions"]/div/div[2]/p[1]/text()').extract_first()).strip().split('$')[1])
        except:
            discount = regular
        # star
        try:
            star = float(response.xpath('//div[@class="ugc-list_stars"]/span/span[@itemprop="ratingValue"]/text()').extract_first())
        except:
        #     # there is no review
            star = 0
        # number of reviews
        try:
            num_review = int(response.xpath('//span[@itemprop="reviewCount"]/text()').extract_first())
        except:
        #     # there is no review
            num_review = 0


        # when there is review and the number of reviews smaller or equal to 10, we do not need to go to the read all reviews page
        if num_review == 0:
            item=ChewyRxItem()
            item['product']=product
            item['brand']=brand
            item['regular']=regular
            item['discount']=discount
            item['num_review']=num_review
            item['categories'] = categories
            item['star'] = star
            time.sleep(0.3)
            yield item


        elif num_review>0 and num_review <=10:
            reviews=response.xpath('//li[@class="js-content"]')
            # print(len(reviews))
            for review in reviews:   

                #rating=int(review.xpath('/div[@class="ugc-rev__helpful__heading"]/span/picture/img/@alt').extract()[0].split()[0])
                title=(review.xpath('.//h4[@class="ugc__title ugc-list__list__title"]/text()').extract_first()).strip()
                # print(title)
                content=review.xpath('.//span[@class="ugc-list__review__display"]/text()').extract_first()
                # print(content)

                item=ChewyRxItem()
                item['product']=product
                item['brand']=brand
                item['regular']=regular
                item['discount']=discount
                item['num_review']=num_review
                item['categories'] = categories
                item['star'] = star
                    


                item['title']=title
                item['content']=content
                time.sleep(0.3)

                yield item



        else:
            first_review_page = response.xpath('//footer[@class="ugc-list__footer js-read-all"]/a/@href').extract()[0]
            num_review_page=math.ceil(num_review/10)
            review_urls=[first_review_page[:-1]+ str(i) for i in range(1,num_review_page+1) ]
            # print(len(review_urls))

            for url in review_urls: 
                new_url='https://www.chewy.com' + url
                yield Request(url= new_url, meta={'brand': brand, 'product':product, 'regular':regular,'discount':discount, 'num_review':num_review,'categories':categories, 'star':star}, callback = self.parse_review_page)


    def parse_review_page(self, response):
        # print('IN THE PARSE REVIEW PAGE')
        
        # print ("####"*50)

        product=response.meta['product']
        brand=response.meta['brand']
        regular=response.meta['regular']
        discount=response.meta['discount']
        num_review=response.meta['num_review']
        categories=response.meta['categories']
        star=response.meta['star']

        #extract all review tags
        reviews=response.xpath('//li[@class="js-content"]')
        # print(len(reviews))

        for review in reviews:
            
            title=(review.xpath('.//h3[@class="ugc__title ugc-list__list__title"]/text()').extract_first()).strip()
            print(title)
            content=review.xpath('.//span[@class="ugc-list__review__display"]/text()').extract_first()
            print(content)


            item=ChewyRxItem()
            item['product']=product
            item['brand']=brand
            item['regular']=regular
            item['discount']=discount
            item['num_review']=num_review
            item['categories'] = categories
            item['star'] = star
                    

            item['title']=title
            item['content']=content
            time.sleep(0.3)

            yield item

    
           

















