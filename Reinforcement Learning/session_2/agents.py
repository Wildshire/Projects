"""
Angents file. TO BE COMPLETED
"""
import numpy as np
import math
import copy #Had some copy problems in PI and VI 

from scipy.special import softmax


class PolicyIteration:
    def __init__(self, mdp):
        self.mdp = mdp
        self.gamma = 0.9
        self.epsilon=0.1

    def policy_evaluation(self, policy):
        """1st step of policy iteration algorithm
            Input:
                policy: current policy
            Return: State Value V of policy
        """
        V = np.zeros(self.mdp.env.nS) # intialize V to 0's
        
        # TO IMPLEMENT
        
        found=False #Stop condition with delta
        while found==False:
            delta=0.0 #Delta
            old_V = copy.deepcopy(V) #Make copy of V (because we are going to edit it meanwhile)
            #Get all states all states
            for state in range(0,self.mdp.env.nS):
                #If it is final state, we do not have succesors, only get reward
                if(state in self.mdp.final_states):
                    V[state]=self.mdp.get_reward(state)
                else:
                    total=0 #Keep track of values
                    v=old_V[state] #Get original value
                    #Get all actions in that state
                    for action in range(0,self.mdp.env.nA):
                        probability_policy = policy[state][action] # My policy let's me do this action, if so, what probability? -> Between (0,1)
                        probability_transition,successor,_,_ = self.mdp.env.P[state][action][0] #Access dictionary -> dictionary -> list -> tuple element 0 or 1 #Is the movement valid?
                        probability=probability_policy*probability_transition #Probability to do the movement regarding policy and transition
                        total +=probability * old_V[successor] #Sum up
                    V[state]=self.mdp.get_reward(state) + self.gamma * total #Update V
                
                #Stop condition
                delta=max(delta,abs(v-V[state]))
                if(delta<=self.epsilon):
                    found=True
        return np.array(V)

    def policy_improvement(self, V, policy):
        """2nd step of policy iteration algorithm
            Input:
                V: improved V
                policy: current policy
            Return: the improved policy
        """
        # TO IMPLEMENT

        new_policy=np.zeros((self.mdp.env.nS, self.mdp.env.nA)) #Construct empty policy
        #Get all states
        for state in range(0,self.mdp.env.nS):
            for action in range(0,self.mdp.env.nA):
                probability_transition,successor,reward,_ = self.mdp.env.P[state][action][0] #Go to this state with this action
                probability=probability_transition #Probability to do the movement regarding only the possibility to do it
                value=probability*V[successor] #Vale
                new_policy[state][action]=value #And update policy according to value

            #Option 1
            #After getting all values, policy probabilities need to sum one, make use of argmax deterministic approach
            index = np.argmax(new_policy[state]) #This is to keep numbers sum sum 1
            for i in range(0,len(new_policy[state])):
                if(i==index):
                    new_policy[state,i]=1.0
                else:
                    new_policy[state,i]=0.0

            #Option 2: make use of softmax: stochastic approach to the problem (here we could keep investigating more)
            #nor = argmax(new_policy[state])
            #new_policy[state]=nor
        #Return
        return new_policy


    def policy_iteration(self):
        """This is the main function of policy iteration algorithm.
            Return:
                final policy
                (optimal) state value function V
        """
        # Start with a random policy
        policy = np.ones((self.mdp.env.nS, self.mdp.env.nA)) / self.mdp.env.nA
        
        # Action in [UP, RIGHT, DOWN, LEFT], see environment.py
        
        # TO IMPLEMENT: call iteratively step 1 and 2 until convergence

        #Iterate until values do not change
        policy_stable=False #Stop condition, only if the policy is mantained
        while policy_stable==False:
            old_policy=copy.deepcopy(policy) #Make copy of policy
            newV = self.policy_evaluation(policy) #New values
            new_policy = self.policy_improvement(newV,policy) #Update policy

            #If not improved then we are done
            if(np.allclose(old_policy,new_policy)): #This checks if elements are equal between matrix
                policy_stable = True #Stop condition true
            
            #Iteration with copy
            V=copy.deepcopy(newV)
            policy=copy.deepcopy(new_policy)

        return policy, V


