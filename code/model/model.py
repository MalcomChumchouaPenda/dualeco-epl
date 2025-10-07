
import pandas as pd
import numpy as np
import agentpy as ap

from .agents import Household, Firm, Bank
from .agents import CentralBank, Government


class DualEcoModel(ap.Model):
    
    sectors = [1, 2]
    
    def setup(self):
        p = self.p
        p = self.init_params(p)
        p = self.calc_block_1(p)
        p = self.calc_block_2(p)
        p = self.calc_block_3(p)
        p = self.calc_block_4(p)
        

    def init_params(self):
        # define SFC variables by agent types
        h_vars = ['M_H', 'D_H', 'E_H', 'C', 'W_H', 'Z_H', 'T_H', 
                  'iota_DH', 'Pi_dH', 'DeltaM_H', 'DeltaD_H', 'DeltaE_H']
        f_vars = ['M_F', 'D_F', 'L_F', 'E_F', 'Q', 'W_F', 'T_F', 'iota_LF', 
                  'iota_DF', 'Pi_dF', 'DeltaM_F', 'DeltaL_F', 'DeltaD_F',
                  'DeltaE_F', 'L_def_F']
        b_vars = ['M_B', 'A_B', 'D_B', 'B_B', 'L_B', 'E_B', 'T_B', 'iota_AB', 
                  'iota_BB', 'iota_LB', 'iota_DB', 'Pi_dB', 'DeltaA_B', 
                  'DeltaB_B', 'DeltaM_B', 'DeltaL_B', 'DeltaD_B',
                  'DeltaE_B', 'L_def_B']
        g_vars = ['M_G', 'B_G', 'W_G', 'Z_G', 'T_G', 'iota_BG', 
                  'Pi_G', 'DeltaB_G', 'DeltaM_G']
        cb_vars = ['M_CB', 'A_CB', 'B_CB', 'iota_ACB', 'iota_BCB', 
                   'Pi_CB', 'DeltaA_CB', 'DeltaB_CB', 'DeltaM_CB']

        # initialize value of SFC variables
        p = self.p
        for s in self.sectors:
            for v in f_vars:
                p[f'{v}{s}'] = 0
        for v in h_vars + b_vars + g_vars + cb_vars:
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

            if s == 1:
                # for modern sector
                p['M_F1'] = 0
                p['D_F1'] = p['theta_W'] * p['W_F1']
                A = np.array([
                    [1, 0, 0, p['zeta_1'] * p['r_L']],
                    [p['tau'], -1, 0, 0],
                    [p['rho'], -p['rho'], -1, 0],
                    [1, -1, -1, p['zeta_2']]
                ])
                B = np.array([
                    p['Q1'] + p['zeta_1'] * p['r_D'] * p['D_F1'] - p['W_F1'],
                    0,
                    0,
                    p['zeta_2'] * p['D_F1']
                ])
                X = np.linalg.solve(A, B)
                p['Pi_F1'] = X[0]
                p['T_F1'] = X[1]
                p['Pi_dF1'] = X[2]
                p['L_F1'] = X[3]
                p['E_F1'] = p['D_F1'] - p['L_F1']
    
            else:
                # for backward sector
                p['L_F2'] = p['D_F2'] = p['T_F2'] = 0
                p['Pi_F2'] = p['Q2'] - p['W_F2']
                p['Pi_dF2'] = p['rho'] - p['Pi_F2']
                p['M_F2'] = (p['Pi_F2'] - p['Pi_dF2'])/ p['zeta_2']
                p['E_F2'] = p['M_F2']
            
            # finalize interest and variation computation
            p[f'iota_LF{s}'] = p['zeta_1'] * p['r_L'] * p[f'L_F{s}']
            p[f'iota_DF{s}'] = p['zeta_1'] * p['r_D'] * p[f'D_F{s}']
            p[f'DeltaL_F{s}'] = p['zeta_2'] * p[f'L_F{s}']
            p[f'DeltaD_F{s}'] = p['zeta_2'] * p[f'D_F{s}']
            p[f'DeltaM_F{s}'] = p['zeta_2'] * p[f'M_F{s}'] 
            p[f'DeltaE_F{s}'] = 0 
            p[f'L_def_F{s}'] = 0


    def calc_block_2(self):
        # compute steady state for bank sector
        p = self.p
        p['A_B'] = 0
        p['L_B'] = p['L_F1']
        A = np.array([
            [0, 0, 0, 0, 0, 0, 1, -1],
            [1, 0, 0, 0, -p['zeta_1'] * p['r_B'], 0, p['zeta_1'] * p['r_D'], 0],
            [p['tau'], -1, 0, 0, 0, 0, 0, 0],
            [p['rho'], -p['rho'], -1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, -1, -1, 1, 0],
            [1, -1, -1, 0, -p['zeta_2'], -p['zeta_2'], p['zeta_2'], 0],
            [0, 0, 0, 1, -p['theta_E'], -p['theta_E'], 0, 0],
            [0, 0, 0, 0, 0, 1, -p['theta_M'], 0]
        ])
        B = np.array([
            p['D_F1'],
            p['zeta_1'] * p['r_L'] * p['L_B'],
            0,
            0,
            p['L_B'],
            p['zeta_2'] * p['L_B'],
            p['theta_E'] * p['L_B'],
            0
        ])
        X = np.linalg.solve(A, B)
        p['Pi_B'] = X[0]
        p['T_B'] = X[1]
        p['Pi_dB'] = X[2]
        p['E_B'] = X[3]
        p['B_B'] = X[4]
        p['M_B'] = X[5]
        p['D_B'] = X[6]
        p['D_H'] = X[7]
        print(p['zeta_2'] * p['M_B'])
        
        # finalize interest and variation computation
        p['iota_LB'] = p['zeta_1'] * p['r_L'] * p['L_B']
        p['iota_DB'] = p['zeta_1'] * p['r_D'] * p['D_B']
        p['iota_BB'] = p['zeta_1'] * p['r_B'] * p['B_B']
        p['DeltaB_B'] = p['zeta_2'] * p['B_B']
        p['DeltaL_B'] = p['zeta_2'] * p['L_B'] 
        p['DeltaD_B'] = p['zeta_2'] * p['D_B'] 
        p['DeltaM_B'] = p['zeta_2'] * p['M_B']
        p['DeltaE_B'] = 0 
        p['L_def_B'] = 0

    
    def calc_block_3(self):
        # compute steady state for households
        p = self.p
        p['C1'] = p['Q1'] 
        p['C2'] = p['Q2']
        p['W_G'] = p['w_G'] * p['N_WG']
        p['W_H'] = p['W_F1'] + p['W_F2'] + p['W_G']
        p['Z_H'] = p['theta_Zbar'] * p['w_G'] * p['N_U']
        p['Pi_dH'] = p['Pi_dF1'] + p['Pi_dF2'] + p['Pi_dB']
        p['Y'] = p['W_H'] + p['Pi_dH'] + p['Z_H'] + p['zeta_1'] * p['r_D'] * p['D_H']
        p['T_H'] = p['tau'] * (p['Y'] - p['Z_H'])
        p['Y_d'] = p['Y'] - p['T_H']                
        p['M_H'] = ((p['Y_d'] - p['C1']- p['C2']) / p['zeta_2']) - p['D_H']
                
         # finalize interest and variation computation
        p['iota_DH'] = p['zeta_1'] * p['r_D'] * p['D_H']
        p['DeltaD_H'] = p['zeta_2'] * p['D_H']
        p['DeltaM_H'] = p['zeta_2'] * p[f'M_H'] 

    
    def calc_block_4(self):
        # compute steady state for public sector
        p = self.p
        p['Z_G'] = p['Z_H']
        p['A_CB'] = p['M_G'] = 0
        p['T_G'] = p['T_H'] + p['T_F1'] + p['T_B']
        p['M_F'] = p['M_F1'] + p['M_F2']
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
        p['Pi_G'] = X[0]
        p['Pi_CB'] = X[1]
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
        bank_owners = ap.AgentList(self, p['N_B'], Household)
        bank_owners.s_EB = 1
        bank_owners.s_E = 1
        
        firm_owners1 = ap.AgentList(self, p['N_E1'], Household)
        firm_owners1.s_E = 1
        firm_owners1.s_Y = 1
        firm_owners1.w_D = p['w1']
        
        firm_owners2 = ap.AgentList(self, p['N_E2'], Household)
        firm_owners2.s_E = 1
        firm_owners2.s_Y = 2
        firm_owners2.w_D = p['w2']

        firm_owners = firm_owners1 + firm_owners2
        owners = bank_owners + firm_owners
        self.households = owners
        
        private_workers1 = ap.AgentList(self, p['N_W1'], Household)
        private_workers1.s_Y = 1
        private_workers1.s_W = 1
        private_workers1.w_D = p['w1']
        
        private_workers2 = ap.AgentList(self, p['N_W2'], Household)
        private_workers2.s_Y = 2
        private_workers2.s_W = 1
        private_workers2.w_D = p['w2']
        
        public_workers = ap.AgentList(self, p['N_WG'], Household)
        public_workers.s_W = 1
        public_workers.s_WG = 1
        public_workers.w_D = p['w_G']

        private_workers = private_workers1 + private_workers2
        workers = public_workers + private_workers
        self.households += workers
        
        unemployed = ap.AgentList(self, p['N_U'], Household)
        unemployed.s_U = 1
        unemployed.w_D = p['w_min']
        self.households += unemployed
    
        # share stocks, flows and prices
        households = self.households
        households.M = p['M_H'] / len(households)
        households.D = p['D_H'] / len(households)
        households.C1 = p['C1'] / len(households)
        households.C2 = p['C2'] / len(households)
        households.W = p['W_H'] / len(households)
        households.Z = p['Z_H'] / len(households)
        households.T = p['T_H'] / len(households)
        households.iota_D = p['iota_DH'] / len(households)
        households.Pi_d = p['Pi_dH'] / len(households)
        households.r_D = p['r_D']


    def create_firms(self):
        p = self.p
        firms1 = ap.AgentList(self, p['N_E1'], Firm)
        firms1.s_Y = 1
        firms1.r_D = p['r_D']
        firms1.r_L = p['r_L']

        firms2 = ap.AgentList(self, p['N_E2'], Firm)
        firms2.s_Y = 2
        self.firms = firms1 + firms2

        # share stocks, flows and prices
        households = self.households
        owners = households.select(households.s_E == 1)
        firms = self.firms
        for s in self.sectors:
            formal = 1 if s == 1 else 0
            group = firms.select(firms.s_Y == s)
            group.n_W = formal
            group.n_T = formal
            
            # share prices
            group.p_y = p[f'p{s}']
            group.w = p[f'w{s}']
            if formal:
                group.r_L = p['r_L']
            
            # share nbehavior parameters
            group.delta = p['delta']
            group.theta_y = p['theta_y']
            group.upsilon = p['upsilon_F']
            group.phi = p[f'phi{s}']

            # share nominal stocks
            group.M = p[f'M_F{s}'] / len(group)
            group.D = p[f'D_F{s}'] / len(group)
            group.L = p[f'L_F{s}'] / len(group)

            # share nominal flows
            group.Q = p[f'Q{s}'] / len(group)
            group.W = p[f'W_F{s}'] / len(group)
            group.T = p[f'T_F{s}'] / len(group)
            group.iota_L = p[f'iota_LF{s}'] / len(group)
            group.iota_D = p[f'iota_DF{s}'] / len(group)
            group.Pi_d = p[f'Pi_dF{s}'] / len(group)

            # share real stocks and flows
            group.y = p[f'Q{s}'] / (len(group) * p[f'p{s}'])
            group.l = p[f'Q{s}'] / (len(group) * p[f'w{s}'])

            group_owners = owners.select(owners.s_Y == s)
            for firm, owner in zip(group, group_owners):
                firm.owner = owner
                firm.E = p[f'E_F{s}'] / len(group)
                owner.E = p[f'E_F{s}'] / len(group_owners)


    def create_banks(self):
        p = self.p
        banks = ap.AgentList(self, p['N_B'], Bank)
        households = self.households
        owners = households.select(households.s_EB == 1)
        for bank, owner in zip(banks, owners):
            bank.owner =  owner
            bank.E = p['E_B'] / len(banks)
            owner.E = p['E_B'] / len(banks)

        banks.M = p['M_B'] / len(banks)
        banks.B = p['B_B'] / len(banks)

        banks.T = p['T_B'] / len(banks)
        banks.iota_A = p['iota_AB'] / len(banks)
        banks.iota_B = p['iota_BB'] / len(banks)
        banks.Pi_d = p['Pi_dB'] / len(banks)

        banks.r_D = p['r_D']
        banks.r_L = p['r_L']
        banks.r_A = p['r_A']
        banks.r_B = p['r_B']
        self.banks = banks
    

    def create_public_sector(self):
        p = self.p
        government = Government(self)
        government.M = p['M_G']
        government.B = p['B_G']

        government.W = p['W_G']
        government.Z = p['Z_G']
        government.T = p['T_G']
        government.iota_B = p['iota_BG']
        government.Pi = p['Pi_G']

        government.w = p['w_G']
        government.r_B = p['r_B']
        self.government = government

        central_bank = CentralBank(self)
        central_bank.M = p['M_CB']
        central_bank.B = p['B_CB']

        central_bank.iota_A = p['iota_ACB']
        central_bank.iota_B = p['iota_BCB']
        central_bank.Pi = p['Pi_CB']

        central_bank.r_A = p['r_A']
        central_bank.r_B = p['r_B']
        self.central_bank = central_bank


    def create_labor_markets(self):
        government = self.government
        households = self.households
        firms = self.firms

        # populate formal urban labor market        
        formal_firms = firms.select(firms.s_Y==1)
        formal_market = ap.Network(self)
        formal_market.add_agents([government])
        formal_market.add_agents(formal_firms)
        formal_market.add_agents(households)

        # create formal labor network for private sector
        j = len(formal_firms)
        private_workers = households.select(households.s_Y==1)
        for i, worker in enumerate(private_workers):
            employer = formal_firms[i % j]
            employer_pos = formal_market.positions[employer]
            worker_pos = formal_market.positions[worker]
            formal_market.graph.add_edge(employer_pos, worker_pos)
        
        # create formal labor network for public sector
        public_workers = households.select(households.s_WG==1)
        employer_pos = formal_market.positions[government]
        for i, worker in enumerate(public_workers):
            worker_pos = formal_market.positions[worker]
            formal_market.graph.add_edge(employer_pos, worker_pos)

        # populate informal urban labor market
        informal_firms = firms.select(firms.s_Y==2)
        informal_market = ap.Network(self)
        informal_market.add_agents(informal_firms)
        informal_market.add_agents(households)

        # create informal urban labor network
        j = len(informal_firms)
        private_workers = households.select(households.s_Y==2)
        for i, worker in enumerate(private_workers):
            employer = informal_firms[i % j]
            employer_pos = informal_market.positions[employer]
            worker_pos = informal_market.positions[worker]
            informal_market.graph.add_edge(employer_pos, worker_pos)
        self.labor_markets = {1:formal_market, 2:informal_market}
        

    def create_deposit_market(self):
        banks = self.banks
        firms = self.firms
        households = self.households
        formal_firms = firms.select(firms.s_Y==1)

        # populate deposit market
        market = ap.Network(self)
        market.add_agents(banks)
        market.add_agents(formal_firms)
        market.add_agents(households)
        self.deposit_market = market

        # create deposit networks
        j = len(banks)
        graph = market.graph
        for i, client in enumerate(formal_firms + households):
            bank = banks[i % j]
            bank.D += client.D
            bank.iota_D += client.iota_D
            bank_pos = market.positions[bank]
            client_pos = market.positions[client]
            graph.add_edge(client_pos, bank_pos)


    def create_credit_market(self):
        banks = self.banks
        firms = self.firms
        formal_firms = firms.select(firms.s_Y==1)

        # populate credit market
        market = ap.Network(self)
        market.add_agents(banks)
        market.add_agents(formal_firms)
        self.credit_market = market

        # create credit networks
        j = len(banks)
        graph = market.graph
        for i, firm in enumerate(formal_firms):
            bank = banks[i % j]
            bank.L  += firm.L
            bank.iota_L += firm.iota_L
            bank_pos = market.positions[bank]
            firm_pos = market.positions[firm]
            graph.add_edge(firm_pos, bank_pos)


    def create_economy(self):
        firms = self.firms
        households = self.households
        economy = ap.Space(self, (0, 1))
        economy.add_agents(firms)
        economy.add_agents(households)
        self.economy = economy

