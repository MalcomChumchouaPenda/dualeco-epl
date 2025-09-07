
import pandas as pd
import numpy as np
import agentpy as ap

from .agents import Household, Firm, Bank
from .agents import CentralBank, Government


class DualEcoModel(ap.Model):
    
    regions = ['a', 'b']
    sectors = [1, 2, 3]
    
    def setup(self):
        p = self.p
        p = self.init_params(p)
        p = self.calc_block_1(p)
        p = self.calc_block_2(p)
        p = self.calc_block_3(p)
        p = self.calc_block_4(p)
        

    def init_params(self):
        # define SFC variables by agent types
        h_vars = ['M_H', 'D_H', 'C', 'W_H', 'Z_H', 'T_H', 
                  'iota_DH', 'pi_dH', 'DeltaM_H', 'DeltaD_H']
        f_vars = ['M_F', 'D_F', 'L_F', 'Q', 'W_F', 'T_F', 'iota_LF', 
                  'iota_DF', 'pi_dF', 'DeltaM_F', 'DeltaL_F', 'DeltaD_F']
        b_vars = ['M_B', 'A_B', 'D_B', 'B_B', 'L_B', 'T_B', 'iota_AB', 
                  'iota_BB', 'iota_LB', 'iota_DB', 'pi_dB', 'DeltaA_B', 
                  'DeltaB_B', 'DeltaM_B', 'DeltaL_B', 'DeltaD_B']
        g_vars = ['M_G', 'B_G', 'W_G', 'Z_G', 'T_G', 'iota_BG', 
                  'pi_G', 'DeltaB_G', 'DeltaM_G']
        cb_vars = ['M_CB', 'A_CB', 'B_CB', 'iota_ACB', 'iota_BCB', 
                   'pi_CB', 'DeltaA_CB', 'DeltaB_CB', 'DeltaM_CB']

        # initialize value of SFC variables
        p = self.p
        for z in self.regions:
            for v in h_vars:
                p[f'{v}{z}'] = 0
        for s in self.sectors:
            for v in f_vars:
                p[f'{v}{s}'] = 0
        for v in b_vars + g_vars + cb_vars:
            p[v] = 0

    
    def calc_block_1(self):
        p = self.p
        p['zeta_1'] = 1 / (1 + p['g_ss'])
        p['zeta_2'] = 1 - p['zeta_1']
        
        for s in self.sectors:
            N = p[f'N_E{s}'] + p[f'N_W{s}']
            p[f'y{s}'] = p[f'phi{s}'] * N
            p[f'W_F{s}'] = p[f'w{s}'] * N
            if N > 0:
                p[f'p{s}'] = (1 + p['m']) * p[f'W_F{s}'] / p[f'y{s}']
                p[f'Q{s}'] = p[f'p{s}'] * p[f'y{s}']
            else:
                p[f'p{s}'] = (1 + p['m']) * p[f'w{s}']
                p[f'Q{s}'] = 0

            
            if s in [1, 3]:
                p[f'L_F{s}'] = 0
                p[f'D_F{s}'] = 0
                p[f'T_F{s}'] = 0
                p[f'pi_F{s}'] = p[f'Q{s}'] - p[f'W_F{s}']
                p[f'pi_dF{s}'] = p['rho'] - p[f'pi_F{s}']
                p[f'M_F{s}'] = (p[f'pi_F{s}'] - p[f'pi_dF{s}'])/ p['zeta_2']
    
            else:
                p['M_F2'] = 0
                p['D_F2'] = p['theta_W'] * p['W_F2']
                A = np.array([
                    [1, 0, 0, p['zeta_1'] * p['r_L']],
                    [p['tau'], -1, 0, 0],
                    [p['rho'], -p['rho'], -1, 0],
                    [1, -1, -1, p['zeta_2']]
                ])
                B = np.array([
                    p['Q2'] + p['zeta_1'] * p['r_D'] * p['D_F2'] - p['W_F2'],
                    0,
                    0,
                    p['zeta_2'] * p['D_F2']
                ])
                X = np.linalg.solve(A, B)
                p['pi_F2'] = X[0]
                p['T_F2'] = X[1]
                p['pi_dF2'] = X[2]
                p['L_F2'] = X[3]
            
            p[f'iota_LF{s}'] = p['zeta_1'] * p['r_L'] * p[f'L_F{s}']
            p[f'iota_DF{s}'] = p['zeta_1'] * p['r_D'] * p[f'D_F{s}']
            p[f'DeltaL_F{s}'] = p['zeta_2'] * p[f'L_F{s}']
            p[f'DeltaD_F{s}'] = p['zeta_2'] * p[f'D_F{s}']
            p[f'DeltaM_F{s}'] = p['zeta_2'] * p[f'M_F{s}'] 

    
    def calc_block_2(self):
        p = self.p
        for z in self.regions:
            if z == 'a':
                p['D_Ha'] = 0
                p['T_Ha'] = 0
                p['Z_Ha'] = 0
                p['W_Ha'] = p['W_F1']
                p['pi_dHa'] = p['pi_dF1']
                p['Ya'] = p['W_Ha'] + p['pi_dHa']
                p['Y_da'] = p['Ya']
                p['Ca'] = (1 - p['alpha_b1']) * p['Q1'] + p['alpha_a2'] * p['Q2']
                p['M_Ha'] = (p['Y_da'] - p['Ca']) / p['zeta_2']
    
            else:
                p['M_Hb'] = 0
                p['Cb'] = p['alpha_b1'] * p['Q1'] + (1 - p['alpha_a2']) * p['Q2'] + p['Q3']
                p['W_G'] = p['w_G'] * p['N_WG']
                p['W_Hb'] = p['W_F2'] + p['W_F3'] + p['W_G']
                p['Z_Hb'] = p['theta_Ubar'] * p['w_min'] * p['N_U']
                p['pi_dB'] = p['rho'] * p['zeta_1'] * p['r_L'] * p['L_F2']
                p['pi_dHb'] = p['pi_dF2'] + p['pi_dF3'] + p['pi_dB']
                A = np.array([
                    [1, 0, 0, -p['zeta_1'] * p['r_D']],
                    [p['tau'], -1, 0, 0],
                    [1, -1, -1, 0],
                    [0, 0, 1, -p['zeta_2']]
                ])
                B = np.array([
                    p['W_Hb'] + p['pi_dHb'] + p['Z_Hb'],
                    p['tau'] * p['Z_Hb'],
                    0,
                    p['Cb']
                ])
                X = np.linalg.solve(A, B)
                p['Yb'] = X[0]
                p['T_Hb'] = X[1]
                p['Y_db'] = X[2]
                p['D_Hb'] = X[3]
                
            p[f'iota_DH{z}'] = p['zeta_1'] * p['r_D'] * p[f'D_H{z}']
            p[f'DeltaD_H{z}'] = p['zeta_2'] * p[f'D_H{z}']
            p[f'DeltaM_H{z}'] = p['zeta_2'] * p[f'M_H{z}'] 

        
    def calc_block_3(self):
        p = self.p
        p['A_B'] = 0
        p['D_B'] = p['D_Hb'] + p['D_F2']
        p['L_B'] = p['L_F2']
        A = np.array([
            [1, 0, 0, -p['zeta_1'] * p['r_B'], 0],
            [p['tau'], -1, 0, 0, 0],
            [p['rho'], -p['rho'], 0, 0, 0],
            [0, 0, 1, -1, -1],
            [1, -1, 0, -p['zeta_2'], -p['zeta_2']]
        ])
        B = np.array([
            p['zeta_1'] * p['r_L'] * p['L_B'] - p['zeta_1'] * p['r_D'] * p['D_B'],
            0,
            p['pi_dB'],
            p['L_B'] - p['D_B'],
            p['pi_dB'] + p['zeta_2'] * p['L_B'] - p['zeta_2'] * p['D_B']
        ])
        X = np.linalg.solve(A, B)
        p['pi_B'] = X[0]
        p['T_B'] = X[1]
        p['E_B'] = X[2]
        p['B_B'] = X[3]
        p['M_B'] = X[4]
        print(p['zeta_2'] * p['M_B'])
        
        p['iota_LB'] = p['zeta_1'] * p['r_L'] * p['L_B']
        p['iota_DB'] = p['zeta_1'] * p['r_D'] * p['D_B']
        p['iota_BB'] = p['zeta_1'] * p['r_B'] * p['B_B']
        p['DeltaB_B'] = p['zeta_2'] * p['B_B']
        p['DeltaL_B'] = p['zeta_2'] * p['L_B'] 
        p['DeltaD_B'] = p['zeta_2'] * p['D_B'] 
        p['DeltaM_B'] = p['zeta_2'] * p['M_B']

    
    def calc_block_4(self):
        p = self.p
        p['Z_G'] = p['Z_Ha'] + p['Z_Hb']
        p['A_CB'] = p['M_G'] = 0
        p['T_G'] = p['T_Hb'] + p['T_F2'] + p['T_B']
        p['M_F'] = p['M_F1'] + p['M_F2'] + p['M_F3']
        p['M_H'] = p['M_Ha'] + p['M_Ha']
        A = np.array([
            [1, -1, 0, 0, 0],
            [0, 0, 1, 0, -1],
            [0, 0, 0, 1, -1],
            [1, 0, 0, p['zeta_2'] - p['zeta_1'] * p['r_B'], 0],
            [0, 1, 0, 0, -p['zeta_1'] * p['r_B']]
        ])
        B = np.array([
            0,
            0,
            p['B_B'],
            p['W_G'] + p['Z_G'] - p['T_G'],
            0
        ])
        X = np.linalg.solve(A, B)
        p['pi_G'] = X[0]
        p['pi_CB'] = X[1]
        p['M_CB'] = X[2]
        p['B_G'] = X[3]
        p['B_CB'] = X[4]
        
        p['iota_BG'] = p['zeta_1'] * p['r_B'] * p['B_G']
        p['iota_BCB'] = p['zeta_1'] * p['r_B'] * p['B_CB']
        p['DeltaB_G'] = p['zeta_2'] * p['B_G']
        p['DeltaB_CB'] = p['zeta_2'] * p['B_CB']
        p['DeltaM_G'] = p['zeta_2'] * p['M_G']
        p['DeltaM_CB'] = p['zeta_2'] * p['M_CB']


    def create_households(self):
        p = self.p
        bankowners = ap.AgentList(self, 1, Household)
        bankowners.s_EB = 1
        bankowners.s_E = 1
        
        firmowners1 = ap.AgentList(self, p['N_E1'], Household)
        firmowners1.s_E = 1
        firmowners1.s = 1
        firmowners1.z = 'a'
        firmowners1.w_D = p['w1']
        
        firmowners2 = ap.AgentList(self, p['N_E2'], Household)
        firmowners2.s_E = 1
        firmowners2.s = 2
        firmowners2.z = 'b'
        firmowners2.w_D = p['w2']
        
        firmowners3 = ap.AgentList(self, p['N_E3'], Household)
        firmowners3.s_E = 1
        firmowners3.s = 3
        firmowners3.z = 'b'
        firmowners3.w_D = p['w3']

        firmowners = firmowners1 + firmowners2 + firmowners3
        owners = bankowners + firmowners
        self.households = owners
        
        privateworkers1 = ap.AgentList(self, p['N_W1'], Household)
        privateworkers1.s = 1
        privateworkers1.s_W = 1
        privateworkers1.z = 'a'
        privateworkers1.w_D = p['w1']
        
        privateworkers2 = ap.AgentList(self, p['N_W2'], Household)
        privateworkers2.s = 2
        privateworkers2.s_W = 1
        privateworkers2.z = 'b'
        privateworkers2.w_D = p['w2']
        
        privateworkers3 = ap.AgentList(self, p['N_W3'], Household)
        privateworkers3.s = 3
        privateworkers3.s_W = 1
        privateworkers3.z = 'b'
        privateworkers3.w_D = p['w3']
        
        publicworkers = ap.AgentList(self, p['N_WG'], Household)
        publicworkers.s_W = 1
        publicworkers.s_WG = 1
        publicworkers.z = 'b'
        publicworkers.w_D = p['w_G']

        privateworkers = privateworkers1 + privateworkers2 + privateworkers3
        workers = publicworkers + privateworkers
        self.households += workers
        
        unemployed = ap.AgentList(self, p['N_U'], Household)
        unemployed.s_U = 1
        unemployed.z = 'b'
        unemployed.w_D = p['w_min']
        self.households += unemployed
    
        households = self.households
        for z in self.regions:
            group = households.select(households.z == z)
            group.M = p[f'M_H{z}'] / len(group)
            group.D = p[f'D_H{z}'] / len(group)

            group.C = p[f'C{z}'] / len(group)
            group.W = p[f'W_H{z}'] / len(group)
            group.Z = p[f'Z_H{z}'] / len(group)
            group.T = p[f'T_H{z}'] / len(group)
            group.iota_D = p[f'iota_DH{z}'] / len(group)
            group.pi_d = p[f'pi_dH{z}'] / len(group)


    def create_firms(self):
        p = self.p
        firms1 = ap.AgentList(self, p['N_E1'], Firm)
        firms1.s = 1
        firms1.z = 'a'

        firms2 = ap.AgentList(self, p['N_E2'], Firm)
        firms2.s = 2
        firms2.z = 'b'
        firms2.r_D = p['r_D']
        firms2.r_L = p['r_L']
        
        firms3 = ap.AgentList(self, p['N_E3'], Firm)
        firms3.s = 3
        firms3.z = 'b'
        self.firms = firms1 + firms2 + firms3

        firms = self.firms
        for s in self.sectors:
            group = firms.select(firms.s == s)
            group.M = p[f'M_F{s}'] / len(group)
            group.D = p[f'D_F{s}'] / len(group)
            group.L = p[f'L_F{s}'] / len(group)

            group.Q = p[f'Q{s}'] / len(group)
            group.W = p[f'W_F{s}'] / len(group)
            group.T = p[f'T_F{s}'] / len(group)
            group.iota_L = p[f'iota_LF{s}'] / len(group)
            group.iota_D = p[f'iota_DF{s}'] / len(group)
            group.pi_d = p[f'pi_dF{s}'] / len(group)

            group.p_y = p[f'p{s}']


    def create_bank(self):
        p = self.p
        bank = Bank(self)
        bank.M = p['M_B']
        bank.D = p['D_B']
        bank.L = p['L_B']
        bank.B = p['B_B']

        bank.T = p['T_B']
        bank.iota_A = p['iota_AB']
        bank.iota_D = p['iota_DB']
        bank.iota_L = p['iota_LB']
        bank.iota_B = p['iota_BB']
        bank.pi_d = p['pi_dB']

        bank.r_D = p['r_D']
        bank.r_L = p['r_L']
        bank.r_A = p['r_A']
        bank.r_B = p['r_B']
        self.bank = bank
    
    def create_public_sector(self):
        p = self.p
        government = Government(self)
        government.M = p['M_G']
        government.B = p['B_G']

        government.W = p['W_G']
        government.Z = p['Z_G']
        government.T = p['T_G']
        government.iota_B = p['iota_BG']
        government.pi = p['pi_G']

        government.w = p['w_G']
        government.r_B = p['r_B']
        self.government = government

        centralbank = CentralBank(self)
        centralbank.M = p['M_CB']
        centralbank.B = p['B_CB']

        centralbank.iota_A = p['iota_ACB']
        centralbank.iota_B = p['iota_BCB']
        centralbank.pi = p['pi_CB']

        centralbank.r_A = p['r_A']
        centralbank.r_B = p['r_B']
        self.centralbank = centralbank

    