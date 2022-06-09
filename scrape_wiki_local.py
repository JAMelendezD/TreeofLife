import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import multiprocessing as mp
from multiprocessing.pool import Pool
from tqdm import tqdm
import os

node_names = pd.read_table('./ott/taxonomy.tsv', 
        usecols = [4]).to_numpy()

links = np.flip(pd.read_table('./ott/taxonomy.tsv', 
        usecols = [0, 2]).to_numpy(dtype=int), axis=1)

name_num = dict(zip(node_names[:,0], links[:,1]))

titles = "/home/julian/Desktop/Wiki/enwiki-20220101-pages-articles-multistream-index.txt"
xml = "/home/julian/Desktop/Wiki/enwiki-20220101-pages-articles-multistream.xml"

f = open('info.csv', 'w', buffering = 1)

def scrape(start, stop):
    done = {}
    for i in range(start, stop):
        print(i)
        data = node_names[i][0].split()[0:2]
        size = len(data)

        if size == 1:
            name = data[0].capitalize()
        else:
            name = data[0].capitalize() + " " + data[1]
        
        srch = f"[0-9][:]{name}$"
        grep = os.popen(f"grep -E '{srch}' {titles}").read()
        
        if len(grep) != 0:                
            srch = f"\"\'\'\'{name}\'\'\'\""
            if srch not in done.keys():
                grep = os.popen(f"grep -m 1 -i {srch} {xml}").read()
                clean = BeautifulSoup(grep, "lxml").text[0:300].replace('\n', '') + " ..."
                done[srch] = clean
            else:
                clean = done[srch]
            f.write(f"{name_num[node_names[i][0]]}" + ", " + clean + "\n")

def main():
    cores = mp.cpu_count()
    pool = Pool(cores)
    size = 100
    divide_conquer = int(np.floor((size+1)/cores))

    start = []
    stop = []

    for i in range(cores):
        start.append(i*divide_conquer)
        if i == cores-1:
            stop.append(size+1)
        else:
            stop.append((i+1)*divide_conquer)

    pool.starmap(scrape, zip(start,stop))

if __name__ == '__main__':
    main()
    f.close()