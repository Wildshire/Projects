import numpy as np
import random

from multiprocessing import Pool



"""
Contains the definition of the agent that will run in an
environment.
"""

class UniformBandit:
    def __init__(self, arms):
        """Init.
        """
        self.arms = arms

    def choose(self):
        """ Choose the most promising arm.
            Return: arm index
        """
        return np.random.randint(0, len(self.arms))

    def update(self, arm, reward):
        """Receive a reward after choosing a particular arm.
        This is where the agent can learn.
            Input:
                arm: choosed arm
                reward: feedback value associated with arm
        """
        pass

class epsGreedyBandit:
    def __init__(self, arms):
        """
        Initialize the set of arms.
        Initialize epsilon
        Initialize cumulative reward
        Initialize empirical rewards
        Initialize selections done by agent
        """
        self.arms = arms
        self.epsilon = 0.1 #Arbitrary epsilon for exploration
        self.cumulative_rewards = np.zeros(len(self.arms)) #All cumulativ rewards are 0 at beginning
        self.empirical_rewards = np.empty(len(self.arms)) #All empirical rewards are 0 at beginning
        self.selections = np.zeros(len(self.arms)) #Selections of each arm
        self.is_initialize=np.ones(len(self.arms)) #We first have to play all arms

    def choose(self):
        """ Choose the most promising arm.
            Return: arm index
        """
        #check if we have played all arms first
        if (sum(self.is_initialize)!=0):
            #We still have to play at least one arm
            arm=np.argmax(self.is_initialize)
            self.is_initialize[arm] = 0 #We played that arm
            return arm

        #Now we can apply algorithm
        else: 
            explore = np.random.random()
            #If explore greater than epsion we do not explore
            if(explore>self.epsilon):
                arm = np.argmax(self.empirical_rewards) #Chose index best
                return arm
            #Then we go randomly
            else:
                arm = np.random.randint(0, len(self.arms))
                return arm

    def update(self, arm, reward):
        """Receive a reward after choosing a particular arm.
        This is where the agent can learn.
            Input:
                arm: choosed arm
                reward: feedback value associated with arm
        """
        self.selections[arm]+=1.0 #We selected it once more
        self.cumulative_rewards[arm]+=reward #Store rewards so far
        self.empirical_rewards[arm] = (1/self.selections[arm]) * self.cumulative_rewards[arm] #Take empirical reward formula


class UCB1Bandit:
    # https://homes.di.unimi.it/~cesabian/Pubblicazioni/ml-02.pdf
    def __init__(self, arms):
        """Initialize the set of arms.
        """
        self.arms = arms
        self.n_plays = 0 #n_plays
        self.cumulative_rewards = np.zeros(len(self.arms)) #All cumulative rewards are 0 at beginning
        self.average_rewards = np.empty(len(self.arms)) #All average rewards are 0 at beginning
        self.selections = np.zeros(len(self.arms)) #Selections of each arm
        self.scores = np.zeros(len(self.arms)) #Score of each arm
        self.is_initialize=np.ones(len(self.arms)) #We first have to play all arms

    def choose(self):
        """ Choose the most promising arm.
            Return: arm index
        """
        #check if we have played all arms first
        if (sum(self.is_initialize)!=0):
            #We still have to play at least one arm
            arm=np.argmax(self.is_initialize)
            self.is_initialize[arm] = 0 #We played that arm
            return arm

        #Now we can apply algorithm
        else:
            return np.argmax(self.scores) #Get index highest score


    def update(self, arm, reward):
        """Receive a reward after choosing a particular arm.
        This is where the agent can learn.
            Input:
                arm: choosed arm
                reward: feedback value associated with arm
        """
        self.n_plays+=1 #One more play
        self.selections[arm]+=1 #We selected it once more
        self.cumulative_rewards[arm]+=reward #Keep track of reward
        self.average_rewards[arm] = self.cumulative_rewards[arm]/self.selections[arm] #Average reward of arm
        
        #Update score of all arms (because they depend on n_plays)
        for arm_1 in range(0,len(self.cumulative_rewards)):
            #Avoid division by zero if not played yet.
            if self.selections[arm_1]==0:
                continue
            else:
                self.scores[arm_1] = self.average_rewards[arm_1] + np.sqrt(2*(np.log(self.n_plays)/self.selections[arm_1]))
        
