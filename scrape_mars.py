

def scrape():


    # import dependencies
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    import requests
    import os
    from splinter import Browser
    from webdriver_manager.chrome import ChromeDriverManager
    import pymongo
    from flask import Flask, render_template, redirect




    # url to be scraped
    mars_url = 'https://redplanetscience.com/'



    # prepare browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)



    # visit the url
    browser.visit(mars_url)



    # create beautiful soup object with html parser
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html = browser.html
    news_soup = bs(html, 'html.parser')



    # collect the most recent article title and store it in a variable
    news_title = news_soup.find('div', class_='content_title').text
    print(news_title)



    # collect the text of the most recent article and store it in a variable
    news_p = news_soup.find("div", class_="article_teaser_body").text
    print(news_p)


    #news_soup


    # url to be scraped

    space_url = 'https://spaceimages-mars.com'


    #visit url
    browser.visit(space_url)


    # create beautiful soup object with html parser
    space_html = browser.html
    space_soup = bs(space_html, 'html.parser')


    #print(space_soup)


    # save the url for the featured image to a variable
    image = space_soup.find('img', class_="headerimage fade-in").get('src')

    print(image)


    #concatenate base url with / and image to create full image url
    image_url = space_url + '/' + image
    image_url


    # put the desired url in a variable
    facts_url = 'https://galaxyfacts-mars.com'



    # read the table at that url into Pandas
    table = pd.read_html(facts_url)
    table



    type(table)


    # convert the table to a DataFrame

    facts_df = table[0]


    # rename columns
    facts_df.columns=['Comparison', 'Mars', 'Earth']


    # drop unnecessary row
    facts_df = facts_df.drop(0, axis=0)
    facts_df


    #convert the dataframe to html
    html_table = facts_df.to_html()


    html_table


    # alias url for scraping hemisphere images
    hemi_url = 'https://marshemispheres.com/'



    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)



    # visit url
    browser.visit(hemi_url)




    # create beautiful soup object with html parser
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html = browser.html
    hemi_soup = bs(html, 'html.parser')



    #hemi_soup


    # prepare for loop
    pre_loop = hemi_soup.find("div", class_="collapsible results")



    # get specific portion for loop
    loop = pre_loop.find_all('a')

    #loop



    # loop through html to get titles and urls for hemisphere images and store them in a list of dictionaries
    hemisphere_image_urls = []
    for x in loop:
        if x.h3:
            title = x.h3.text
            new_url = hemi_url + x['href']
            browser.visit(new_url)
            browser.is_element_present_by_css('div.list_text', wait_time=1)
            html = browser.html
            new_soup = bs(html, 'html.parser')
            part = new_soup.find('img', class_="wide-image").get('src')
            full_url = hemi_url + part
            hemi_dict = {}
            hemi_dict['title'] = title
            hemi_dict['image_url'] = full_url
            hemisphere_image_urls.append(hemi_dict)
            browser.back()
            


    # new_url

    # full_url


    # check that titles and urls were collected correctly
    hemisphere_image_urls

    mars_dictionary = {}
    mars_dictionary['news_title'] = news_title
    mars_dictionary['news_paragraph'] = news_p
    mars_dictionary['mars_image'] = image_url
    mars_dictionary['mars_facts_table'] = html_table
    mars_dictionary['hemisphere_images'] = hemisphere_image_urls

    return mars_dictionary





