import random
import math
import equations as eq
from rocketcea.cea_obj import CEA_Obj, add_new_fuel, add_new_oxidizer
import propelentes as prop

#---------------------------------- Entradas do Programa ----------------------------------
deltav = 4000 # m/s - Acréscimo de velocidade
mpay = 100 # kg - massa da payload
#m_rocket = 40 # kg - massa estimada do foguete

add_new_fuel('Ethanol90', prop.card_Ethanol90)

fuel = "Ethanol"
oxidizer = "LOX"
comb_efficiency = 0.92 # 0.90 # 0.93
exp_efficiency = 0.97 # 1 # 0.98
energ_efficiency = comb_efficiency * exp_efficiency
#---------------------------------- Entradas do Programa ----------------------------------


#----------------------------------- Preço dos reagnetes ----------------------------------    
precoFuel_litro = prop.preco_Ethanol90
precoOxidizer_Kg = prop.preco_n2o
precoPressurizante_m3 = prop.preco_N2
#----------------------------------- Preço dos reagnetes ----------------------------------  


#---------------------------------- Classes do Programa -----------------------------------

class Population:
    def __init__(self, max_pop):
        self.population = []
        self.frentes = [[]]
        self.generation = 0
        self.max_pop = max_pop
        
        # adicionados apenas para plotar no txt
        self.fuel = fuel
        self.oxidizer = oxidizer
        self.deltav = deltav
        self.mpay = mpay
        #self.m_rocket = m_rocket
        
    def __len__(self):
        return len(self.population)
    

