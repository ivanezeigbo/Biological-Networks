'''
Agent-based model on evolution of cooperation and defection in a biological network without costly punishment. Tests the impact of diversity and decreasing density of connectivity on cooperation.
'''
import networkx as nx
import matplotlib.pyplot as plt
from random import *
import pandas as pd
from collections import Counter
import pdb #; pdb.set_trace()

strategy = [] #list of strategies
stat = 1 #counter for games
limit = 1e+2 #limit for counter above ("stat") which is also number of games to be played
avg_payoff = 0 #average payoff
while stat <= limit:
 
    Network = {} #dictionary of networks
    total_num = 18
    defect = sample(range(1, total_num + 1), int(total_num/2))
    for i in range(total_num):
        if (i + 1) in defect:
            M = 'D'
        else:
            M = 'C'
        Network[i] = [str(i + 1), M, 0, 'N', 0]#[label of node, current strategy, payoff, imitated strategy, payoff for comparison] 
    players = [a for a in range(total_num)] #nodes

    path = []
    f = 1.0 #multiplying factor
    
    for gg in range(round(total_num * f)):
        x, y = sample(players, 2)
        while ((x, y) in path or (y, x) in path):
            x, y = sample(players, 2)
        path.append((x, y))

        

    def random_layering(): #function for diversity of players and connections
        path = []
        for g in range(round(total_num * f)):
            x, y = sample(players, 2)
            while ((x, y) in path or (y, x) in path):
                x, y = sample(players, 2)
            path.append((x, y))
        return path
                
                

    def Graph():
        global path
        Connect = False
        while not Connect: #makes sure graph is connected
            G = nx.Graph()   
            G.add_nodes_from(players)
            path = random_layering() #function that calls for diversity in every round of a game. Commenting this line of code removes diversity in the rounds of the game
            G.add_edges_from(path)
            if nx.is_connected(G): #makes sure graph is a connected graph
                Connect = True
            else:
                path = random_layering() #else, form a new network
        #print("Is graph connected? ", 'Yes' if nx.is_connected(G) else 'No')
        #print("There are", G.number_of_nodes(), "nodes and", G.number_of_edges(), "edges.")
        Edge = G.edges()
        #print("These are the edges we have in the graph: \n", Edge)
        #print("")
        labels = {}
        for j in range(len(Network)):
            labels[j] = Network[j][1]

        #pos = nx.circular_layout(G) 
        #nx.draw(G, pos)
        #nx.draw_networkx_labels(G, pos,labels, font_size = 14)
        #plt.show() #plots the network using Networkx Python Package. Uncommenting these four lines of code makes it possible to visually see and follow how a strategy emerges in the network


        #payoffs without costly punishment
            '''
        Following Dreber et. al (2008) "Winners don't punish"
        '''


        for k in players: #synchronous update of strategy
            Network[k][4] = Network[k][2]
            for t in G.neighbors(k):
                if Network[t][2] > Network[k][4]:
                    Network[k][4] = Network[t][2]
                    Network[k][3] = Network[t][1]
        for b in players:
            if Network[b][3] != 'N':
                Network[b][1] = Network[b][3]
            

        for s in players:
            #for y in G.neighbors(s):
                #if Network[y][2] > Network[s][2]:
                    #Network[s][3] = Network[y][1]
            
            if Network[s][1] == 'D': #payoff of a defector
                for g in G.neighbors(s):
                    if Network[g][1] == 'C': #when defector meets cooperator
                        Network[s][2] += 4
                    else:                   #payoff of defector and defector
                        Network[s][2] += 0
            else:    #payoff of cooperator
                for h in G.neighbors(s):
                    if Network[h][1] == 'C': #cooperator and cooperator
                        Network[s][2] += 2
                    else:
                        Network[s][2] += -2 #when cooperator meets cooperator
                        
                        

    count = 1 #counter to times of rounds
    times = 1e+3 #number of rounds
    while count <= times:
        #import pdb; pdb.set_trace()
        Graph() #calls function to run a round
        Same = True
        for z in range(len(Network) - 1):
            if Network[z][1] != Network[z + 1][1]:
                Same = False
                break
        if Same == True:  #case for everyone having the same strategy
            if Network[z][1] == 'D':
                #print('Everyone is a defector\n')
                strategy.append('Defect')
            
            else:
                #print ('Everyone is a cooperator\n')
                strategy.append('Cooperate')
            break
        if count == times and not Same:
            strategy.append('No Preference')
            #print(Network)
            break
        count += 1
    local_payoff = 0
    for pay in range(len(Network)):
        local_payoff += Network[pay][2]
    avg_payoff += local_payoff/total_num
    #print(Network)
    #print('\nIt took %s games' %count)

    stat += 1

coding = Counter(strategy)
if 'Cooperate' not in coding:
    coding['Cooperate'] = 0
if 'No Preference' not in coding:
    coding['No Preference'] = 0
if 'Defect' not in coding:
    coding['Defect'] = 0
avg_payoff = avg_payoff/limit #calculates payoff
print("Average payoff is", avg_payoff)
#coding = {'Defection':strategy.count('Defect'), 'Cooperation':strategy.count('Cooperate'), 'No Preference':strategy.count('No Preference')}

#df = pd.DataFrame(coding, index = range(len(coding)))

df = pd.DataFrame.from_dict(coding, orient= 'index') #creates bar chart of probabilities
df.columns = ['Amount']
df.columns.name = 'Probability'
ax = df.plot(kind='bar')
ax.set_ylabel("Probability of observing strategy")
ax.set_xlabel("Strategy")
ax.set_title('Probability of strategies in biological network')
plt.show() #creates bar chart of probabilities
print(coding)
#print("\n", strategy)
#print("\n", Network)

