

import pytest
import agentpy as ap
from model.environment import TransactionSpace


@pytest.fixture
def space():
    model = ap.Model({})
    return TransactionSpace(model)


def test_withdraw_deposits(space):
    bank = ap.Agent(space.model)
    bank.M = 25
    bank.D = 50
    
    client = ap.Agent(space.model)
    client.M = 0
    client.D = 50

    space.withdraw_deposits(25, client, bank)
    assert client.M == 25
    assert client.D == 25
    assert bank.M == 25
    assert bank.D == 25


def test_ask_advances(space):
    central_bank = ap.Agent(space.model)
    central_bank.A = 10
    central_bank.M = 10

    bank = ap.Agent(space.model)
    bank.A = 0
    bank.M = 0

    space.ask_advances(20, bank, central_bank)
    assert bank.A == 20
    assert bank.M == 20
    assert central_bank.A == 30
    assert central_bank.M == 30


def test_grant_loans(space):
    firm = ap.Agent(space.model)
    firm.L = 0
    firm.D = 10

    bank = ap.Agent(space.model)
    bank.L = 0
    bank.D = 10

    space.grant_loans(20, bank, firm)
    assert bank.L == 20
    assert bank.D == 30
    assert firm.L == 20
    assert firm.D == 30


def test_pay_wages(space):
    household = ap.Agent(space.model)
    household.M = 0
    household.W = 0

    firm = ap.Agent(space.model)
    firm.M = 50
    firm.W = 0

    space.pay_wages(20, firm, household)
    assert firm.M == 30
    assert firm.W == 20
    assert household.M == 20
    assert household.W == 20

    government = ap.Agent(space.model)
    government.M = 0
    government.W = 0

    space.pay_wages(20, government, household)
    assert government.M == -20
    assert government.W == 20
    assert household.M == 40
    assert household.W == 40


def test_pay_doles(space):
    household = ap.Agent(space.model)
    household.M = 0
    household.Z = 0

    government = ap.Agent(space.model)
    government.M = 0
    government.Z = 0

    space.pay_doles(20, government, household)
    assert government.M == -20
    assert government.Z == 20
    assert household.M == 40
    assert household.Z == 40


def test_pay_taxes(space):
    government = ap.Agent(space.model)
    government.M = 0
    government.W = 0

    household = ap.Agent(space.model)
    household.M = 50
    household.T = 0

    space.pay_taxes(20, household, government)
    assert household.M == 30
    assert household.T == 20
    assert government.M == 20
    assert government.T == 20

    firm = ap.Agent(space.model)
    firm.M = 50
    firm.T = 0

    space.pay_taxes(20, firm, government)
    assert firm.M == 30
    assert firm.T == 20
    assert government.M == 20
    assert government.T == 20
    
    bank = ap.Agent(space.model)
    bank.M = 50
    bank.T = 0

    space.pay_taxes(20, bank, government)
    assert bank.M == 30
    assert bank.T == 20
    assert government.M == 20
    assert government.T == 20


def test_pay_dividends(space):
    household = ap.Agent(space.model)
    household.M = 0
    household.pi_d = 0

    firm = ap.Agent(space.model)
    firm.M = 50
    firm.pi_d = 0

    space.pay_dividends(20, firm, household)
    assert firm.M == 30
    assert firm.pi_d == 20
    assert household.M == 20
    assert household.pi_d == 20    

    bank = ap.Agent(space.model)
    bank.M = 50
    bank.pi_d = 0

    space.pay_dividends(20, bank, household)
    assert bank.M == 30
    assert bank.pi_d == 20
    assert household.M == 40
    assert household.pi_d == 40    


def test_transfer_profits(space):
    government = ap.Agent(space.model)
    government.M = 0
    government.pi = 0

    central_bank = ap.Agent(space.model)
    central_bank.M = 0
    central_bank.pi = 0

    space.transfer_profits(15, government, central_bank)
    assert government.M == 15
    assert government.pi == 15
    assert central_bank.M == 15
    assert central_bank.pi == 15


def test_consume_goods(space):
    household = ap.Agent(space.model)
    household.C = 0
    household.M = 50

    firm = ap.Agent(space.model)
    firm.Q = 0
    firm.M = 0

    space.consume_goods(20, household, firm)
    assert household.C == 20
    assert household.M == 30
    assert firm.Q == 20
    assert firm.M == 20


def test_repay_bonds(space):
    government = ap.Agent(space.model)
    government.iota_B = 0
    government.B = 30
    government.M = 40

    bank = ap.Agent(space.model)
    bank.iota_B = 0
    bank.B = 10
    bank.M = 0

    space.repay_bonds(10, 5, bank, government)
    assert bank.iota_B == 5
    assert bank.B == 0
    assert bank.M == 15
    assert government.iota_B == 5
    assert government.B == 20
    assert government.M == 25

    central_bank = ap.Agent(space.model)
    central_bank.iota_B = 0
    central_bank.B = 20
    central_bank.M = 0

    space.repay_bonds(10, 5, central_bank, government)
    assert central_bank.iota_B == 5
    assert central_bank.B == 10
    assert central_bank.M == 15
    assert government.iota_B == 10
    assert government.B == 10
    assert government.M == 10


def test_repay_loans(space):
    firm = ap.Agent(space.model)
    firm.iota_L = 0
    firm.L = 10
    firm.M = 40

    bank = ap.Agent(space.model)
    bank.iota_L = 0
    bank.L = 10
    bank.M = 0

    space.repay_loans(10, 5, bank, firm)
    assert bank.iota_L == 5
    assert bank.L == 0
    assert bank.M == 15
    assert firm.iota_L == 5
    assert firm.L == 0
    assert firm.M == 25


def test_pay_deposit_interests(space):
    bank = ap.Agent(space.model)
    bank.iota_D = 0
    bank.D = 10

    firm = ap.Agent(space.model)
    firm.iota_D = 0
    firm.D = 10

    space.pay_deposit_interests(5, bank, firm)
    assert bank.iota_D == 5
    assert bank.D == 15
    assert firm.iota_D == 5
    assert firm.D == 15

    household = ap.Agent(space.model)
    household.iota_D = 0
    household.D = 10

    space.pay_deposit_interests(5, bank, household)
    assert bank.iota_D == 5
    assert bank.D == 15
    assert household.iota_D == 5
    assert household.D == 15


def test_repay_advances(space):
    central_bank = ap.Agent(space.model)
    central_bank.iota_A = 0
    central_bank.A = 10
    central_bank.M = 40

    bank = ap.Agent(space.model)
    bank.iota_A = 0
    bank.A = 10
    bank.M = 0

    space.repay_advances(10, 5, bank, central_bank)
    assert bank.iota_A == 5
    assert bank.A == 0
    assert bank.M == 15
    assert central_bank.iota_A == 5
    assert central_bank.A == 0
    assert central_bank.M == 25

