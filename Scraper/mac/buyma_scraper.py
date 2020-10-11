import json
from datetime import date, timedelta, datetime
import pandas as pd
import time

import scrapy
import requests
from fuzzywuzzy import process

def item_name_cleaner(item_name):
    '''
    Parameters
    ----------
    item_name : string
        Raw item name as displayed on Buyma

    Returns
    -------
    string
        Item name without the junk words

    '''
    junk_words = [
    '人気', '大人気', '超人気', '人気商品',
    '人気アイテム', 'コラボ', 'レア', '激レア', '特価',
    '最終', 'セール', '定番', '追加料金',
    '送料無料', '送込', '送料込', '送料込み','国内発送',
    '国内発', '国内即発', '国内在庫', '即発',
    '即納', '最新作', '新作', '入手困難', '関税込', '関税', 
    '関税無料', '無料', '兼用', '日本未発売', '日本未入荷', '海外限定',
    '期間限定', '限定', '完売', '日本完売', '在庫確認', 
    '別注', '追跡', '追跡付', '追跡あり', '追跡有り', 'カラバリ', '直営', 
    '送料込', '送料', '最新', '正規保証', '国内',
    '◆', '〓', '》', '《',
    '☆','★','♦','・','!','!!','【','】','（','）','(',')','：',':'
    ]
    
    for w in junk_words:
        item_name = item_name.replace(w,'')
    
    return item_name

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
    if previous_days > 100:
        previous_days = 100

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
            item_names_cleaned = [item_name_cleaner(i) for i in item_names]
            
            sold_info_xp = '..//li[@class="buyeritemtable_info"]'
            # Get sold amounts
            sold_amounts_unformatted = [buyer_table.xpath(sold_info_xp)[i].xpath('..//p/text()').extract()[-2] 
                                        for i in range(len(item_names))]
            sold_amounts = [int(i.split('：')[1].split('個')[0]) for i in sold_amounts_unformatted]
            # Get sold dates
            sold_dates_unformatted = [buyer_table.xpath(sold_info_xp)[i].xpath('..//p/text()').extract()[-1] 
                                      for i in range(len(item_names))]
            sold_dates = [datetime.strptime(i.split('：')[1], '%Y/%m/%d')  for i in sold_dates_unformatted]

            keys = ['url_ext', 'img', 'item_name','item_name_clean','sold_amount', 'sold_date']

            # Combine to a dictionary
            items_dict+= [dict(zip(keys,[item_url_extensions[i],
                              item_images[i],
                              item_names[i],
                              item_names_cleaned[i],
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
    counter = 0
    for i in buyer_page_data:
        item_url = 'https://www.buyma.com{}'.format(i.get('url_ext'))
        try:
            item_data = item_json(item_url)
        except:
            #item_data = {'ERROR':'PAGE UNAVAILABLE'}
            item_data ={
            'url':'PAGE UNAVAILABLE', 
            'access_count':'PAGE UNAVAILABLE', 
            'fav_count':'PAGE UNAVAILABLE', 
            'syo_id':'PAGE UNAVAILABLE', 
            'syo_name':'PAGE UNAVAILABLE', 
            'syo_img1':'PAGE UNAVAILABLE', 
            'syo_img_090_1':'PAGE UNAVAILABLE', 
            'syo_img_210_1':'PAGE UNAVAILABLE', 
            'syo_url':'PAGE UNAVAILABLE', 
            'tanka_format':'PAGE UNAVAILABLE', 
            'discount_percentage':'PAGE UNAVAILABLE', 
            'on_timesale':'PAGE UNAVAILABLE', 
            'brand_name_eigo':'PAGE UNAVAILABLE', 
            'brand_url':'PAGE UNAVAILABLE', 
            'category_id':'PAGE UNAVAILABLE', 
            'category':'PAGE UNAVAILABLE', 
            'buyer_id':'PAGE UNAVAILABLE', 
            'brand_id':'PAGE UNAVAILABLE', 
            'model_id':'PAGE UNAVAILABLE', 
            'season_id':'PAGE UNAVAILABLE', 
            'thm_id':'PAGE UNAVAILABLE', 
            'kokaidate':'PAGE UNAVAILABLE', 
            'yukodate':'PAGE UNAVAILABLE', 
            'cate_id1':'PAGE UNAVAILABLE', 
            'cate_id2':'PAGE UNAVAILABLE', 
            'cate_id3':'PAGE UNAVAILABLE', 
            'tag_ids':'PAGE UNAVAILABLE', 
            'reference_price_kbn':'PAGE UNAVAILABLE', 
            'reference_price':'PAGE UNAVAILABLE', 
            'timesale_start_date':'PAGE UNAVAILABLE', 
            'timesale_end_date':'PAGE UNAVAILABLE', 
            'item_id':'PAGE UNAVAILABLE', 
            'price':'PAGE UNAVAILABLE', 
            'coupon':'PAGE UNAVAILABLE'}
            
        all_item_data = {**i, **item_data}
        items.append(all_item_data)

        # Try not to spam the network too much
        counter += 1
        if counter == 10:
            time.sleep(5)
            counter = 0

    return items


def fuzzy_extract(target_item_name, list_of_item_names, minimum_score=90):
    '''
    Parameters
    ----------
    target_item_name: string
        Item name.
    list_of_item_names : list
        List of strings.
    minimum_score : Int
        Set the minimum fuzzy score value, default set to 90.
        100 = exact match
        0 =  not matching at all

    Returns
    -------
    List
        List of tuples containing the matching item name and the fuzzy score
        if it is equal to or above the minimum score.
        
        Example
        [("THE NORTH FACE M'S TECH NUPTSE S S R TEE YU212", 100),
         ("THE NORTH FACE M'S TECH NUPTSE S S R TEE YU212", 100),
         ("THE NORTH FACE M'S TECH NUPTSE S S R TEE YU212", 100),
         ('THE NORTH FACE NUPTSE S/S R/TEE YU211', 87),
         ('THE NORTH FACE NUPTSE S/S R/TEE YU211', 87)]
        
    '''
    close_matches = []
    
    init_scores = process.extract(target_item_name, list_of_item_names)
    for i in init_scores:
        if i[1] >= minimum_score:
            close_matches.append(i)
    
    return close_matches


def similar_items(listed_items, minimum_score=90):
    '''Fuzzy string matching will be applied to all CLEAN item names in a list of items.
    If another item has a match of 90-100, the url_extension will be noted,
    And the sold amount will be aggregrated.

    Parameters
    ----------
    listed_items : List
        List of dictionaries containing:
            'url_ext', 'img', 'item_name', 'item_name_clean', 'sold_amount', 'sold_date'

    Returns
    -------
    List
        List of dictionaries containing:
            'url_ext', 'img', 'item_name',  'item_name_clean', 
            'sold_amount', 'sold_date', 
            'similar_url_ext', 'sold_amount_agg'
    '''
    
    updated_listed_items = listed_items
    
    for i in range(len(listed_items)):
        # Distinguish between target item and other items
        target_item = listed_items[i].get('item_name_clean')
        
        if i == 0:
            other_items = [li for li in listed_items[1:]]
        elif i == len(listed_items):
            other_items = [li for li in listed_items[:-1]]
        else:
            other_items = [li for li in listed_items[i+1:]] + [li for li in listed_items[:i]]
        
        similar_url_ext = []
        sold_amount_agg = listed_items[i].get('sold_amount')
        # Get Fuzzy Scores for all other items
        for other_item in other_items:
            fuzzy_score = fuzzy_extract(target_item, [other_item.get('item_name_clean')], minimum_score)
            # add the url extension and sold amount aggregate to 
            # target item dictionary if it is a close match
            if fuzzy_score != []:
                similar_url_ext.append(other_item.get('url_ext'))
                sold_amount_agg += other_item.get('sold_amount')
            updated_listed_items[i]['similar_url_ext'] = similar_url_ext
            updated_listed_items[i]['sold_amount_agg'] = sold_amount_agg
        
    return updated_listed_items
    

def extra_search(search_item_name):
    '''
    Parameters
    ----------
    item_name : string
        Name of the item to be searched in Buyma

    Returns
    -------
    Dictionary containing found items.
    '''
    
    # Format the item name into a Buyma search URL string
    item_name_formatted = search_item_name.replace(' ','%20')
    url = 'https://www.buyma.com/r/-F1/{}'.format(item_name_formatted)
    
    response = scrapy.Selector(text=requests.get(url, timeout=10).text)
    
    # Item info
    prices = response.xpath('//div[@id="n_ResultList"]/ul/li/div[1]/div[1]/a/@price').extract()
    item_ids = response.xpath('//div[@id="n_ResultList"]/ul/li/div[1]/div[1]/a[1]/@item-id').extract()

    brand_names = response.xpath('//div[@id="n_ResultList"]/ul/li/div/div/a/@brand_name').extract()

    item_names = response.xpath('//div[@id="n_ResultList"]/ul/li//img/@alt').extract()
    item_names_clean = [item_name_cleaner(i) for i in item_names]
    images = response.xpath('//div[@id="n_ResultList"]/ul/li//img/@src').extract()
    
    # Buyer info
    buyer_names =  response.xpath('..//div[@class="product_Buyer"]/a/text()').extract()
    buyer_url_slugs =  response.xpath('..//div[@class="product_Buyer"]/a/@href').extract()
    buyer_ids = [b.split('/')[-1].split('.')[0] for b in buyer_url_slugs]
    
    items_dict = []
    keys = ['price', 'item_id', 'brand', 'item_name', 'item_name_clean', 'image', 'buyer_name', 'buyer_id']
    # Combine to a dictionary
    items_dict+= [dict(zip(keys,[prices[i],
                      item_ids[i],
                      brand_names[i],
                      item_names[i],
                      item_names_clean[i],
                      images[i],
                      buyer_names[i],
                      buyer_ids[i]])) 
                  for i in range(len(prices))]

    return items_dict


def extra_search_similar_items(search_item_name, listed_items, minimum_score=90):
    '''Fuzzy string matching will be applied to all results from an extra_search
    and matched against a search_item_name.
    
    Matches that are within the fuzzy minimum score threshold will be returned

    Parameters
    ----------
    listed_items : List
        List of dictionaries containing:
            'price', 'item_id', 'brand', 'item_name', 'item_name_clean', 'image', 'buyer_name', 'buyer_id'

    Returns
    -------
    List
        List of dictionaries containing:
            'price', 'item_id', 'brand', 'item_name', 'item_name_clean', 'image', 'buyer_name', 'buyer_id'
    '''
    
    # Get all of the CLEAN names
    all_clean_names = [i['item_name_clean'] for i in listed_items]
    search_item_name_clean = item_name_cleaner(search_item_name)
    
    # Filter and keep only the scores that are at least the minimum score
    good_matches = []
    
    for i in range(len(listed_items)):
        # Run a fuzzy match against the cleaned search item name
        fuzzy_score = process.extract(search_item_name_clean, [all_clean_names[i]])[0][-1]
        if fuzzy_score >= minimum_score:
            similarity_score = {'similarity_score':fuzzy_score}
            good_matches.append({**listed_items[i],**similarity_score})
        
    return good_matches

def similar_extra_search(search_item_name, minimum_score=85):
    '''Search query with fuzzy string matching applied to all results 
    matched against a search_item_name.
    
    Matches that are within the fuzzy minimum score threshold will be returned

    Parameters
    ----------
    search_item_name : string
        Search Item Query

    minimum_score : integer
        Minimum fuzzy score

    Returns
    -------
    List
        List of dictionaries containing:
            'price', 'item_id', 'brand', 'item_name', 'item_name_clean', 'image', 'buyer_name', 'buyer_id', 'similarity_score'
    '''
    
    search = extra_search(search_item_name)
    similar_items = extra_search_similar_items(search_item_name, search, minimum_score)
    
    return similar_items
    
    
    
    

#buyer_page_data = seller_list('https://www.buyma.com/buyer/4880785/sales_1.html', 60)

#all = all_listed_items_details('https://www.buyma.com/buyer/4880785/sales_1.html', 60)

#df_all = pd.DataFrame(all)

#df_all.to_csv('test.csv')



#item_json('https://www.buyma.com/item/53799545/')

#good example:  https://www.buyma.com/buyer/3556134/sales_1.html

