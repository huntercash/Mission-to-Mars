from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import cssutils
import time
import pandas as pd
import requests


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
    # Windows USERS -> Uncommented these 2 lines below, and comment out the top 2 lines
    #executable_path = {'executable_path': 'resources/v74/chromedriver.exe'}
    #return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    # Define URL Links
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    mars_space_url = 'https://www.jpl.nasa.gov'
    mars_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    mars_facts_url = 'https://space-facts.com/mars/'
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Scrape Text From Nasa Mars News
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    article = soup.find('div', class_="slide")
    news_title = article.find('div', class_='content_title').text
    news_p = article.find('div', class_='rollover_description_inner').text
    # Scrape Featured Image
    mars_image_response = requests.get(mars_image_url)
    mars_soup = bs(mars_image_response.text, 'html.parser')
    mars_div = mars_soup.find('article')['style']
    mars_url = mars_div.split("('", 1)[1].split("')")[0]
    featured_image_url = f'{mars_space_url}{mars_url}'

    # 3. Mars Weather - Twitter
    weather_response = requests.get(weather_url)
    weather_soup = bs(weather_response.text, 'html.parser')
    weather_tweet = weather_soup.find('p', class_='TweetTextSize').text

    # 4 Mars Facts - table containing facts about the planet including Diameter, Mass, etc.
    mars_data = pd.read_html(mars_facts_url)
    df = mars_data[0]
    df.columns = ['Description', 'Values']
    df.replace("\n","")
    df.to_html('resources/mars_table.html') 
    html_table = ('resources/mars_table.html')

    # 5 Mars Hemispheres - Use a Python dictionary to store the data using the keys img_url and title
    
    # Create an Empty List to hold the dicitionary 
    hemisphere_list = []
    # Call the Function
    browser = init_browser()
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    time.sleep(1)


    html = browser.html
    hem_soup_master = bs(html, 'html.parser')
    items = hem_soup_master.find_all('div', class_='item')

    for item in items:
        item_url = item.find('h3').text
        try:
            browser.find_link_by_partial_text(item_url)[0].click()
            time.sleep(3)
        except ElementDoesNotExist:
            print("Complete")
            
        html = browser.html
        hem_soup_two = bs(html, 'html.parser')
        hemisephere_image = hem_soup_two.find('img', class_='wide-image')['src']
        hemisphere_title = hem_soup_two.find('h2', class_='title').text
        
        hemisphere_dict = {}
        hemisphere_dict["img_url"] = "https://astrogeology.usgs.gov" + hemisephere_image
        hemisphere_dict["title"] = hemisphere_title
        hemisphere_list.append(hemisphere_dict)
        
        browser.back()
    browser.quit()
    # Store data in a dictionary
    scape_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "weather_tweet": weather_tweet,
        "table": html_table,
        "hemisphere_list":  hemisphere_list

    }
    return scape_data 