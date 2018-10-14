
# coding: utf-8

# # Mission to Mars: Web-Scraping

#Importing dependencies 
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import re

# Importing Splinter
from splinter import Browser
browser = Browser("chrome", headless=False)


def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    nasa_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    tweeter_url = "https://twitter.com/marswxreport?lang=en"
    facts_url = 'https://space-facts.com/mars/'
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #Initializing a dictionary to hold mars-related info
    mars_collection = {}
    
    browser = init_browser()
    browser.visit(nasa_url)
    xpath = '//div[@class="content_title"]/a' # Path for news title
    ypath = '//div[@class="article_teaser_body"]' #Path for news teaser
    news_title = browser.find_by_xpath(xpath).first.text
    news_teaser = browser.find_by_xpath(ypath).first.text

    #Saving news title and its teaser to the dictionary
    mars_collection['news_title'] = news_title
    mars_collection['news_p'] = news_teaser

    #Getting the featured image
    browser.visit(jpl_url)
    browser.find_by_id('full_image').click()
    featured_image_url = browser.find_by_css('.fancybox-image').first['src']
    
    mars_collection['featured_image_url'] = featured_image_url 

    #Getting the weather tweet
    browser.visit(tweeter_url)
    for text in browser.find_by_css('.tweet-text'):
        if text.text.partition(' ')[0] == 'Sol':
            mars_weather = text.text
            break

    mars_collection['mars_weather'] = mars_weather

    #Getting mars facts
    tables = pd.read_html(facts_url)
    # Now let's slice off the dataframe using normal indexing.
    mars_df = tables[0]
    mars_df.columns = ['Parameters', 'Values']
    mars_df.set_index('Parameters', inplace=True)
    mars_html = mars_df.to_html()
    mars_html.replace("\n", " ")

    mars_collection['mars_facts'] = mars_html

    # Getting titles and links for each of Mar's hemispheres.
    browser = init_browser()
    browser.visit(usgs_url)
    first = browser.find_by_tag('h3')[0].text
    second = browser.find_by_tag('h3')[1].text
    third = browser.find_by_tag('h3')[2].text
    fourth = browser.find_by_tag('h3')[3].text

    browser.find_by_css('.thumb')[0].click()
    first_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.find_by_css('.thumb')[1].click()
    second_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.find_by_css('.thumb')[2].click()
    third_img = browser.find_by_text('Sample')['href']
    browser.back()

    browser.find_by_css('.thumb')[3].click()
    fourth_img = browser.find_by_text('Sample')['href']

    hemisphere_image_urls = [
        {'title': first, 'img_url': first_img},
        {'title': second, 'img_url': second_img},
        {'title': third, 'img_url': third_img},
        {'title': fourth, 'img_url': fourth_img}
    ]
      
    mars_collection['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_collection
