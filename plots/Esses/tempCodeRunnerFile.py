import matplotlib.pyplot as plt
import pandas as pd

isp_list = []
mass_list = []

arquivo = open('solucoes.txt', 'r')
for linha in arquivo:
    if linha[0] == 'R':
        isp = float(linha[19:22])
        print(isp)
        isp_list.append(isp)