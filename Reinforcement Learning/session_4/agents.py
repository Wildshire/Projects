import cma
import numpy as np
import copy #Copy 

from environment import Mountain
from sklearn.preprocessing import StandardScaler
from sklearn.kernel_approximation import RBFSampler
from sklearn.pipeline import Pipeline


class MC_State_Value_Approximation:
    """ MC State-value Learning with Function Approximation
    """

    def __init__(self):
        """
        Init:
            gamma: discount factor
            preprocessing_states: preprocessing state features for better representation
            mdp: instance of environment, allowing to simulate action with self.mdp.step_from_state(current_state, action)
            theta: linear weight (function approximation)
        """
        self.gamma = 0.9
        n_components = 10 # You can change
        self.preprocessing_states = Pipeline([("scaler", StandardScaler()), ("feature_generation", RBFSampler(n_components=n_components))])
        self.preprocessing_states.fit(np.array([[np.random.uniform(-1.2, 0.6), np.random.uniform(-0.07, 0.07)] for _ in range(10000)]))
        self.mdp = Mountain()
        self.theta = np.zeros(n_components) # Linear weight
        
        #Extra parameters
        self.lr = 0.01 #Learning rate for update
        self.G_r = 0 #V_pi (accumulated rewards)
        self.actions = [0,1,2] #Actions
        self.epsilon =0.2 #epsilon greedy parameter

    def preprocessing(self, state):
        """
        Return the featurized representation of a state.
        """
        return self.preprocessing_states.transform([state])[0]

    def act(self, state):
        """Output optimal action of a given state
        Return: action in [0, 1, 2]
        """
        # TO IMPLEMENT
        #Epsilon greedy
        random_value = np.random.random()
        self.epsilon/=2 #Reduce to half each time
        if(random_value<self.epsilon):
            return np.random.choice([0, 1, 2])
        else:
            #Try all actions and get best value
            values = np.zeros(3)
            for action in self.actions:
                new_state,_,_=self.mdp.step_from_state(state, action)
                values[action]=self.v(new_state)
            return np.argmax(values)


    def update(self, state, action, reward, new_state, terminal):
        """Receive a reward after performing given action.

        This is where your agent can learn. (Update theta.)
        Input:
            state: current state
            action: action done in state
            reward: reward received after doing action in state
            new_state: next state
            terminal: boolean if new_state is a terminal state or not
        """
        # TO IMPLEMENT
        #new_theta <- theta - lr[-2*(G_r-v_hat(state,theta))]*grad(v_hat(state,theta))
        
        #self.G_r +=(self.gamma**self.steps) * reward #We cannot do this, it is cheating apparently.
        
        if(terminal):
            pass
        
        found=False
        i=0
        self.G_r +=(self.gamma**i) * reward
        while(not found):
            i+=1
            next_action = self.act(new_state)
            new_state,new_reward,boolean=self.mdp.step_from_state(new_state, next_action)
            self.G_r +=(self.gamma**i) * new_reward
            #Reach final state
            if(boolean):
                found=True
            #Cannot stay forever
            if(i==10):
                found=True

        

        grad_v = self.preprocessing(state) #This is because derivtive preprocessing * theta = preprocessing
        value_state = self.v(state)
        new_theta = self.theta - self.lr*(-2*((self.G_r)-value_state))*grad_v

        #Copy
        self.theta = copy.deepcopy(new_theta)

    def v(self, state):
        """Final V function.
        Return:
            Value (scalar): V(state)
        """
        # TO IMPLEMENT
        #We multiply features of state with weights (theta)
        preprocess_state = self.preprocessing(state)
        result = np.dot(np.transpose(preprocess_state),self.theta)
        return result



