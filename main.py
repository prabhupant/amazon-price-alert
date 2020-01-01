from __future__ import print_function
import requests
import sys
from bs4 import BeautifulSoup
import pickle
import os.path
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64

from apiclient import errors

HEADERS = {
        "User-Agent" : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
}

SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


def get_price(url):
    page = requests.get(url, headers=HEADERS)
    print(page)
    soup = BeautifulSoup(page.content, 'html.parser')
    product_title = soup.find(id='productTitle').get_text().strip()
    print('Title - ', product_title)
    try:
        product_price = soup.find('span', class_='a-size-medium a-color-price inlineBlock-display offer-price a-text-normal price3P').get_text()[2:]
    except:
        try:
            product_price = soup.find('span', class_='a-size-medium a-color-price priceBlockBuyingPriceString').get_text()[2:]
        except:
            sys.exit('Unable to find price!')
    print('Price - ', product_price)


def create_message(sender, to, subject, message_text):
    """Create a message for an email.

     Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    msg = MIMEText(message_text)
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode())}


def send_message(service, user_id, message):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message.decode('utf-8'))
               .execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

if __name__ == '__main__':
    # Using Gmail API
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    #product_url = sys.argv[1]
    #get_price(product_url)

    m = create_message('prabhupant9@gmail.com', 'prabhupant9@gmail.com', 'testing', 'hello there prabhu')
    k = send_message(service, 'me', m['raw'])
    print(k)
