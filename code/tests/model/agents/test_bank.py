
import pytest
import agentpy as ap
from mock import MagicMock, call
from model.agents import Bank


@pytest.fixture
def model():
    model = ap.Model({'seed':0})
    model.deposit_market = MagicMock()
    model.credit_market = MagicMock()
    model.bond_market = MagicMock()
    model.country = MagicMock()
    return model

@pytest.fixture
def bank1(model):
    return Bank(model)


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
def firms1(model):
    firms = ap.AgentList(model, 3)
    firms.r_L = 0
    firms.V = 100
    model.credit_market.neighbors.return_value = firms
    return firms

@pytest.fixture
def bank2(bank1):
    bank = bank1
    bank.theta_Ebar = 0.5  # ratio reglementaire de capital
    bank.beta_L = 0.5      # elastticite du taux d'interet
    bank.gamma_L = 1.0     # probabilite de pret
    bank.r_L = 0.1
    bank.V = 100
    return bank


@pytest.mark.repeat(5)
def test_do_not_grant_loans_if_no_demand(bank2, firms1):
    firms = firms1
    firms.L_D = 0
    bank = bank2
    bank.grant_loans()
    
    market = bank.model.credit_market
    market.neighbors.assert_called_once_with(bank)
    market.give_loans.assert_not_called()



@pytest.mark.repeat(5)
def test_grant_loans_to_best_borrower(bank2, firms1):
    firms = firms1
    firms.L_D = 5
    firms.V = 50000
    bank = bank2
    bank.V = 300
    bank.grant_loans()
        
    market = bank.model.credit_market
    give_loans = market.give_loans
    for firm in firms:
        assert firm.r_L > bank.r_L
        give_loans.assert_any_call(firm.L_D, bank, firm)


@pytest.mark.repeat(5)
def test_grant_loans_with_maximum_loan(bank2, firms1):
    firms = firms1
    firms.L_D = 50
    firms.V = 500
    bank = bank2
    bank.V = 150
    bank.grant_loans()

    market = bank.model.credit_market
    calls = market.give_loans.call_args_list
    loans = sum([call.args[0] for call in calls])
    assert loans <= bank.theta_Ebar * bank.V


@pytest.mark.repeat(5)
def test_do_not_grant_loans_to_worst_borrower(bank2, firms1):
    firms = firms1
    firms.L_D = 50000
    firms.V = 50
    bank = bank2
    bank.V = 300
    bank.grant_loans()
        
    market = bank.model.credit_market
    market.give_loans.assert_not_called()


@pytest.fixture
def central_bank1(model):
    central_bank = ap.Agent(model)
    model.central_bank = central_bank
    model.country = MagicMock()
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

    country = bank.model.country
    country.give_advances.assert_called_with(25, central_bank, bank)


def test_do_not_ask_advances_if_sufficient_reserves(bank3, central_bank1):
    bank = bank3
    bank.R = 125
    bank.ask_advances()

    country = bank.model.country
    country.give_advances.assert_not_called()


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



# @pytest.fixture
# def bank3(bank1):
#     bank = bank1
#     bank.theta_Rbar = 0.5  # ratio reglementaire de liquidite
#     bank.D = 100
#     return bank

# def test_compute_profits():
#     pass


# def test_update_networth():
#     pass


# def test_pay_dividends_if_profits():
#     pass


# def test_do_not_pay_dividends_if_losses():
#     pass


# def test_pay_taxes_if_profits():
#     pass


# def test_do_not_pay_taxes_if_losses():
#     pass