class TD0_State_Value_Approximation:
    """ TD(0) State-value Learning with Function Approximation
    """

    def __init__(self):
        """
        Init:
            gamma: discount factor
            preprocessing_states: preprocessing state features for better representation
            mdp: instance of environment, allowing to simulate action with self.mdp.step_from_state(current_state, action)
            theta: linear weight (function approximation)
        """
        self.gamma = 0.9
        n_components = 10 # You can change
        self.preprocessing_states = Pipeline([("scaler", StandardScaler()), ("feature_generation", RBFSampler(n_components=n_components))])
        self.preprocessing_states.fit(np.array([[np.random.uniform(-1.2, 0.6), np.random.uniform(-0.07, 0.07)] for _ in range(10000)]))
        self.mdp = Mountain()
        self.theta = np.zeros(n_components) # Linear weight

        #Extra parameters
        self.lr = 0.1 #Learning rate for update
        self.G_r = 0
        self.actions = [0,1,2] #Actions
        self.epsilon =0.2 #epsilon greedy parameter

    def preprocessing(self, state):
        """
        Return the featurized representation of a state.
        """
        return self.preprocessing_states.transform([state])[0]

    def act(self, state):
        """Output optimal action of a given state
        Return: action in [0, 1, 2]
        """
        # TO IMPLEMENT
        #Epsilon greedy
        random_value = np.random.random()
        self.epsilon/=2 #Reduce to half each time
        if(random_value<self.epsilon):
            return np.random.choice([0, 1, 2])
        else:
            #Try all actions and get best value
            values = np.zeros(3)
            for action in self.actions:
                new_state,_,_=self.mdp.step_from_state(state, action)
                values[action]=self.v(new_state)
            return np.argmax(values)


    def update(self, state, action, reward, new_state, terminal):
        """Receive a reward after performing given action.

        This is where your agent can learn. (Update theta.)
        Input:
            state: current state
            action: action done in state
            reward: reward received after doing action in state
            new_state: next state
            terminal: boolean if new_state is a terminal state or not
        """
        # TO IMPLEMENT
        
        grad_v = self.preprocessing(state) #This is because derivtive preprocessing * theta = preprocessing
        self.G_r =reward + self.gamma * self.v(new_state)
        value_state = self.v(state)
        new_theta = self.theta - self.lr*(-2*((self.G_r)-value_state))*grad_v

        #Copy
        self.theta = copy.deepcopy(new_theta)
        

    def v(self, state):
        """Final V function.
        Return:
            Value (scalar): V(state)
        """
        # TO IMPLEMENT
        #We multiply features of state with weights (theta)
        preprocess_state = self.preprocessing(state)
        result = np.dot(np.transpose(preprocess_state),self.theta)
        return result
        #return np.random.uniform(0, 1)



class TDLambda_State_Value_Approximation:
    """ TD(lambda) State-value Learning with Function Approximation
    """

    def __init__(self):
        """
        Init:
            gamma: discount factor
            preprocessing_states: preprocessing state features for better representation
            mdp: instance of environment, allowing to simulate action with self.mdp.step_from_state(current_state, action)
            theta: linear weight (function approximation)
            lambda_value: Monte-Carlo step
        """
        self.gamma = 0.9
        n_components = 10 # You can change
        self.preprocessing_states = Pipeline([("scaler", StandardScaler()), ("feature_generation", RBFSampler(n_components=n_components))])
        self.preprocessing_states.fit(np.array([[np.random.uniform(-1.2, 0.6), np.random.uniform(-0.07, 0.07)] for _ in range(10000)]))
        self.mdp = Mountain()
        self.theta = np.zeros(n_components) # Linear weight
        self.lambda_value = 5

        #Extra parameters
        self.lr = 0.1 #Learning rate for update
        self.G_r = 0
        self.actions = [0,1,2] #Actions
        self.epsilon =0.2 #epsilon greedy parameter


    def preprocessing(self, state):
        """
        Return the featurized representation of a state.
        """
        return self.preprocessing_states.transform([state])[0]

    def act(self, state):
        """Output optimal action of a given state
        Return: action in [0, 1, 2]
        """
        # TO IMPLEMENT
        #Epsilon greedy
        random_value = np.random.random()
        self.epsilon/=2 #Reduce to half each time
        if(random_value<self.epsilon):
            return np.random.choice([0, 1, 2])
        else:
            #Try all actions and get best value
            values = np.zeros(3)
            for action in self.actions:
                new_state,_,_=self.mdp.step_from_state(state, action)
                values[action]=self.v(new_state)
            return np.argmax(values)


    def update(self, state, action, reward, new_state, terminal):
        """Receive a reward after performing given action.

        This is where your agent can learn. (Update theta.)
        Input:
            state: current state
            action: action done in state
            reward: reward received after doing action in state
            new_state: next state
            terminal: boolean if new_state is a terminal state or not
        """
        # TO IMPLEMENT
        self.G_r +=(self.gamma**0) * reward
        for i in range(1,self.lambda_value):
            next_action = self.act(new_state)
            new_state,new_reward,boolean=self.mdp.step_from_state(new_state, next_action)
            self.G_r +=(self.gamma**i) * new_reward

        grad_v = self.preprocessing(state) #This is because derivtive preprocessing * theta = preprocessing
        value_state = self.v(state)
        new_theta = self.theta - self.lr*(-2*((self.G_r)-value_state))*grad_v

        #Copy
        self.theta = copy.deepcopy(new_theta)

    def v(self, state):
        """Final V function.
        Return:
            Value (scalar): V(state)
        """
        # TO IMPLEMENT
        preprocess_state = self.preprocessing(state)
        result = np.dot(np.transpose(preprocess_state),self.theta)
        return result
        #return np.random.uniform(0, 1)



