#!/Users/andersaarvikBC/PycharmProjects/webdl/bin/python

import datetime
import db

db.s = db.session()

# Websites

websites = [
        'aarvik.dk',
        'anders.aarvik.dk'
]

for website in websites:
    web = db.Website(url=website, last_modified=datetime.datetime.now())
    db.s.add(web)

# Options

options = [
        {
         'option': 'transfer_dest_dir',
         'option_type': 'transfer',
         'option_value': '/var/www/html'
        },
        {
         'option': 'transfer_unix_user',
         'option_type': 'transfer',
         'option_value': 'user'
        },
        {
         'option': 'transfer_unix_passwd',
         'option_type': 'transfer',
         'option_value': '123123'
        },
        {
         'option': 'transfer_dest_ip',
         'option_type': 'transfer',
         'option_value': '1.2.3.4'
        }
]

for option in options:
    option = db.Options(option=option['option'], option_type=option['option_type'], option_value=option['option_value'])
    db.s.add(option)

db.s.commit()
