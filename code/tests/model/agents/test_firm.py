
import pytest
import numpy as np
import agentpy as ap
from mock import MagicMock
from model.agents import Firm


@pytest.fixture
def model():
    model = ap.Model({'seed':0})
    model.good_market = MagicMock()
    model.deposit_market = MagicMock()
    model.credit_market = MagicMock()
    model.economy = MagicMock()
    return model

@pytest.fixture
def firm1(model):
    return Firm(model)


def test_default_status(firm1):
    firm = firm1
    assert firm.s_Y == 0
    assert firm.n_W == 0
    assert firm.n_T == 0


def test_default_real_stocks_and_flows(firm1):
    firm = firm1
    assert firm.N_J == 0
    assert firm.l == 0
    assert firm.l_D == 0
    assert firm.y == 0
    assert firm.y_inv == 0
    assert firm.y_star == 0
    assert firm.q_e == 0
    assert firm.q_D == 0


def test_default_nominal_stocks_and_flows(firm1):
    firm = firm1
    assert firm.E == 0
    assert firm.L == 0
    assert firm.L_D == 0
    assert firm.L_def == 0
    assert firm.Y_inv == 0
    assert firm.D == 0
    assert firm.M == 0
    assert firm.V == 0
    assert firm.W == 0
    assert firm.Q == 0
    assert firm.iota_D == 0
    assert firm.iota_L == 0
    assert firm.Pi == 0
    assert firm.Pi_d == 0
    assert firm.T == 0
    

def test_default_prices(firm1):
    firm = firm1
    assert firm.w == 0
    assert firm.p_Y == 0
    assert firm.r_L == 0

    
def test_default_params(firm1):
    firm = firm1
    assert firm.phi == 0
    assert firm.delta_max == 0
    assert firm.theta_y == 0
    assert firm.upsilon == 0


@pytest.fixture
def random(model, monkeypatch):
    f = MagicMock()
    monkeypatch.setattr(model, 'nprandom', f)
    return f


@pytest.fixture
def firm2(firm1):
    firm = firm1
    firm.delta_max = 0.5
    firm.theta_y = 0.25
    firm.p_Y = 10
    firm.q_e = 10
    return firm


@pytest.mark.parametrize('Q, y, y_inv', 
                         [(110, 4, 5), (100, 4, 5),
                          (110, 6, 5), (100, 6, 5)])
def test_increase_sales_expectation(firm2, random, Q, y, y_inv):
    random.uniform.return_value = 0.25
    firm = firm2
    firm.Q = Q
    firm.y = y
    firm.y_inv = y_inv

    firm.plan_production()
    random.uniform.assert_called_with(firm.delta_max)
    assert firm.q_e == 12.5
        

@pytest.mark.parametrize('Q, y, y_inv', 
                         [(90, 6, 5), (80, 6, 5), 
                          (90, 7, 5), (80, 7, 5)])
def test_decrease_sales_expectation(firm2, random, Q, y, y_inv):
    random.uniform.return_value = 0.25
    firm = firm2
    firm.Q = Q
    firm.y = y
    firm.y_inv = y_inv

    firm.plan_production()
    random.uniform.assert_called_with(firm.delta_max)
    assert firm.q_e == 7.5


@pytest.mark.parametrize('Q, y, y_inv', 
                         [(90, 4, 5), (80, 3, 5), 
                          (90, 3, 5), (80, 2, 5)])
def test_maintain_sales_expectation(firm2, random, Q, y, y_inv):
    random.uniform.return_value = 0.25
    firm = firm2
    firm.Q = Q
    firm.y = y
    firm.y_inv = y_inv

    firm.plan_production()
    random.uniform.assert_not_called()
    assert firm.q_e == 10


@pytest.mark.parametrize('Q, y, y_inv, q_D', 
                         [(100, 4, 5, 10.625), (90, 4, 5, 7.5), 
                          (100, 6, 5, 10.625), (90, 6, 5, 4.375)])
def test_set_desired_production_level(firm2, random, Q, y, y_inv, q_D):
    random.uniform.return_value = 0.25
    firm = firm2
    firm.Q = Q
    firm.y = y
    firm.y_inv = y_inv

    firm.plan_production()
    assert firm.q_D == q_D


# @pytest.fixture
# def labor_market():
#     market = MagicMock()
#     market.upsilon = 0.5
#     market.u = 0.5
#     return market

# @pytest.fixture
# def firm2(firm1, labor_market):
#     firm = firm1
#     firm.upsilon = 0.25
#     firm.theta_y = 0.25
#     firm.phi = 1
#     firm.y = 100
#     firm.y_inv = 0
#     firm.p_Y = 1
#     firm.w = 1
#     firm.l = 100
#     firm.model.labor_market = labor_market
#     return firm

# @pytest.fixture
# def exp(monkeypatch):
#     f = MagicMock()
#     monkeypatch.setattr(np, 'exp', f)
#     return f


# @pytest.mark.parametrize('y_inv', [0, 10, 20])
# def test_increase_price(firm2, y_inv, random):
#     random.uniform.return_value = 0.25
#     firm = firm2
#     firm.y_inv = y_inv
#     firm.plan_production()
#     assert firm.p_Y == 1.25


# @pytest.mark.parametrize('y_inv', [100, 75, 50])
# def test_decrease_price(firm2, y_inv, random):
#     random.uniform.return_value = 0.25
#     firm = firm2
#     firm.y_inv = y_inv
#     firm.plan_production()
#     assert firm.p_Y == 0.75


