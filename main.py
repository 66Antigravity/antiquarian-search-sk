from googlesearch import search
from pandas import read_excel
import xlrd
from jinja2 import Environment, FileSystemLoader
from time import time


class Searcher:
    def __init__(self, pause):
        self.pause = pause

    def search_dummy(self, filename):
        if ".xlsx" not in filename:
            raise RuntimeError("File not supported!")
        books = read_excel(filename)
        pages = books['Webstranka'][~books['Webstranka'].isna()]
        books = books.fillna('')

        seconds = pages.size * books.shape[0] * self.pause
        m, s = divmod(seconds * 2, 60)
        h, m = divmod(m, 60)
        print(f"Vyhladavanie potrva priblizne:{h}:{m}:{s}. Pocet vyhladavani: {int(seconds/self.pause)}")

        results = []
        for i, row in books.iterrows():
            for page in pages:
                print("Hladam: ", (page, row['Autor'], row['Kniha']))
                res = self.search_entry(page, row['Autor'], row['Kniha'])
                s = row['Autor'] + ": " + row['Kniha'] + "; " + page
                results.append([s, res])
                print(res)
                html_writer(results)
        return results


    def search_entry(self, page, author, title):
        query = author + ' ' + title
        try:
            results = search(query, tld='sk', lang='sk', tbs='1', safe='off', num=10, start=0, stop=9,
                         domains=[page], pause=self.pause, tpe='', country='', extra_params=None, user_agent=None)
        except Exception:
            results = "Nieco sa pri vyhladavani pokazilo. Pravdepodobne ta Google odpojil." + str(Exception)

        return list(results)


def main():
    start = time()
    num = input("Zadaj cislo (cele) ako pocet sekund medzi jednotlivymi vyhladavaniami: ")
    pause = int(num)

    searcher = Searcher(pause)
    results = searcher.search_dummy('Antik.xlsx')
    html_writer(results)
    end = time()
    print("celkovy cas: ", end-start)
#     2:12:30 ; 4:24:51


def html_writer(results):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    template = env.get_template('vysledky.html')

    output = template.render(results=results)
    with open("vysledky.html", "w") as html_file:
        print(output, file=html_file)


if __name__ == "__main__":
    main()
