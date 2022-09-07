# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set up Splinter
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere": hemisphere_data(browser)        
    }
    # Stop webdriver and return data
    browser.quit()
    return data



def mars_news(browser):
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    try:
        slide_elem.find('div', class_='content_title')
        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):

    # ## JPL Space Images Featured Image

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()



def hemisphere_data(browser):
    # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for mar_imgs in range(4):
        # Find and click to new pg
        new_pg_elem = browser.find_by_tag('h3')[mar_imgs]
        new_pg_elem.click()

        # Parse the resulting html with soup
        html = browser.html
        img_soup = soup(html, 'html.parser')

        # Find and create the image url
        img_url_rel = img_soup.find('li').a.get('href')
        img_url = f'https://marshemispheres.com/{img_url_rel}'
        
        # Find the title
        title = img_soup.find('h2', class_='title').get_text()
        
        hemispheres_dict = {'img_url':img_url, 'title': title}
        hemisphere_image_urls.append(hemispheres_dict)
        
        browser.back()

    # 4. Print the list that holds the dictionary of each image url and title.
    hemisphere_image_urls

    # 5. Quit the browser
    browser.quit()
    return hemisphere_image_urls




if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())




