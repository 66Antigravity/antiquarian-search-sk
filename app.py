from flask import Flask, request, url_for, redirect, render_template
import pandas as pd
from googlesearch import search

example = [['Božena NěmcováBabičkahttps://www.antikvariatshop.sk', ['https://www.antikvariatshop.sk/kniha/m5785/nemcova-bozena-babicka/', 'https://www.antikvariatshop.sk/kniha/f8172/nemcova-bozena-babicka/', 'https://www.antikvariatshop.sk/kniha/i90/nemcova-bozena-babicka/', 'https://www.antikvariatshop.sk/kniha/d1895/nemcova-bozena-babicka/', 'https://www.antikvariatshop.sk/kniha/J6990/nemcova-bozena-babicka/', 'https://www.antikvariatshop.sk/kniha/B7339/nemcova-bozena-babicka-chyze-pod-horami-pohorska-vesnice/', 'https://www.antikvariatshop.sk/kniha/g7072/nemcova-bozena-v-zamku-a-v-podzamci/', 'https://www.antikvariatshop.sk/kniha/e3945/kolektiv-autorov-hadi-kral/', 'https://www.antikvariatshop.sk/kniha/j4499/darcekove-poukazky/', 'https://www.antikvariatshop.sk/deti-mladez/strana-13/?order=autor&orderby=zostupne']], ['Božena NěmcováBabičkahttps://www.ciernenabielom.sk', ['https://www.ciernenabielom.sk/kniha/babicka-184988/', 'https://www.ciernenabielom.sk/kniha-detail/nemcova-bozena-babicka/29071/', 'https://www.ciernenabielom.sk/knihy/beletria-ceska/2/', 'https://www.ciernenabielom.sk/knihy/autor/scott-arthur-c/strana-133/']], ['Němcová, BoženaKytička národních pohádekhttps://www.antikvariatshop.sk', ['https://www.antikvariatshop.sk/deti-mladez/strana-7/?order=rok_vydani&orderby=vzostupne', 'https://www.antikvariatshop.sk/cenik-katalog/strana-29/', 'https://www.antikvariatshop.sk/soubory/xml/zbozi_cz.xml', 'https://www.antikvariatshop.sk/soubory/xml/superdeal_sk.xml', 'https://www.antikvariatshop.sk/soubory/xml/tovar_sk.xml']], ['Němcová, BoženaKytička národních pohádekhttps://www.ciernenabielom.sk', []], ['Sadoul, GeorgesDějiny filmu. Od Lumièra až do doby současnéhttps://www.antikvariatshop.sk', ['https://www.antikvariatshop.sk/kniha/J4478/sadoul-georges-dejiny-filmu-od-lumiera-az-do-doby-soucasne/']], ['Sadoul, GeorgesDějiny filmu. Od Lumièra až do doby současnéhttps://www.ciernenabielom.sk', []]]

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results/')
@app.route('/results/<results>')
def results():
    # results = [item for sublist in example for item in sublist]
    # results = search_dummy()
    results = example
    print(results)
    return render_template('results.html', results=results)


def search_all(webpages_csv='./webpages.csv', books_csv='./books.csv'):
    pages = pd.read_csv(webpages_csv, sep=';')
    books = pd.read_csv(books_csv, sep=';')

    results = []
    for i_b, row_b in books.iterrows():
        pages_results = []
        for i_p, row_p in pages.iterrows():
            res = search_entry(row_p.webpage, row_b.author, row_b.title)
            pages_results.append({row_p.webpage: res})
        s = row_b.author + ": " + row_b.title
        results.append({s: pages_results})

    return results


def search_dummy(webpages_csv='./webpages.csv', books_csv='./books.csv'):
    pages = pd.read_csv(webpages_csv, sep=';')
    books = pd.read_csv(books_csv, sep=';')

    results = []
    for i_b, row_b in books.iterrows():
        for i_p, row_p in pages.iterrows():
            res = search_entry(row_p.webpage, row_b.author, row_b.title)
            s = row_b.author + ": " + row_b.title + "; " + row_p.webpage
            results.append([s, res])

    return results


def search_entry(page, author, title):
    query = author + ' ' + title
    results = search(query, tld='sk', lang='sk', tbs='1', safe='off', num=10, start=0, stop=10,
                     domains=[page], pause=2.0, tpe='', country='', extra_params=None, user_agent=None)

    return list(results)


if __name__ == '__main__':
    app.run()
