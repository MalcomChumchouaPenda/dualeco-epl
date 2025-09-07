
import agentpy as ap


class Household(ap.Agent):
    
    def setup(self):
        self.s_EB = 0
        self.s_E = 0
        self.s = 0
        self.s_W = 0
        self.s_WG = 0
        self.s_U = 0
        self.z = ''

        self.M = 0
        self.D = 0
        self.C = 0

        self.W = 0
        self.Z = 0
        self.T = 0
        self.iota_D = 0
        self.pi_d = 0

        self.w_D = 0
        self.r_D = 0


class Firm(ap.Agent):
    
    def setup(self):
        self.s = 0
        self.z = ''

        self.M = 0
        self.D = 0
        self.L = 0

        self.Q = 0
        self.W = 0
        self.T = 0
        self.iota_D = 0
        self.iota_L = 0
        self.pi_d = 0

        self.p_y = 0
        self.r_D = 0
        self.r_L = 0


class Bank(ap.Agent):
    
    def setup(self):
        self.M = 0
        self.A = 0
        self.D = 0
        self.B = 0
        self.L = 0

        self.T = 0
        self.iota_A = 0
        self.iota_D = 0
        self.iota_B = 0
        self.iota_L = 0
        self.pi_d = 0

        self.r_D = 0
        self.r_A = 0
        self.r_B = 0
        self.r_L = 0
    

class Government(ap.Agent):
    
    def setup(self):
        self.M = 0
        self.B = 0

        self.W = 0
        self.Z = 0
        self.T = 0
        self.iota_B = 0
        self.pi = 0

        self.w = 0
        self.r_B = 0


class CentralBank(ap.Agent):
    
    def setup(self):
        self.M = 0
        self.A = 0
        self.B = 0

        self.iota_A = 0
        self.iota_B = 0
        self.pi = 0

        self.r_A = 0
        self.r_B = 0

