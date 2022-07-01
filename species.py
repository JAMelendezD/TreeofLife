import numpy as np
import pandas as pd
from argparse import ArgumentParser
import readline
from Levenshtein import distance as lev
#from fastDamerauLevenshtein import damerauLevenshtein as lev
from heapq import nsmallest

parser = ArgumentParser(description="Python Game of Life")
    
parser.add_argument('--database',
                    default='tol',
                    const='tol',
                    nargs='?',
                    choices=['tol', 'ott'],
                    help='list of databases, (default: %(default)s)')

args = parser.parse_args()

YELLOW = "\x1b[38;2;255;200;105;208m"
GREEN = "\x1b[38;2;120;255;105;208m"
BLUE = "\x1b[38;2;120;105;235;208m"
RED = "\x1b[38;2;255;55;50;208m"
R = "\x1b[0m"
GRAD = "\x1b[38;2;{};250;120;208m"

if args.database == 'tol':

    links = pd.read_csv('./tol/treeoflife_links.csv', 
        usecols = [0, 1]).to_numpy(dtype = int)

    node_names = pd.read_csv('./tol/treeoflife_nodes.csv', 
        usecols = [1]).to_numpy()

    nodes = pd.read_csv('./tol/treeoflife_nodes.csv', 
        usecols = [0, 2, 3, 4, 5, 6, 7]).to_numpy()
    
    info = pd.read_csv('./tol/info.csv', 
        usecols = [0, 1], delimiter =',').to_numpy()

    extinct = np.where(nodes[:,4] == 1)

    for i in extinct:
        node_names[i,0] = node_names[i,0] + " †"

    num_name = dict(zip(nodes[:,0], node_names[:,0]))
    name_num = dict(zip(node_names[:,0], nodes[:,0]))
    num_info = dict(zip(info[:,0], info[:,1]))

    def back_track(num, connections):
        '''
        Given a node back track all the other connecting nodes
        with recursion
        '''
        indeces = np.where(links[:, 1] == num)[0]
        if len(indeces) == 0:
            return
        else:
            new_num = links[indeces][0][0]
            if num_name[new_num] != 'none' and num_name[new_num][:4] != 'Node':
                connections.append(num_name[new_num])
            back_track(new_num, connections)
        return connections

    def get_tree(target, nodes):

        print(YELLOW + 40*"-")
        print("Target: ", num_name[target])
        print(40*"-" + R)

        for i, item in enumerate(nodes[::-1]):
            space = i*" "
            fmt = 255//len(nodes)*i
            print(f"{space}-{GRAD.format(255-fmt)}{item:20s}{R}")

elif args.database == 'ott':

    links = np.flip(pd.read_table('./ott/taxonomy.tsv', 
        usecols = [0, 2]).to_numpy(dtype=int), axis=1)

    node_names = pd.read_table('./ott/taxonomy.tsv', 
        usecols = [4, 6]).to_numpy()

    num_name = dict(zip(links[:,1], zip(node_names[:,0],node_names[:,1])))
    name_num = dict(zip(node_names[:,0], links[:,1]))

    links = links[1:]

    def back_track(num, connections):
        '''
        Given a node back track all the other connecting nodes
        with recursion
        '''
        indeces = np.where(links[:, 1] == num)[0]
        if len(indeces) == 0:
            return
        else:
            new_num = links[indeces][0][0]
            connections.append((num_name[new_num][0], num_name[new_num][1]))
            back_track(new_num, connections)
        return connections

    def get_tree(target, nodes):
        
        print(YELLOW + 40*"-")
        print("Target: ", num_name[target])
        print(40*"-" + R)

        for i, item in enumerate(nodes[::-1]):
            space = i*" "
            fmt = 255//len(nodes)*i
            if item[1] == 'no rank':
                print(f"{space}-{GRAD.format(255-fmt)}{item[0]:20s}{R}")
            else:
                print(f"{space}-{GRAD.format(255-fmt)}{item[0]:20s}{item[1]:20s}{R}")

