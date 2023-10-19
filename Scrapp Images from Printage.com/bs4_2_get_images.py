import io
import os
from bs4 import BeautifulSoup
import requests


os.chdir(r'F:\Python\Web Scrapping\w1\books_imgs')

page = requests.get("https://printige.net/")

# so we can get the page content using .content
page.content

# also with .text
page.text

# first we parse the content using bs4
soup = BeautifulSoup(page.content,'html.parser')

#  also to get it more handy we use .prettify() this after we parse it using bs4
# print(soup.prettify())


#  now we are looking for images of books 
area_books = soup.find('div' , {'class':'shop-container'}).find('div',{'class':'products'}).find_all('div',{'class':'col-inner'})

def get_images(area_books):

    for i in range(len(area_books)):
        # find the actual image 
        img_page = area_books[i].find('div',{'class':'box-image'}).find('a')

        image_name =img_page['aria-label']

        #  going to img link 
        img_link = requests.get(img_page['href'])
        img_soup = BeautifulSoup(img_link.content,'html.parser')

        #  get the img div 
        real_img = img_soup.find('div',{'class':'product-container'}).find('a')

        # get content of an image 
        image_info = requests.get(real_img['href']).content

        # then write and save the image 
        with open(f'{image_name}.png','wb') as f:
            f.write(image_info)

get_images(area_books)