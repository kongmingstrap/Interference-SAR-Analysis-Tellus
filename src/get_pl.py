import numpy as np


## reference: https://sorabatake.jp/12465/


def get_pl(fp, latlon):
    fp.seek(
        720 + 4096 + 0 + 4680 + 8192 + 9860 + 1620 + 0 + 1540000 + 4314000 +
        345000 + 325000 + 325000 + 3072 + 511000 + 4370000 + 728000 + 15000 +
        2064, 0)
    c = np.zeros(25, dtype="float64")
    for i in range(25):
        c[i] = fp.read(20)
    d = np.zeros(25, dtype="float64")
    for i in range(25):
        d[i] = float(fp.read(20))
    lat0 = float(fp.read(20))
    lon0 = float(fp.read(20))
    phi = np.zeros(2, dtype="float64")
    lam = np.zeros(2, dtype="float64")
    phi[0] = latlon[0] - lat0
    phi[1] = latlon[1] - lat0
    lam[0] = latlon[2] - lon0
    lam[1] = latlon[3] - lon0
    pl = np.zeros(4, dtype="float64")
    for i in range(5):
        for j in range(5):
            id = i * 5 + j
            pl[0] += c[id] * lam[0]**(4 - j) * phi[0]**(4 - i)
            pl[1] += c[id] * lam[1]**(4 - j) * phi[1]**(4 - i)
            pl[2] += d[id] * lam[0]**(4 - j) * phi[0]**(4 - i)
            pl[3] += d[id] * lam[1]**(4 - j) * phi[1]**(4 - i)
    return pl