class TD0_Q_Learning_Function_Approximation:
    """ Q-Learning with Function Approximation
    """

    def __init__(self):
        """
        Init:
            gamma: discount factor
            preprocessing_states: preprocessing state features for better representation
            mdp: instance of environment, allowing to simulate action with self.mdp.step_from_state(current_state, action)
            theta: linear weight (function approximation)
        """
        self.gamma = 0.9
        n_components = 10
        self.preprocessing_states = Pipeline([("scaler", StandardScaler()), ("feature_generation", RBFSampler(n_components=n_components))])
        self.preprocessing_states.fit(np.array([[np.random.uniform(-1.2, 0.6), np.random.uniform(-0.07, 0.07)] for _ in range(10000)]))
        self.mdp = Mountain()

        #Extra parameters
        self.lr = 0.1 #Learning rate for update
        self.G_r = 0
        self.actions = [0,1,2] #Actions
        self.epsilon = 0.2 #epsilon greedy parameter
        self.theta =  np.zeros((n_components,len(self.actions))) # Assign weights to each action# TO IMPLEMENT

    def preprocessing(self, state):
        """
        Return the featurized representation of a state.
        """
        return self.preprocessing_states.transform([state])[0]

    def act(self, state):
        """Output optimal action of a given state
        Return: action in [0, 1, 2]
        """
        # TO IMPLEMENT
        #Epsilon greedy
        random_value = np.random.random()
        self.epsilon/=2 #Reduce to half each time
        if(random_value<self.epsilon):
            return np.random.choice([0, 1, 2])
        else:
            #Try all actions and get best value
            values = np.zeros(3)
            for action in self.actions:
                new_state,_,_=self.mdp.step_from_state(state, action)
                values[action]=self.q(new_state,action)
            return np.argmax(values)

        #return np.random.choice([0, 1, 2])

    def update(self, state, action, reward, new_state, terminal):
        """Receive a reward for performing given action.

        This is where your agent can learn. (Update self.theta)
        Input:
            state: current state
            action: action done in state
            reward: reward received after doing action in state
            new_state: next state
            terminal: boolean if new_state is a terminal state or not
        """
        grad_v = self.preprocessing(state) #This is because derivtive preprocessing * theta = preprocessing
        
        #Get best future action
        future_action = self.act(new_state)
        
        self.G_r = reward + self.gamma * self.q(new_state,future_action)
        value_state = self.q(state,action)
        new_theta = self.theta[:,action] - self.lr*(-2*((self.G_r)-value_state))*grad_v

        #Copy
        self.theta[:,action] = copy.deepcopy(new_theta)
        #pass


    def q(self, state, action):
        """Final Q function.
            Value (scalar): Q(state, action)
        """
        # TO IMPLEMENT
        preprocess_state = self.preprocessing(state)
        result = np.dot(np.transpose(preprocess_state),self.theta[:,action])
        return result


class Direct_Policy_Search_Agent:
    def __init__(self):
        """
        Init a new agent.
        """
        #self.policy_opt = np.zeros(2) #We have no optimal policy
        pass

    def train(self):
        """
        Learn the policy.
        """

        ############### EXAMPLE ########

        # 1- Define state features

        #state = [position, velocity]

        # 2- Define search space (of a policy)
        policy = np.zeros(2) # R**2

        # 3- Define objective function (to assess a policy)
        def objective_function(policy):
            total = 0
            env = Mountain()
            state = env.observe()
            done = False
            while not done:
                action = np.random.choice([0, 1, 2]) # random action :/
                state, reward, done = env.step_from_state(state, action)
                total += -1
            return - total # loss

        # 4- Optimize the objective function (using cma.fmin2)
        # 5- Save optimal policy; and use in `act` method
        self.policy_opt, _ = cma.fmin2(objective_function, policy, 0.5)
        print(self.policy_opt)


    def act(self, observation):
        """Output optimal action of a given state
            Return: action in [0, 1, 2]
        """
        return np.random.choice([0, 1, 2])
