# Import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    browser.quit()
    return data

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    mars={}
    
    # Get the URL for NASA latest news
    url = 'https://redplanetscience.com/'
    # Open the URL
    browser.visit(url)

    # Create the html
    html = browser.html
    soup = bs(html, 'html.parser')
    
    # Get the latest news
    news_latest = soup.find("div", class_="content_title").text
    news_latest_p = soup.find("div", class_="article_teaser_body").text
    mars["news_latest"]=news_latest
    mars["news_latest_p"]=news_latest_p
    
    # Get the images in the JPL Mars Space Image - Featured Image
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    browser.find_by_tag("button")[1].click()

    html = browser.html
    jpl_image = bs(html, "html.parser")
    image = jpl_image.find('img', class_="fancybox-image").get('src')
    # image = jpl_image.find('img', class_="fancybox-image")
    feature_image = "https://spaceimages-mars.com/"+image
    mars["featured_image_url"]=feature_image
    
    # Mars facts
    url = "https://galaxyfacts-mars.com/"
    mars_df = pd.read_html(url)
    mars_df=mars_df[0]

    mars_df.columns=["Description", "Mars", "Earth"]
    mars_df.set_index("Description", inplace=True)
    mars_df
    mars_df_html = mars_df.to_html()
    mars_df_html
    mars["facts"]=mars_df_html
    
    # Mars hemisphere
    url = "https://marshemispheres.com/"
    browser.visit(url)
    result = browser.find_by_css("a.product-item img")
    hemisphere_img_url = []
    for i in range(len(result)):
        hemisphere = {}
        browser.find_by_css("a.product-item img")[i].click()
        element = browser.links.find_by_text('Sample').first
        img_url = element["href"]
        hemisphere["img_url"]=img_url
        hemisphere["title"]=browser.find_by_css("h2.title").text
        hemisphere_img_url.append(hemisphere)
        browser.back()
    hemisphere_img_url
    
    return mars

if __name__ == "__main__":
        print(scrape())