class ValueIteration:
    def __init__(self, mdp):
        self.mdp = mdp
        self.gamma = 0.9
        self.epsilon = 0.001

    def optimal_value_function(self):
        """1st step of value iteration algorithm
            Return: State Value V
        """
        # Initialize random policy and V

        policy = np.ones((self.mdp.env.nS, self.mdp.env.nA)) / self.mdp.env.nA
        V = np.zeros(self.mdp.env.nS)

        # TO IMPLEMENT

        old_V=copy.deepcopy(V) #We need copy of old one to access good values

        found=False #Until found we stay here
        while(found==False):
            #Get states
            for state in range(0,self.mdp.env.nS):
                
                #Put a very low value and try to improve it
                max_tot=-np.inf
                old_v = old_V[state] #Old value of state
                
                #If it is final state, we do not have succesors
                if(state in self.mdp.final_states):
                    V[state]=self.mdp.get_reward(state)
                
                else:
                    #Get actions
                    for action in range(0,self.mdp.env.nA):
                        probability_transition,successor,_,_ = self.mdp.env.P[state][action][0] #Go to this state with this action
                        probability=probability_transition #Probability to do the movement regarding only the possibility to do it
                        #print(probability_transition)
                        value=probability*old_V[successor] #Get value
                        #We found a good action, update its value
                        if(value>max_tot):
                            max_tot=value
                    #Update value of state with best value found
                    V[state]=self.mdp.get_reward(state) + self.gamma * max_tot

                #If this condition is met, even only once we have to continue search (this condition I used it in another project)
                if(abs(old_v-V[state])>((self.epsilon*(1-self.gamma))/(2*self.gamma))):
                    found=True
            
            if(found):
                #Update V
                old_V=copy.deepcopy(V)
                found=False
                continue
            #Then we stop
            else:
                found=True

        
        return V

    def optimal_policy_extraction(self, V):
        """2nd step of value iteration algorithm
            Input:
                V: optimal state values
            Return: optimal policy
        """
        policy = np.zeros([self.mdp.env.nS, self.mdp.env.nA])
        # TO IMPLEMENT
        #Go to states
        for state in range(0,self.mdp.env.nS):
            #Create a subpolicy of that state
            subpolicy=np.zeros(4)
            #Go to actions
            for action in range(0,self.mdp.env.nA):
                _,successor,_,_ = self.mdp.env.P[state][action][0] #We are only interested in succesor
                subpolicy[action]=V[successor] #To get its value
            
            #Option 1: Deterministic approach  
            index = np.argmax(subpolicy)
            for i in range(0,len(subpolicy)):
                if(i==index):
                    subpolicy[i]=1.0
                else:
                    subpolicy[i]=0.0
            policy[state]=subpolicy
            
            #Option 2: And same as before, make all elements sum 1 (Stochastic)   
            #nor = softmax(subpolicy)
            #Update policy
            #policy[state]=nor
        return policy

    def value_iteration(self):
        """This is the main procedure of value iteration algorithm.
            Return:
                final policy
                (optimal) state value function V
        """

        # TO IMPLEMENT
        #Get V
        V=self.optimal_value_function()
        #Get policy with good V, simple.
        policy=self.optimal_policy_extraction(V)
        return policy, V


class QLearning:
    def __init__(self, mdp):
        self.policy = np.zeros((4, mdp.env.observation_space.n)) + 0.25
        self.mdp = mdp
        self.discount = 0.9
        self.lr=0.1 #Added learning rate, seems 0.1 is good

    def update(self, state, action, reward):
        """
        Update Q-table according to previous state (observation), current state, action done and obtained reward.
            Input:
                state: state s(t), before moving according to 'action'
                action: action a(t) moving from state s(t) (='state') to s(t+1)
                reward: reward received after achieving 'action' from state 'state'
            Return: None
        """
        new_state = self.mdp.observe() # To get the new current state

        # TO IMPLEMENT
        #Update the policy, we follow q-learning algorithm by the books (1-alpha) * Q(a,s) + alpha*gamma*max(Q(actions,s'))
        self.policy[action,state] = (1-self.lr) * self.policy[action,state] +self.lr*(reward + self.discount*max(self.policy[:,new_state]))
        #raise NotImplementedError

    def action(self, state):
        """
        Find which action to do given a state.
            Input:
                state: state observed at time t, s(t)
            Return:
                action: optimal action a(t) to run
        """
        # TO IMPLEMENT
        #raise NotImplementedError
        #Same here, just get index of best action
        action = np.argmax(self.policy[:,state])
        
        return action


class Agent(object):
    """Agent base class. DO NOT MODIFY THIS CLASS
    """

    def __init__(self, mdp):
        super(Agent, self).__init__()
        self.mdp = mdp


    def update(self, state, action, reward):
        # DO NOT MODIFY. This is an example
        pass

    def action(self, state):
        # DO NOT MODIFY. This is an example
        return self.mdp.env.action_space.sample()
