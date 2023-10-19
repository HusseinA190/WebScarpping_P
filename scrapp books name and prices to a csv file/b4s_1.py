import requests
from bs4 import BeautifulSoup
import csv



#  get the page content using requests -- requests.get(page_link)

# enter the page number you want to retrieve books from it
page_num = int(input("ENter the page number : "))


page = requests.get(f"https://printige.net/page/{page_num}")


#  create a function to retrieve page content 
def get_content(page):

    # books_info 
    book_data = []

    data = page.content # this will return content in non-formatted way

    # then we parse it using beautiful soup parser "lxml" BeautifulSoup(content,parser)
    soup = BeautifulSoup(data,'lxml')

    # then we try to find divs that have our desired content
    area_books = soup.find('div' , {'class':'shop-container'}).find('div',{'class':'products'}).find_all('div',{'class':'col-inner'})

    def get_info(area_books):

        for i in range(len(area_books)):

            # get book-title
            book_title = area_books[i].find('p',{'class':'product-title'}).text.strip()


            # navigate book-price span
            book_prices = area_books[i].find('span',{'class':'price'}).contents

            # as there are books that dosen't have discount we should handle it 
            if len(book_prices)>2:

                # book-actual-price
                real_price = book_prices[0].text.strip().replace("\xa0",' ')

                # book-discounted-price
                discount_price = book_prices[2].text.strip().replace("\xa0",' ')

            elif len(book_prices) == 2:
                discount_price = '--'
            else:
                discount_price = '--'
                real_price = '--'

            #  adding data 
            book_data.append({
                'book-name':book_title,
                'actual-price':real_price,
                'discount-price':discount_price
            })


    # then saving data to csv file
    headers = book_data[0].keys() # getting headers

    with open(f"printige_books{page_num}.csv",'w',encoding='utf-8') as output_file:

        writer = csv.DictWriter(output_file,headers)

        writer.writeheader()

        writer.writerows(book_data)

        print('file created')
    

# then call the function
get_content(page)