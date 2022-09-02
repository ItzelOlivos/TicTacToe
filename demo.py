import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from helper import Environment
from matplotlib.animation import FuncAnimation
from matplotlib import animation


def create_demo():
    # ================= Setting subplots ===================
    fig, ax = plt.subplots(1, 1, figsize=(12,7))

    def clear():
        ax.clear()
        ax.add_patch(Rectangle((0, 0), 30, 30, facecolor='white'))
        ax.plot(np.arange(0, 30), 10 * np.ones(30), 'k', linewidth=1.)
        ax.plot(np.arange(0, 30), 20 * np.ones(30), 'k', linewidth=1.)
        ax.axvline(10, 0, 30, linewidth=1., color='black')
        ax.axvline(20, 0, 30, linewidth=1., color='black')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal')

    def animate(t):
        if match.gameOver:
            clear()
            match.reset()

        match.AI_step()
        if not match.gameOver:
            match.Random_step()

    clear()
    match = Environment(ax)
    match.Q = np.load('best_policy_offensive.npy')

    anim = FuncAnimation(
        fig,
        animate,
        frames=50,
        interval=1,
        blit=False,
        repeat=False
    )

    plt.show()

    return anim


anim = create_demo()

f = r"animation-tictactoe.gif"
writergif = animation.PillowWriter(fps=2)
anim.save(f, writer=writergif)