# @pytest.mark.parametrize('y_inv', [0, 10, 20])    
# def test_increase_desired_production(firm2, y_inv, random):
#     random.uniform.return_value = 0.25
#     firm = firm2
#     firm.y_inv = y_inv
#     firm.plan_production()
#     assert firm.y_star == 125


# @pytest.mark.parametrize('y_inv', [100, 75, 50])
# def test_decrease_desired_production(firm2, y_inv, random):
#     random.uniform.return_value = 0.25
#     firm = firm2
#     firm.y_inv = y_inv
#     firm.plan_production()
#     assert firm.y_star == 75


# @pytest.mark.parametrize('y_inv, l_D', [(0, 125), (100, 75)])
# def test_set_labor_demand(firm2, y_inv, l_D, random):
#     random.uniform.return_value = 0.25
#     firm = firm2
#     firm.y_inv = y_inv
#     firm.plan_production()
#     assert firm.l_D == l_D    # y_star / phi


# @pytest.mark.parametrize('y_inv, N_J', [(0, 25), (100, 0)])
# def test_create_vacant_jobs(firm2, y_inv, N_J, random):
#     random.uniform.return_value = 0.25
#     firm = firm2
#     firm.y_inv = y_inv
#     firm.plan_production()
#     assert firm.N_J == N_J    # max(0, l_D - l)


# @pytest.mark.parametrize('Pr, w', [(0, 1), (1, 1.25)])    
# def test_increase_wage(firm2, Pr, w, random, exp):
#     random.uniform.return_value = 0.25
#     random.choice.return_value = Pr
#     exp.return_value = 0.5
#     firm = firm2
#     firm.y_inv = 0

#     firm.plan_production()  
#     exp.assert_called_with(-0.25)
#     random.choice.assert_called_with([0, 1], p=[0.875, 0.125])
#     assert firm.l_D > firm.l
#     assert firm.w == w


# @pytest.mark.parametrize('Pr, w', [(0, 1), (1, 0.75)])   
# def test_decrease_wage(firm2, Pr, w, random, exp):
#     random.uniform.return_value = 0.25
#     random.choice.return_value = Pr
#     exp.return_value = 0.5
#     firm = firm2
#     firm.y_inv = 100

#     firm.plan_production()
#     exp.assert_called_with(-0.25)
#     random.choice.assert_called_with([0, 1], p=[0.125, 0.875])
#     assert firm.l_D <= firm.l
#     assert firm.w == w


# @pytest.mark.parametrize('D, M, L_D', [(50, 50, 0), (0, 50, 50), 
#                                        (50, 0, 50), (100, 50, 0)])
# def test_set_credit_demand(firm2, D, M, L_D, random):
#     random.uniform.return_value = 0
#     random.choice.return_value = 0
#     firm = firm2
#     firm.D = D
#     firm.M = M
#     firm.plan_production()
#     assert firm.w == 1
#     assert firm.l_D == 100
#     assert firm.L_D == L_D


@pytest.fixture
def economy():
    economy = MagicMock()
    economy.tau = 0.1
    return economy


@pytest.fixture
def firm3(firm1, economy):
    firm = firm1
    firm.owner = MagicMock()
    firm.model.economy = economy
    return firm


def test_compute_profits(firm3):
    firm = firm3
    firm.Q = 100
    firm.iota_D = 50
    firm.W = 75
    firm.iota_L = 25
    firm.compute_profit()
    assert firm.Pi == 50.0


@pytest.fixture
def government1(model):
    government = ap.Agent(model)
    model.government = government
    return government


@pytest.mark.parametrize('Pi, T', [(25, 2.5), (50, 5.0)])
def test_pay_taxes_if_profits(firm3, government1, Pi, T):
    firm = firm3
    firm.n_T = 1
    firm.Pi = Pi
    firm.pay_taxes()
        
    government = government1
    economy = firm.model.economy
    economy.pay_taxes.assert_called_with(T, firm, government)


@pytest.mark.parametrize('Pi', [0, 25, 50])
def test_do_not_pay_taxes_if_informal(firm3, government1, Pi):
    firm = firm3
    firm.n_T = 0
    firm.Pi = Pi
    firm.pay_taxes()
    
    economy = firm.model.economy
    economy.pay_taxes.assert_not_called()


@pytest.mark.parametrize('Pi', [0, -25, -50])
def test_do_not_pay_taxes_if_losses(firm3, Pi):
    firm = firm3
    firm.n_T = 1
    firm.Pi = Pi
    firm.pay_taxes()
    
    economy = firm.model.economy
    economy.pay_taxes.assert_not_called()


@pytest.mark.parametrize('Pi, T, Pi_d', [(25, 5, 10.0), (50, 10.0, 20.0)])
def test_pay_dividends_if_profits(firm3, Pi, T, Pi_d):
    firm = firm3
    firm.rho = 0.5
    firm.Pi = Pi
    firm.T = T
    firm.pay_dividends()
    
    economy = firm.model.economy
    economy.pay_dividends.assert_called_with(Pi_d, firm, firm.owner)


@pytest.mark.parametrize('Pi', [0, -25, -50])
def test_do_not_pay_dividends_if_losses(firm3, Pi):
    firm = firm3
    firm.Pi = Pi
    firm.pay_dividends()
    
    economy = firm.model.economy
    economy.pay_dividends.assert_not_called()


def test_update_net_worth(firm3):
    firm = firm3
    firm.E = 60
    firm.Pi = 40
    firm.T = 15
    firm.Pi_d = 10
    firm.owner = MagicMock()
    firm.update_net_worth()
    assert round(firm.E, 2) == round(60 + 40 - 15 - 10, 2)
    assert round(firm.E, 2) == round(firm.owner.E, 2)

