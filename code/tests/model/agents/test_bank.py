
import pytest
import numpy as np
import agentpy as ap
from mock import MagicMock
from model.agents import Bank


@pytest.fixture
def model():
    model = ap.Model({'seed':0})
    model.deposit_market = MagicMock()
    model.credit_market = MagicMock()
    model.bond_market = MagicMock()
    model.economy = MagicMock()
    return model

@pytest.fixture
def bank1(model):
    return Bank(model)


def test_default_state(bank1):
    bank = bank1
    assert bank.E == 0
    assert bank.L == 0
    assert bank.L_def == 0
    assert bank.D == 0
    assert bank.M == 0
    assert bank.B == 0
    assert bank.A == 0
    assert bank.V == 0
    assert bank.iota_D == 0
    assert bank.iota_L == 0
    assert bank.iota_B == 0
    assert bank.iota_A == 0
    assert bank.Pi == 0
    assert bank.Pi_d == 0
    assert bank.T == 0
    

@pytest.fixture
def clients1(model):
    clients = ap.AgentList(model, 3)
    for i, client in enumerate(clients):
        client.D = i * 10
    model.deposit_market.neighbors.return_value = clients
    return clients


def test_pay_deposit_interests(bank1, clients1):
    bank = bank1
    bank.r_D = 0.1
    bank.pay_deposit_interests()

    market = bank.model.deposit_market
    market.neighbors.assert_called_once_with(bank)
    for client in clients1:
        iota = bank.r_D * client.D
        market.pay_interests.assert_any_call(iota, bank, client)


@pytest.fixture
def credit_market(model):
    market = MagicMock()
    market.r_L = 0.1
    model.credit_market = market
    return market

@pytest.fixture
def firms1(model, credit_market):
    firms = ap.AgentList(model, 3)
    firms.r_L = 0
    firms.E = 100
    credit_market.neighbors.return_value = firms
    return firms

@pytest.fixture
def bank2(bank1):
    bank = bank1
    bank.theta_Ebar = 0.5  # ratio reglementaire de capital
    bank.beta_L = 0.5      # elastticite du taux d'interet
    bank.gamma_L = 0.5     # probabilite de pret
    bank.E = 300
    return bank

@pytest.fixture
def random(model, monkeypatch):
    f = MagicMock()
    monkeypatch.setattr(model, 'nprandom', f)
    return f

@pytest.fixture
def exp(monkeypatch):
    f = MagicMock()
    monkeypatch.setattr(np, 'exp', f)
    return f


@pytest.mark.parametrize('L_D', [25, 50])   
def test_grant_loans_to_ranked_borrower(bank2, firms1, L_D, random, exp):
    random.choice.return_value = 1
    exp.return_value = 0.75
    firms1.L_D = L_D
    bank = bank2
    bank.grant_loans()

    exp.assert_called_with(-0.005 * L_D)
    random.choice.assert_called_with([0, 1], p=[0.25, 0.75])
    give_loans = bank.model.credit_market.give_loans
    for firm in firms1:
        give_loans.assert_any_call(L_D, bank, firm)


@pytest.mark.parametrize('L_D, r_L', [(25, 0.225), (50, 0.35)])   
def test_grant_loans_with_differents_rates(bank2, firms1, L_D, r_L, random):
    random.choice.return_value = 1
    firms1.L_D = L_D
    bank2.grant_loans()    
    for firm in firms1:
        assert firm.r_L == r_L


def test_grant_loans_with_maximum_loan(bank2, firms1, random):
    random.choice.return_value = 1
    firms1.L_D = 100
    bank = bank2
    bank.grant_loans()

    market = bank.model.credit_market
    calls = market.give_loans.call_args_list
    loans = sum([call.args[0] for call in calls])
    assert loans <= bank.theta_Ebar * bank.E


@pytest.mark.parametrize('L_D', [25, 50])
def test_do_not_grant_loans_to_ranked_borrower(bank2, firms1, L_D, random):
    random.choice.return_value = 0
    firms1.L_D = L_D
    bank = bank2
    bank.grant_loans()

    give_loans = bank.model.credit_market.give_loans
    give_loans.assert_not_called()


