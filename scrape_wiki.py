from bs4 import BeautifulSoup
import pandas as pd
import requests
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

'''

links = pd.read_csv('./tol/treeoflife_links.csv', 
    usecols = [0, 1]).to_numpy(dtype = int)

node_names = pd.read_csv('./tol/treeoflife_nodes.csv', 
    usecols = [1]).to_numpy()

nodes = pd.read_csv('./tol/treeoflife_nodes.csv', 
    usecols = [0, 2, 3, 4, 5, 6, 7]).to_numpy()

name_num = dict(zip(node_names[:,0], nodes[:,0]))
'''

G = "\x1b[38;2;120;255;105;208m"
Y = "\x1b[38;2;255;200;105;208m"
R = "\x1b[38;2;255;50;50;208m"
r  = "\x1b[0m"

f = open('info.csv', 'w')

def scrape(name):


    webpage = f"https://en.wikipedia.org/wiki/{name.capitalize()}"

    try:
        page = requests.get(webpage)
    except:
        print(30*"#"+"\n"+f"Failed at index: {i}")
    
    if page.status_code != 404:
        soup = BeautifulSoup(page.content, 'html.parser')
        for paragraph in soup.find_all('p'):
            text = str(paragraph.get_text())
            if len(text) >= 100:
                print(Y, name, G, text[0:200].replace('\n', ' '), "...", r)
                line = f"{name}," + "\"" + text[0:200] + "..."
                f.write(line.replace('\n', '') + "\"\n")
                break
    else:
        print(Y, name, R, "No information found", r)
        line = f"{name}," + "\"" + "No information found"
        #f.write(line + "\"\n")

if __name__ == "__main__":
    
    tmp = []
    for i in tqdm(range(len(node_names))):
        data = node_names[i][0].split()[0:1]
        tmp.append(data[0])

    unique = np.unique(tmp)

    abcd = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    out = 256
    for dat in unique:
        if dat[0] in abcd:
            scrape(dat)