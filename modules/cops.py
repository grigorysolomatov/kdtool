import pandas as pd
import numpy as np

def read(path_E0, path_Ez, path_meta):
    df_E0 = pd.read_csv(path_E0, header=None); print('Read:', path_E0)
    df_Ez = pd.read_csv(path_Ez, header=None); print('Read:', path_Ez)
    df_meta = pd.read_csv(path_meta); print('Read:', path_meta)

    z = df_meta['depth'].values.reshape(-1, 1)
    t = np.ones_like(z)
    w = df_E0.values[:, 0]
    E0 = df_E0.values[:, 1:].T
    Ez = df_Ez.values[:, 1:].T
    Er = Ez/E0

    return w, t, z, Er