class ThompsonBandit:
    # https://web.stanford.edu/~bvr/pubs/TS_Tutorial.pdf, chapter 3
    # I am supposing rewards are ~ (0,1)
    def __init__(self, arms):
        """Initialize the set of arms.
        """
        self.arms = arms
        self.selections = np.zeros(len(self.arms))
        self.scores = np.zeros(len(self.arms))

        # Uniform distribution of prior beta (A,B)
        self.a = np.ones(len(self.arms))
        self.b = np.ones(len(self.arms)) 

    def choose(self):
        """ Choose the most promising arm.
            Return: arm index
        """
        # You can use np.random.beta
        #n_arms = self.arms
        
        # Pair up all beta params of a and b for each arm
        beta_params = np.column_stack((self.a,self.b)) #[[a1,b1],[a2,b2]...]
        
        # Perform random draw for all arms based on their params (a,b)
        draws = np.array([np.random.beta(i[0], i[1]) for i in beta_params])
        
        # return index of arm with the highest draw
        return np.argmax(draws)

        #raise NotImplementedError()

    def update(self, arm, reward):
        """Receive a reward after choosing a particular arm.
        This is where the agent can learn.
            Input:
                arm: choosed arm
                reward: feedback value associated with arm
        """
        # update counts pulled for chosen arm
        self.selections[arm] += 1
        n = self.selections[arm] #Keep this for the score
        
        # Update average/mean value/reward for chosen arm
        value = self.scores[arm]
        first = ((n-1)/float(n)) * value
        second = (1/float(n)) * reward
        self.scores[arm] = first + second
        
        # Update a and b
        
        # a depends on rewards
        self.a[arm] = self.a[arm] + reward
        
        # b depends on reverse reward (punishment)
        self.b[arm] = self.b[arm] + (1-reward)

        #raise NotImplementedError()


