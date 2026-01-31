import pytest
import agentpy as ap
from model.environment import BondMarket


@pytest.fixture
def market():
    model = ap.Model({})
    market = BondMarket(model)
    market.central_bank = ap.Agent(model)
    return market


def test_is_space(market):
    assert isinstance(market, ap.Space)
    assert market.shape == (1, 1)


def test_bank_buy_bonds(market):
    model = market.model
    bank = ap.Agent(model)
    bank.B = 0
    bank.M = 100
    government = ap.Agent(model)
    government.B = 0
    government.M = 0

    market.buy_bonds(50, bank, government)
    assert bank.B == 50
    assert bank.M == 50
    assert government.B == 50
    assert government.M == 50


def test_central_bank_buy_bonds(market):
    model = market.model
    central_bank = market.central_bank
    central_bank.B = 0
    central_bank.M = 100
    government = ap.Agent(model)
    government.B = 0
    government.M = 0

    market.buy_bonds(50, central_bank, government)
    assert central_bank.B == 50
    assert central_bank.M == 150
    assert government.B == 50
    assert government.M == 50


def test_repay_bonds_to_bank(market):
    model = market.model
    bank = ap.Agent(model)
    bank.iota_B = 0
    bank.B = 50
    bank.M = 50
    government = ap.Agent(model)
    government.iota_B = 0
    government.B = 50
    government.M = 100

    market.repay_bonds(50, 10, government, bank)
    assert government.iota_B == 10
    assert government.B == 0
    assert government.M == 40
    assert bank.iota_B == 10
    assert bank.B == 0
    assert bank.M == 110


def test_repay_bonds_to_central_bank(market):
    model = market.model
    central_bank = market.central_bank
    central_bank.iota_B = 0
    central_bank.B = 50
    central_bank.M = 100
    government = ap.Agent(model)
    government.iota_B = 0
    government.B = 50
    government.M = 100

    market.repay_bonds(50, 10, government, central_bank)
    assert government.iota_B == 10
    assert government.B == 0
    assert government.M == 40
    assert central_bank.iota_B == 10
    assert central_bank.B == 0
    assert central_bank.M == 40


def test_bank_transfer_bonds_to_central_bank(market):
    model = market.model
    central_bank = market.central_bank
    central_bank.B = 50
    central_bank.M = 50
    bank = ap.Agent(model)
    bank.B = 50
    bank.M = 50

    market.transfer_bonds(50, bank, central_bank)
    assert bank.B == 0
    assert bank.M == 100
    assert central_bank.B == 100
    assert central_bank.M == 100
