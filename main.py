from bs4 import BeautifulSoup
import requests
import smtplib
import os


target_price = 1500.00
smtp_address = "smtp.gmail.com"
email = os.environ['EMAIL']
password = os.environ['PW']
to_email = os.environ['TO']

AMAZON_ENDPOINT = "https://www.amazon.co.uk/Lenovo-ThinkPad-i7-8665U-Backlit-Keyboard/dp/B08XBM3PTQ/ref=sr_1_37?dchild=1&keywords=lenovo+thinkpad&qid=1623497479&sr=8-37"

amazon_headers = {
"Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
}

response = requests.get(url=AMAZON_ENDPOINT, headers=amazon_headers)
website_data = response.text

soup = BeautifulSoup(website_data, "lxml")
price = soup.find(class_= "priceBlockBuyingPriceString").getText()
price = price.replace("£", "")
price = float(price.replace(",", ""))

product_name = soup.find(id="productTitle").getText().replace("\n", "")
email_body = f"Subject: Low price for {product_name}!\n\n The item you are watching - {product_name} - is below your target price of £{target_price:.2f}.\nIf you would like to purchase, please visit:\n{AMAZON_ENDPOINT}"

if price < target_price:
    connection = smtplib.SMTP(smtp_address)
    connection.starttls()
    connection.login(user=email, password=password)
    connection.sendmail(from_addr=email,to_addrs=to_email, msg=f"{email_body}".encode("utf-8"))

