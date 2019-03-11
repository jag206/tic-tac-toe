from copy import copy
import matplotlib.pyplot as plt
import numpy as np
import random
import time

from env import Environment, Player


class RandomAgent:
    def learn(self):
        pass

    def process(self, state, learning=True):
        action_space = env.action_space()
        return action_space[random.randint(0, len(action_space)-1)]

    def learn(self, state, action, new_state, reward):
        pass

class LearnedAgent:
    def __init__(self, q_table=None):
        self.q_table = q_table if q_table else np.zeros([pow(3, 9), 9])
        self.alpha = 0.1
        self.eps = 0.0001
        self.gamma = 0.9

    def learn(self, state, action, new_state, reward):
        old_value = self.q_table[state, action]
        next_max = np.max(self.q_table[new_state])

        new_value = (1-self.alpha) * old_value + self.alpha * (reward - self.gamma * next_max)
        self.q_table[state, action] = new_value

    def process(self, state, learning=True):
        if learning and random.uniform(0, 1) < self.eps:
            return random.randint(0, 7)
        else:
            return np.argmax(self.q_table[state])

old_q_table = LearnedAgent().q_table
agent1 = LearnedAgent()
agent2 = RandomAgent()
env = Environment()
epochs = 20
train_size = 10000
test_size = 1000
games_to_debug = 0
record_losses = False

win_ratios = []
draw_ratios = []
loss_ratios = []
for idx_e, e in enumerate(range(epochs)):
    print("Start of epoch {}:".format(idx_e+1))
    # time.sleep(1)
    for i in range(train_size):
        env.reset()
        # env.render()
        done = False
        while not done:
            state = env.get_state()
            cur_go = env.who_next()
            if cur_go == Player.X:
                action = agent1.process(state, learning=True)
            else:
                action = agent2.process(state, learning=True)

            # print("Playing action {}".format(action))
            valid, done, winner = env.play(action)

            new_state = env.get_state()

            reward = 0
            if cur_go == Player.X:
                if not valid:
                    reward = -1
                    # print("Oops, that move was invalid")

            if done:
                if winner == cur_go:
                    reward = +1
                elif winner == Player.UNASSIGNED:
                    reward = 0
                else:
                    reward = -1

            agent1.learn(state, action, new_state, reward)

            # env.render()

    print("\tTest time!")
    winners = np.array([])
    debug = False
    for i in range(test_size):
        if i >= test_size - games_to_debug:
            debug = True

        env.reset()

        record = np.array([])
        record = np.append(record, env.render())
        done = False
        while not done:
            if debug:
                print("{}'s go".format(env.who_next_str()))
                time.sleep(1)

            state = env.get_state()
            if env.who_next() == Player.X:
                action = agent1.process(state, learning=False)
            else:
                action = agent2.process(state, learning=False)

            _, done, winner = env.play(action)

            record = np.append(record, env.render())
            if debug:
                print(env.render())
                time.sleep(1)

        if record_losses and winner == Player.O:
            for r in record:
                print(r)
            print("Winner is {}".format(winner))

        winners = np.append(winners, winner)

    wins = np.count_nonzero(winners==Player.X)
    draws = np.count_nonzero(winners==Player.UNASSIGNED)
    losses = np.count_nonzero(winners==Player.O)
    print("\tRatio is {}/{}/{}".format(wins / len(winners), draws / len(winners), losses / len(winners)))
    # time.sleep(2)

    win_ratios.append(wins/len(winners))
    draw_ratios.append(draws/len(winners))
    loss_ratios.append(losses/len(winners))
    print("\tQ-table changed by {}%".format(100 * np.linalg.norm(agent1.q_table - old_q_table)/np.linalg.norm(agent1.q_table)))
    old_q_table = copy(agent1.q_table)

plt.plot(win_ratios,'g')
plt.plot(draw_ratios,'b')
plt.plot(loss_ratios,'r')
plt.show()
