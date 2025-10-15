
import numpy as np
import agentpy as ap


class Household(ap.Agent):
    
    def setup(self):
        self.s_U = 0        # unemployed indicator variable
        self.s_W = 0        # employee indicator variable
        self.s_WG = 0       # public employee indicator variable
        self.s_E = 0        # entrepreneur indicator variable
        self.s_EB = 0       # bank owner indicator variable
        self.s_Y = 0        # employment sector of household
        self.n_W = 0        # degree of formality of employment
        self.l = 0          # labor employed
        self.l_S = 1        # labor supply

        self.M = 0          # cash money
        self.D = 0          # deposits
        self.D_D = 0     # deposits desired
        self.E = 0          # equities
        self.E_D = 0     # equities desired
        self.V = 0          # net worth

        self.C_D = 0     # consumption desired
        self.C1 = 0         # consumption of goods 1
        self.C2 = 0         # consumption of goods 2
        self.W = 0          # wages
        self.w_D = 0        # reservation wage
        self.Z = 0          # public transfers
        self.T = 0          # taxes
        self.iota_D = 0     # reimbursement of deposit interests
        self.Pi_d = 0       # dividends

        self.r_D = 0        # deposit interest rate
        self.delta = 0      # adjustment
        self.upsilon = 0    # ...
        self.bank = None


    def search_job(self):
        # reservation wage revision
        labor_market = self.model.labor_market
        random = self.model.nprandom
        U = random.uniform
        Pr = self.upsilon * np.exp(-labor_market.upsilon * labor_market.u)
        if self.s_U == 0:
            print([0, 1], [1-Pr, Pr])
            if random.choice([0, 1], p=[1-Pr, Pr]):
                self.w_D = self.w_D * (1 + U(0, self.delta))
        else:
            if random.choice([0, 1], p=[Pr, 1-Pr]):
                self.w_D = self.w_D * (1 - U(0, self.delta))


class Firm(ap.Agent):
    
    def setup(self):
        self.s_Y = 0        # firm's sector
        self.n_W = 0        # degree of formality on labor market
        self.n_T = 0        # degree of formality on credit market
        
        self.p_Y = 0        # production price
        self.r_L = 0        # loan interest rate
        self.w = 0          # wage offered
        self.m = 0          # price markup

        self.N_Jc = 0       # number of job created
        self.N_Jd = 0       # number of job destroyed
        self.l = 0          # labour employed
        self.l_D = 0        # labour demand
        self.y_D = 0        # desired level of production
        self.y_inv = 0      # real inventories
        self.y = 0          # production
        self.q_e = 0        # sales expectation

        self.Y_inv = 0      # nominal inventories
        self.M = 0          # cash money
        self.D = 0          # deposits
        self.L = 0          # loans
        self.L_D = 0        # credit demand
        self.L_def = 0      # loan defaults
        self.E = 0          # equities
        self.V = 0          # net worth
        self.Q = 0          # sales
        self.W = 0          # wages
        self.T = 0          # taxes
        self.iota_D = 0     # reimbursement of deposit interests
        self.iota_L = 0     # reimbursement of loan interests
        self.Pi = 0         # profit
        self.Pi_d = 0       # dividends

        self.phi = 0        # productivity
        self.delta = 0  # max adjustment parameters
        self.theta_y = 0    # desired maximum proportion of inventories
        self.upsilon = 0    # stickness of wage

        self.bank = None
        self.owner = None
    

    def plan_production(self):
        random = self.model.nprandom
        U, delta = random.uniform, self.delta
        labor_market = self.model.labor_markets[self.n_W]
        
        # revision of sales expectation and price markup
        y_tot = self.y + self.y_inv
        q = self.Q / self.p_Y
        if q >= self.q_e:
            self.q_e = self.q_e * (1 + U(0, delta))
            self.m = self.m * (1 + U(0, delta))
        elif q < y_tot:
            self.q_e = self.q_e * (1 - U(0, delta))
            self.m = self.m * (1 - U(0, delta))

        # desired production level and labor demand
        self.y_D = self.q_e * (1 + self.theta_y) - self.y_inv
        self.l_D = self.y_D / self.phi

        # wage revision and price setting
        Pr = self.upsilon * np.exp(-labor_market.upsilon * labor_market.u)
        if self.l_D > self.l:
            if random.choice([0, 1], p=[1-Pr, Pr]):
                self.w = self.w * (1 + U(0, self.delta))
        else:
            if random.choice([0, 1], p=[Pr, 1-Pr]):
                self.w = self.w * (1 - U(0, self.delta))
        print(self.m, self.w , self.phi)
        self.p_Y = (1 + self.m) * self.w / self.phi


    def apply_for_credit(self):
        self.L_D = max(0, self.w * self.l_D - self.D - self.M)
    
    def destroy_jobs(self):
        labor_market = self.model.labor_markets[self.n_W]
        workers = labor_market.neighbors(self)
        self.N_Jd = int(np.ceil(max(0, self.l - self.l_D)))
        for worker in workers.random(self.N_Jd):
            labor_market.leave_job(worker, self)
    
    def create_jobs(self):
        l_max = min(self.l_D, (self.M + self.D) / self.w)
        self.N_Jc = int(np.ceil(max(0, l_max - self.l)))
    
    def produce_goods(self):
        labor_market = self.model.labor_markets[self.n_W]
        workers = labor_market.neighbors(self)
        l = min(self.l_D, len(workers))
        workers.l = l / len(workers)
        self.y = l * self.phi
        self.y_inv += self.y
        self.l = l
        

    def compute_profit(self):
        Y_inv = self.w * self.y_inv / self.phi
        DeltaY_inv = Y_inv - self.Y_inv
        self.Pi = self.Q + DeltaY_inv + self.iota_D - self.W - self.iota_L
        self.Y_inv = Y_inv
    
    def pay_taxes(self):
        if self.Pi > 0 and self.n_T:
            model = self.model
            gov = model.government
            economy = model.economy
            economy.pay_taxes(economy.tau * self.Pi, self, gov)

    def pay_dividends(self):
        if self.Pi > 0:
            Pi_d = self.rho * (self.Pi - self.T)
            economy = self.model.economy
            economy.pay_dividends(Pi_d, self, self.owner)
    
    def update_net_worth(self):
        self.E = self.E + self.Pi - self.T - self.Pi_d
        self.owner.E = self.E



