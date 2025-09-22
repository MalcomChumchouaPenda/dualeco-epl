

import agentpy as ap


class Region(ap.Space):
    
    def pay_doles(self, amount, government, household):
        government.Z += amount
        government.M -= amount
        household.Z += amount
        household.M += amount
    
    def pay_taxes(self, amount, payer, government):
        payer.T += amount
        payer.M -= amount
        government.T += amount
        government.M += amount
    
    def pay_dividends(self, amount, source, owner):
        source.pi_d += amount
        source.M -= amount
        owner.pi_d += amount
        owner.M += amount
    
    def transfer_profits(self, amount, source, target):
        source.pi += amount
        source.M += amount
        target.pi += amount
        target.M += amount

    def give_advances(self, amount, central_bank, bank):
        central_bank.A += amount
        central_bank.M += amount
        bank.A += amount
        bank.M += amount
    
    def repay_advances(self, capital, interests, bank, central_bank):
        bank.iota_A += interests
        bank.A -= capital
        bank.M -= capital + interests
        central_bank.iota_A += interests
        central_bank.A -= capital
        central_bank.M -= capital +  interests
    
    def invest_equities(self, amount, owner, target):
        owner.E += amount
        owner.M -= amount
        target.E += amount
        target.M += amount
    
    def reimburse_equities(self, target, owner):
        cash = target.M
        amount = target.E
        target.pi_d -= amount - cash
        target.E -= amount
        target.M -= cash
        owner.pi_d -= amount - cash
        owner.E -= amount
        owner.M += cash
        


class GoodMarket(ap.Network):
    
    def consume_goods(self, amount, client, firm):
        client.C += amount
        client.M -= amount
        firm.Q += amount
        firm.M += amount


class LaborMarket(ap.Network):
    
    def pay_wages(self, amount, employer, worker):
        employer.W += amount
        employer.M -= amount
        worker.W += amount
        worker.M += amount


class DepositMarket(ap.Network):
    
    def make_deposits(self, amount, client, bank):
        client.D += amount
        client.M -= amount
        bank.D += amount
        bank.M += amount

    def withdraw_deposits(self, amount, bank, client):
        bank.D -= amount
        bank.M -= amount
        client.D -= amount
        client.M += amount
    
    def pay_interests(self, amount, bank, client):
        bank.iota_D += amount
        bank.D += amount
        client.iota_D += amount
        client.D += amount


class CreditMarket(ap.Network):
    
    def give_loans(self, amount, bank, firm):
        bank.L += amount
        bank.D += amount
        firm.L += amount
        firm.D += amount
    
    def repay_loans(self, capital, interests, firm, bank):
        firm.iota_L += interests
        firm.L -=  capital
        firm.D -= capital + interests
        bank.iota_L += interests
        bank.L -= capital
        bank.D -= capital + interests
    
    def make_defaults(self, value, firm, bank):
        firm.L -= value
        firm.L_def += value
        bank.L -= value
        bank.L_def += value


class BondMarket(ap.Network):

    def setup(self, **kwargs):
        self.central_bank =  None
    
    def buy_bonds(self, amount, buyer, government):
        government.B += amount
        government.M += amount
        if buyer is self.central_bank:
            buyer.B += amount
            buyer.M += amount
        else:
            buyer.B += amount
            buyer.M -= amount
    
    def repay_bonds(self, capital, interests, government, buyer):
        government.iota_B += interests
        government.B -= capital
        government.M -= capital + interests
        if buyer is self.central_bank:
            buyer.iota_B += interests
            buyer.B -= capital
            buyer.M -= capital + interests
        else:
            buyer.iota_B += interests
            buyer.B -= capital
            buyer.M += capital + interests
    
    def transfer_bonds(self, amount, bank, central_bank):
        bank.B -= amount
        bank.M += amount
        central_bank.B += amount
        central_bank.M += amount

