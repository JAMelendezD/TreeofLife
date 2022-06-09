import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from tqdm import tqdm
from collections import defaultdict
import os

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

titles = "/home/julian/Desktop/Wiki/enwiki-20220101-pages-articles-multistream-index.txt"
path = "/home/julian/Desktop/Wiki/"

def to_scrape():
    dic = {}
    for node in tqdm(node_names, desc = "scrapping", colour = 'Green'):
        data = node[0].split()[0:2]
        size = len(data)

        if size == 1:
            name = data[0].capitalize()
        else:
            name = data[0].capitalize() + " " + data[1]

        srch = f"\'\'\'{name}\'\'\'"
        tmp = name.replace(" ", "")
        if all(map(str.isalpha, tmp)):
            dic[srch] = name_num[node[0]]
    return dic

def scrape(dic, char):

    file_ =  path+char+'.txt'
    keys = list(dic.keys())

    for key in tqdm(keys, desc = 'key', colour = 'Green'):
        grep = os.popen(f"grep -m 1 -i \"{key}\" {file_}").read()
        if len(grep) != 0:
            clean = BeautifulSoup(grep, "lxml").text[0:300].replace('\n', '') + " ..."
            print(key, dic[key])
            print(clean)
        print(key, dic[key])

def main():
    dic = to_scrape()
    ordered = dict(sorted(dic.items()))
    print(len(ordered))
    
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for char in abc:
        new_dic = {}
        for key in ordered.keys():
            if key[3] == char:
                new_dic[key] = ordered[key]
        scrape(new_dic, char)

if __name__ == '__main__':
    main()