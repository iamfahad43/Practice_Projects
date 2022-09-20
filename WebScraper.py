from fake_headers import Headers
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs4


the_headers = Headers(os="win", headers=True).generate()


# a function that takes parent link as input and return scrapped products in dataframe
def Parent_To_Child_Scrapped(parent_link):
    
    HEADER = Headers(os="win", headers=True).generate()
    # response for the parent link
    response = requests.get(parent_link, headers=HEADER)
    soup = bs4(response.content, 'html.parser')
    
    # list to store the individual products link
    Products_List_From_Parent_Link = []
    ultag = soup.find('ul', {'class': 'products-grid product-listing deal-category'})
    # title of main category
    Title = soup.find('h1', {'class': 'category-title-h1'})
    if ultag:
        for litag in ultag.find_all('li'):
            for a in litag.find_all('a', href=True):
                Products_List_From_Parent_Link.append(a['href'])
    
    print(f'fetched {len(Products_List_From_Parent_Link)} products from this link')
    
    Name_List = []
    Price_List = []
    Description_List = []
    Image_List = []
    
    # dataframe to save the results
    Scrap_DF = pd.DataFrame(columns = ['Name', 'Price', 'Description', 'Images'])
    
    # loop through each individual link
    for index, single_product_link in enumerate(Products_List_From_Parent_Link):
        response = requests.get(single_product_link)
        soup = bs4(response.content, 'html.parser')
        # title of product
        product_title = soup.find('h1')
        if product_title:
            Name_List.append(product_title.text)
#             Scrap_DF['Name'] = product_title.text
#         print(product_title.text)
        # title of product
        product_price = soup.find('span', {'class': 'regular-price'})
        if product_price:
            Price_List.append(product_price.text)
#             Scrap_DF['Price'] = product_price.text
#         print(product_price.text)
        # description of product
        product_description = soup.find('ul', {'class': 'description'})
        if product_description:
            Description_List.append(product_description.text)
            Scrap_DF['Description'] = product_description.text
#         print(product_description.text)
        # image main
        product_image = soup.find('a', {'class': 'MagicZoom'})
        image_link = product_image['href']
        if image_link:
            Image_List.append(image_link)
#             Scrap_DF['Images'] = image_link
        
        print(f'successfully scraped {index+1} product out of {len(Products_List_From_Parent_Link)}\t{Title.text}\n')
    
    # now it's time to save the data into pandas data frame
    data = {'Name': pd.Series(Name_List),
            'Price': pd.Series(Price_List),
            'Description': pd.Series(Description_List),
            'Images': pd.Series(Image_List)
            }

#     df = pd.DataFrame(data, columns = ['Name', 'Price', 'Description', 'Images'])
    df = pd.DataFrame(data)
    df.to_excel(f'{Title.text}.xlsx')


# scrap the parent links from main website
response = requests.get('https://www.mobilesentrix.com/', headers=the_headers)
soup = bs4(response.content, 'html.parser')

# loop through each category
for ultag in soup.find_all('ul', {'role': 'navigation'}):
    # A list where the link will be stored
    LinkList = []
    for litag in ultag.find_all('li'):
        for a in litag.find_all('a', href=True):
            print(a['href'])
            LinkList.append(a['href'])
        print("*" * 100)
        
LinkList2 = []

for i in LinkList:
    if 'https://www.mobilesentrix.com/' in i:
        LinkList2.append(i)
        
for the_link in LinkList2[24:1000]:
    Parent_To_Child_Scrapped(the_link)
    


