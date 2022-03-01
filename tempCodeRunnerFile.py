#-------------------------------- Plotando graficos --------------------------------

isp = []
massa_total = []

isp_g1 = []
massa_total_g1 = []


for individuo in P[num_geracoes-1]:
    isp.append(individuo.isp)
    massa_total.append(individuo.massa_total)

for individuo in P[1]:
    isp_g1.append(individuo.isp)
    massa_total_g1.append(individuo.massa_total)


plt.title('Etanol - LOX(Geração 1)', fontsize = 20, color='#0c2356')
plt.scatter(isp_g1, massa_total_g1, color='r')
plt.xlabel('isp [s]', fontsize = 15, color='#0c2356')
plt.ylabel('Massa Total do Sistema Prpulsivo [kg]', fontsize = 15, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()


# plt.figure()
plt.scatter(isp, massa_total, color='#27a9e1')
plt.title('Etanol - LOX', fontsize = 20, color='#0c2356')
plt.xlabel('isp [s]', fontsize = 15, color='#0c2356')
plt.ylabel('Massa Total do Sistema Prpulsivo [kg]', fontsize = 15, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()


plt.title('Etanol - LOX', fontsize = 20, color='#0c2356')
plt.scatter(isp_g1, massa_total_g1, color='r')
plt.scatter(isp, massa_total, color='#27a9e1')
plt.xlabel('isp [s]', fontsize = 15, color='#0c2356')
plt.ylabel('Massa Total do Sistema Prpulsivo [kg]', fontsize = 15, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()

#-------------------------------- Plotando graficos --------------------------------