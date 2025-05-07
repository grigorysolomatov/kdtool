import pandas as pd
import numpy as np

def load_cops(path_E0, path_Ez, path_meta):
    df_E0 = pd.read_csv(path_E0, header=None); print('Read:', path_E0)
    df_Ez = pd.read_csv(path_Ez, header=None); print('Read:', path_Ez)
    df_meta = pd.read_csv(path_meta); print('Read:', path_meta)

    z = df_meta['depth'].values#.reshape(-1, 1)
    t = np.ones_like(z)
    w = df_E0.values[:, 0]
    E0 = df_E0.values[:, 1:].T
    Ez = df_Ez.values[:, 1:].T
    vlEr = np.log(Ez/E0)

    return w, t, z, vlEr

def save_poly(rw, rt, rz, poly, path):
    np.savez(path, rw=rw, rt=rt, rz=rz, poly=poly); print('Wrote:', path)
def load_poly(path):
    archive = np.load(path)
    poly = archive['poly']; print('Read:', path)
    rw = archive['rw']
    rz = archive['rz']
    rt = archive['rt']
    return rw, rt, rz, poly

def save_vals(w, t, z, vals, path):
    t = t.reshape(-1, 1)
    z = z.reshape(-1, 1)
    data = np.concatenate([t, z, vals], axis=1)
    df_out = pd.DataFrame(data, columns=['t', 'z'] + w.tolist())
    df_out.to_csv(path, index=False); print('Wrote:', path)
def load_vals(path, dropnans=True, dropzeros=False):
    df = pd.read_csv(path); print('Read:', path)
    if dropnans: df = df.dropna()
    if dropzeros: df = df[(df != 0).all(axis=1)]
    
    t = df['t']
    z = df['z']
    w = df.columns[2:].values.astype(float)
    vals = df.values[:, 2:]

    return w, t, z, vals

def save_cols(path, **kwargs):
    data = np.concatenate([x.reshape(-1, 1) for x in kwargs.values()], axis=1)
    
    df = pd.DataFrame(data, columns=[*kwargs.keys()])
    df.to_csv(path, index=False); print('Wrote:', path)
def load_cols(path):
    df = pd.read_csv(path); print('Read:', path)
    data = df.values
    cols = [col for col in data.T]
    return cols
    
