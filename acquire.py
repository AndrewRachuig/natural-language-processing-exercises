from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import os

def get_blog_links(soup, existing_list):
    blog_list = existing_list
    for a in soup.select('a'):
        if 'read more' in a.text:
            blog_list.append(a['href'])
    return blog_list

def get_next_page(soup):
    for a in soup.select('a'):
        if 'Older Entries' in a.text:
            return a['href']

def get_soup(url):
    headers = {'User-Agent': 'Codeup Data Science'}
    response =  get(url, headers = headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def get_all_blog_links(initial_url):
    existing_list = []
    url = initial_url
    while True:
        soup = get_soup(url)
        existing_list = get_blog_links(soup, existing_list)
        url = get_next_page(soup)
        if url == None:
            return existing_list

def get_all_codeup_blogs(reaquire = False):
    # Setting base filename
    filename = 'master_blog_list.csv'

    # If reaquisition of the data is required or no data exists in filename provided, acquire data anew.
    if (reaquire == True) or (os.path.isfile(filename) == False):
        master_list = get_all_blog_links('https://codeup.com/blog/')
        title = []
        content = []
        link = []
        date = []
        for i in range(len(master_list)):
            page = get_soup(master_list[i])
            date.append(page('p')[0].text.split('|')[0])
            title.append(page.title.text)
            link.append(master_list[i])
            content.append(page.article.text.strip())
        all_info = {'title':title, 'date':date, 'content':content, 'link':link}
        
        # Put data into a DataFrame
        df = pd.DataFrame(all_info)
        
        # Save a locally cached copy of data
        df.to_csv(filename, index = False)

        return df

    else:
        return pd.read_csv(filename)

def get_all_inshorts_articles(reaquire = False):
    # Setting base filename
    filename = 'in_shorts_articles.csv'

    # If reaquisition of the data is required or no data exists in filename provided, acquire data anew.
    if (reaquire == True) or (os.path.isfile(filename) == False):

        # Setting base variables
        base_url = 'https://inshorts.com/en/read/'
        category_list = ['business', 'sports', 'technology', 'entertainment']
        full_list = []

        # Making a for loop to go to the pages of all the categories
        for cat in category_list:

            # Getting the soup object
            url = base_url + cat
            headers = {'User-Agent': 'Codeup Data Science'}
            response = get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Getting the page articles
            page = soup.select('div[class = "news-card z-depth-1"]')

            # Getting the article title and content for the page
            for i in range(len(page)):
                single = {'title': (page[i].select('span[itemprop = "headline"]')[0].text), 
                        'content': (page[i].select('div[itemprop="articleBody"]')[0].text) , 
                        'category': cat}
                full_list.append(single)
        
        # Put data into a DataFrame        
        df = pd.DataFrame(final)

        # Save a locally cached copy of data
        df.to_csv(filename, index = False)

        return df
    else:
        return pd.read_csv(filename)