def test_do_not_grant_loans_if_no_demand(bank2, firms1, random):
    random.choice.return_value = 1
    firms1.L_D = 0
    bank = bank2
    bank.grant_loans()
    
    market = bank.model.credit_market
    market.neighbors.assert_called_once_with(bank)
    market.give_loans.assert_not_called()


@pytest.fixture
def central_bank1(model):
    central_bank = ap.Agent(model)
    model.central_bank = central_bank
    model.economy = MagicMock()
    return central_bank

@pytest.fixture
def bank3(bank1):
    bank = bank1
    bank.theta_Rbar = 0.5  # ratio reglementaire de liquidite
    bank.D = 100
    return bank


def test_ask_advances_if_insufficient_reserves(bank3, central_bank1):
    central_bank = central_bank1
    bank = bank3
    bank.R = 25
    bank.ask_advances()

    economy = bank.model.economy
    economy.give_advances.assert_called_with(25, central_bank, bank)


def test_do_not_ask_advances_if_sufficient_reserves(bank3, central_bank1):
    bank = bank3
    bank.R = 125
    bank.ask_advances()

    economy = bank.model.economy
    economy.give_advances.assert_not_called()


@pytest.fixture
def government1(model):
    government = ap.Agent(model)
    model.government = government
    model.bond_market = MagicMock()
    return government


def test_buy_bonds_if_sufficient_reserves(bank3, government1):
    government = government1
    government.B_S = 200
    bank = bank3
    bank.R = 150
    bank.buy_bonds()

    market = bank.model.bond_market
    market.buy_bonds.assert_called_with(100, bank, government)


def test_buy_available_bonds(bank3, government1):
    government = government1
    government.B_S = 50
    bank = bank3
    bank.R = 150
    bank.buy_bonds()

    market = bank.model.bond_market
    market.buy_bonds.assert_called_with(50, bank, government)


def test_do_not_buy_bonds_if_insufficient_reserves(bank3, government1):
    government = government1
    government.B_S = 50
    bank = bank3
    bank.R = 25
    bank.buy_bonds()

    market = bank.model.bond_market
    market.buy_bonds.assert_not_called()


def test_compute_profits(bank1):
    bank = bank1
    bank.iota_L = 50
    bank.iota_B = 50
    bank.L_def = 10
    bank.iota_D = 20
    bank.iota_A = 20
    bank.compute_profit()
    assert round(bank.Pi, 2) == 50.0


@pytest.mark.parametrize('Pi, T', [(25, 2.5), (50, 5.0)])
def test_pay_taxes_if_profits(bank1, government1, Pi, T):
    bank = bank1
    bank.tau = 0.1
    bank.Pi = Pi
    bank.pay_taxes()
        
    government = government1
    economy = bank.model.economy
    economy.pay_taxes.assert_called_with(T, bank, government)


@pytest.mark.parametrize('Pi', [0, -25, -50])
def test_do_not_pay_taxes_if_losses(bank1, Pi):
    bank = bank1
    bank.tau = 0.1
    bank.Pi = Pi
    bank.pay_taxes()
    
    economy = bank.model.economy
    economy.pay_taxes.assert_not_called()


@pytest.mark.parametrize('Pi, T, Pi_d', [(25, 5, 10.0), (50, 10.0, 20.0)])
def test_pay_dividends_if_profits(bank1, Pi, T, Pi_d):
    bank = bank1
    bank.rho = 0.5
    bank.Pi = Pi
    bank.T = T
    bank.pay_dividends()
    
    economy = bank.model.economy
    economy.pay_dividends.assert_called_with(Pi_d, bank, bank.owner)


@pytest.mark.parametrize('Pi', [0, -25, -50])
def test_do_not_pay_dividends_if_losses(bank1, Pi):
    bank = bank1
    bank.Pi = Pi
    bank.pay_dividends()
    
    economy = bank.model.economy
    economy.pay_dividends.assert_not_called()


def test_update_net_worth(bank1):
    bank = bank1
    bank.E = 60
    bank.Pi = 40
    bank.T = 15
    bank.Pi_d = 10
    bank.owner = MagicMock()
    bank.update_net_worth()
    assert round(bank.E, 2) == round(60 + 40 - 15 - 10, 2)
    assert round(bank.E, 2) == round(bank.owner.E, 2)

