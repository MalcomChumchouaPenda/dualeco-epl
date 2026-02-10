import pandas as pd
import numpy as np
import agentpy as ap
from . import agents as ag
from . import environment as env


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
        h_vars = [
            "M_H",
            "D_H",
            "E_H",
            "C",
            "W_H",
            "Z_H",
            "T_H",
            "iota_DH",
            "Pi_dH",
            "DeltaM_H",
            "DeltaD_H",
            "DeltaE_H",
        ]
        f_vars = [
            "M_F",
            "D_F",
            "L_F",
            "E_F",
            "Q",
            "W_F",
            "T_F",
            "iota_LF",
            "iota_DF",
            "Pi_dF",
            "DeltaM_F",
            "DeltaL_F",
            "DeltaD_F",
            "DeltaE_F",
            "L_def_F",
        ]
        b_vars = [
            "M_B",
            "A_B",
            "D_B",
            "B_B",
            "L_B",
            "E_B",
            "T_B",
            "iota_AB",
            "iota_BB",
            "iota_LB",
            "iota_DB",
            "Pi_dB",
            "DeltaA_B",
            "DeltaB_B",
            "DeltaM_B",
            "DeltaL_B",
            "DeltaD_B",
            "DeltaE_B",
            "L_def_B",
        ]
        g_vars = [
            "M_G",
            "B_G",
            "W_G",
            "Z_G",
            "T_G",
            "iota_BG",
            "Pi_G",
            "DeltaB_G",
            "DeltaM_G",
        ]
        cb_vars = [
            "M_CB",
            "A_CB",
            "B_CB",
            "iota_ACB",
            "iota_BCB",
            "Pi_CB",
            "DeltaA_CB",
            "DeltaB_CB",
            "DeltaM_CB",
        ]

        # initialize value of SFC variables
        p = self.p
        for s in self.sectors:
            for v in f_vars:
                p[f"{v}{s}"] = 0
        for v in h_vars + b_vars + g_vars + cb_vars:
            p[v] = 0

    def calc_block_1(self):
        # calculate steady state for firms
        p = self.p
        p["zeta_1"] = 1 / (1 + p["g"])
        p["zeta_2"] = 1 - p["zeta_1"]

        # for each sector of production
        for s in self.sectors:
            N = p[f"N_E{s}"] + p[f"N_W{s}"]
            p[f"y{s}"] = p[f"phi{s}"] * N
            p[f"W_F{s}"] = p[f"w{s}"] * N
            if N > 0:
                p[f"p{s}"] = (1 + p["m"]) * p[f"W_F{s}"] / p[f"y{s}"]
                p[f"Q{s}"] = p[f"p{s}"] * p[f"y{s}"]
            else:
                p[f"p{s}"] = (1 + p["m"]) * p[f"w{s}"]
                p[f"Q{s}"] = 0
            p[f"y_inv{s}"] = p["theta_y"] * p[f"y{s}"]
            p[f"Y_inv{s}"] = p[f"w{s}"] * p[f"y_inv{s}"] / p[f"phi{s}"]

            if s == 1:
                # for modern sector
                p["M_F1"] = 0
                p["D_F1"] = p["theta_W"] * p["W_F1"]
                A = np.array(
                    [
                        [1, 0, 0, p["zeta_1"] * p["r_L"]],
                        [p["tau"], -1, 0, 0],
                        [p["rho"], -p["rho"], -1, 0],
                        [1, -1, -1, p["zeta_2"]],
                    ]
                )
                B = np.array(
                    [
                        p["Q1"] + p["zeta_1"] * p["r_D"] * p["D_F1"] - p["W_F1"],
                        0,
                        0,
                        p["zeta_2"] * p["D_F1"],
                    ]
                )
                X = np.linalg.solve(A, B)
                p["Pi_F1"] = X[0]
                p["T_F1"] = X[1]
                p["Pi_dF1"] = X[2]
                p["L_F1"] = X[3]
                p["E_F1"] = p["D_F1"] - p["L_F1"]

            else:
                # for backward sector
                p["L_F2"] = p["D_F2"] = p["T_F2"] = 0
                p["Pi_F2"] = p["Q2"] - p["W_F2"]
                p["Pi_dF2"] = p["rho"] - p["Pi_F2"]
                p["M_F2"] = (p["Pi_F2"] - p["Pi_dF2"]) / p["zeta_2"]
                p["E_F2"] = p["M_F2"]

            # finalize interest and variation computation
            p[f"iota_LF{s}"] = p["zeta_1"] * p["r_L"] * p[f"L_F{s}"]
            p[f"iota_DF{s}"] = p["zeta_1"] * p["r_D"] * p[f"D_F{s}"]
            p[f"DeltaL_F{s}"] = p["zeta_2"] * p[f"L_F{s}"]
            p[f"DeltaD_F{s}"] = p["zeta_2"] * p[f"D_F{s}"]
            p[f"DeltaM_F{s}"] = p["zeta_2"] * p[f"M_F{s}"]
            p[f"DeltaE_F{s}"] = 0
            p[f"L_def_F{s}"] = 0

    def calc_block_2(self):
        # compute steady state for bank sector
        p = self.p
        p["A_B"] = 0
        p["L_B"] = p["L_F1"]
        A = np.array(
            [
                [0, 0, 0, 0, 0, 0, 1, -1],
                [1, 0, 0, 0, -p["zeta_1"] * p["r_B"], 0, p["zeta_1"] * p["r_D"], 0],
                [p["tau"], -1, 0, 0, 0, 0, 0, 0],
                [p["rho"], -p["rho"], -1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, -1, -1, 1, 0],
                [1, -1, -1, 0, -p["zeta_2"], -p["zeta_2"], p["zeta_2"], 0],
                [0, 0, 0, 1, -p["theta_E"], -p["theta_E"], 0, 0],
                [0, 0, 0, 0, 0, 1, -p["theta_M"], 0],
            ]
        )
        B = np.array(
            [
                p["D_F1"],
                p["zeta_1"] * p["r_L"] * p["L_B"],
                0,
                0,
                p["L_B"],
                p["zeta_2"] * p["L_B"],
                p["theta_E"] * p["L_B"],
                0,
            ]
        )
        X = np.linalg.solve(A, B)
        p["Pi_B"] = X[0]
        p["T_B"] = X[1]
        p["Pi_dB"] = X[2]
        p["E_B"] = X[3]
        p["B_B"] = X[4]
        p["M_B"] = X[5]
        p["D_B"] = X[6]
        p["D_H"] = X[7]

        # finalize interest and variation computation
        p["iota_LB"] = p["zeta_1"] * p["r_L"] * p["L_B"]
        p["iota_DB"] = p["zeta_1"] * p["r_D"] * p["D_B"]
        p["iota_BB"] = p["zeta_1"] * p["r_B"] * p["B_B"]
        p["DeltaB_B"] = p["zeta_2"] * p["B_B"]
        p["DeltaL_B"] = p["zeta_2"] * p["L_B"]
        p["DeltaD_B"] = p["zeta_2"] * p["D_B"]
        p["DeltaM_B"] = p["zeta_2"] * p["M_B"]
        p["DeltaE_B"] = 0
        p["L_def_B"] = 0

    def calc_block_3(self):
        # compute steady state for households
        p = self.p
        p["C1"] = p["Q1"]
        p["C2"] = p["Q2"]
        p["W_G"] = p["w_G"] * p["N_WG"]
        p["W_H"] = p["W_F1"] + p["W_F2"] + p["W_G"]
        p["Z_H"] = p["kappa_Z"] * p["w_G"] * p["N_U"]
        p["Pi_dH"] = p["Pi_dF1"] + p["Pi_dF2"] + p["Pi_dB"]
        p["Y"] = p["W_H"] + p["Pi_dH"] + p["Z_H"] + p["zeta_1"] * p["r_D"] * p["D_H"]
        p["T_H"] = p["tau"] * (p["Y"] - p["Z_H"])
        p["Y_d"] = p["Y"] - p["T_H"]
        p["M_H"] = ((p["Y_d"] - p["C1"] - p["C2"]) / p["zeta_2"]) - p["D_H"]

        # finalize equities, interest and variation computation
        p["E_H"] = p["E_F1"] + p["E_F2"] + p["E_B"]
        p["iota_DH"] = p["zeta_1"] * p["r_D"] * p["D_H"]
        p["DeltaD_H"] = p["zeta_2"] * p["D_H"]
        p["DeltaM_H"] = p["zeta_2"] * p[f"M_H"]

    def calc_block_4(self):
        # compute steady state for public sector
        p = self.p
        p["Z_G"] = p["Z_H"]
        p["A_CB"] = p["M_G"] = 0
        p["T_G"] = p["T_H"] + p["T_F1"] + p["T_B"]
        A = np.array(
            [
                [1, -1, 0, 0, 0],
                [0, 0, 1, 0, -1],
                [0, 0, 0, 1, -1],
                [1, 0, 0, p["zeta_2"] - p["zeta_1"] * p["r_B"], 0],
                [0, 1, 0, 0, -p["zeta_1"] * p["r_B"]],
            ]
        )
        B = np.array([0, 0, p["B_B"], p["W_G"] + p["Z_G"] - p["T_G"], 0])
        X = np.linalg.solve(A, B)
        p["Pi_G"] = X[0]
        p["Pi_CB"] = X[1]
        p["M_CB"] = X[2]
        p["B_G"] = X[3]
        p["B_CB"] = X[4]

        # finalize interest and variation computation
        p["iota_BG"] = p["zeta_1"] * p["r_B"] * p["B_G"]
        p["iota_BCB"] = p["zeta_1"] * p["r_B"] * p["B_CB"]
        p["DeltaB_G"] = p["zeta_2"] * p["B_G"]
        p["DeltaB_CB"] = p["zeta_2"] * p["B_CB"]
        p["DeltaM_G"] = p["zeta_2"] * p["M_G"]
        p["DeltaM_CB"] = p["zeta_2"] * p["M_CB"]

    def create_households(self):
        p = self.p
        bank_owners = ap.AgentList(self, p["N_B"], ag.Household)
        bank_owners.s_EB = 1
        bank_owners.s_E = 1

        firm_owners1 = ap.AgentList(self, p["N_E1"], ag.Household)
        firm_owners1.s_E = 1
        firm_owners1.s_Y = 1

        firm_owners2 = ap.AgentList(self, p["N_E2"], ag.Household)
        firm_owners2.s_E = 1
        firm_owners2.s_Y = 2

        firm_owners = firm_owners1 + firm_owners2
        owners = bank_owners + firm_owners
        self.households = owners

        private_workers1 = ap.AgentList(self, p["N_W1"], ag.Household)
        private_workers1.s_Y = 1
        private_workers1.s_W = 1

        private_workers2 = ap.AgentList(self, p["N_W2"], ag.Household)
        private_workers2.s_Y = 2
        private_workers2.s_W = 1

        public_workers = ap.AgentList(self, p["N_WG"], ag.Household)
        public_workers.s_W = 1
        public_workers.s_WG = 1

        private_workers = private_workers1 + private_workers2
        workers = public_workers + private_workers
        self.households += workers

        unemployed = ap.AgentList(self, p["N_U"], ag.Household)
        unemployed.s_U = 1
        self.households += unemployed
        self.households.delta = p["delta"]

    def create_firms(self):
        p = self.p
        firms1 = ap.AgentList(self, p["N_E1"], ag.Firm)
        firms1.s_Y = 1
        firms1.n_W = 1
        firms1.n_T = 1
        firms1.phi = p["phi1"]

        firms2 = ap.AgentList(self, p["N_E2"], ag.Firm)
        firms2.s_Y = 2
        firms2.n_W = 0
        firms2.n_T = 0
        firms2.phi = p["phi2"]

        self.firms = firms1 + firms2
        self.firms.m = p["m"]
        self.firms.delta = p["delta"]
        self.firms.theta_y = p["theta_y"]
        self.firms.upsilon_F = p["upsilon_F"]

    def create_banks(self):
        p = self.p
        banks = ap.AgentList(self, p["N_B"], ag.Bank)
        banks.delta = p["delta"]
        banks.kappa_E = p["kappa_E"]
        banks.kappa_R = p["kappa_R"]
        banks.gamma_L = p["gamma_L"]
        banks.beta_L = p["beta_L"]
        self.banks = banks

    def create_public_sector(self):
        self.government = ag.Government(self)
        self.central_bank = ag.CentralBank(self)

    def create_good_markets(self):
        firms = self.firms
        markets = {}
        for s in self.sectors:
            sector_firms = firms.select(firms.s_Y == s)
            market = env.GoodMarket(self)
            market.add_suppliers(sector_firms)
            market.s_Y = s
            markets[s] = market
        self.good_markets = markets

    def create_labor_markets(self):
        government = self.government
        households = self.households
        firms = self.firms

        # populate formal labor market
        formal_firms = firms.select(firms.s_Y == 1)
        formal_market = env.LaborMarket(self)
        formal_market.n_W = 1
        formal_market.add_employers([government])
        formal_market.add_employers(formal_firms)
        formal_market.add_workers(households)

        # create formal network for private sector
        j = len(formal_firms)
        private_workers = households.select(households.s_Y == 1)
        for i, worker in enumerate(private_workers):
            employer = formal_firms[i % j]
            employer_pos = formal_market.positions[employer]
            worker_pos = formal_market.positions[worker]
            formal_market.graph.add_edge(employer_pos, worker_pos)

        # create formal network for public sector
        public_workers = households.select(households.s_WG == 1)
        employer_pos = formal_market.positions[government]
        for i, worker in enumerate(public_workers):
            worker_pos = formal_market.positions[worker]
            formal_market.graph.add_edge(employer_pos, worker_pos)

        # populate informal labor market
        informal_firms = firms.select(firms.s_Y == 2)
        informal_market = env.LaborMarket(self)
        informal_market.n_W = 0
        informal_market.add_employers(informal_firms)
        informal_market.add_workers(households)

        # create informal labor network
        j = len(informal_firms)
        private_workers = households.select(households.s_Y == 2)
        for i, worker in enumerate(private_workers):
            employer = informal_firms[i % j]
            employer_pos = informal_market.positions[employer]
            worker_pos = informal_market.positions[worker]
            informal_market.graph.add_edge(employer_pos, worker_pos)
        self.labor_markets = {1: formal_market, 0: informal_market}

    def create_deposit_market(self):
        households = self.households
        banks = self.banks
        firms = self.firms
        formal_firms = firms.select(firms.s_Y == 1)
        market = env.DepositMarket(self)
        market.add_agents(formal_firms)
        market.add_agents(banks)
        market.add_agents(households)

        # create deposit networks
        j = len(banks)
        graph = market.graph
        for i, client in enumerate(formal_firms + households):
            bank = banks[i % j]
            bank_pos = market.positions[bank]
            client_pos = market.positions[client]
            graph.add_edge(client_pos, bank_pos)
            client.bank = bank
        self.deposit_market = market

    def create_credit_market(self):
        banks = self.banks
        firms = self.firms
        formal_firms = firms.select(firms.s_Y == 1)
        market = env.CreditMarket(self)
        market.add_agents(self.banks)
        market.add_agents(formal_firms)

        # create credit networks
        graph = market.graph
        j = len(banks)
        for i, firm in enumerate(formal_firms):
            bank = banks[i % j]
            bank_pos = market.positions[bank]
            firm_pos = market.positions[firm]
            graph.add_edge(firm_pos, bank_pos)
        self.credit_market = market

    def create_bond_market(self):
        market = env.BondMarket(self)
        market.add_agents(self.banks)
        market.add_agents([self.government, self.central_bank])
        self.bond_market = market

    def create_economy(self):
        banks = self.banks
        firms = self.firms
        households = self.households
        economy = env.Economy(self)
        economy.add_agents(firms)
        economy.add_agents(households)
        self.economy = economy

        # create bank ownerships
        owners = households.select(households.s_E == 1)
        bank_owners = owners.select(owners.s_EB == 1)
        for bank, owner in zip(banks, bank_owners):
            bank.owner = owner

        # create firm ownerships
        for s in self.sectors:
            sector_firms = firms.select(firms.s_Y == s)
            sector_owners = owners.select(owners.s_Y == s)
            for firm, owner in zip(sector_firms, sector_owners):
                firm.owner = owner

    def share_initial_equities(self):
        # for firms
        p = self.p
        firms = self.firms
        for s in self.sectors:
            sector_firms = firms.select(firms.s_Y == s)
            E = p[f"E_F{s}"] / len(sector_firms)
            for firm in sector_firms:
                firm.E = E
                firm.owner.E = E

        # for banks
        banks = self.banks
        E = p["E_B"] / len(banks)
        for bank in banks:
            bank.E = E
            bank.owner.E = E

    def share_initial_credits(self):
        # for interest rates
        p = self.p
        banks = self.banks
        banks.r_L = p["r_L"]
        firms = self.firms
        formal_firms = firms.select(firms.s_Y == 1)
        formal_firms.r_L

        # for stocks and flows
        L = p["L_F1"] / len(formal_firms)
        iota_L = p["iota_LF1"] / len(formal_firms)
        for firm in formal_firms:
            firm.r_L = p["r_L"]
            firm.L = L
            firm.iota_L = iota_L
            bank = firm.bank
            bank.L += L
            bank.iota_L += iota_L

    def share_initial_deposits(self):
        # for interest rates
        p = self.p
        banks = self.banks
        banks.r_D = p["r_D"]

        # for households stocks and flows
        households = self.households
        D = p["D_H"] / len(households)
        iota_D = p["iota_DH"] / len(households)
        for household in households:
            household.D = D
            household.iota_D = iota_D
            bank = household.bank
            bank.D += D
            bank.iota_D += iota_D

        # for firms stocks and flows
        firms = self.firms
        formal_firms = firms.select(firms.s_Y == 1)
        D = p["D_F1"] / len(formal_firms)
        iota_D = p["iota_DF1"] / len(formal_firms)
        for firm in formal_firms:
            firm.D = D
            firm.iota_D = iota_D
            bank = firm.bank
            bank.D += D
            bank.iota_D += iota_D

    def share_initial_bonds(self):
        p = self.p
        banks = self.banks
        banks.B = p["B_B"] / len(banks)
        banks.iota_B = p["iota_BB"] / len(banks)

        government = self.government
        government.B = p["B_G"]
        government.iota_B = p["iota_BG"]
        government.r_B = p["r_B"]

        central_bank = self.central_bank
        central_bank.B = p["B_CB"]
        central_bank.iota_B = p["iota_BCB"]

    def share_initial_cash(self):
        # private sector
        p = self.p
        households = self.households
        firms = self.firms
        banks = self.banks
        banks.r_A = p["r_A"]
        banks.M = p["M_B"] / len(banks)
        banks.A = p["A_B"] / len(banks)
        banks.iota_A = p["iota_AB"] / len(banks)
        households.M = p["M_H"] / len(households)
        for s in self.sectors:
            sector_firms = firms.select(firms.s_Y == s)
            sector_firms.M = p[f"M_F{s}"] / len(sector_firms)

        # public sector
        government = self.government
        central_bank = self.central_bank
        central_bank.M = p["M_CB"]
        central_bank.A = p["A_CB"]
        central_bank.iota_A = p["iota_ACB"]
        government.M = p["M_G"]

    def share_initial_production(self):
        p = self.p
        firms = self.firms
        for s in self.sectors:
            sector_firms = firms.select(firms.s_Y == s)
            sector_firms.Y_inv = p[f"Y_inv{s}"] / len(sector_firms)
            sector_firms.y_inv = p[f"y_inv{s}"] / len(sector_firms)
            sector_firms.y = p[f"Q{s}"] / (len(sector_firms) * p[f"p{s}"])
            sector_firms.q_e = p[f"Q{s}"] / (len(sector_firms) * p[f"p{s}"])
            sector_firms.Q = p[f"Q{s}"] / len(sector_firms)
            sector_firms.p_Y = p[f"p{s}"]

    def share_initial_wages(self):
        # for households
        p = self.p
        households = self.households
        public_workers = households.select(households.s_WG == 1)
        public_workers.W = p["W_G"] / len(public_workers)
        public_workers.w = p["w_G"]
        for s in self.sectors:
            private_workers = households.select(households.s_Y == s)
            private_workers.W = p[f"W_F{s}"] / len(private_workers)
            private_workers.w = p[f"w{s}"]
        unemployed = households.select(households.s_U == 1)
        unemployed.w = p["w_min"]

        # for firms
        firms = self.firms
        for s in self.sectors:
            sector_firms = firms.select(firms.s_Y == s)
            sector_firms.W = p[f"W_F{s}"] / len(sector_firms)
            sector_firms.l = p[f"Q{s}"] / (len(sector_firms) * p[f"w{s}"])
            sector_firms.w = p[f"w{s}"]

        # for government
        government = self.government
        government.W = p["W_G"]
        government.w = p["w_G"]

    def share_initial_transfers(self):
        p = self.p
        government = self.government
        households = self.households
        unemployed = households.select(households.s_U == 1)
        unemployed.Z = p["Z_H"] / len(unemployed)
        government.Z = p["Z_G"]

    def share_initial_profits(self):
        households = self.households
        owners = households.select(households.s_E == 1)

        # for firms
        p = self.p
        firms = self.firms
        for s in self.sectors:
            sector_firms = firms.select(firms.s_Y == s)
            sector_owners = owners.select(owners.s_Y == s)
            sector_owners.Pi_d = p[f"Pi_dF{s}"] / len(sector_owners)
            sector_firms.Pi_d = p[f"Pi_dF{s}"] / len(sector_firms)

        # for banks
        banks = self.banks
        bank_owners = owners.select(owners.s_EB == 1)
        bank_owners.Pi_d = p["Pi_dB"] / len(bank_owners)
        banks.Pi_d = p["Pi_dB"] / len(banks)

        # for central bank
        government = self.government
        central_bank = self.central_bank
        central_bank.Pi = p["Pi_CB"]
        government.Pi = p["Pi_G"]

    def share_initial_taxes(self):
        # for households
        p = self.p
        households = self.households
        Y = households.W + households.Pi_d + households.iota_D
        households.T = Y * p["T_H"] / sum(Y)

        # for firms
        firms = self.firms
        for s in self.sectors:
            sector_firms = firms.select(firms.s_Y == s)
            sector_firms.T = p[f"T_F{s}"] / len(sector_firms)

        # for banks and government
        banks = self.banks
        banks.T = p["T_B"] / len(banks)
        self.government.T = p["T_G"]

    def share_initial_consumption(self):
        p = self.p
        households = self.households
        Y = households.W + households.Pi_d + households.iota_D
        Y_d = Y - households.T + households.Z
        households.C1 = Y_d * p["C1"] / sum(Y_d)
        households.C2 = Y_d * p["C2"] / sum(Y_d)

    def share_initial_prices(self):
        pass