class BesaBandit():
    # https://hal.archives-ouvertes.fr/hal-01025651v1/document
    def __init__(self, arms):
        """Initialize the set of arms.
        """
        self.arms = arms
        self.rewards = [[] for i in range(len(self.arms))] #Create list of lists lists of rewards inside
        self.is_initialize=np.ones(len(self.arms)) #We first have to play all arms

    def Besa_binary(self,arm_1,arm_2):
        '''
        Given two arms, choose best
        '''
        rewards_1 = self.rewards[arm_1] #Rewards of arm 1
        rewards_2 = self.rewards[arm_2] #Rewards of arm 2

        smallest_length = min(len(rewards_1),len(rewards_2)) #Take smallest

        subsample_1 = list(random.sample(rewards_1,smallest_length)) #Subsample arm 1 rewards length smallest
        subsample_2 = list(random.sample(rewards_2,smallest_length)) #Subsample arm 2 rewards length smallest

        #Take means
        mean_1 = np.array(subsample_1).mean()
        mean_2 = np.array(subsample_2).mean()

        #Better option is arm 1
        if(mean_1 > mean_2):
            return arm_1
        #No, it is two
        elif(mean_2 > mean_1):
            return arm_2
        #Unbreak tie with less length
        elif(len(rewards_1)<len(rewards_2)):
            return arm_1
        elif(len(rewards_2)<len(rewards_1)):
            return arm_2
        #Equal chance if same
        else:
            return random.choice([arm_1,arm_2])

    def tournament(self,indexes):
        '''
        Tournament between arms!
        '''

        #One candidate, you won
        if len(indexes) <= 1:
            chosen_arm = indexes[0]
        #Two, fight!
        elif len(indexes) == 2:
            chosen_arm = self.Besa_binary(indexes[0], indexes[1])
        else:
            # Divide tournament two sections
            left_side = indexes[:len(indexes)//2]
            right_side = indexes[len(indexes)//2:]
        
            # Get winners
            winner_left = self.tournament(left_side)
            winner_right = self.tournament(right_side)

            #And final match
            chosen_arm = self.Besa_binary(winner_left, winner_right)
        
        return chosen_arm

    def choose(self):
        """ Choose the most promising arm.
            Return: arm index
        """
        #check if we have played all arms first
        if (sum(self.is_initialize)!=0):
            #We still have to play at least one arm
            arm=np.argmax(self.is_initialize)
            self.is_initialize[arm] = 0 #We played that arm
            return arm
        
        #Else we apply algorithm
        else:
            #Get random tournament
            indexes = np.arange(0,len(self.arms),1)
            #Randomizator
            random.shuffle(indexes)
            indexes=list(indexes)

            winner = self.tournament(indexes)
            return winner

        #raise NotImplementedError()

    def update(self, arm, reward):
        """Receive a reward after choosing a particular arm.
        This is where the agent can learn.
            Input:
                arm: choosed arm
                reward: feedback value associated with arm
        """
        #Update rewards
        self.rewards[arm].append(reward) #Update de correspondant list of rewards of chosen arm.
        #raise NotImplementedError()


class KLUCBBandit:
    # See: https://arxiv.org/pdf/1102.2490.pdf
    def __init__(self, arms):
        """Initialize the set of arms.
        """
        self.arms = arms
        self.n_plays = 0 #n_plays
        self.cumulative_rewards = np.zeros(len(self.arms)) #All cumulative rewards are 0 at beginning
        self.selections = np.zeros(len(self.arms)) #Selections of each arm
        self.q_s = np.arange(0.1,1,0.1) #We are going to try this q parameters for bernouilli distributions
        self.is_initialize=np.ones(len(self.arms)) #We first have to play all arms
        self.c=0

    def kl_bernoulli(self,p, q):
        """
        kl-divergence for bernouilli distribution
        """
        
        #This is to avoid runn time warnings

        delta=0.001 
        delta_p = max(p,delta)
        delta_1_p = max((1-p),delta)

        first = delta_p*np.log(delta_p/q)
        second = delta_1_p*np.log(delta_1_p/(1-q))
        total = first + second
        return total

    def choose(self):
        """ Choose the most promising arm.
            Return: arm index
        """
        #check if we have played all arms first
        if (sum(self.is_initialize)!=0):
            #We still have to play at least one arm
            arm=np.argmax(self.is_initialize)
            self.is_initialize[arm] = 0 #We played that arm
            return arm
        
        #Else we apply algorithm
        else:
            mimimum_distances = [] #List of all minimum kl distances of the arms
            condition = np.log(self.n_plays) + self.c * np.log(np.log(self.n_plays)) #Condition to store
            #For each arm
            for arm in range(0,len(self.arms)):
                minimum_q_s=[]
                ratio=self.cumulative_rewards[arm]/self.selections[arm]
                #We try for every q
                for q in self.q_s:
                    result = self.selections[arm]*self.kl_bernoulli(ratio,q)
                    #Store result of q if condition
                    if(result <= condition):
                        minimum_q_s.append(result)
                    else:
                        minimum_q_s.append(np.inf)
                #Take lowest q
                mimimum_distances.append(self.q_s[np.argmin(minimum_q_s)])
            #Take maximum of all the q_s of each arm
            return np.argmax(mimimum_distances) #Take greatest
        #raise NotImplementedError()

    def update(self, arm, reward):
        """Receive a reward after choosing a particular arm.
        This is where the agent can learn.
            Input:
                arm: choosed arm
                reward: feedback value associated with arm
        """
        #Update this variables
        self.n_plays+=1
        self.selections[arm]+=1
        self.cumulative_rewards[arm]+=reward
        #raise NotImplementedError()
