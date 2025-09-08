
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
        # calculate steady state for firms
        p = self.p
        p['zeta_1'] = 1 / (1 + p['g_ss'])
        p['zeta_2'] = 1 - p['zeta_1']
        
        # for each sector of production
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
                # for unbanked sectors
                p[f'L_F{s}'] = 0
                p[f'D_F{s}'] = 0
                p[f'T_F{s}'] = 0
                p[f'pi_F{s}'] = p[f'Q{s}'] - p[f'W_F{s}']
                p[f'pi_dF{s}'] = p['rho'] - p[f'pi_F{s}']
                p[f'M_F{s}'] = (p[f'pi_F{s}'] - p[f'pi_dF{s}'])/ p['zeta_2']
    
            else:
                # for banked sectors
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
            
            # finalize interest and variation computation
            p[f'iota_LF{s}'] = p['zeta_1'] * p['r_L'] * p[f'L_F{s}']
            p[f'iota_DF{s}'] = p['zeta_1'] * p['r_D'] * p[f'D_F{s}']
            p[f'DeltaL_F{s}'] = p['zeta_2'] * p[f'L_F{s}']
            p[f'DeltaD_F{s}'] = p['zeta_2'] * p[f'D_F{s}']
            p[f'DeltaM_F{s}'] = p['zeta_2'] * p[f'M_F{s}'] 

    
    def calc_block_2(self):
        # compute steady state for households
        p = self.p

        # for each region
        for z in self.regions:
            if z == 'a':
                # for rural households
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
                # for urban households
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
                
            # finalize interest and variation computation
            p[f'iota_DH{z}'] = p['zeta_1'] * p['r_D'] * p[f'D_H{z}']
            p[f'DeltaD_H{z}'] = p['zeta_2'] * p[f'D_H{z}']
            p[f'DeltaM_H{z}'] = p['zeta_2'] * p[f'M_H{z}'] 

        
    def calc_block_3(self):
        # compute steady state for bank sector
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
        
        # finalize interest and variation computation
        p['iota_LB'] = p['zeta_1'] * p['r_L'] * p['L_B']
        p['iota_DB'] = p['zeta_1'] * p['r_D'] * p['D_B']
        p['iota_BB'] = p['zeta_1'] * p['r_B'] * p['B_B']
        p['DeltaB_B'] = p['zeta_2'] * p['B_B']
        p['DeltaL_B'] = p['zeta_2'] * p['L_B'] 
        p['DeltaD_B'] = p['zeta_2'] * p['D_B'] 
        p['DeltaM_B'] = p['zeta_2'] * p['M_B']

    
    def calc_block_4(self):
        # compute steady state for public sector
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
        
        # finalize interest and variation computation
        p['iota_BG'] = p['zeta_1'] * p['r_B'] * p['B_G']
        p['iota_BCB'] = p['zeta_1'] * p['r_B'] * p['B_CB']
        p['DeltaB_G'] = p['zeta_2'] * p['B_G']
        p['DeltaB_CB'] = p['zeta_2'] * p['B_CB']
        p['DeltaM_G'] = p['zeta_2'] * p['M_G']
        p['DeltaM_CB'] = p['zeta_2'] * p['M_CB']


    def create_households(self):
        p = self.p
        bank_owners = ap.AgentList(self, 1, Household)
        bank_owners.s_EB = 1
        bank_owners.s_E = 1
        
        firm_owners1 = ap.AgentList(self, p['N_E1'], Household)
        firm_owners1.s_E = 1
        firm_owners1.s = 1
        firm_owners1.z = 'a'
        firm_owners1.w_D = p['w1']
        
        firm_owners2 = ap.AgentList(self, p['N_E2'], Household)
        firm_owners2.s_E = 1
        firm_owners2.s = 2
        firm_owners2.z = 'b'
        firm_owners2.w_D = p['w2']
        
        firm_owners3 = ap.AgentList(self, p['N_E3'], Household)
        firm_owners3.s_E = 1
        firm_owners3.s = 3
        firm_owners3.z = 'b'
        firm_owners3.w_D = p['w3']

        firm_owners = firm_owners1 + firm_owners2 + firm_owners3
        owners = bank_owners + firm_owners
        self.households = owners
        
        private_workers1 = ap.AgentList(self, p['N_W1'], Household)
        private_workers1.s = 1
        private_workers1.s_W = 1
        private_workers1.z = 'a'
        private_workers1.w_D = p['w1']
        
        private_workers2 = ap.AgentList(self, p['N_W2'], Household)
        private_workers2.s = 2
        private_workers2.s_W = 1
        private_workers2.z = 'b'
        private_workers2.w_D = p['w2']
        
        private_workers3 = ap.AgentList(self, p['N_W3'], Household)
        private_workers3.s = 3
        private_workers3.s_W = 1
        private_workers3.z = 'b'
        private_workers3.w_D = p['w3']
        
        public_workers = ap.AgentList(self, p['N_WG'], Household)
        public_workers.s_W = 1
        public_workers.s_WG = 1
        public_workers.z = 'b'
        public_workers.w_D = p['w_G']

        private_workers = private_workers1 + private_workers2 + private_workers3
        workers = public_workers + private_workers
        self.households += workers
        
        unemployed = ap.AgentList(self, p['N_U'], Household)
        unemployed.s_U = 1
        unemployed.z = 'b'
        unemployed.w_D = p['w_min']
        self.households += unemployed
    
        # share stocks, flows and prices
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

        # share stocks, flows and prices
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

        central_bank = CentralBank(self)
        central_bank.M = p['M_CB']
        central_bank.B = p['B_CB']

        central_bank.iota_A = p['iota_ACB']
        central_bank.iota_B = p['iota_BCB']
        central_bank.pi = p['pi_CB']

        central_bank.r_A = p['r_A']
        central_bank.r_B = p['r_B']
        self.central_bank = central_bank


    def create_labor_markets(self):
        government = self.government
        households = self.households
        firms = self.firms

        # populate rural labor markets
        rural_households = households.select(households.z=='a')
        rural_firms = firms.select(firms.s==1)
        rural_market = ap.Network(self)
        rural_market.add_agents(rural_firms)
        rural_market.add_agents(rural_households)

        # create rural labor network
        j = len(rural_firms)
        rural_workers = rural_households.select(rural_households.s==1)
        for i, worker in enumerate(rural_workers):
            employer = rural_firms[i % j]
            employer_pos = rural_market.positions[employer]
            worker_pos = rural_market.positions[worker]
            rural_market.graph.add_edge(employer_pos, worker_pos)

        # populate formal urban labor market        
        urban_households = households.select(households.z=='b')
        formal_firms = firms.select(firms.s==2)
        formal_market = ap.Network(self)
        formal_market.add_agents([government])
        formal_market.add_agents(formal_firms)
        formal_market.add_agents(urban_households)

        # create formal labor network for private urban sector
        j = len(formal_firms)
        private_workers = urban_households.select(urban_households.s==2)
        for i, worker in enumerate(private_workers):
            employer = formal_firms[i % j]
            employer_pos = formal_market.positions[employer]
            worker_pos = formal_market.positions[worker]
            formal_market.graph.add_edge(employer_pos, worker_pos)
        
        # create formal labor network for public sector
        public_workers = urban_households.select(urban_households.s_WG==1)
        employer_pos = formal_market.positions[government]
        for i, worker in enumerate(public_workers):
            worker_pos = formal_market.positions[worker]
            formal_market.graph.add_edge(employer_pos, worker_pos)

        # populate informal urban labor market
        informal_firms = firms.select(firms.s==3)
        informal_market = ap.Network(self)
        informal_market.add_agents(informal_firms)
        informal_market.add_agents(urban_households)

        # create informal urban labor network
        j = len(informal_firms)
        private_workers = urban_households.select(urban_households.s==3)
        for i, worker in enumerate(private_workers):
            employer = informal_firms[i % j]
            employer_pos = informal_market.positions[employer]
            worker_pos = informal_market.positions[worker]
            informal_market.graph.add_edge(employer_pos, worker_pos)

        self.labor_markets = {1:rural_market,
                              2:formal_market,
                              3:informal_market}
        
    def create_deposit_market(self):
        bank = self.bank
        firms = self.firms
        households = self.households
        formal_firms = firms.select(firms.s==2)
        urban_households = households.select(households.z=='b')

        # populate deposit market
        market = ap.Network(self)
        market.add_agents([bank])
        market.add_agents(formal_firms)
        market.add_agents(urban_households)
        self.deposit_market = market

        # create firm deposit networks
        bank_pos = market.positions[bank]
        graph = market.graph
        for firm in formal_firms:
            firm_pos = market.positions[firm]
            graph.add_edge(firm_pos, bank_pos)

        # create household deposit networks
        bank_pos = market.positions[bank]
        graph = market.graph
        for household in urban_households:
            household_pos = market.positions[household]
            graph.add_edge(household_pos, bank_pos)


    def create_credit_market(self):
        bank = self.bank
        firms = self.firms
        formal_firms = firms.select(firms.s==2)

        # populate credit market
        market = ap.Network(self)
        market.add_agents([bank])
        market.add_agents(formal_firms)
        self.credit_market = market

        # create credit networks
        bank_pos = market.positions[bank]
        graph = market.graph
        for firm in formal_firms:
            firm_pos = market.positions[firm]
            graph.add_edge(firm_pos, bank_pos)


    def create_region_spaces(self):
        firms = self.firms
        households = self.households

        # create and populate rural area
        rural_households = households.select(households.z=='a')
        rural_firms = firms.select(firms.z=='a')
        rural_space = ap.Space(self, (0, 1))
        rural_space.add_agents(rural_firms)
        rural_space.add_agents(rural_households)

        # create and populate urban area
        urban_households = households.select(households.z=='b')
        urban_firms = firms.select(firms.z=='b')
        urban_space = ap.Space(self, (0, 1))
        urban_space.add_agents(urban_firms)
        urban_space.add_agents(urban_households)
        self.region_spaces = {'a': rural_space,
                              'b': urban_space}

