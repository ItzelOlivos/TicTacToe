import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from helper import Environment

plt.figure(figsize=(7, 7))
ax = plt.subplot(1, 1, 1)
plt.ion()
plt.show()

repeat = "2"
while repeat == "2":
    ax.clear()
    ax.add_patch(Rectangle((0, 0), 30, 30, facecolor='white'))
    ax.plot(np.arange(0, 30), 10 * np.ones(30), 'k', linewidth=1.)
    ax.plot(np.arange(0, 30), 20 * np.ones(30), 'k', linewidth=1.)
    ax.axvline(10, 0, 30, linewidth=1., color='black')
    ax.axvline(20, 0, 30, linewidth=1., color='black')
    ax.set_xticks([])
    ax.set_yticks([])

    match = Environment(ax)

    match.Q = np.load('best_policy_offensive.npy')

    while not match.gameOver:
        match.AI_step()
        print(match.state)
        if not match.gameOver:
            match.Human_step()
            print(match.state)

    repeat = input('quit? (1) or play again? (2)')

plt.ioff()
