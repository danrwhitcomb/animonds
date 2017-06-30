import numpy as np
from random import choice, random
from util.moves import MOVES
from estimator import deep_estimator, recurrent_estimator

from keras import backend as K

LEARNING_RATE = 0.001
PERCENT_RANDOM = 0.1
BATCH_SIZE = 32
DISCOUNT = 1.0
MAX_D_SIZE = 10000

MIN = -999999

T1 = 't1'
ACTION = 'action'
REWARD = 'reward'
T2 = 't2'

class QPredictor:

    def __init__(self, time_steps, state_size, replay_size):
        # self.estimator = deep_estimator((state_size * replay_size), (len(MOVES)), LEARNING_RATE)
        self.estimator = recurrent_estimator((replay_size, state_size), (len(MOVES)), LEARNING_RATE)

        self.count = 1

        #The number of time steps there will be per episode
        self.T = time_steps

        #The number of states to include in the network input
        self.replay_size = replay_size

        # The data size to represent a single state
        self.state_size = state_size

        #The replay memory store
        self.D = []

        self.exploration_chance = 1.0

    '''
    Resets the memory contents to a default state
    initial_state --  the starting state of the environment
    '''
    def reset(self, initial_state):
        self.count = 1
        self.s = {self.count: initial_state}
        self.phi = {self.count: self._get_state_series(self.count)}

    '''
    Gets a move from based on the optimal move
    or randomly based on `PERCENT_RANDOM`
    '''
    def get_move(self):
        move = None
        if random() < self.exploration_chance:
            move = choice(MOVES)
        else:
            state_series = [self._get_state_series(self.count)]
            q_vals = self.estimator.predict(np.array(state_series))[0]
            move = MOVES[np.argmax(q_vals)]

        return move

    '''
    Updates the model with the latest about an initial state
    the action performed, the resulting state, and the reward
    of the resulting state

    Also trains the model based on replay-memory
    '''
    def update(self, action, reward, start, end):
        ind = self.count

        #Save the new state
        self.s[ind + 1] = end

        #Preprocess the new state to a standard sized data
        self.phi[ind + 1] = self._get_state_series(ind + 1)

        #Save the transition
        self.D.append({ T1: self.phi[ind],
                        ACTION: action,
                        REWARD: reward,
                        T2: self.phi[ind + 1] })

        if len(self.D) > MAX_D_SIZE:
            self.D.pop(0)

        self._train()
        self.count += 1

        if self.exploration_chance > PERCENT_RANDOM:
            self.exploration_chance -= 0.001

    '''
    Train the predictor for a single timestep
    '''
    def _train(self):
        # Select a random group of transitions from memory
        batch = self._get_random_memory_batch(BATCH_SIZE)

        # We use the estimator to select the what would
        # have been the best move and calculate the reward
        memory = self._build_optimal_labels(batch)
        input_states = np.array([d[T1] for d in batch])
        self.estimator.fit(input_states, memory, batch_size=BATCH_SIZE, epochs=1, verbose=0)

    '''
    Given a batch of transitions,
    get the expected reward for the best action
    '''
    def _build_optimal_labels(self, batch):
        memory = []

        for d in batch:
            indOfAction = MOVES.index(d[ACTION])

            target = d[REWARD] + DISCOUNT * self.estimator.predict(np.array([d[T2]]))[0]
            target_future = self.estimator.predict(np.array([d[T1]]))[0]

            target_future[indOfAction] = target[indOfAction]

            memory.append(target_future)

        return np.array(memory)

    '''
    Select 'n' random samples from D
    returns a list of transitions
    '''
    def _get_random_memory_batch(self, n):
        batch = []

        if len(self.D) < n:
            return self.D

        for i in range(n):
            rand = self._get_random_memory()
            while is_transition_in_list(rand, batch):
                rand = self._get_random_memory()

            batch.append(rand)

        return np.array(batch)

    def _get_random_memory(self):
        return choice(self.D)

    '''
    Creates a numpy array that represents a series of states
    from `start_index` to 0 or `start_index - replay_size` whichever
    comes first. Any unfilled values are set to -inf
    '''
    def _get_state_series(self, start_index, is_flat=False):
        end_index = start_index - self.replay_size if \
                    start_index - self.replay_size > 0 else 0

        #Flatten all the previous states to a single list
        states = [self.s[i] for i in range(start_index, end_index, -1)]
        history = None
        if is_flat:
            states = [val for item in states for val in item]
            history = np.zeros(self.replay_size * self.state_size)
        else:
            history = np.zeros((self.replay_size, self.state_size))

        history[:] = MIN
        for i in range(len(states)):
            history[i] = states[i]

        return history

def is_transition_in_list(transition, list):
    def equal(t1, t2):
        return t1[ACTION] == t2[ACTION] and \
               t1[REWARD] == t2[REWARD] and \
               (t1[T1] == t2[T1]).all() and \
               (t1[T2] == t2[T2]).all()

    return len([t for t in list if equal(transition, t)]) > 0
