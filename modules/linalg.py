import numpy as np

def solve_pKd(ww, tt, zz, vlEr, dw, dt, dz):
    z = normalize(zz, zz.min(), zz.max())
    t = normalize(tt, tt.min(), tt.max())
    w = normalize(ww, ww.min(), ww.max())

    M = {}    
    M['Ew'] = Matrix.evaluate(w, dw)
    M['Etz'] = Matrix.evaluate2(t, z, dt, dz+1)
    M['Ew ⊗ Etz'] = np.kron(M['Ew'], M['Etz'])

    A = M['Ew ⊗ Etz']
    b = vlEr.reshape(-1, 1, order='F')
    plEr = np.linalg.lstsq(A, b, rcond=None)[0]

    M['Iw'] = np.eye(dw)
    M['It'] = np.eye(dt)
    M['Dz'] = Matrix.differentiate(dz+1)
    M['Iw ⊗ It ⊗ Dz'] = np.kron(M['Iw'], np.kron(M['It'], M['Dz']))
    pKd = - M['Iw ⊗ It ⊗ Dz'] @ plEr

    plEr = plEr.reshape(dz+1, dt, dw, order='F')
    pKd = pKd.reshape(dz, dt, dw, order='F')/(zz.max() - zz.min())

    rw = np.array([ww.min(), ww.max()])
    rt = np.array([tt.min(), tt.max()])
    rz = np.array([zz.min(), zz.max()])

    return rw, rt, rz, pKd, plEr
def eval_poly(w, t, z, poly, rw, rt, rz):
    dz, dt, dw = poly.shape
    z = normalize(z, rz[0], rz[1])
    t = normalize(t, rt[0], rt[1])
    w = normalize(w, rw[0], rw[1])

    M = {}
    M['Ew'] = Matrix.evaluate(w, dw)
    M['Etz'] = Matrix.evaluate2(t, z, dt, dz)
    M['Ew ⊗ Etz'] = np.kron(M['Ew'], M['Etz'])
    M['[poly]'] = poly.reshape(-1, order='F')
    M['(Ew ⊗ Etz) [poly]'] = M['Ew ⊗ Etz'] @ M['[poly]']
    poly = M['(Ew ⊗ Etz) [poly]'].reshape(len(z), len(w), order='F')

    return poly
# Internal ---------------------------------------------------------------------
def normalize(x, xmin, xmax):
    if xmax == xmin: return x/xmax
    return (x - xmin)/(xmax-xmin)
class Matrix:
    def integrate(d):
        diag = np.array([1/(i+1) for i in range(d)])
        zeros = np.zeros((1, d))
        mat = np.diag(diag)
        mat = np.concatenate([zeros, mat], axis=0)
        return mat
    def differentiate(d):
        zeros = np.zeros((d-1, 1))
        diag = np.array([float(i+1) for i in range(d-1)])
        mat = np.concatenate([zeros, np.diag(diag)], axis=1)
        return mat
    def evaluate(x, d):
        mat = np.vander(x, N=d, increasing=True)
        return mat
    def evaluate2(x, y, dx, dy):
        ex = Matrix.evaluate(x, dx)
        ey = Matrix.evaluate(y, dy)
        mat = Matrix.coldiag(ex) @ np.kron(np.eye(dx), ey)
        return mat
    def coldiag(inmat):
        cols = [np.diag(col) for col in inmat.T]
        mat = np.concatenate(cols, axis=1)
        return mat
