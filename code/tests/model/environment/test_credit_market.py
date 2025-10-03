
import pytest
import agentpy as ap
from model.environment import CreditMarket 


@pytest.fixture
def market():
    model = ap.Model({})
    return CreditMarket(model)


def test_is_network(market):
    assert isinstance(market, ap.Network)


def test_give_loans(market):
    model = market.model
    bank = ap.Agent(model)
    bank.L = 0
    bank.D = 10
    firm = ap.Agent(model)
    firm.L = 0
    firm.D = 0

    market.give_loans(10, bank, firm)
    assert bank.L == 10
    assert bank.D == 20
    assert firm.L == 10
    assert firm.D == 10


def test_repay_loans(market):
    model = market.model
    bank = ap.Agent(model)
    bank.iota_L = 0
    bank.L = 10
    bank.D = 20
    firm = ap.Agent(model)
    firm.iota_L = 0
    firm.L = 10
    firm.D = 20

    market.repay_loans(10, 5, firm, bank)
    assert firm.iota_L == 5
    assert firm.L == 0
    assert firm.D == 5
    assert bank.iota_L == 5
    assert bank.L == 0
    assert bank.D == 5


def test_make_defaults(market):
    model = market.model
    bank = ap.Agent(model)
    bank.L = 10
    bank.L_def = 0
    firm = ap.Agent(model)
    firm.L = 10
    firm.L_def = 0

    market.make_defaults(10, firm, bank)
    assert firm.L == 0
    assert firm.L_def == 10
    assert bank.L == 0
    assert bank.L_def == 10



