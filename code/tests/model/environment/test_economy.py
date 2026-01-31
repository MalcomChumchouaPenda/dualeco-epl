import pytest
import agentpy as ap
from model.environment import Economy


@pytest.fixture
def economy():
    model = ap.Model({})
    return Economy(model)


def test_is_space(economy):
    assert isinstance(economy, ap.Space)
    assert economy.shape == (1, 1)


def test_pay_doles(economy):
    model = economy.model
    government = ap.Agent(model)
    government.Z = 0
    government.M = 100
    household = ap.Agent(model)
    household.Z = 0
    household.M = 0

    economy.pay_doles(50, government, household)
    assert government.Z == 50
    assert government.M == 50
    assert household.Z == 50
    assert household.M == 50


def test_pay_taxes(economy):
    model = economy.model
    government = ap.Agent(model)
    government.T = 0
    government.M = 0
    payer = ap.Agent(model)
    payer.T = 0
    payer.M = 20

    economy.pay_taxes(10, payer, government)
    assert payer.T == 10
    assert payer.M == 10
    assert government.T == 10
    assert government.M == 10


def test_pay_dividends(economy):
    model = economy.model
    payer = ap.Agent(model)
    payer.Pi_d = 0
    payer.M = 100
    owner = ap.Agent(model)
    owner.Pi_d = 0
    owner.M = 0

    economy.pay_dividends(20, payer, owner)
    assert payer.Pi_d == 20
    assert payer.M == 80
    assert owner.Pi_d == 20
    assert owner.M == 20


def test_transfert_profits(economy):
    model = economy.model
    central_bank = ap.Agent(model)
    central_bank.Pi = 0
    central_bank.M = 25
    government = ap.Agent(model)
    government.Pi = 0
    government.M = 0

    economy.transfer_profits(10, central_bank, government)
    assert central_bank.Pi == 10
    assert central_bank.M == 35
    assert government.Pi == 10
    assert government.M == 10


def test_give_advances(economy):
    model = economy.model
    bank = ap.Agent(model)
    bank.A = 0
    bank.M = 0
    central_bank = ap.Agent(model)
    central_bank.A = 0
    central_bank.M = 0

    economy.give_advances(20, central_bank, bank)
    assert central_bank.A == 20
    assert central_bank.M == 20
    assert bank.A == 20
    assert bank.M == 20


def test_repay_advances(economy):
    model = economy.model
    bank = ap.Agent(model)
    bank.iota_A = 0
    bank.A = 50
    bank.M = 100
    central_bank = ap.Agent(model)
    central_bank.iota_A = 0
    central_bank.A = 50
    central_bank.M = 100

    economy.repay_advances(50, 10, bank, central_bank)
    assert bank.iota_A == 10
    assert bank.A == 0
    assert bank.M == 40
    assert central_bank.iota_A == 10
    assert central_bank.A == 0
    assert central_bank.M == 40


def test_invest_equities(economy):
    model = economy.model
    owner = ap.Agent(model)
    owner.M = 100
    owner.E = 0
    target = ap.Agent(model)
    target.M = 0
    target.E = 0

    economy.invest_equities(50, owner, target)
    assert owner.M == 50
    assert owner.E == 50
    assert target.M == 50
    assert target.E == 50


def test_reimburse_equities(economy):
    model = economy.model
    owner = ap.Agent(model)
    owner.Pi_d = 0
    owner.M = 0
    owner.E = 100
    target = ap.Agent(model)
    target.Pi_d = 0
    target.M = 50
    target.E = 100

    economy.reimburse_equities(target, owner)
    assert target.Pi_d == -50
    assert target.M == 0
    assert target.E == 0
    assert owner.Pi_d == -50
    assert owner.M == 50
    assert owner.E == 0
