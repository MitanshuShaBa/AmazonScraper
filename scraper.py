import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.message import EmailMessage

URL = 'https://www.amazon.in/Test-Exclusive-609/dp/B07HGJFVL2/ref=pd_sbs_107_2/257-0163823-3642022?_' \
      'encoding=UTF8&pd_rd_i=B07HGJFVL2&pd_rd_r=9ade700b-9f11-11e9-a5ca-9db2b39189b1&pd_rd_w=wUriD&pd_rd_wg=eMUui&' \
      'pf_rd_p=87667aae-831c-4952-ab47-0ae2a4d747da&pf_rd_r=0QRC27EXQBTGAZYXHYS9&psc=1&refRID=0QRC27EXQBTGAZYXHYS9'

headers = {'User Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                         '75.0.3770.100 Safari/537.36'}

page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


def check_price():
    title = soup.find(id='productTitle').get_text()
    price = soup.find(id='priceblock_dealprice').get_text()

    conv_price = price[2:]
    conv_price = float(conv_price.replace(',', ''))

    print(title.strip())
    print(conv_price)

    if conv_price < 35_000:
        send_email()


def send_email():
    contacts = [EMAIL_ADDRESS, 'rmitanshu@gmail.com']
    msg = EmailMessage()
    msg['Subject'] = 'Email List'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ', '.join(contacts)
    msg.set_content(f'Price below Rs. 38,000\nURL : {URL}')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg)


check_price()
