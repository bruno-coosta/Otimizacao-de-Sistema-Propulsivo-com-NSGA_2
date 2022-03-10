# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 16:51:48 2020

@author: Bruno Costa
"""
from math import e, pi
import pickle
import warnings

# Arquivo com as principais funcões utilizadas no programa 

#---------------------------------- Entradas do Programa ----------------------------------
deltav = 5300 # m/s - Acréscimo de velocidade
mpay = 100 # kg - massa da payload
Pi = 21 * 10**6 # Pa - Pressão inicial do gás pressurizante (Valor padrão)

model_forest = pickle.load(open('random_forest_mass_2.sav', 'rb')) # Abrindo arquivo com modelo preditivo feito com random forest

#---------------------------------- Entradas do Programa ----------------------------------


def razao_expansao(Pressao_CC, Pressao_saida, Razao_CpCv):
    '''Calculo da razão de expanão do propulsor'''
    P1 = Pressao_CC
    P2 = Pressao_saida
    k = Razao_CpCv
    R_inverso = (((k + 1)/2)**(1/(k - 1))) * ((P2/P1)**(1/k)) * ((((k + 1)/(k - 1)) * (1 - ((P2/P1)**((k - 1)/k))))**(0.5))

    Razao_Expansao = 1/R_inverso
    
    return Razao_Expansao


def empuxo(P1, P2, At, A2, k, P3 = 0):
    F = At * P1 * (((2*(k**2)/(k - 1)) * ((2/(k + 1))**((k + 1)/(k - 1))) * (1 - (P2/P1)**((k - 1)/k))) ** 0.5)+ ((P2 - P3)*A2)   
    return F



#---------------------------------- Equações de Estimativa de Massa ----------------------------------

def engine_mass(Empuxo, Pc_Bar, razao_exp):
    ''' Metodo do Schlingloff para calculo da massa estrutural do motor F[KN] e Pc[bar] '''    
    F_KN = Empuxo/1000 # Passando de [N] para [KN]
    
    #C_prop = 0.11
    #C_tp = 1
    C_tub = 1
    
    m_valv = 0.02*(F_KN*Pc_Bar)**0.71 # Kg - massa da valvula
    m_inj = 0.25 * F_KN**0.85 # Kg - massa do injetor
    m_cc = 0.75 * F_KN**0.85 # Kg - massa da câmara de combustão
    m_ne = razao_exp * F_KN * (0.00225 * C_tub + ((0.225 - 0.075 * C_tub)/Pc_Bar)) # Kg - massa da tubeira
    m_eng_schlingloff = 1.34 * (m_valv + m_inj + m_cc + m_ne) # massa total do motor
    return m_eng_schlingloff

def engine_mass_randomForest(Empuxo, Pc_Bar, razao_exp):

    #* Sisteema de pressurização: Turbo Bomba(0); Pressure Feed(1)

    F_KN = Empuxo/1000

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        #m_eng_randomforest = model_forest.predict([[Sistema_pressurizacao, Pc_Bar, razao_exp, F_KN, Isp]])[0] 
        m_eng_randomforest = model_forest.predict([[Pc_Bar, razao_exp, F_KN]])[0] 
    
    return m_eng_randomforest


def propellant_mass(Isp, deltaV, razao_of, massa_payload, massa_motor, massa_tanks = 0):
    '''Estimativa de massa de propelente'''
    
    g = 9.81
    m_prop = (massa_payload + massa_motor + massa_tanks) * ((e**(deltaV/(Isp * g))) - 1)
    return m_prop


def massa_pressurizante(PressaoMediaTank, VolumePropelente):
    '''Estimativa de massa de pressurizante'''
  
    Ptank_average = PressaoMediaTank
    v_prop = VolumePropelente
    
    MM = 28.0134 # Massa molar do H2 - Pressurizante
    R = 8314 # constante universal dos gases #alteracao feita de 8314 para 8,314
    Ti = 273 # K - Temperatura inicial do Gás pressurizante
    Pi = 20 * 10**6 # Pa - Pressão inicial do gás pressurizante (Valor padrão)
    gamma_pressurizante = 1.407
    
    Tf = Ti * (Ptank_average/Pi)**((gamma_pressurizante - 1)/gamma_pressurizante) 
    v_press = 0
    i = 0
    m_press = []
    m_press.append(0)

    while True:
        i += 1
        m_press.append(1.05 * ((Ptank_average * (v_prop + v_press) * MM)/(R * Tf)))
        if (m_press[i] - m_press[i-1]) <= 0.0001: break
        v_press = (m_press[i] * R * Ti) / (Pi * MM)
        
    return m_press[i], v_press

def massa_tank(volume_substancia, pressao_tank = Pi):
    '''Estimativa de massa dos tanques esfericos'''
    
    fs = 2 # safety factor
    ultimate_yield = 520 * 10**6# MPa - Limite de Escoamento
    rho_tank = 2710 # kg/m^3
   
    r_tank =(0.75 * volume_substancia * (1/pi))**(1/3)
    A_tank = 4 * pi * r_tank**2
    t_tank = fs * ((pressao_tank)/(2 * ultimate_yield))
    m_tank = A_tank * t_tank * rho_tank
    
    
    return m_tank  
#---------------------------------- Equações de Estimativa de Massa ----------------------------------
