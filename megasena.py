#!/usr/bin/env python3
import requests
import sqlite3
from bs4 import BeautifulSoup
from io import BytesIO
from zipfile import ZipFile
from datetime import datetime

zip_file = 'http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_megase.zip'
html_file = 'D_MEGA.HTM'

with requests.get(zip_file) as request:
    if request.ok:
        with ZipFile(BytesIO(request.content)).open(html_file) as html:
            db = sqlite3.connect('megasena.db')
            db.execute('''
                DROP TABLE IF EXISTS polls;
                ''')
            db.execute('''
                CREATE TABLE polls (
                    id INTEGER NOT NULL PRIMARY KEY,
                    date DATE NOT NULL,
                    n1 INTEGER NOT NULL,
                    n2 INTEGER NOT NULL,
                    n3 INTEGER NOT NULL,
                    n4 INTEGER NOT NULL,
                    n5 INTEGER NOT NULL,
                    n6 INTEGER NOT NULL
                );''')
            soup = BeautifulSoup(html, 'html.parser')
            for tr in soup('tr'):
                td = [tag.get_text() for tag in tr('td', limit=8, rowspan=True)]
                if td and td[0].isdigit():
                    td[1] = datetime.strptime(td[1], '%d/%m/%Y')
                    db.execute('INSERT INTO polls VALUES (?, ?, ?, ?, ?, ?, ?, ?);', td)
            db.commit()
            db.close()
