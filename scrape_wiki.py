from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np
import multiprocessing as mp
from multiprocessing.pool import Pool
from tqdm import tqdm


'''
node_names = pd.read_table('./ott/taxonomy.tsv', 
        usecols = [4]).to_numpy()

links = np.flip(pd.read_table('./ott/taxonomy.tsv', 
        usecols = [0, 2]).to_numpy(dtype=int), axis=1)

name_num = dict(zip(node_names[:,0], links[:,1]))
'''

links = pd.read_csv('./tol/treeoflife_links.csv', 
    usecols = [0, 1]).to_numpy(dtype = int)

node_names = pd.read_csv('./tol/treeoflife_nodes.csv', 
    usecols = [1]).to_numpy()

nodes = pd.read_csv('./tol/treeoflife_nodes.csv', 
    usecols = [0, 2, 3, 4, 5, 6, 7]).to_numpy()

name_num = dict(zip(node_names[:,0], nodes[:,0]))

G = "\x1b[38;2;120;255;105;208m"
Y = "\x1b[38;2;255;200;105;208m"
R = "\x1b[38;2;255;50;50;208m"
r  = "\x1b[0m"

f = open('info.csv', 'w')

def scrape(start, stop):

    for i in range(start,stop):
        data = node_names[i][0].split()[0:2]
        size = len(data)

        if size == 1 or size == 2:
            if size == 1:
                webpage = f"https://en.wikipedia.org/wiki/{data[0].capitalize()}"
            else:
                webpage = f"https://en.wikipedia.org/wiki/{data[0].capitalize()}_{data[1]}"

            page = requests.get(webpage)

            if page.status_code != 404:
                soup = BeautifulSoup(page.content, 'html.parser')
                for paragraph in soup.find_all('p'):
                    text = str(paragraph.get_text())
                    if len(text) >= 100:
                        print(Y, name_num[node_names[i][0]], node_names[i][0], G, text[0:200].replace('\n', ' '), "...", r)
                        line = f"{name_num[node_names[i][0]]}," + "\"" + text[0:200] + "..."
                        f.write(line.replace('\n', '') + "\"\n")
                        break
            else:
                print(Y, name_num[node_names[i][0]], node_names[i][0], R, "No information found", r)
                line = f"{name_num[node_names[i][0]]}," + "\"No information found"
                #f.write(line + "\"\n")

def main():
    '''
    cores = mp.cpu_count()
    pool = Pool(cores)
    divide_conquer = int(np.ceil((len(node_names)+1)/cores))

    start = []
    stop = []

    for i in range(cores):
        start.append(i*divide_conquer)
        if i == cores-1:
            stop.append(len(node_names)+1)
        else:
            stop.append((i+1)*divide_conquer)

    pool.starmap(scrape,zip(start,stop))
    '''
    scrape(0, len(node_names)+1)

if __name__ == "__main__":
    main()