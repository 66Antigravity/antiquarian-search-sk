import sys
import os
from googlesearch_copy import search
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
    num = input("Zadaj cislo (cele) ako pocet sekund medzi jednotlivymi vyhladavaniami: \n")
    # num = 1
    pause = int(num)

    cur_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    print("\n\n")
    start = time()
    searcher = Searcher(pause)
    path = f"{cur_dir}/Antik.xlsx"
    results = searcher.search_dummy(path)
    html_writer(results)
    end = time()
    print("\n\nCelkovy cas (sekundy): ", end-start)
#     2:12:30 ; 4:24:51


def html_writer(results):
    cur_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    file_loader = FileSystemLoader(f"{cur_dir}/templates/")
    env = Environment(loader=file_loader)

    template = env.get_template("vysledky.html")

    output = template.render(results=results)
    with open(f"{cur_dir}vysledky.html", "w") as html_file:
        print(output, file=html_file)


if __name__ == "__main__":
    main()
