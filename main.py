# HTTP requests
import requests
# Webscraping
from bs4 import BeautifulSoup
# send the mail
import smtplib
# email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# system data and time manipulation
import datetime

now = datetime.datetime.now()

# email content placeholder
content = ''

#Extracting Hacker News Stories
def extract_news(url):
    print('EXtracting Hacker News Stories...')
    text = ''
    text += ('<b>HN Top Stories</b> \n' + '<br>' + '-' * 50 + '<br>\n')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    # Getting the title of Hacker news articles
    for i, tag in enumerate(soup.find_all('a', attrs={'class': 'storylink'}), start=1):
        text += (str(i) + ' - ' + tag.get_text() + ' - (' + tag.get('href') + ')\n' + '<br>' + '<br>')
    return text


url = 'https://news.ycombinator.com'
cnt = extract_news(url)
content += cnt
content += ('\n <br>' + '-' * 50 + '<br>\n\n')
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
msg['Subject'] = 'Top News Stories HN (Automated Email)' + '-' + str(now.day) + '-' + str(now.month) + '-' + \
                 str(now.year)
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