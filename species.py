import numpy as np
import pandas as pd

links = pd.read_csv('./archive/treeoflife_links.csv', 
       usecols = [0, 1]).to_numpy()

node_names = pd.read_csv('./archive/treeoflife_nodes.csv', 
       usecols = [1]).to_numpy()

nodes = pd.read_csv('./archive/treeoflife_nodes.csv', 
       usecols = [0, 2, 3, 4, 5, 6, 7]).to_numpy()

num_name = dict(zip(nodes[:,0], node_names[:,0]))
name_num = dict(zip(node_names[:,0], nodes[:,0]))

extinct = np.where(nodes[:,4] == 1)

for i in extinct:
    node_names[i,0] = node_names[i,0] + " †"

num_name = dict(zip(nodes[:,0], node_names[:,0]))
name_num = dict(zip(node_names[:,0], nodes[:,0]))

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

def get_info(target, nodes):
    
    reset  = "\x1b[0m"
    
    color = "\x1b[38;2;255;200;105;208m"
    print(color + "----------------------------------------")
    print("Target: ", num_name[target])
    print("----------------------------------------" + reset)

    color = "\x1b[38;2;{};250;120;208m"
    for i, item in enumerate(nodes[::-1]):
        space = i*" "
        fmt = 255//len(nodes)*i
        print(f"{space}-{color.format(255-fmt)}{item:15s}{reset}")

def get_possible(nodes):
    
    opt = {}
    reset  = "\x1b[0m"
    color = "\x1b[38;2;255;200;105;208m"
    for i, node in enumerate(nodes):
        print(f"{color} {i+1}) {num_name[node]}{reset}")
        opt[i+1] = node
    return opt

commands = ['help', 'tree', 'info']

print("\x1b[38;2;120;255;105;208m" + ''' 
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
\n\n#############################
''' + "\x1b[0m")

print("Hello type a \"command: value\" or help for more information")
options = {}
while True:
    inp = input("").split(":")
    if len(inp) == 1:
        if inp[0].isdigit() and options:
            target = options[int(inp[0])]     
            output = forward(target, [])
            options = get_possible(output)
        else:
            if inp[0] == "help":
                print("Possible commands: tree, info")
                print("Example: info: Life on Earth\n")
            else:
                print(f"{inp[0]} requires other keyword")
                print("Example: info: Life on Earth\n")

    elif len(inp) == 2:
        command = inp[0]
        if command in commands:
            target = inp[1].strip()
            if command == 'info':
                output = forward(name_num[target], [])
                options = get_possible(output)
            elif command == 'tree': 
                output = back_track(name_num[target], [])
                get_info(name_num[target], output)
    else:
        print("Command or input not found try again\n")
        print("Possible commands: tree, info")
        print("Example: info: Life on Earth\n")