class Bank(ap.Agent):
    
    def setup(self):
        self.M = 0             # cash money
        self.A = 0             # cash advances
        self.D = 0             # deposits
        self.B = 0             # bonds
        self.L = 0             # loans
        self.L_def = 0         # default loans
        self.E = 0             # equities
        self.V = 0             # net worth

        self.T = 0             # taxes
        self.iota_A = 0        # reimbursement of advance interest
        self.iota_D = 0        # reimbursement of deposit interest
        self.iota_B = 0        # reimbursement of bonds interest
        self.iota_L = 0        # reimbursement of loans interest
        self.Pi = 0            # profits
        self.Pi_d = 0          # dividends

        self.delta = 0     # adjustment parameter
        self.kappa_E = 0    # minimum capital ratio
        self.kappa_R = 0    # minimum liquidity ratio
        self.beta_L = 0        # elasticity of interest rate to leverage ratio
        self.gamma_L = 0       # elasticity of loan probability to leverage ratio
        
        self.owner = None


    def pay_deposit_interests(self):
        deposit_market = self.model.deposit_market
        clients = deposit_market.neighbors(self)
        for client in clients:
            iota = client.D * deposit_market.r_D
            deposit_market.pay_interests(iota, self, client)
    

    def grant_loans(self):
        random = self.model.nprandom
        L_max = self.kappa_E * self.E
        credit_market =  self.model.credit_market
        firms = credit_market.neighbors(self)
        for firm in firms:
            print('Max', firm.L_D, L_max)
            if 0 < firm.L_D <= L_max:
                Pr = np.exp(-self.gamma_L * firm.L_D / firm.E)
                choice = random.choice([0, 1], p=[1-Pr, Pr])
                if choice:
                    firm.r_L = credit_market.r_L + (self.beta_L * firm.L_D / firm.E)
                    credit_market.give_loans(firm.L_D, self, firm)
                    L_max -= firm.L_D
                print('choice', choice, 'with prob', Pr)
                print('r_L', firm.r_L, 'from', self.beta_L , firm.L_D , firm.E)


    def ask_advances(self):
        A = self.kappa_R * self.D - self.R
        if A > 0:
            central_bank = self.model.central_bank
            economy = self.model.economy
            economy.give_advances(A, central_bank, self)
            

    def buy_bonds(self):
        B = self.R - self.kappa_R * self.D
        if B > 0:
            government = self.model.government
            B = min(government.B_S, B)        
            bond_market = self.model.bond_market
            bond_market.buy_bonds(B, self, government)
        

    def compute_profit(self):
        self.Pi = self.iota_L + self.iota_B - self.L_def - self.iota_D - self.iota_A
    

    def pay_taxes(self):
        economy = self.model.economy
        if self.Pi > 0:
            T = economy.tau * self.Pi
            gov = self.model.government
            economy.pay_taxes(T, self, gov)


    def pay_dividends(self):
        economy = self.model.economy
        if self.Pi > 0:
            Pi_d = self.rho * (self.Pi - self.T)
            economy.pay_dividends(Pi_d, self, self.owner)


    def update_net_worth(self):
        self.E = self.E + self.Pi - self.T - self.Pi_d
        self.owner.E = self.E



class Government(ap.Agent):
    
    def setup(self):
        self.M = 0          # reserves
        self.B = 0          # bonds
        self.B_S = 0        # bonds supply

        self.W = 0          # wage bill
        self.Z = 0          # public transfers
        self.T = 0          # taxes
        self.iota_B = 0     # reimbursement of bond interests
        self.Pi = 0         # profits

        self.w = 0          # wage offered
        self.r_B = 0        # bond interest rate


class CentralBank(ap.Agent):
    
    def setup(self):
        self.M = 0          # reserves
        self.A = 0          # cash advances
        self.B = 0          # bonds

        self.iota_A = 0     # reimbursement of advance interests
        self.iota_B = 0     # reimbursement of bond interests
        self.Pi = 0         # profit

        self.r_A = 0        # advance interest rate
        self.r_B = 0        # bond interest rate

