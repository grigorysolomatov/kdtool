import matplotlib.pyplot as plt
import numpy as np

def heatmap(path, w, z, vals, **kwargs):
    fig, axs = plt.subplots(1, 1)
    axs.pcolormesh(w, z, vals, **kwargs)
    axs.invert_yaxis()
    axs.set_xlabel(r'$\lambda$ [nm]')
    axs.set_ylabel(r'$z$ [m]')
    
    fig.savefig(path); print('Wrote:', path); plt.show()
def slices(w, z, vlEr1, vlEr2, path):
    fig, axs = plt.subplots(1, 1)
    for i, wi in enumerate(w):
        axs.plot(z, vlEr1[:, i],
                 linewidth=5, linestyle='none', marker='.', color='#000000')
    for i, wi in enumerate(w):
        axs.plot(z, vlEr2[:, i], color='#ff44ff')
    fig.savefig(path); print('Wrote:', path); plt.show()

def slices2(path, args):
    fig, axs = plt.subplots(1, 1)
    for z, slice1, i in args:
        axs.plot(z, slice1[:, i])
    fig.savefig(path); print('Wrote:', path); plt.show()
    
