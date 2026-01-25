
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

        self.E = 0          # equities
        self.E_star = 0     # equities desired
        self.D = 0          # deposits
        self.D_star = 0     # deposits desired
        self.M = 0          # cash money
        self.V = 0          # net worth

        self.l = 0          # labor employed
        self.Z = 0          # public transfers
        self.W = 0          # wages
        self.C1_star = 0    # desired consumption of goods 1
        self.C2_star = 0    # desired consumption of goods 2
        self.C1 = 0         # consumption of goods 1
        self.C2 = 0         # consumption of goods 2
        self.T = 0          # taxes
        self.iota_D = 0     # reimbursement of deposit interests
        self.Pi_d = 0       # dividends

        self.w = 0          # reservation wage


        self.r_D = 0        # deposit interest rate
        self.delta = 0      # adjustment
        self.upsilon = 0    # ...
        self.chi_N = 0      # ...

        self.bank = None


    def search_job(self):
        labor_markets = self.model.labor_markets
        informal_market = labor_markets[0]
        formal_market = labor_markets[1]

        # reservation wage revision
        random = self.model.nprandom
        U = random.uniform
        Pr = self.upsilon * np.exp(-formal_market.upsilon * formal_market.u)
        if self.s_U == 0:
            print([0, 1], [1-Pr, Pr])
            if random.choice([0, 1], p=[1-Pr, Pr]):
                self.w = self.w * (1 + U(0, self.delta))
        else:
            if random.choice([0, 1], p=[Pr, 1-Pr]):
                self.w = self.w * (1 - U(0, self.delta))
        
        # search best formal jobs
        if self.n_W == 0:
            employers = formal_market.employers.random(self.chi_N)
            employers = employers.select(employers.w >= self.w)
            employers = employers.select(employers.N_v > 0)
            if len(employers) > 0:
                if self.s_W == 1 or self.s_E == 1:
                    old_employer = informal_market.neighbors(self)[0]
                    informal_market.leave_job(self, old_employer)
                choice = employers.sort('w', reverse=True)[0]
                formal_market.accept_job(self, choice)
                return
        
        # search best informal jobs
        if self.s_U == 1:
            employers = informal_market.employers.random(self.chi_N)
            employers = employers.select(employers.w >= self.w)
            employers = employers.select(employers.N_v > 0)
            if len(employers) > 0:
                choice = employers.sort('w', reverse=True)[0]
                informal_market.accept_job(self, choice)


    def pay_taxes(self):
        model = self.model
        economy = model.economy
        government = model.government
        Y = self.W + self.iota_D + self.Pi_d
        T = economy.tau * Y
        economy.pay_taxes(T, self, government)
        self.Y = Y


    def consume_goods(self):
        Y_d = self.Y - self.T + self.Z
        V_d = self.D + self.M
        C_star = self.alphaY * Y_d + self.alphaV * V_d
        self.C1_star = self.alphaC1 * C_star
        self.C2_star = (1 - self.alphaC1) * C_star

        C1 = 0
        market1 = self.model.goods_markets[1]
        sample = market1.suppliers.random(self.chiY)
        for supplier in sample:
            C = min(self.C1_star - C1, supplier.p_Y * supplier.y_inv)
            market1.consume_goods(C, self, supplier)
            C1 += C

        C2 = 0
        market2 = self.model.goods_markets[2]
        sample = market2.suppliers.random(self.chiY)
        for supplier in sample:
            C = min(self.C2_star - C2, supplier.p_Y * supplier.y_inv)
            market2.consume_goods(C, self, supplier)
            C2 += C



class Firm(ap.Agent):
    
    def setup(self):
        self.s_Y = 0        # firm's sector
        self.n_W = 0        # degree of formality on labor market
        self.n_T = 0        # degree of formality on credit market
        self.phi = 0        # productivity
        
        self.N = 0          # employment
        self.N_star = 0     # desired employment
        self.N_v = 0        # number of vacant job
        self.y_inv = 0      # real inventories
        self.Y_inv = 0      # nominal inventories
        self.E = 0          # equities
        self.L = 0          # loans
        self.L_d = 0        # credit demand
        self.L_def = 0      # loan defaults
        self.D = 0          # deposits
        self.M = 0          # cash money
        self.V = 0          # net worth

        self.y = 0          # production
        self.y_star = 0     # desired level of production
        self.W = 0          # wages
        self.q_e = 0        # sales expectation
        self.Q = 0          # sales
        self.iota_D = 0     # reimbursement of deposit interests
        self.iota_L = 0     # reimbursement of loan interests
        self.Pi = 0         # profit
        self.Pi_d = 0       # dividends
        self.T = 0          # taxes

        self.w = 0          # wage offered
        self.m = 0          # price markup
        self.p_Y = 0        # production price
        self.r_L = 0        # loan interest rate


        self.delta = 0      # max adjustment parameters
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
        self.y_star = self.q_e * (1 + self.theta_y) - self.y_inv
        self.N_star = self.y_star / self.phi

        # wage revision and price setting
        Pr = self.upsilon * np.exp(-labor_market.upsilon * labor_market.u)
        if self.N_star > self.N:
            if random.choice([0, 1], p=[1-Pr, Pr]):
                self.w = self.w * (1 + U(0, self.delta))
        else:
            if random.choice([0, 1], p=[Pr, 1-Pr]):
                self.w = self.w * (1 - U(0, self.delta))
        print(self.m, self.w , self.phi)
        self.p_Y = (1 + self.m) * self.w / self.phi


    def apply_for_credit(self):
        self.L_d = max(0, self.w * self.N_star - self.D - self.M)
    
    def destroy_jobs(self):
        labor_market = self.model.labor_markets[self.n_W]
        workers = labor_market.neighbors(self)
        N, N_star = len(workers), self.N_star
        Delta_N = int(np.floor(max(0, N - N_star)))
        for worker in workers.random(Delta_N):
            labor_market.leave_job(worker, self)
        self.N = N - Delta_N
    
    def create_jobs(self):
        N_max = min(self.N_star, (self.M + self.D) / self.w)
        self.N_v = int(np.ceil(max(0, N_max - self.N)))
    
    def produce_goods(self):
        self.y = self.phi * self.N
        self.y_inv += self.y

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

        self.iota_A = 0        # reimbursement of advance interest
        self.iota_D = 0        # reimbursement of deposit interest
        self.iota_B = 0        # reimbursement of bonds interest
        self.iota_L = 0        # reimbursement of loans interest
        self.Pi = 0            # profits
        self.Pi_d = 0          # dividends
        self.T = 0             # taxes

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
            print('Max', firm.L_d, L_max)
            if 0 < firm.L_d <= L_max:
                Pr = np.exp(-self.gamma_L * firm.L_d / firm.E)
                choice = random.choice([0, 1], p=[1-Pr, Pr])
                if choice:
                    firm.r_L = credit_market.r_L + (self.beta_L * firm.L_d / firm.E)
                    credit_market.give_loans(firm.L_d, self, firm)
                    L_max -= firm.L_d
                print('choice', choice, 'with prob', Pr)
                print('r_L', firm.r_L, 'from', self.beta_L , firm.L_d , firm.E)


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
            B = min(government.B_s, B)        
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
        self.B_s = 0        # bonds supply
        self.N = 0          # employments
        self.N_v = 0        # vacant jobs

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

