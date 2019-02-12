import numpy as np
from numpy import sin, cos
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import gridspec
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Cart-Pole Collocation')
    parser.add_argument('--graph', default=False, action='store_true',
                        help='Plot the results')
    parser.add_argument('--animate', default=False, action='store_true',
                        help='Animate the results')

    return parser.parse_args()


def plot_cart_pole_graphs(t, x, u):
    gs = gridspec.GridSpec(3, 2)
    ax0 = plt.subplot(gs[0, 0])
    plt.plot(t, x[:, 0])
    ax1 = plt.subplot(gs[0, 1])
    plt.plot(t, x[:, 1])
    ax2 = plt.subplot(gs[1, 0])
    plt.plot(t, x[:, 2])
    ax3 = plt.subplot(gs[1, 1])
    plt.plot(t, x[:, 3])
    ax4 = plt.subplot(gs[2, :])
    plt.plot(t, u)
    plt.show()


def animate_cart_pole(t, x):
    cp = x[:, 0]
    phi = x[:, 2]

    cart_width = 0.25
    cart_height = 0.1

    rod_length = 0.5
    pendulum_size = 0.015

    fig = plt.figure()

    xmin = np.around(x[:, 0].min() - cart_width / 2.0, 1)
    xmax = np.around(x[:, 0].max() + cart_width / 2.0, 1)

    ax = plt.axes(xlim=(xmin, xmax), ylim=(-1.1, 1.1), aspect='equal')
    time_text = ax.text(0.04, 0.9, '', transform=ax.transAxes)
    rect = patches.Rectangle([x[0, 0] - cart_width / 2.0, -cart_height / 2],
                             cart_width, cart_height, fill=True, color='red', ec='black')

    ax.add_patch(rect)
    line, = ax.plot([], [], lw=2, marker='o', markersize=6)

    def init():
        time_text.set_text('')
        rect.set_xy((0.0, 0.0))
        line.set_data([], [])
        return time_text, rect, line,

    def update(i):
        x_car = cp[i]
        y_car = 0

        x_pendulum = -rod_length * sin(phi[i]) + x_car
        y_pendulum = rod_length * cos(phi[i])

        time_text.set_text('time = {:2.2f}'.format(t[i]))
        rect.set_xy((x_car - 0.5 * cart_width, y_car - cart_height))
        line.set_data([x_car, x_pendulum], [y_car, y_pendulum])

        return time_text, rect, line,

    ani = FuncAnimation(fig, update, frames=len(t), init_func=init,
                        blit=True, interval=10)

    plt.show()

    return ani
