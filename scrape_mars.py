from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd


def init_browser():
    executable_path = {'executable_path': '../chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    results_dict = {}
    # #### Scraping Mars News 
    # GET Mars News HTML
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    news_html= requests.get(news_url).text
    soup = BeautifulSoup(news_html, 'html.parser')
    # Find Latest Article Title
    news_title = soup.find('div', class_="content_title").text.strip()
    # Find latest Article body
    news_p = soup.body.find('div', class_="rollover_description_inner").text.strip()
    # Add output to result dictionary
    results_dict["news_title"] = news_title
    results_dict["news_body"] = news_p

    # #### Scraping Mars Twitter
    # GET Mars Twitter Account HTML
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    twitter_html = requests.get(twitter_url).text
    #Find Latest Tweet Text
    soup = BeautifulSoup(twitter_html, 'html.parser')
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip()
    # Add output to result dictionary
    results_dict["weather"] = mars_weather

    # #### Scrape Mars Facts Table 
    # GET Tables from Mars Facts using Pandas
    facts_url = "https://space-facts.com/mars/"
    facts_html = requests.get(facts_url).text
    facts_df = pd.read_html(facts_html)
    # Find Mars Table and convert it to HTML
    facts_table = facts_df[1].to_html()
    # Add output to result dictionary
    results_dict["facts_html"] = facts_table

    # #### Scrape Mars Featured Image
    # GET Featured Image Page HTML and Find Featured Image URL
    image_html = requests.get("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars").text
    soup = BeautifulSoup(image_html, 'html.parser')
    image = soup.find('a', class_="button fancybox")
    image_url_extension = image['data-fancybox-href']
    featured_image_url = f"https://www.jpl.nasa.gov{image_url_extension}"
    # Add output to result dictionary
    results_dict["featured_image"] = featured_image_url
    
    # #### Scrape 4 Mars Images

    # Create all our input and output variables
    images = ['Cerberus', 'Schiaparelli', 'Syrtis Majo', 'Valles Marineris']
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser = init_browser()
    hemisphere_image_urls = []
    # Run a Loop to capture all image URL's
    for i in images:
        browser.visit(url)
        browser.click_link_by_partial_text(i)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image_url = soup.find('li').find('a')['href']
        image_dict = {}
        image_dict["title"] = f"{i} Hemisphere Enhanced"
        image_dict["img_url"] = image_url
        hemisphere_image_urls.append(image_dict)
    # Add output dict to result dict
    results_dict["hemisphere_images"] = hemisphere_image_urls

    return results_dict
    
