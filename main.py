import random
import time

from env import Environment

env = Environment()
env.render()

num_steps = 1000
done = False
while not done:
    print("New go for {}".format(env.who_next()))
    # time.sleep(2)
    square = random.randint(0, 8)
    print("Playing in square {}".format(square))
    valid, done = env.play(square)
    if not valid:
        print("Oops, that move was invalid")

    env.render()

print("Done!")