class Individual:#(object)
    def __init__(self):
        self.cea = CEA_Obj(oxName=oxidizer, fuelName=fuel)
        self.name = 'Padrao'
        self.num = 0
        self.rank = 0
        self.parentes = []
        self.crowding_distance = 0
        self.domination_count = 0
        self.dominated_solutions = []
        self.genes = [] #genes =[OF, Pc, dt, Pe] #primeiro será feito com um unico of e unico propelente
        self.genes_lower = (1, 10, 20, 0.075)#(1, 10, 30, 1.0)
        self.genes_upper = (8, 20, 110, 0.075) #(8, 50, 70, 1.01325)
        self.k = 1.2 # Razão dos calores específicos Proviniente da razão of
        self.rho_fuel = 785 # kg/m^3 - Densidade do Ethanol 
        self.rho_oxidante = 1142 # kg/m^3 - Densidade do LOX
        self.isp = 0
        self.massa_total = 0
        self.t_burn = 0
        self.empuxo = 0
        self.temperaturaCC = 0
        self.Razao_Expansao = 0

        self.inverso_isp = 0
        
        self.massa_motor = 0
        self.massa_propelente = 0
        self.massa_pressurizante = 0
        self.volume_pressurizante = 0
        self.massa_tank_fuel = 0
        self.massa_tank_oxi = 0
        self.massa_tank_pressurizante = 0
        self.deltaP_inj = 0

        self.massa_estrutural = 0
        self.relacao_empuxo_peso_inicial = 0
        self.relacao_empuxo_peso_final = 0
        
        self.preco_fuel = 0
        self.preco_oxi = 0
        self.preco_pressurizante = 0
        self.preco_total = 0
        
               
    def calcula_objetivos(self):
    # Variáveis de entrada 
        OF = self.genes[0]
        P1 = self.genes[1]  
        At = (math.pi/4)*self.genes[2]**2
        P2 = self.genes[3]
        g = 9.81
        dt = self.genes[2]
        self.cstar = comb_efficiency * (self.cea.get_Cstar(Pc = P1* 14.5038, MR = OF)) * 0.3048 #mudando de ft/s para m/s
        
        Razao_Expansao = self.cea.get_eps_at_PcOvPe(Pc=P1* 14.5038, MR=OF, PcOvPe = (P1/P2))   # passando de bar para psi   
        #A2 = At * Razao_Expansao
        self.Razao_Expansao = Razao_Expansao

        # Diâmetro externo do Bocal                                                 
        de = dt * Razao_Expansao


        #* Se o motor for testado em pressão ambiente, usar: 
        #isp, mode = propelente.estimate_Ambient_Isp(Pc=P1* 14.5038, MR=OF, eps=Razao_Expansao, Pamb=14.7, frozen=0, frozenAtThroat=0)
        isp = energ_efficiency * self.cea.get_Isp(Pc=P1* 14.5038, MR=OF, eps=Razao_Expansao, frozen=0, frozenAtThroat=0)
        self.isp = isp #self.cea.get_Isp(Pc=P1* 14.5038, MR=OF)
        
        self.Cf = ((self.isp * g)/self.cstar)  
             
        self.empuxo = self.Cf * P1 * 0.1 * At # passando de Bar para psi
        F = self.empuxo

        # Calculando Temperatura chama adiabática
        temp_F = self.cea.get_Tcomb(Pc=P1, MR=OF) # temperatura de chama em °F
        self.temperaturaCC = (((temp_F - 32) * (5/9)) + 273.15)

        # Calculo da massa do motor
        self.massa_motor = eq.engine_mass(F, P1, Razao_Expansao)


        #!Calculo da massa de propelente, pressurizante e tanques
        m_tanks = [0]
        i = 0 #contador
        self.massa_pressurizante = 0

        while True:
            # Calculo da massa de propelente, combustivel e oxidante
            self.massa_propelente = eq.propellant_mass(self.isp, deltav, OF, mpay, self.massa_motor, m_tanks[i]) - self.massa_pressurizante
            massa_fuel = self.massa_propelente / (1 + self.genes[0])
            volume_fuel = massa_fuel / self.rho_fuel       
            massa_oxi = (self.massa_propelente * self.genes[0]) / (1 + self.genes[0])
            volume_oxi = massa_oxi / self.rho_oxidante
            volume_propelente = volume_fuel + volume_oxi
        
            # Calculo pressões dos tanques de combustivel e oxidante
            Pc = P1 * 10**(5) #  passando para pascal
            deltaP_inj = 0.4 * Pc
            self.deltaP_inj = 0.4 * P1
            deltaP_feed = 50000 
            deltaP_dynamics_fuel = 0.5 * self.rho_fuel * 10**2
            deltaP_dynamics_oxi = 0.5 * self.rho_oxidante * 10**2        
            Ptank_fuel = deltaP_inj + deltaP_feed + deltaP_dynamics_fuel + Pc
            Ptank_oxi = deltaP_inj + deltaP_feed + deltaP_dynamics_oxi + Pc
            Ptank_average = (Ptank_fuel + Ptank_oxi)/2
        
        
            # Calculo da massa e do volume de pressurizate
            self.massa_pressurizante, self.volume_pressurizante = eq.massa_pressurizante(Ptank_average, volume_propelente)

            # Calculo da massa dos tanques de combustivel, oxidante e pressurizante
            self.massa_tank_fuel = eq.massa_tank(volume_fuel, Ptank_fuel)
            self.massa_tank_oxi = eq.massa_tank(volume_oxi, Ptank_oxi)
            self.massa_tank_pressurizante = eq.massa_tank(self.volume_pressurizante)

            i += 1
            m_tanks.append(self.massa_tank_fuel + self.massa_tank_oxi + self.massa_tank_pressurizante)
            if (abs(m_tanks[i] - m_tanks[i-1]) <= 0.0001) : break
        
        
        
        # Calculando Tempo de Queima tb
        self.t_burn = (self.isp * self.massa_propelente * g) / F

        self.massa_total = self.massa_motor + self.massa_propelente + self.massa_pressurizante + self.massa_tank_fuel + self.massa_tank_oxi + self.massa_tank_pressurizante
        self.relacao_empuxo_peso_inicial = F/((self.massa_total + mpay) * g)

        self.massa_estrutural = self.massa_motor + self.massa_tank_fuel + self.massa_tank_oxi + self.massa_tank_pressurizante
        self.relacao_empuxo_peso_final = F/((self.massa_estrutural + mpay) * g)

        #Calculando o preço total de reagentes
        self.preco_fuel = volume_fuel * 1000 * precoFuel_litro # passando unidade do volume de m³ para litro
        self.preco_oxi = massa_oxi * precoOxidizer_Kg
        self.preco_pressurizante = self.volume_pressurizante * precoPressurizante_m3
        self.preco_total = (self.preco_fuel + self.preco_oxi + self.preco_pressurizante)

        #! Adicionando Restrições e Punições nas soluções
        if de >= 1500 or self.t_burn >= 250: #or self.massa_total > 780:
            self.isp = 0.80 * self.isp
            self.massa_total = 1.2 * self.massa_total
            
        # else:            
        #     self.massa_total = self.massa_motor + self.massa_propelente + self.massa_pressurizante + self.massa_tank_fuel + self.massa_tank_oxi + self.massa_tank_pressurizante
            
            
        # self.massa_total = self.massa_motor + self.massa_propelente + self.massa_pressurizante + self.massa_tank_fuel + self.massa_tank_oxi + self.massa_tank_pressurizante
        
    
#---------------------------------- Classes do Programa -----------------------------------      
