# myTeam.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, thirdIndex, isRed,
               first = 'AttackAgent', second = 'DefenseAgent', third = 'DefenseAgent'):
  """
  This function should return a list of three agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex), eval(third)(thirdIndex)]

##########
# Agents #
##########
class AttackAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """
	
  
  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''
	
	
    self.patrol_goal=1
    self.repeat_1 = 0
    self.repeat_2 = 0
    self.judge = 0
	

  def chooseAction(self, gameState):
		

		legalMoves = gameState.getLegalActions(self.index)
		legalMoves.remove('Stop')
		
		#print "current : ",gameState.getAgentDistances()[3]
		
		scores = [self.evaluationFunction(gameState, action,self.index) for action in legalMoves]
		print ""
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best
         
         

		"Add more of your code here if you want to"
		return legalMoves[chosenIndex]
		"""
		Picks among actions randomly.

		actions = gameState.getLegalActions(self.index)
		print(" ")
		print self.getTeam(gameState)

		return random.choice(actions)
		"""
  def evaluationFunction(self, currentGameState, action, index):
		"""
		Design a better evaluation function here.
		The evaluation function takes in the current and proposed successor
		GameStates (pacman.py) and returns a number, where higher numbers are better.
		The code below extracts some useful information from the state, like the
		remaining food (newFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.
		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
		# Useful information you can extract from a GameState (pacman.py)
		
		# judge red team or blue team
		if currentGameState.isOnRedTeam(index) == 1:
			if currentGameState.getAgentPosition(index)[0] <=15:
				in_DefenseArea = 1
			else:
				in_DefenseArea = 0
		else:
			if currentGameState.getAgentPosition(index)[0] >=16:
				in_DefenseArea = 1
			else:
				in_DefenseArea = 0
		
		
		
		# index is the agent's number
		successorGameState = currentGameState.generateSuccessor(index,action)
		old_pos = currentGameState.getAgentPosition(index)
		newPos = successorGameState.getAgentPosition(index)
	
	
		newFood = self.getFood(currentGameState)		
		current_pacman_position = currentGameState.getAgentPosition(index)
		
		food_count = 0;
		
		closest_food_distance = 1000
		for x, col in enumerate(newFood):
			for y, has_food in enumerate(col):
				if has_food:
					food_count = food_count + 1
					food_distance = self.getMazeDistance(newPos,(x,y))
					if food_distance < closest_food_distance:
						closest_food_distance = food_distance
      
      
		closest_Capsules_distance = 1000
		newCapsules = self.getCapsules(currentGameState)

		if currentGameState.getAgentState(1).scaredTimer==0 and currentGameState.getAgentState(3).scaredTimer==0 and currentGameState.getAgentState(5).scaredTimer==0:
			for capsule_index in newCapsules:
				if self.getMazeDistance(newPos,capsule_index) < closest_Capsules_distance:
						closest_Capsules_distance = self.getMazeDistance(newPos,capsule_index)
			
		# List every feature for calculating the utility
		#feature_will_lose = 1 if [successorGameState.generateSuccessor(1, direction).isOver() for direction in successorGameState.getLegalActions(1)].count(True) > 0 else 0
		feature_will_has_food = 1 if currentGameState.hasFood(*newPos) and in_DefenseArea!= 1 else 0
		feature_closest_food_distance = closest_food_distance


		"""
		if index ==0:
			print successorGameState.getAgentState(1).scaredTimer
			print successorGameState.getAgentState(3).scaredTimer
			print successorGameState.getAgentState(5).scaredTimer
			print("")
		"""
         
        # below is for pacman mode		
		eat_enemy = 0
		escape = 0
		dead_end = 0
		
		for enemy_index in self.getOpponents(currentGameState):
			if currentGameState.getAgentPosition(enemy_index)!= None:
			# if enemy in sight
				old_distance = self.getMazeDistance(old_pos,currentGameState.getAgentPosition(enemy_index))
				new_distance = self.getMazeDistance(newPos,currentGameState.getAgentPosition(enemy_index))
				# current distance and distance after action  between agent and opponent

				# below is for pacman mode
				if currentGameState.getAgentState(enemy_index).scaredTimer==0:
				# if ghost not scared
					if new_distance > old_distance and (new_distance < 5 or old_distance <5):
						escape = escape + 1
						if len(successorGameState.getLegalActions(index)) <= 2:
							dead_end = 1
				else:
				# if scared
					if new_distance < old_distance and (new_distance < 5 or old_distance <5):
						eat_enemy = eat_enemy + 1
						

		
						
		
		if in_DefenseArea:
		# when agent is ghost
			utility = -feature_closest_food_distance
		else:
		# when agent is pacman
			if closest_Capsules_distance==1000:
			# no capsules 
				utility = 500*feature_will_has_food - 550*dead_end - feature_closest_food_distance + 10000*escape + 1000*eat_enemy
			else:                                                                   
				utility = 500*feature_will_has_food - 550*dead_end - feature_closest_food_distance + 10000*escape + 1000*eat_enemy - 100*closest_Capsules_distance
		

		if currentGameState.isOnRedTeam(index) == 1:
			count_point_dis = self.getMazeDistance((21,14),currentGameState.getAgentPosition(index))
			count_point2_dis = self.getMazeDistance((21,2),currentGameState.getAgentPosition(index))

			if count_point_dis == 0:
				self.repeat_1 = self.repeat_1 + 1
			if count_point2_dis == 0:
				self.repeat_2 = self.repeat_2 + 1
			
			
			if self.repeat_1 >= 5 and len(self.getCapsules(currentGameState)) == 2:
				#flag_distance = self.getMazeDistance(self.getFlags(currentGameState)[0],successorGameState.getAgentPosition(index))
				capsules_distance = self.getMazeDistance(self.getCapsules(currentGameState)[0],successorGameState.getAgentPosition(index))
				utility = -capsules_distance + 10*escape - dead_end + feature_will_has_food

			if self.repeat_2 >= 5:
				temp_distance = self.getMazeDistance((18,7),successorGameState.getAgentPosition(index))
				utility = -temp_distance + 10*escape - dead_end + feature_will_has_food
				if temp_distance == 0:
					self.judge = 1
			if self.judge == 1:
				utility = 500*feature_will_has_food - 550*dead_end - feature_closest_food_distance + 10000*escape + 1000*eat_enemy


		
		else:	
			count_point_dis = self.getMazeDistance((10,1),currentGameState.getAgentPosition(index))
			count_point2_dis = self.getMazeDistance((9,13),currentGameState.getAgentPosition(index))

			if count_point_dis == 0:
				self.repeat_1 = self.repeat_1 + 1
			if count_point2_dis == 0:
				self.repeat_2 = self.repeat_2 + 1
			
			
			if self.repeat_1 >= 6 and len(self.getCapsules(currentGameState)) == 2:
				#flag_distance = self.getMazeDistance(self.getFlags(currentGameState)[0],successorGameState.getAgentPosition(index))
				capsules_distance = self.getMazeDistance(self.getCapsules(currentGameState)[1],successorGameState.getAgentPosition(index))
				utility = -capsules_distance + 10*escape - dead_end + feature_will_has_food

			if self.repeat_2 >= 6:
				temp_distance = self.getMazeDistance((13,8),successorGameState.getAgentPosition(index))
				utility = -temp_distance + 10*escape - dead_end + feature_will_has_food
				if temp_distance == 0:
					self.judge = 1
			if self.judge == 1:
				utility = 500*feature_will_has_food - 550*dead_end - feature_closest_food_distance + 10000*escape + 1000*eat_enemy


		
		
		


		# a variable "patrol_goal" is initial in registerInitialState
		if currentGameState.isOnRedTeam(index) == 1:
			patrol_p1_dis = self.getMazeDistance((4,6),successorGameState.getAgentPosition(index))
			patrol_p2_dis = self.getMazeDistance((13,6),successorGameState.getAgentPosition(index))
		else:
			patrol_p1_dis = self.getMazeDistance((27,9),successorGameState.getAgentPosition(index))
			patrol_p2_dis = self.getMazeDistance((18,9),successorGameState.getAgentPosition(index))
		# below is for ghost mode
		chase_pacman = 0
		scared_escape = 0		
		
		if len(newCapsules)==0 and food_count<=2:
		# when there is no food left , go back to help defense , patrol between point p1 and p2
			if self.patrol_goal == 1:
			# go to p1
				utility = -10*patrol_p1_dis 
				if patrol_p1_dis == 0:
					self.patrol_goal = 2
					
			elif self.patrol_goal == 2:
			# go to p2
				utility = -10*patrol_p2_dis
				if patrol_p2_dis == 0:
						self.patrol_goal = 1
			# below is for ghost mode
			if in_DefenseArea and currentGameState.getAgentState(index).scaredTimer == 0:
			# agent not scared				
				for enemy_index in self.getOpponents(currentGameState):
					if currentGameState.getAgentPosition(enemy_index)!= None  and new_distance < old_distance and (new_distance < 3 or old_distance <3):
						chase_pacman = chase_pacman + 1
						utility = 100000*chase_pacman
			elif in_DefenseArea and currentGameState.getAgentState(index).scaredTimer != 0:
			# agent is scared
				for enemy_index in self.getOpponents(currentGameState):
					if currentGameState.getAgentPosition(enemy_index)!= None  and new_distance > old_distance and (new_distance < 3 or old_distance <3):
						scared_escape = scared_escape + 1
						utility = 100000*scared_escape
				
		
		
		
		return utility
  
  
  
 
class DefenseAgent(CaptureAgent):


  def registerInitialState(self, gameState):

    CaptureAgent.registerInitialState(self, gameState)

    #Your initialization code goes here, if you need any.
    		
    self.patrol_goal=1

  def chooseAction(self, gameState):
		

		legalMoves = gameState.getLegalActions(self.index)
		legalMoves.remove('Stop')

		scores = [self.evaluationFunction(gameState, action,self.index) for action in legalMoves]

		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best
         
		return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action, index):

		# judge red team or blue team
		if currentGameState.isOnRedTeam(index) == 1:
			if currentGameState.getAgentPosition(index)[0] <=15:
				in_DefenseArea = 1
			else:
				in_DefenseArea = 0
		else:
			if currentGameState.getAgentPosition(index)[0] >=16:
				in_DefenseArea = 1
			else:
				in_DefenseArea = 0
		
		
		# index is the agent's number
		successorGameState = currentGameState.generateSuccessor(index,action)
		old_pos = currentGameState.getAgentPosition(index)
		newPos = successorGameState.getAgentPosition(index)

		
		for enemy_index in self.getOpponents(currentGameState):
			if currentGameState.getAgentPosition(enemy_index)!= None:
			# if enemy in sight
				old_distance = self.getMazeDistance(old_pos,currentGameState.getAgentPosition(enemy_index))
				new_distance = self.getMazeDistance(newPos,currentGameState.getAgentPosition(enemy_index))
				# current distance and distance after action  between agent and opponent
	
		
		# assign the patrol point
		if currentGameState.isOnRedTeam(index) == 1:
			if index==self.getTeam(currentGameState)[1]:
				# a variable "patrol_goal" is initial in registerInitialState		
				patrol_p1_dis = self.getMazeDistance((8,1),successorGameState.getAgentPosition(index))
				patrol_p2_dis = self.getMazeDistance((5,3),successorGameState.getAgentPosition(index))		
			elif index==self.getTeam(currentGameState)[2]:
				patrol_p1_dis = self.getMazeDistance((8,13),successorGameState.getAgentPosition(index))
				patrol_p2_dis = self.getMazeDistance((6,12),successorGameState.getAgentPosition(index))
		else:
			if index==self.getTeam(currentGameState)[1]:		
				patrol_p1_dis = self.getMazeDistance((23,14),successorGameState.getAgentPosition(index))
				patrol_p2_dis = self.getMazeDistance((26,12),successorGameState.getAgentPosition(index))		
			elif index==self.getTeam(currentGameState)[2]:
				patrol_p1_dis = self.getMazeDistance((23,2),successorGameState.getAgentPosition(index))
				patrol_p2_dis = self.getMazeDistance((25,4),successorGameState.getAgentPosition(index))
				
				

		
		# below is for ghost mode
		chase_pacman = 0
		scared_escape = 0		
		

		if self.patrol_goal == 1:
		# go to p1
			utility = -10*patrol_p1_dis 
			if patrol_p1_dis == 0:
				self.patrol_goal = 2
				
		elif self.patrol_goal == 2:
		# go to p2
			utility = -10*patrol_p2_dis
			if patrol_p2_dis == 0:
					self.patrol_goal = 1
					
		if in_DefenseArea and currentGameState.getAgentState(index).scaredTimer == 0:
		# agent not scared
			for enemy_index in self.getOpponents(currentGameState):
				if currentGameState.getAgentPosition(enemy_index)!= None  and new_distance < old_distance and (new_distance < 3 or old_distance <3):
					chase_pacman = chase_pacman + 1
					utility = 100000*chase_pacman
		elif in_DefenseArea and currentGameState.getAgentState(index).scaredTimer != 0:
		# agent is scared
			for enemy_index in self.getOpponents(currentGameState):
				if currentGameState.getAgentPosition(enemy_index)!= None  and new_distance > old_distance and (new_distance < 3 or old_distance <3):
					scared_escape = scared_escape + 1
					utility = 100000*scared_escape
		
		# flag defense		
		if self.getOwnFlagOpponent(currentGameState) != None:
		#if flag was eaten
			if currentGameState.isOnRedTeam(index) == 1:
				next_original_distance = self.getMazeDistance((1,1),successorGameState.getAgentPosition(index))
				crossroad_distance = self.getMazeDistance((4,7),successorGameState.getAgentPosition(index))
				if index==self.getTeam(currentGameState)[2]:
					utility = - next_original_distance
				elif index==self.getTeam(currentGameState)[1]:
					utility = - crossroad_distance
			else:
				next_original_distance = self.getMazeDistance((30,14),successorGameState.getAgentPosition(index))
				crossroad_distance = self.getMazeDistance((27,8),successorGameState.getAgentPosition(index))
				if index==self.getTeam(currentGameState)[2]:
					utility = - next_original_distance
				elif index==self.getTeam(currentGameState)[1]:
					utility = - crossroad_distance
					
			

		#print self.getOwnFlagOpponent(currentGameState)
		#print self.getFlags(currentGameState)
		
		return utility