import scrapy
import requests
import json
from datetime import date, timedelta, datetime
import pandas as pd

def item_json(url):
    '''Gets the item data from the JSON of an item page.
    INPUT: Item page URL
    OUTPUT: JSON data'''

    # Get a response from the URL
    response = scrapy.Selector(text=requests.get(url, timeout=10).text)
    
    # Get tracking data
    track_item_response = response.xpath('//meta[@name="buyma:track_item_json"]/@content').get()
    track_item_json = json.loads(track_item_response)
    # Get main item data
    recent_item_response = response.xpath('//meta[@name="buyma:recent_item_json"]/@content').get()
    recent_item_json = json.loads(recent_item_response)
    # Get access data
    access = response.xpath('//span[@class="ac_count"]/text()').get()
    # Get favourite data
    fav = response.xpath('//span[@class="fav_count"]/text()').get().split('人')[0]
    
    # Combine JSON data and output
    return {'url':url, 'access_count': int(access), 'fav_count': int(fav), **recent_item_json,**track_item_json}

#item_json('https://www.buyma.com/item/53799545/')

def seller_list(buyer_page_url, previous_days):
    '''Gets the base data for items listed on a page.
    A date threshold can be set which will tell the scraper to stop going through
    past pages depending on the sale date of the last item on that page.
    INPUT: Buyer page url, number of days from today to previously check
    OUTPUT: List of JSON data 
    '''
    
    items_dict = []
    dt_threshold = datetime.today() - timedelta(previous_days)
    page_number=1
    buyer_id = buyer_page_url.split('/')[4]
    while True:
        try:
            url = 'https://www.buyma.com/buyer/{}/sales_{}.html'.format(buyer_id,page_number)
            
            response = scrapy.Selector(text=requests.get(url, timeout=10).text)
            buyer_table = response.xpath('//div[@id="buyeritemtable"]')

            # Get item urls
            item_url_extensions = buyer_table.xpath('..//li[@class="buyeritemtable_img"]/a/@href').extract()
            # Get item_images
            item_images = buyer_table.xpath('..//img/@src').extract()
            # Get item_names
            item_names = buyer_table.xpath('..//img/@alt').extract()
            # Get sold amounts
            sold_amounts_unformatted = buyer_table.xpath('..//li[@class="buyeritemtable_info"]/p[2]/text()').extract()
            sold_amounts = [int(i.split('：')[1].split('個')[0]) for i in sold_amounts_unformatted]
            # Get sold dates
            sold_dates_unformatted = buyer_table.xpath('..//li[@class="buyeritemtable_info"]/p[3]/text()').extract()
            sold_dates = [datetime.strptime(i.split('：')[1], '%Y/%m/%d')  for i in sold_dates_unformatted]

            keys = ['url_ext', 'img', 'item_name','sold_amount', 'sold_date']

            # Combine to a dictionary
            items_dict+= [dict(zip(keys,[item_url_extensions[i],
                              item_images[i],
                              item_names[i],
                              sold_amounts[i],
                              sold_dates[i]])) 
                          for i in range(len(item_url_extensions))]
            print('Buyer page:', page_number)
            print('Last date sold:', sold_dates[-1])
            
            # Loop check
            if sold_dates[-1] > dt_threshold:
                page_number+=1
            else:
                print('end')
                break
                
        except:
            print('No more item pages to get in time frame')
            break

        
    return items_dict

#seller_list('https://www.buyma.com/buyer/4880785/sales_1.html', 60)

def all_listed_items_details(buyer_page_url, previous_days):
    '''Gets the base data for items listed on a page.
    A date threshold can be set which will tell the scraper to stop going through
    past pages depending on the sale date of the last item on that page.
    From the gathered URLs, each item page is accessed individually and the
    pages are scraped.
    INPUT: Buyer page url, number of days from today to previously check
    OUTPUT: List of JSON data 
    '''
    
    # Get the list of items
    buyer_page_data = seller_list(buyer_page_url, previous_days)

    items = []
    for i in buyer_page_data:
        item_url = 'https://www.buyma.com{}'.format(i.get('url_ext'))
        try:
            item_data = item_json(item_url)
        except:
            item_data = {'ERROR':'PAGE UNAVAILABLE'}
        all_item_data = {**i, **item_data}
        items.append(all_item_data)
    
    return items

#buyer_page_data = seller_list('https://www.buyma.com/buyer/4880785/sales_1.html', 60)

#all = all_listed_items_details('https://www.buyma.com/buyer/4880785/sales_1.html', 60)

#df_all = pd.DataFrame(all)

#df_all.to_csv('test.csv')



#item_json('https://www.buyma.com/item/53799545/')



