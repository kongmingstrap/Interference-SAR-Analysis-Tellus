import itertools
import os
import numpy as np
import matplotlib.pyplot as plt
import math
from io import BytesIO
import cv2
import wrap_to_pi


# reference: https://sorabatake.jp/12465/


# 画像の位置合わせを行う関数
# 強度画像A,Bを用いて変位量を求めて、位相画像C,Dをその変位量で画像をカットします
# 変位量は小数点以下まで結果がでますが、それを四捨五入して整数として扱っています
def coregistration(A,B,C,D):
    py = len(A)
    px = len(A[0])
    A = np.float64(A)
    B = np.float64(B)
    d, etc = cv2.phaseCorrelate(B,A)
    dx, dy = d
    print(d) #画像の変位量です
    if dx < 0 and dy >= 0:
        dx = math.ceil(dx)-1
        dy = math.ceil(dy)
        rD = D[dy:py,0:px+dx]
        rC = C[dy:py,0:px+dx]
    elif dx < 0 and dy < 0:
        dx = math.ceil(dx)-1
        dy = math.ceil(dy)-1
        rD = D[0:py+dy,0:px+dx]
        rC = C[0:py+dy,0:px+dx]
    elif dx >= 0 and dy < 0:
        dx = math.ceil(dx)
        dy = math.ceil(dy)-1
        rD = D[0:py+dy,dx:px]
        rC = C[0:py+dy,dx:px]
    elif dx >= 0 and dy >= 0:
        dx = math.ceil(dx)
        dy = math.ceil(dy)-1
        rD = D[dy:py,dx:px]
        rC = C[dy:py,dx:px]
    return rC, rD


def get_ifgm(data_A, data_B, AB):
    file_name_sigma = "./processed_2/sigma_{}.npy"
    file_name_phase = "./processed_2/phase_{}.npy"
    sigma01 = np.load(file_name_sigma.format(data_A))
    sigma02 = np.load(file_name_sigma.format(data_B))
    phase01 = np.load(file_name_phase.format(data_A))
    phase02 = np.load(file_name_phase.format(data_B))
    #　data_A と data_B で干渉処理を実施
    coreg_phase2, coreg_phase1 = coregistration(sigma01, sigma02, phase01,
                                                phase02)
    ifgm = wrap_to_pi.wrap_to_pi(coreg_phase2 - coreg_phase1)

    np.save('./processed_3/ifgm{}.npy'.format(AB), ifgm)
    # 画像の保存
    # processed_3 ディレクトリを作成しておいてください
    plt.imsave('./processed_3/ifgm{}.jpg'.format(AB), ifgm, cmap="jet")
    return


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

    combinations = list(itertools.combinations(range(len(data_names)), 2))
    for combination in combinations:
        AB = str(combination[0]) + "_" + str(combination[1])
        data_A = data_names[int(combination[0])]
        data_B = data_names[int(combination[1])]
        try:
            get_ifgm(data_A, data_B, AB)
        except:
            print(f"Error: AB: {AB} data_A: {data_A} data_B: {data_B}")


if __name__ == "__main__":
    main()
