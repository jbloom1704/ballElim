# Name - Abhishek Mishra
# Student id - 0934024
# Course - CSE 417
# Instructor - Steve Tanimoto
# File - ballElim.py
# Date of turn in - March 8th 2013
# Decripton - This program find whether a certain team has been eliminated in a game
#			  series scenario using Ford-Fulkerson/Edmonds-Karp min-cut/max flow algorithm

import Edge
import sys
import string 
import random
S="s"
T="t"
adjacency_list={}
optFlow={}
fordFulkerson = 0
	
# Function that makes the graph. The parameters 
# teams contains the list of teams, w
# wins is a dictionary mapping teams to their respective wins.
# gamesLeft is a dictionary mapping pair of teams to their number of games left to be played.
# elimTeam is the team to be eliminated.
# elimWinBound is the number of wins needed by the eliminating team in order to win the series.	
def makeDict(teams, wins, gamesLeft, elimTeam, elimWinBound):
	for team in teams:
		if team!=elimTeam:
			adjacency_list[team] = []	
	for key in gamesLeft.keys():
		if 	key[0]!=elimTeam and key[1]!=elimTeam:
			adjacency_list[key] = []
			adjacency_list[S] = []
			adjacency_list[T] = []	
	
	for key in gamesLeft.keys():
		if 	key[0]!=elimTeam and key[1]!=elimTeam:
			add_edge(S, key, gamesLeft[key])
			add_edge(key, key[0], gamesLeft[key])
			add_edge(key, key[1], gamesLeft[key])
	
	for team in teams:
		if team!=elimTeam:
			add_edge(team, T, elimWinBound-wins[team])

			
# Add an edge with vertices v1, v2 and weight capacity w
# For each edge, we also add a residual edge that points from
# v2 to v1 with an initial weight capacity of 0. this is Edge.Edge(v2,v1,0)
# The purpose of this edge is to store the residual capacity of corresponding edge. 			
def add_edge(v1, v2, w):
	edge = Edge.Edge(v1,v2,w)
	resEdge = Edge.Edge(v2,v1,0)
	edge.res = resEdge
	resEdge.res = edge
	adjacency_list[v1].append(edge)
	adjacency_list[v2].append(resEdge)
	optFlow[edge] = 0
	optFlow[resEdge] = 0

	
# Compute max flow using Depth First Search. The max flow algorithm is then Ford Fulkerson Algorithm	
def DFS(v1,v2, path):
	if v1 == v2:
		return path
	for edge in adjacency_list[v1]:
		endVertex = edge.v2
		resCapacity = edge.w - optFlow[edge]
		if ((resCapacity)>0) and (not ((edge, resCapacity) in path)):
			foundPath = DFS(endVertex, v2, path + [(edge, resCapacity)])
			if foundPath!=None:
				return foundPath
				
	
# Computer max flow using Breadth First Search. The algorithm then becomes Edmond's Karp Algorithm	
def BFS(source, sink):
	queue = [source]                 
	paths = {source:[]}
	while queue:
		v1 = queue.pop(0)
		for edge in adjacency_list[v1]:
			resCapacity = edge.w - optFlow[edge]
			if resCapacity > 0 and (not (edge.v2 in paths)):
				paths[edge.v2] = paths[v1] + [(edge, resCapacity)]
				if edge.v2 == sink:
					return paths[edge.v2]
				queue.append(edge.v2)
	return None		
		
