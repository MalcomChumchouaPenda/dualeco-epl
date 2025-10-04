
import numpy as np
import agentpy as ap


class Household(ap.Agent):
    
    def setup(self):
        self.z = ''         # region of household
        self.s = 0          # employment sector of household
        self.s_E = 0        # entrepreneur indicator variable
        self.s_EB = 0       # bank owner indicator variable
        self.s_W = 0        # employee indicator variable
        self.s_WG = 0       # public employee indicator variable
        self.s_U = 0        # unemployed indicator variable

        self.M = 0          # cash money
        self.D = 0          # deposits
        self.E = 0          # equities

        self.C = 0          # consumption
        self.W = 0          # wages
        self.Z = 0          # public transfers
        self.T = 0          # taxes
        self.iota_D = 0     # reimbursement of deposit interests
        self.pi_d = 0       # dividends

        self.w_D = 0        # reservation wage
        self.r_D = 0        # deposit interest rate

        self.bank = None


    def withdraw_deposits(self, amount):
        self.M += amount
        self.D -= amount
        self.bank.M -= amount
        self.bank.D -= amount



class Firm(ap.Agent):
    
    def setup(self):
        self.s = 0          # firm's sector
        self.z = ''         # firm's region

        self.M = 0          # cash money
        self.D = 0          # deposits
        self.L = 0          # loans
        self.E = 0          # equities

        self.Q = 0          # sales
        self.W = 0          # wages
        self.T = 0          # taxes
        self.iota_D = 0     # reimbursement of deposit interests
        self.iota_L = 0     # reimbursement of loan interests
        self.pi_d = 0       # dividends

        self.p_y = 0        # production price
        self.r_D = 0        # deposit interest rate
        self.r_L = 0        # loan interest rate

        self.bank = None
        self.owner = None


    def withdraw_deposits(self, amount):
        self.M += amount
        self.D -= amount
        self.bank.M -= amount
        self.bank.D -= amount



class Bank(ap.Agent):
    
    def setup(self):
        self.M = 0          # cash money
        self.A = 0          # cash advances
        self.D = 0          # deposits
        self.B = 0          # bonds
        self.L = 0          # loans
        self.E = 0          # equities

        self.T = 0          # taxes
        self.iota_A = 0     # reimbursement of advance interest
        self.iota_D = 0     # reimbursement of deposit interest
        self.iota_B = 0     # reimbursement of bonds interest
        self.iota_L = 0     # reimbursement of loans interest
        self.pi_d = 0       # dividends

        self.r_D = 0        # deposit interest rate
        self.r_A = 0        # advance interest rate
        self.r_B = 0        # bonds interest rate
        self.r_L = 0        # loans interest rate

        self.owner = None
        

    def pay_deposit_interests(self):
        deposit_market = self.model.deposit_market
        clients = deposit_market.neighbors(self)
        for client in clients:
            iota = client.D * self.r_D
            deposit_market.pay_interests(iota, self, client)
    

    def grant_loans(self):
        random = self.model.nprandom
        L_max = self.theta_Ebar * self.V
        credit_market =  self.model.credit_market
        firms = credit_market.neighbors(self)
        for firm in firms:
            print(firm.L_D, L_max)
            if 0 < firm.L_D <= L_max:
                Pr = np.exp(-self.gamma_L * firm.L_D / firm.V)
                choice = random.choice([0, 1], p=[1-Pr, Pr])
                print('choice', choice, Pr)
                if choice:
                    firm.r_L = self.r_L + (self.beta_L * firm.L_D / firm.V)
                    print(firm.r_L)
                    credit_market.give_loans(firm.L_D, self, firm)
                    L_max -= firm.L_D


    def ask_advances(self):
        A = self.theta_Rbar * self.D - self.R
        if A > 0:
            central_bank = self.model.central_bank
            country = self.model.country
            country.give_advances(A, central_bank, self)
            

    def buy_bonds(self):
        B = self.R - self.theta_Rbar * self.D
        if B > 0:
            government = self.model.government
            B = min(government.B_S, B)        
            bond_market = self.model.bond_market
            bond_market.buy_bonds(B, self, government)
        


class Government(ap.Agent):
    
    def setup(self):
        self.M = 0          # reserves
        self.B = 0          # bonds

        self.W = 0          # wages
        self.Z = 0          # public transfers
        self.T = 0          # taxes
        self.iota_B = 0     # reimbursement of bond interests
        self.pi = 0         # profits

        self.w = 0          # wage
        self.r_B = 0        # bond interest rate


class CentralBank(ap.Agent):
    
    def setup(self):
        self.M = 0          # reserves
        self.A = 0          # cash advances
        self.B = 0          # bonds

        self.iota_A = 0     # reimbursement of advance interests
        self.iota_B = 0     # reimbursement of bond interests
        self.pi = 0         # profit

        self.r_A = 0        # advance interest rate
        self.r_B = 0        # bond interest rate

