import os
import numpy as np
import struct
import math
import matplotlib.pyplot as plt
from io import BytesIO
import cv2
import get_pl


## reference: https://sorabatake.jp/12465/


def gen_img(fp, off_col, col, off_row, row):
    cr = np.array([off_col, off_col + col, off_row, off_row + row], dtype="i4")
    fp.seek(236)
    nline = int(fp.read(8))
    nline = cr[3] - cr[2]  # row
    fp.seek(248)
    ncell = int(fp.read(8))
    prefix = 412 # PALSAR-1 L1.1の場合
    nrec = prefix + ncell * 8

    nline = cr[3] - cr[2]
    fp.seek(720)
    fp.seek(int((nrec / 4) * (cr[2]) * 4))
    data = struct.unpack(">%s" % (int((nrec * nline) / 4)) + "f",
                         fp.read(int(nrec * nline)))
    data = np.array(data).reshape(-1, int(nrec / 4))
    data = data[:, int(prefix / 4):]
    data = data[:, ::2] + 1j * data[:, 1::2]
    data = data[:, cr[0]:cr[1]]
    sigma = 20 * np.log10(abs(data)) - 83.0 - 32.0
    phase = np.angle(data)
    sigma = np.array(255 * (sigma - np.amin(sigma)) /
                     (np.amax(sigma) - np.amin(sigma)),
                     dtype="uint8")
    sigma = cv2.equalizeHist(sigma)
    return sigma, phase


def main():
    data_names = [
        "ALPSRP156372940",
        "ALPSRP095982940",
        "ALPSRP082562940",
        "ALPSRP075852940",
        "ALPSRP069142940",
        "ALPSRP062432940",
        "ALPSRP055722940",
        "ALPSRP102692940",
        "ALPSRP089272940",
        "ALPSRP183212940",
        "ALPSRP189922940",
        "ALPSRP196632940",
        "ALPSRP210052940",
        "ALPSRP243602940",
    ]

    latlon = np.array([33.585, 33.600, 130.415, 130.420], dtype="float64")
    for data_name in data_names:
        fpimg = open(os.path.join("./processed_1/IMG-HH-" + data_name +
                                  "-H1.1__D"),
                     mode='rb')
        fpled = open(os.path.join("./processed_1/LED-" + data_name +
                                  "-H1.1__D"),
                     mode='rb')
        pl = np.array(np.ceil(get_pl.get_pl(fpled, latlon)), dtype=np.int64)
        off_col = min(pl[0], pl[1])
        off_row = min(pl[2], pl[3])

        # ピクセル値を調整して強度・位相画像を出力
        try:
            sigma, phase = gen_img(fpimg, off_col - 200, 1000, off_row - 300,
                                   1000)
            sigma = np.rot90(sigma, k=3)
            sigma = np.rot90(sigma, k=-1)
            sigma = np.fliplr(sigma)  # 画像が反転しているため
            phase = np.rot90(phase, k=3)
            phase = np.rot90(phase, k=-1)
            phase = np.fliplr(phase)  # 画像が反転しているため

            # 強度画像(sigma)と位相画像(phase)をそれぞれグレースケールとjetカラーマップで表示
            # processed_2 ディレクトリを作成しておいてください
            plt.imsave('./processed_2/sigma_{}.jpg'.format(data_name),
                       sigma,
                       cmap="gray")
            plt.imsave('./processed_2/phase_{}.jpg'.format(data_name),
                       phase,
                       cmap="jet")
            np.save('./processed_2/sigma_{}.npy'.format(data_name), sigma)
            np.save('./processed_2/phase_{}.npy'.format(data_name), phase)
        except:
            print("Error: ", data_name)
        fpimg.close()


if __name__=="__main__":
    main()
