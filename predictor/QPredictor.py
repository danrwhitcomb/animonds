import numpy as np
from random import choice, random

from predictor import Predictor
from util.moves import MOVES
from estimator import deep_q_estimator


import tensorflow as tf

LEARNING_RATE = 0.000005
PERCENT_RANDOM = 0.1
BATCH_SIZE = 32
DISCOUNT = 0.99
MAX_D_SIZE = 1000
RELU_E = 0.001
DROPOUT = 0.5
MOMENTUM = 0.5

MIN = -999999

T1 = 't1'
ACTION = 'action'
REWARD = 'reward'
T2 = 't2'

MODEL_FILE = 'animond.model'


class QPredictor(Predictor):

    def __init__(self,
                 epoch_size,
                 replay_size,
                 random_percent=PERCENT_RANDOM,
                 learning_rate=LEARNING_RATE,
                 discount=DISCOUNT,
                 momentum=MOMENTUM,
                 dropout=DROPOUT):
        self.discount = discount
        self.random_percent = random_percent
        self.learning_rate = learning_rate
        self.dropout = dropout
        self.momentum = momentum

        self.count = 1
        self.episode = 1

        # The number of time steps there will be per episode
        self.T = epoch_size

        # The number of states to include in the network input
        self.replay_size = replay_size

        # The replay memory store
        self.D = []

        self.exploration_chance = 1.0

    def initialize(self, initial_state):
        self.state_size = len(initial_state)
        self.reset(initial_state)

        output_count = len(MOVES)

        self.X = tf.placeholder(tf.float32, shape=(None, self.state_size * self.replay_size), name='state_inputs')
        self.y = tf.placeholder(tf.float32, shape=(None, output_count), name='labels')
        self.move_masks = tf.placeholder(tf.float32, shape=(None, output_count), name='move_masks')

        self.graph_output, self.train, self.summaries = deep_q_estimator(self.X, self.y,
                                                                         self.move_masks,
                                                                         output_count,
                                                                         self.learning_rate,
                                                                         self.dropout, self.momentum)

        self.session = tf.InteractiveSession()
        tf.global_variables_initializer().run()

        self.summary_writer = tf.summary.FileWriter('summary', self.session.graph)

    '''
    Resets the memory contents to a default state
    initial_state --  the starting state of the environment
    '''
    def reset(self, initial_state):
        self.count = 1
        self.episode += 1
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
            q_vals = self.session.run(self.graph_output,
                                      feed_dict={self.X: np.array(state_series)})[0]
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

        # Save the new state
        self.s[ind + 1] = end

        # Preprocess the new state to a standard sized data
        self.phi[ind + 1] = self._get_state_series(ind + 1)

        # Save the transition
        self.D.append({T1: self.phi[ind],
                       ACTION: action,
                       REWARD: reward,
                       T2: self.phi[ind + 1]})

        if len(self.D) > MAX_D_SIZE:
            self.D.pop(0)

        self._train()
        self.count += 1

        if self.exploration_chance > self.random_percent:
            self.exploration_chance -= 0.00001

    '''
    Train the predictor for a single timestep
    '''
    def _train(self):
        # Select a random group of transitions from memory
        batch = self._get_random_memory_batch(BATCH_SIZE)

        # We use the estimator to select the what would
        # have been the best move and calculate the reward
        memory, move_masks = self._build_optimal_labels(batch)
        input_states = np.array([d[T1] for d in batch])
        summary, _ = self.session.run([self.summaries, self.train], feed_dict={self.X: input_states,
                                                                               self.y: memory,
                                                                               self.move_masks: move_masks})

        self.summary_writer.add_summary(summary, self.episode * self.T + self.count)

    '''
    Given a batch of transitions,
    get the expected reward for the best action
    '''
    def _build_optimal_labels(self, batch):
        memory = []
        move_masks = []

        for d in batch:

            # Get the future output
            target = self.session.run(self.graph_output, feed_dict={self.X: np.array([d[T2]])})[0]
            ind_best_action = np.argmax(target)
            ind_recorded_action = MOVES.index(d[ACTION])

            target_q_value = d[REWARD] + (self.discount * target[ind_best_action])
            label = np.zeros(len(MOVES))
            label[ind_recorded_action] = target_q_value
            # Generate the move mask that will be used
            # to hide loss differences from other actions
            # during training
            move_mask = np.zeros((len(MOVES)))
            move_mask[ind_recorded_action] = 1

            move_masks.append(move_mask)
            memory.append(target)

        return np.array(memory), np.array(move_masks)

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
    def _get_state_series(self, start_index, is_flat=True):
        end_index = start_index - self.replay_size if \
                    start_index - self.replay_size > 0 else 0

        # Flatten all the previous states to a single list
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

    def get_callbacks(self):
        return [self.monitor]

    def save(self):
        saver = tf.train.Saver()
        saver.save(self.session, MODEL_FILE)
        print("Model saved.")

    def load(self, file_path):
        saver = tf.train.Saver()
        saver.restore(self.session, file_path)
        print("Model restored.")

    def close(self):
        self.summary_writer.close()


def is_transition_in_list(transition, list):
    def equal(t1, t2):
        return t1[ACTION] == t2[ACTION] and \
               t1[REWARD] == t2[REWARD] and \
               (t1[T1] == t2[T1]).all() and \
               (t1[T2] == t2[T2]).all()

    return len([t for t in list if equal(transition, t)]) > 0