# The main min-cut/max-flow algorithm. When the global variable ford-fulkerson is set to 1
# it uses DFS for finding augmented path. Else it uses BFS 	
def computeFlow(source, sink):
	augmentedPath=[]
	if fordFulkerson == 1:
		augmentedPath = DFS(source, sink, [])
	else:
		augmentedPath = BFS(source, sink)
	while augmentedPath:	# We keep going with out iteration until there is no augmented path left. 
		maxCapacity = sys.maxsize
		# Find the maximum capacity of this path	
		for component in augmentedPath:
			edge, resCapacity = component
			if (resCapacity < maxCapacity):
				maxCapacity = resCapacity
		for component in augmentedPath:
			edge, res = component
			optFlow[edge] = optFlow[edge] + maxCapacity  # Increase the flow through the edges in this path
			optFlow[edge.res] = optFlow[edge.res] - maxCapacity # Update the residual capacity of the corresponding components of this path
		augmentedPath = DFS(source, sink, [])	# Find an augmented path using the new flows and capacities
		
	minCut = 0
	for edge in adjacency_list[source]:
		minCut = minCut + optFlow[edge]
	flowStr = [(edge.v1, edge.v2, optFlow[edge]) for edge in adjacency_list[source]]
	return minCut	
	
		
# Mini test suite. This takes a set of 4 teams and uses 3 of them in the graph while the 4th one
# is tested for elimination.		
def miniTest():
	gamesLeft = {("Toronto","Baltimore"):1,("NY","Baltimore"):1,("NY","Toronto"):6}
	teams=["Toronto","NY","Baltimore","Boston"]
	wins = {"Toronto":87, "Baltimore":88, "NY":90,"Boston":79}
	elimTeam="Boston"
	elimWinBound = 91
	makeDict(teams, wins, gamesLeft, elimTeam, elimWinBound)
	
	g_star = 0
	for key in gamesLeft.keys():
		if key[0]!=elimTeam and key[1]!=elimTeam:
			g_star+=gamesLeft[key]
	
	flow = computeFlow(S,T)
	print("Eliminating team "+str(elimTeam)+" needs at least "+str(elimWinBound))  
	print("g* -> "+str(g_star))
	print("g --> "+str(flow))
	
	if flow < g_star:
		print(str(elimTeam)+" has been eliminated")
	else:
		print(str(elimTream)+" was not eliminated")


	
# Large test suit. This test constructs random team names using the random and string library.
# Once the teams are constructed, we assign all teams, within a particular range, a random win value
# which differes for each team.
# Similarly, a random set of pairs of teams is selected and each pair is assigned a random
# value of remaining games to be played within a particular range.
	
def largeTest():

	
	teamNameLength = 10
	numTeams = 30
	gLeftLow = 1
	gLeftHigh = 7
	winLow = 81
	winHigh = 91
	elimWinBound = 92
	
	wins = {}
	gamesLeft ={}
	
	for i in range(numTeams):
		newTeam = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(teamNameLength))	#construct a random name
		try:
			val = wins[newTeam] 
			i-=1
		except KeyError:
			wins[newTeam] = random.randint(winLow, winHigh)	# Set up a random win for this team
	
	teamList = [team for team in wins.keys()]
	for i in range(numTeams):
		team_a = teamList[random.randint(0,numTeams-1)]
		team_b = teamList[random.randint(0,numTeams-1)]
		try:
			val = gamesLeft[(team_a, team_b)]
			i-=1
		except KeyError:
			gamesLeft[(team_a,team_b)] = random.randint(gLeftLow, gLeftHigh)	# set up random number of games left for two randomly picked teams		
		
	elimTeam = teamList[random.randint(0,numTeams-1)] #Randomly pick a team to be eliminated.
	
	
	g_star = 0	#total flow from the source-u_xy	
	for key in gamesLeft.keys():
		if key[0]!=elimTeam and key[1]!=elimTeam:
			g_star+=gamesLeft[key]

					
	makeDict(teamList,wins, gamesLeft, elimTeam, elimWinBound)
	fordFulkerson = 0
	flow = computeFlow(S,T)		#optimal flow
	print("Eliminating team "+str(elimTeam)+" needs at least "+str(elimWinBound))  
	print("g* -> "+str(g_star))
	print("g --> "+str(flow))
	if flow < g_star:
		print(str(elimTeam)+" has been eliminated")
	else:
		print(str(elimTeam)+" was not eliminated")
	
		
largeTest()

	
#miniTest()