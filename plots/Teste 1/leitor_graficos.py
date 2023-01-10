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

arquivo = open('solucoes.txt', 'r')
for linha in arquivo:
    if linha[0] == ' ':
        massa = float(linha[-10:-5])
        mass_list.append(massa)


arquivo.close()

plt.figure(dpi=145)
plt.title('Combustion Chamber Pressure', fontsize = 20, color='#0c2356')
plt.xlabel('Time [s]', fontsize = 15, color='#0c2356')
plt.ylabel('Pressure [Psi]', fontsize = 15, color='#0c2356')
plt.grid(alpha=0.3)
# plt.xticks(np.arange(0, 12, step=1))
plt.tick_params(labelsize=12)
plt.scatter(isp_list, mass_list, color='#27A9E1')
plt.show()
