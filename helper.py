import matplotlib.pyplot as plt
import numpy as np


def cast_user_input(val):
    if val == "q":
        return "(0, 2)"
    elif val == "a":
        return "(0, 1)"
    elif val == "z":
        return "(0, 0)"
    elif val == "w":
        return "(1, 2)"
    elif val == "s":
        return "(1, 1)"
    elif val == "x":
        return "(1, 0)"
    elif val == "e":
        return "(2, 2)"
    elif val == "d":
        return "(2, 1)"
    elif val == "c":
        return "(2, 0)"
    else:
        return "(-1, -1)"


def get_states_ids():
    state_masks = np.zeros([3**9, 9], dtype=int)
    for col in range(9):
        r = 0
        while r < 3**9:
            for i in range(r, r+3**col):
                state_masks[i, col] = -1
            for j in range(i+1, i+1+3**col):
                state_masks[j, col] = 0
            for k in range(j+1, j+1+3**col):
                state_masks[k, col] = 1
            r = k + 1

    state_ids = []
    for row in range(state_masks.shape[0]):
        state_ids.append(str(state_masks[row, :])[1:-1])
    return state_ids


class Environment:
    def __init__(self, ax):
        self.ax = ax
        self.state = np.zeros([3, 3], dtype=int)
        self.actions = ["(0, 0)", "(0, 1)", "(0, 2)", "(1, 0)", "(1, 1)", "(1, 2)", "(2, 0)", "(2, 1)", "(2, 2)"]
        self.available_actions = self.actions
        self.gameOver = False
        self.state_ids = get_states_ids()
        self.goal_masks = [np.array([[1, 1, 1], [0, 0, 0], [0, 0, 0]]),
                           np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]]),
                           np.array([[0, 0, 0], [0, 0, 0], [1, 1, 1]]),
                           np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0]]),
                           np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]]),
                           np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1]]),
                           np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
                           np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]])]
        self.scales = [5, 15, 25]
        self.Q = None
        self.first_move = True

    def reset(self):
        self.state = np.zeros([3, 3], dtype=int)
        self.actions = ["(0, 0)", "(0, 1)", "(0, 2)", "(1, 0)", "(1, 1)", "(1, 2)", "(2, 0)", "(2, 1)", "(2, 2)"]
        self.available_actions = self.actions
        self.gameOver = False
        self.first_move = True

    def AI_step(self):
        # AI's turn:
        id_prev_state = self.state_ids.index(str(self.state.flatten())[1:-1])

        if self.first_move:
            # Act randomly in the first move
            b = np.random.choice(self.available_actions)
        else:
            q_vals = self.Q[id_prev_state, :]
            while True:
                id_best_action = np.argmax(q_vals)
                b = self.actions[id_best_action]
                if b in self.available_actions:
                    break
                else:
                    q_vals[id_best_action] = - np.inf

        self.state[eval(b)] = -1
        self.available_actions.remove(b)
        self.ax.plot(self.scales[eval(b)[0]], self.scales[eval(b)[1]], 'o', markersize=100, color="crimson")
        # plt.pause(.1)

        for mask in self.goal_masks:
            if np.abs(np.sum(self.state * mask)) == 3:
                self.gameOver = True
                self.ax.set_title("Machine wins!!")
                return

        if len(self.available_actions) == 0:
            self.gameOver = True
            self.ax.set_title("Nobody wins")
            return

    def Human_step(self):
        while True:
            a = cast_user_input(input())
            if a in self.available_actions:
                break
            print("Action not available, try again: ")

        self.state[eval(a)] = 1
        self.available_actions.remove(a)
        self.ax.plot(self.scales[eval(a)[0]], self.scales[eval(a)[1]], 'x', markersize=100, color="blue")
        # plt.pause(.1)

        for mask in self.goal_masks:
            if np.abs(np.sum(self.state * mask)) == 3:
                self.gameOver = True
                self.ax.set_title("Player wins!!")
                # print("A wins")
                return

        if len(self.available_actions) == 0:
            self.gameOver = True
            self.ax.set_title("Nobody wins")
            return

    def Random_step(self):
        a = np.random.choice(self.available_actions)

        self.state[eval(a)] = 1
        self.available_actions.remove(a)
        self.ax.plot(self.scales[eval(a)[0]], self.scales[eval(a)[1]], 'x', markersize=100, color="blue")
        # plt.pause(.1)

        for mask in self.goal_masks:
            if np.abs(np.sum(self.state * mask)) == 3:
                self.gameOver = True
                self.ax.set_title("Player wins!!")
                print("A wins")
                return

        if len(self.available_actions) == 0:
            self.gameOver = True
            self.ax.set_title("Nobody wins")
            print("Nobody wins")
            return