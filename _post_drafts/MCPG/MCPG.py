'''
REINFORCE Monte Carlo Policy Gradient AI Player
Author: Lei Mao
Date: 5/2/2017
Introduction: 
The REINFORCE_AI used REINFORCE, one of the Monte Carlo Policy Gradient methods, to optimize the AI actions in certain environment.
This script used Keras to implement the neural network and loss functions. There is also another script using Tensorflow and customized loss functions available. Personally I think the Keras version is not as good as the Tensorflow version because it used some approximations due to lacking some of the functions in Keras.

It is extremely complicated to implement the loss function of REINFORCE in Keras.
'''

import numpy as np
import keras
from keras import backend as K

GAME_STATE_FRAMES = 1  # number of game state frames used as input
GAMMA = 0.9 # decay rate of past observations
LEARNING_RATE = 0.0001 # learning rate in deep learning
FRAME_PER_ACTION = 1 # number of frames per action
REPLAYS_SIZE = 1000 # maximum number of replays in cache
SAVING_PERIOD = 5000 # period of time steps to save the model
LOG_PERIOD = 500 # period of time steps to save the log of training
MODEL_DIR = 'model/' # path for saving the model
LOG_DIR = 'log/' # path for saving the training log

class OpenAI_REINFORCE_FC():

    def __init__(self, num_actions, num_features, rand_seed, mode):
    
        # Initialize the number of player actions available in the game
        self.num_actions = num_actions
        # Initialize the number of features in the state
        self.num_features = num_features
        # Determine the shape of input to the model
        self.input_shape = self.num_features * GAME_STATE_FRAMES
        # Initialize the model
        self.model = self.REINFORCE_FC_Setup()
        # Initialize the episode number
        self.episode = 0
        # Initialize episode replays used for caching game transitions in one single episode
        self.episode_states = list() # state feature list
        self.episode_actions = list() # one-hot encoded action
        self.episode_rewards = list() # immediate reward
        # Initialize time_step to count the time steps during training
        self.time_step = 0
        # Initialize the mode of AI
        self.mode = mode

        # Initialize random seed
        self.rand_seed = rand_seed
        # Set seed for psudorandom numbers
        random.seed(self.rand_seed)
        np.random.seed(self.rand_seed)

    def Softmax_Cross_Entropy(softmax_label, softmax_pred):

        # Calculate cross entropy for softmaxed label and prediction matrices 
        return (-1.) * np.dot(softmax_label, np.log(softmax_pred.T))

    def One_Hot_Encoding(labels, num_class = self.num_actions):

        # Transform labels to one-hot encoded array
        matrix_encoded = np.zeros(len(labels), num_class, dtype = np.bool)
        matrix_encoded[np.arrange(len(labels)), labels] = 1

        return matrix_encoded

    def Customized_Loss(y_true, y_pred):

        # Customize loss function for REINFORCE policy gradient
        # We could only use Keras tensors here but not numpy

        return K.mean(y_true - y_pred)
    
    def REINFORCE_FC_Setup(self):
    
        # Prepare Policy Neural Network
        # Note that we did not use regularization here
        model = Sequential()
        # FC layer_1
        model.add(Dense(36, activation = 'relu', input_dim = self.input_shape))
        # FC layer_2
        #model.add(Dense(64, activation = 'relu'))
        # FC layer_3
        #model.add(Dense(128, activation = 'relu'))
        # FC layer_4
        model.add(Dense(self.num_actions, activation='softmax'))
        # Optimizer
        optimizer = keras.optimizers.Adam(lr = LEARNING_RATE)
        # Compile the model
        model.compile(loss = self.Customized_Loss, optimizer = optimizer)
        
        return model

    def Store_Transition(self, observation, action, reward):

        # Store game transitions used for updating the weights in the Policy Neural Network

        self.episode_states.append(observation)
        self.episode_actions.append(action)
        self.episode_rewards.append(reward)

    def Clear_Episode_Replays(self):

        self.episode_states = list()
        self.episode_actions = list()
        self.episode_rewards = list()

    def Calculate_Value(self):

        # The estimate of v(St) is updated in the direction of the complete return:
        # Gt = Rt+1 + gamma * Rt+2 + gamma^2 * Rt+3 + ... + gamma^(T-t+1)RT;
        # where T is the last time step of the episode.

        state_values = np.zeros_like(self.episode_rewards)
        state_values[-1] = self.episode_rewards[-1]
        for t in reversed(range(0, len(self.episode_rewards)-1)):
            state_values[t] = GAMMA * state_values[t+1] + self.episode_rewards[t]

        # Normalization to help the control of the gradient estimator variance
        state_values -= np.mean(state_values)
        state_values /= np.std(state_values)

        return state_values

    def REINFORCE_FC_Train(self):

        # Train model using data from one episode

        inputs = np.array(self.episode_states)
        state_values = self.Calculate_Value()
        episode_actions_encoded = self.One_Hot_Encoding(labels = np.array(self.episode_actions), num_class = self.num_actions)
        targets = np.multiply(self.softmax_cross_entropy(self.model.predict(inputs), episode_actions_encoded), state_values)

        train_loss = self.model.fit(inputs, targets)

        print('Episode: %d Train Loss: %f' %(self.episode, train_loss))
        
        # Save model routinely
        if self.time_step % SAVING_PERIOD == 0:
            if not os.path.exists(MODEL_DIR):
                os.makedirs(MODEL_DIR)
            self.model.save(MODEL_DIR + 'AI_model.h5')

        return train_loss

    def AI_Action(self, observation):
        
        action_probs = self.model.predict(observation)[0]
        action = np.random.choice(range(len(action_probs)), p = action_probs)

        return action



'''


import theano
from keras import backend as K
from keras.layers import Dense
from keras.models import Sequential

def customized_loss(y_true, y_pred):
    loss = K.switch(K.equal(y_true, -1), 0, K.square(y_true-y_pred))
    return K.sum(loss)

if __name__ == '__main__':
    model = Sequential([ Dense(3, input_shape=(4,)) ])
    model.compile(loss=customized_loss, optimizer='sgd')

    import numpy as np
    x = np.random.random((1, 4))
    y = np.array([[1,-1,0]])

    output = model.predict(x)
    print output
    # [[ 0.47242549 -0.45106074  0.13912249]]
    print model.evaluate(x, y)  # keras's loss
    # 0.297689884901
    print (output[0, 0]-1)**2 + 0 +(output[0, 2]-0)**2 # double-check
    # 0.297689929093
'''