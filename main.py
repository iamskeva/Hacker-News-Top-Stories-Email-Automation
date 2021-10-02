import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

import requests
from bs4 import BeautifulSoup


def extract_news(url):
    print('Extracting Hacker News Stories...')
    underline = '-' * 50
    text = f'<b>HN Top Stories</b> \n <br> {underline} <br>\n'
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    # Getting the title of Hacker news articles
    for i, tag in enumerate(soup.find_all('a', attrs={'class': 'storylink'}), start=1):
        text += f'{i} - {tag.get_text()} -  ({tag.get("href")}) \n <br><br>'
    return text


def send_mail():

    url = 'https://news.ycombinator.com'
    underline = '-' * 50
    content = extract_news(url)
    content += f'\n <br> {underline} <br>\n\n'
    content += 'End of Message'
    print(content)

    # Let's send the mail
    print('Composing email')
    # Update your email details

    SERVER = 'smtp.gmail.com'
    PORT = 587
    FROM = 'sender email address'
    TO = 'receiver email address'
    PASS = 'your email password'

    msg = MIMEMultipart()
    today = datetime.date()
    formatted_date = datetime.strftime(today, '%d-%m-%Y')

    msg['Subject'] = f'Top News Stories HN (Automated Email) - {formatted_date}'
    msg['From'] = FROM
    msg['To'] = TO
    msg.attach(MIMEText(content, 'html'))

    print('Initiating Server')

    server = smtplib.SMTP(SERVER, PORT)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(FROM, PASS)
    server.sendmail(FROM, TO, msg.as_string())

    print('Email Sent...')
    server.quit()


if __name__ == '__main__':
    send_mail()
