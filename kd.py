import typer; app = typer.Typer(pretty_exceptions_show_locals=False)
from modules import data, linalg, plot
import numpy as np
from pathlib import Path

@app.command()
def cops(
        path_E0 = typer.Option(..., '--E0'),
        path_Ez = typer.Option(..., '--Ez'),
        path_meta = typer.Option(..., '--meta'),
        path_vlEr = typer.Option(..., '--vlEr'),
        zmin: float = typer.Option(float('-inf')),
        zmax: float = typer.Option(float('inf')),
):
    w, t, z, vlEr = data.load_cops(path_E0, path_Ez, path_meta)

    mask = np.logical_and(zmin <= z, z < zmax)
    z = z[mask]
    t = t[mask]
    vlEr = vlEr[mask]
    
    data.save_vals(w, t, z, vlEr, path_vlEr)
@app.command(name='solve-pKd')
def solve_pKd(
        path_vlEr = typer.Option(..., '--vlEr'),
        path_pKd = typer.Option(..., '--pKd'),
        path_plEr = typer.Option(..., '--plEr'),
        dw: int = typer.Option(19),
        dt: int = typer.Option(1),
        dz: int = typer.Option(100),
):
    w, t, z, vlEr = data.load_vals(path_vlEr, dropzeros=True)
    rw, rt, rz, pKd, plEr = linalg.solve_pKd(w, t, z, vlEr, dw, dt, dz)
    data.save_poly(rw, rt, rz, pKd, path_pKd)
    data.save_poly(rw, rt, rz, plEr, path_plEr)
@app.command()
def make_w(
        path_w = typer.Option(..., '--w'),
        num: int = typer.Option(100),
        wmin: float = typer.Option(313.0),
        wmax: float = typer.Option(765.0),
        path_vlEr = typer.Option(None, '--vlEr'),
):
    if path_vlEr is None: w = np.linspace(wmin, wmax, num).reshape(-1, 1)
    else: w, _, _, _ = data.load_vals(path_vlEr)
    
    data.save_cols(path_w, w=w)
@app.command()    
def make_tz(
        path_tz = typer.Option(..., '--tz'),
        num: int = typer.Option(100),
        zmin: float = typer.Option(0.0),
        zmax: float = typer.Option(100.0),
        tmin: float = typer.Option(0.0),
        tmax: float = typer.Option(60.0),
):
    z = np.linspace(zmin, zmax, num).reshape(-1, 1)
    t = np.linspace(tmin, tmax, num).reshape(-1, 1)
    data.save_cols(path_tz, t=t, z=z)
@app.command(name='eval-poly')
def eval_poly(
        path_poly = typer.Option(..., '--poly'),
        path_w = typer.Option(..., '--w'),
        path_tz = typer.Option(..., '--tz'),
        path_vals = typer.Option(..., '--vals'),
        wrap = typer.Option(None, '--wrap'),
):
    rw, rt, rz, poly = data.load_poly(path_poly)
    w, = data.load_cols(path_w)
    t, z = data.load_cols(path_tz)
    vals = linalg.eval_poly(w, t, z, poly, rw, rt, rz)
    if wrap == 'exp': vals = np.exp(vals)
    data.save_vals(w, t, z, vals, path_vals)
@app.command()
def heatmap(
        path_vals = typer.Option(..., '--vals'),
        path_out = typer.Option(..., '--out'),
        wrap = typer.Option(None),
):
    w, t, z, vals = data.load_vals(path_vals)
    if wrap == 'log': vals = np.log(vals)
    plot.heatmap(path_out, w, z, vals)
@app.command()    
def slices(
        path_plEr = typer.Option(..., '--plEr'),
        path_vlEr = typer.Option(..., '--vlEr'),
        path_out = typer.Option(..., '--out'),
):
    rw, rt, rz, poly = data.load_poly(path_plEr)
    w, t, z, vlEr1 = data.load_vals(path_vlEr)
    vlEr2 = linalg.eval_poly(w, t, z, poly, rw, rt, rz)
    
    plot.slices(w, z, vlEr1, vlEr2, path_out)
    
@app.command()
def figures(
        path_vKd = typer.Option(..., '--vKd'),
        path_vlEr = typer.Option(..., '--vlEr'),
        path_vlEr_noisy = typer.Option(..., '--vlEr-noisy'),
        path_w = typer.Option(..., '--w'),
        path_tz = typer.Option(..., '--tz'),
        path_dest = typer.Option(..., '--dest'),
):
    dest = Path(path_dest)
    w, t, z, vKd = data.load_vals(path_vKd)
    _, _, _, vlEr = data.load_vals(path_vlEr)
    ww, tt, zz, vlEr_noisy = data.load_vals(path_vlEr_noisy)    

    mask = vlEr > float('-inf')
    
    plot.heatmap(dest/'heatmap-pKd.pdf', w, z, np.log(vKd*mask))
    plot.heatmap(dest/'heatmap-plEr.pdf', w, z, vlEr) # vmax = 0
    plot.heatmap(dest/'heatmap-plEr-noisy.pdf', ww, zz, vlEr_noisy)

    wi = lambda i: (ww[i] - ww.min())/(ww.max() - ww.min())*(len(w)-1)

    l = []
    for i in range(19):
        l.append([zz, vlEr_noisy, i])
        l.append([z, vlEr, int(wi(i))])
    plot.slices(dest/'slices.pdf', l)
    
if __name__ == '__main__': app()    