def forward(father_node, result):
    '''
    Get all the possible forward options given a father node.
    Recursion when a node is none to get the options that none
    points towards
    '''
    indeces = np.where(links[:, 0] == father_node)[0]
    nodes = links[indeces][:, 1]
    for node in nodes:
        if num_name[node] == 'none':
            forward(node, result)
        else:
            result.append(node)

    return result

def get_possible(nodes):

    opt = {}
    size  = len(nodes)
    for i, node in enumerate(nodes[::-1]):
        print(f"{YELLOW} {size-i}) {num_name[node]}{R}")
        opt[size-i] = node
    return opt

def get_info(target): 
    return YELLOW+num_info[name_num[target]]+R

def suggestions(target):

    max_suggestions = 20

    scores = {}
    for name in name_num.keys():
        scores[lev(target, name[:30])] = name
    best_twenty = nsmallest(max_suggestions, scores, key=scores.get)

    opt = {}
    for i, score in enumerate(best_twenty[::-1]):
        name = scores[score]
        print(f"{BLUE} {max_suggestions-i}) {name}{R}")
        opt[max_suggestions-i] = name_num[name]
    return opt

def main():
    commands = ['help', 't', 'i', 'n']
    
    if args.database == 'tol':
        EXAMPLE = "Example: n: Life on Earth"
    elif args.database == 'ott':
        EXAMPLE = "Example: n: life"

    NOT_FOUND = "Target not found in database maybe you meant:"

    def execute(target, command):

        options = None

        if command == 'n':
            if target in name_num.keys():
                output = forward(name_num[target], [])
                options = get_possible(output)
            else:
                print(RED + NOT_FOUND)
                options = suggestions(target)
        elif command == 't':
            if target in name_num.keys(): 
                output = back_track(name_num[target], [])
                get_tree(name_num[target], output)
            else:
                print(RED + NOT_FOUND)
                options = suggestions(target)
        elif command == 'i':
            if target in name_num.keys():
                if name_num[target] in num_info.keys(): 
                    print(get_info(target))
                else:
                    print(RED + "No information found" + R)
            else:
                print(RED + NOT_FOUND)
                options = suggestions(target)
        
        return options, command

    print("\x1b[38;2;120;255;105;208m" + 
'''
######## Tree of Life ########\n
            * *    
        *    *  *
    *  *    *     *  *
    *     *    *  *    *
* *   *    *    *    *   *
*     *  *    * * .#  *   *
*   *     * #.  .# *   *
*     "#.  #: #" * *    *
*   * * "#. ##"       *
*       "###
            "##
            ##.
            .##:
            :###
            ;###
            ,####.
/\/\/\/\/\/.######.\/\/\/\/\
\n\n##############################
''' + "\x1b[0m")

    print("Hello type a \"command: value\" or help for more information")
    options = {}
    while True:
        inp = input("").split(":")
        if len(inp) == 1:
            if inp[0].isdigit() and options:
                target = options[int(inp[0])]
                if args.database == 'tol':
                    options, command = execute(num_name[target], command)
                elif args.database == 'ott':
                    options, command = execute(num_name[target][0], command)
            else:
                if inp[0] == "help":
                    print("Possible commands: t (tree), i (info), n (nodes)")
                    print(EXAMPLE)
                else:
                    if inp[0] in commands:
                        print(f"{inp[0]} requires other keyword")
                        print(EXAMPLE)
                    else:
                        print("Command not implemented try", commands)

        elif len(inp) == 2:
            command = inp[0]
            if command in commands:
                target = inp[1].strip().capitalize()
                options, command = execute(target, command)
            else:
                print(RED + "Command not implemented try" + R, commands)
        else:
            print(RED + "Command or input not found try:" + R, commands)
            print(EXAMPLE)

if __name__ == '__main__':
    main()