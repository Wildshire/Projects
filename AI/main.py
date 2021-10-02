import itertools

from game import Game
from random_agent import RandomAgent
from markov_agent import MarkovAgent
from minimax_agent import MinimaxAgent
from wildshire import Wildshire
from wildshire_depth_3 import WildshireDP3
from wildshire_iterative import WildshireID
from wildshire_iterative_no_weights import WildshireIDNW
from abh_agent import ABHAgent
from abhtab_agent import ABHTABAgent
from DylanAgent import Agent


def main():
	#for i in range(0,10):
	game = Game(Agent(),Wildshire())
	game.play(output=True, timeout_per_turn=5.0)	
	#agents=[RandomAgent(),MarkovAgent(),MinimaxAgent(2),MinimaxAgent(3),MinimaxAgent(4),Wildshire(),WildshireDP3(),WildshireID(),WildshireIDNW(), ABHAgent([120,1.7,30,20]),ABHTABAgent()]
	
	
	
	#"Name:(victories, draws, loses, matches)"
	#dict_points={"Random":[0,0,0,0],"Markov":[0,0,0,0],"Minimax(2)":[0,0,0,0],"Minimax(3)":[0,0,0,0],"Minimax(4)":[0,0,0,0],"ABHTABAgent AKA THE SUPER RESHUFFLER":[0,0,0,0],"Wildshire":[0,0,0,0],"WildshireDP3":[0,0,0,0],"WildshireID":[0,0,0,0],"WildshireIDNW":[0,0,0,0],"ABH AKA THE RESHUFFLER":[0,0,0,0]}
	
	#pairs=list(itertools.combinations(agents,2))
	
	
	#times=[5.0,7.0,10.0,15.0]
	#i=0
	#while(i<3): #Number of rounds
		##Print results
		##Store results
		#results=[]
		#for (key,value) in dict_points.items():
			#results.append((key,value))
		#print("Round: ", i)
		#print(sorted(results,key=lambda points:points[1][0],reverse=True))
		#j=0
		#while(j<len(times)): #Depends on the time of the matches
			#z=0
			#time=times[j]
			#while(z<len(pairs)):
				#contestant1,contestant2=pairs[z][0],pairs[z][1]
				#game = Game(contestant1,contestant2)
				#winner,loser=game.play(output=False, timeout_per_turn=time)	
				##If they are not in draw
				#if(winner!=None):
					##Victory
					#dict_points[winner.info()["agent name"]][0]+=1
					##Lost
					#dict_points[loser.info()["agent name"]][2]+=1
				#else:
					##Draw for both
					#dict_points[contestant1.info()["agent name"]][1]+=1
					#dict_points[contestant2.info()["agent name"]][1]+=1
				##Either case we sum up a match
				#dict_points[contestant1.info()["agent name"]][3]+=1
				#dict_points[contestant2.info()["agent name"]][3]+=1
				#z+=1
			#j+=1
		#i+=1
	
	##Store results
	#results=[]
	#for (key,value) in dict_points.items():
		#results.append((key,value))
	
	#print(sorted(results,key=lambda points:points[1][0],reverse=True))


if __name__ == "__main__":
    main()
