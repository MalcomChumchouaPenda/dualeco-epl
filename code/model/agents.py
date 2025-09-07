
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

        self.C = 0          # consumption
        self.W = 0          # wages
        self.Z = 0          # public transfers
        self.T = 0          # taxes
        self.iota_D = 0     # reimbursement of deposit interests
        self.pi_d = 0       # dividends

        self.w_D = 0        # reservation wage
        self.r_D = 0        # deposit interest rate


class Firm(ap.Agent):
    
    def setup(self):
        self.s = 0          # firm's sector
        self.z = ''         # firm's region

        self.M = 0          # cash money
        self.D = 0          # deposits
        self.L = 0          # loans

        self.Q = 0          # sales
        self.W = 0          # wages
        self.T = 0          # taxes
        self.iota_D = 0     # reimbursement of deposit interests
        self.iota_L = 0     # reimbursement of loan interests
        self.pi_d = 0       # dividends

        self.p_y = 0        # production price
        self.r_D = 0        # deposit interest rate
        self.r_L = 0        # loan interest rate


class Bank(ap.Agent):
    
    def setup(self):
        self.M = 0          # cash money
        self.A = 0          # cash advances
        self.D = 0          # deposits
        self.B = 0          # bonds
        self.L = 0          # loans

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

