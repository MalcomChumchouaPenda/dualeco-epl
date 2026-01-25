
import pytest
import numpy as np
import agentpy as ap
from mock import MagicMock
from model.agents import Firm


@pytest.fixture
def model():
    return ap.Model()

@pytest.fixture
def firm1(model):
    return Firm(model)


def test_default_status(firm1):
    firm = firm1
    assert firm.s_Y == 0
    assert firm.n_W == 0
    assert firm.n_T == 0
    assert firm.phi == 0


def test_default_stocks(firm1):
    firm = firm1
    assert firm.N == 0
    assert firm.N_star == 0
    assert firm.N_v == 0
    assert firm.y_inv == 0
    assert firm.Y_inv == 0
    assert firm.E == 0
    assert firm.L == 0
    assert firm.L_d == 0
    assert firm.L_def == 0
    assert firm.D == 0
    assert firm.M == 0
    assert firm.V == 0


def test_default_flows(firm1):
    firm = firm1
    assert firm.y == 0
    assert firm.y_star == 0
    assert firm.W == 0
    assert firm.q_e == 0
    assert firm.Q == 0
    assert firm.iota_D == 0
    assert firm.iota_L == 0
    assert firm.Pi == 0
    assert firm.Pi_d == 0
    assert firm.T == 0
    

def test_default_prices(firm1):
    firm = firm1
    assert firm.w == 0
    assert firm.m == 0
    assert firm.p_Y == 0
    assert firm.r_L == 0

    
def test_default_params(firm1):
    firm = firm1
    assert firm.phi == 0
    assert firm.delta == 0
    assert firm.theta_y == 0
    assert firm.upsilon == 0


@pytest.fixture
def random(model, monkeypatch):
    f = MagicMock()
    monkeypatch.setattr(model, 'nprandom', f)
    return f

@pytest.fixture
def labor_markets():
    markets = {}
    for n_W in (0, 1):
        market = MagicMock()
        market.upsilon = 0.5
        market.u = 0.5
        markets[n_W] = market
    return markets

@pytest.fixture
def firm2(firm1, random, labor_markets):
    firm = firm1
    firm.delta = 0.5
    firm.theta_y = 0.25
    firm.p_Y = 10
    firm.q_e = 10
    firm.phi = 1
    firm.n_W = 1
    firm.model.labor_markets = labor_markets
    random.uniform.return_value = 0.25
    return firm


@pytest.mark.parametrize('Q, y, y_inv', 
                         [(110, 4, 5), (100, 4, 5),
                          (110, 6, 5), (100, 6, 5)])
def test_increase_sales_expectation(firm2, random, Q, y, y_inv):
    firm = firm2
    firm.Q = Q
    firm.y = y
    firm.y_inv = y_inv
    firm.plan_production()
    random.uniform.assert_called_with(0, firm.delta)
    assert firm.q_e == 12.5
        

@pytest.mark.parametrize('Q, y, y_inv', 
                         [(90, 6, 5), (80, 6, 5), 
                          (90, 7, 5), (80, 7, 5)])
def test_decrease_sales_expectation(firm2, random, Q, y, y_inv):
    firm = firm2
    firm.Q = Q
    firm.y = y
    firm.y_inv = y_inv
    firm.plan_production()
    random.uniform.assert_called_with(0, firm.delta)
    assert firm.q_e == 7.5


@pytest.mark.parametrize('Q, y, y_inv', 
                         [(90, 4, 5), (80, 3, 5), 
                          (90, 3, 5), (80, 2, 5)])
def test_maintain_sales_expectation(firm2, Q, y, y_inv):
    firm = firm2
    firm.Q = Q
    firm.y = y
    firm.y_inv = y_inv
    firm.plan_production()
    assert firm.q_e == 10


@pytest.mark.parametrize('Q, y, y_inv, y_star', 
                         [(100, 4, 5, 10.625), (90, 4, 5, 7.5), 
                          (100, 6, 5, 10.625), (90, 6, 5, 4.375)])
def test_set_desired_production_level(firm2, Q, y, y_inv, y_star):
    firm = firm2
    firm.Q = Q
    firm.y = y
    firm.y_inv = y_inv
    firm.plan_production()
    assert firm.y_star == y_star


@pytest.mark.parametrize('Q, y, y_inv, N_star', 
                         [(100, 4, 5, 10.625), (90, 4, 5, 7.5), 
                          (100, 6, 5, 10.625), (90, 6, 5, 4.375)])
def test_set_labor_demand(firm2, Q, y, y_inv, N_star):
    firm = firm2
    firm.Q = Q
    firm.y = y
    firm.y_inv = y_inv
    firm.plan_production()
    assert firm.N_star == N_star


@pytest.fixture
def exp(monkeypatch):
    f = MagicMock()
    monkeypatch.setattr(np, 'exp', f)
    return f

@pytest.fixture
def firm3(firm2, exp):
    firm = firm2
    firm.Q = 100
    firm.w = 1
    firm.y = 4
    firm.y_inv = 5
    firm.upsilon = 0.25
    exp.return_value = 0.5
    return firm


@pytest.mark.parametrize('Pr, N, w', [(0, 10, 1), (1, 10, 1.25)])    
def test_increase_wage(firm3, random, exp, Pr, N, w):
    random.choice.return_value = Pr
    firm = firm3
    firm.N = N
    firm.plan_production()  
    exp.assert_called_with(-0.25)
    random.choice.assert_called_with([0, 1], p=[0.875, 0.125])
    assert firm.N_star == 10.625   # check previous computation
    assert firm.w == w


@pytest.mark.parametrize('Pr, N, w', [(0, 11, 1), (1, 11, 0.75)])   
def test_decrease_wage(firm3, random, exp, Pr, N, w):
    random.choice.return_value = Pr
    firm = firm3
    firm.N = N
    firm.plan_production()
    exp.assert_called_with(-0.25)
    random.choice.assert_called_with([0, 1], p=[0.125, 0.875])
    assert firm.N_star == 10.625   # check previous computation
    assert firm.w == w


@pytest.fixture
def firm4(firm3):
    firm = firm3
    firm.m = 1
    return firm


@pytest.mark.parametrize('Q, y, y_inv', 
                         [(110, 4, 5), (100, 4, 5),
                          (110, 6, 5), (100, 6, 5)])
def test_increase_price_markup(firm4, Q, y, y_inv):
    firm = firm4
    firm.Q = Q
    firm.y = y
    firm.y_inv = y_inv
    firm.plan_production()
    assert firm.m == 1.25
        

@pytest.mark.parametrize('Q, y, y_inv', 
                         [(90, 6, 5), (80, 6, 5), 
                          (90, 7, 5), (80, 7, 5)])
def test_decrease_price_markup(firm4, Q, y, y_inv):
    firm = firm4
    firm.Q = Q
    firm.y = y
    firm.y_inv = y_inv
    firm.plan_production()
    assert firm.m == 0.75


@pytest.mark.parametrize('Q, y, y_inv', 
                         [(90, 4, 5), (80, 3, 5), 
                          (90, 3, 5), (80, 2, 5)])
def test_maintain_price_markup(firm4, Q, y, y_inv):
    firm = firm4
    firm.Q = Q
    firm.y = y
    firm.y_inv = y_inv
    firm.plan_production()
    assert firm.m == 1


@pytest.mark.parametrize('Q, y, y_inv, Pr, N, p_Y', 
                         [(90, 4, 5, 0, 10, 2), 
                          (90, 6, 5, 0, 10, 1.75),
                          (100, 6, 5, 0, 10, 2.25)])
def test_set_price(firm4, random, Q, y, y_inv, Pr, N, p_Y):
    random.choice.return_value = Pr
    firm = firm4
    firm.N = N
    firm.Q = Q
    firm.y = y
    firm.y_inv = y_inv
    firm.plan_production()
    assert firm.p_Y == p_Y


@pytest.mark.parametrize('D, M, L_d', 
                         [(50, 50, 0), (0, 50, 50), 
                          (50, 0, 50), (100, 50, 0)])
def test_apply_for_credit(firm1, D, M, L_d):
    firm = firm1
    firm.D = D
    firm.M = M
    firm.N_star = 100
    firm.w = 1
    firm.apply_for_credit()
    assert firm.L_d == L_d


@pytest.fixture
def workers(model, labor_markets):
    workers = ap.AgentList(model, 5)
    labor_markets[1].neighbors.return_value = workers
    return workers

@pytest.fixture
def firm5(firm2):
    firm = firm2
    firm.N = 5
    firm.w = 1
    return firm


@pytest.mark.usefixtures('workers')
@pytest.mark.parametrize('N_star, Delta_N', 
                         [(3, 2), (3.5, 1),
                          (4.5, 0), (5, 0)])
def test_destroy_jobs(firm5, N_star, Delta_N):
    firm = firm5
    firm.N_star = N_star
    firm.destroy_jobs()
    labor_market = firm.model.labor_markets[1]
    assert labor_market.leave_job.call_count == Delta_N
    assert firm.N_v == 0


@pytest.mark.parametrize('N_star, N_v, M, D, w', 
                         [(7, 2, 10, 0, 1),         # sufficient wage funds (cash)
                          (5.5, 1, 0, 10, 1),       # sufficient wage funds (deposit) 
                          (6, 1, 0, 4, 0.5),        # sufficient wage funds (low wage)   
                          (7, 1, 6, 0, 1),          # insufficient wage funds (cash)
                          (5.5, 0, 0, 4, 1),        # insufficient wage funds (deposit)  
                          (6, 0, 0, 4, 1.5),        # insufficient wage funds (high wage)   
                          (5, 0, 0, 10, 1)])        # sufficient past employment
def test_create_jobs(firm5, N_star, N_v, M, D, w):
    firm = firm5
    firm.M = M
    firm.D = D
    firm.w = w
    firm.N_star = N_star
    firm.create_jobs()
    assert firm.N_v == N_v


@pytest.mark.parametrize('y_inv, phi', 
                         [(0, 1),        # no inventory
                          (1, 1),        # inventory
                          (1, 1.5)])     # larger productivity
def test_produce_goods(firm5, workers, y_inv, phi):
    firm = firm5
    firm.phi = phi
    firm.y_inv = y_inv
    firm.produce_goods()
    assert firm.y == len(workers) * phi
    assert firm.y_inv == y_inv + len(workers) * phi


@pytest.fixture
def economy():
    economy = MagicMock()
    economy.tau = 0.1
    return economy

@pytest.fixture
def government(model):
    return ap.Agent(model)

@pytest.fixture
def firm6(firm1, economy, government):
    firm = firm1
    firm.owner = MagicMock()
    firm.model.economy = economy
    firm.model.government = government
    return firm


def test_compute_profits(firm6):
    firm = firm6
    firm.Q = 100
    firm.Y_inv = 25
    firm.y_inv = 10
    firm.iota_D = 50
    firm.phi = 1
    firm.w = 5
    firm.W = 75
    firm.iota_L = 25
    firm.compute_profit()
    assert firm.Pi == 75.0
    assert firm.Y_inv == 50


@pytest.mark.parametrize('Pi, T', [(25, 2.5), (50, 5.0)])
def test_pay_taxes_if_profits(firm6, government, Pi, T):
    firm = firm6
    firm.n_T = 1
    firm.Pi = Pi
    firm.pay_taxes()
    economy = firm.model.economy
    economy.pay_taxes.assert_called_with(T, firm, government)


@pytest.mark.parametrize('Pi', [0, 25, 50])
def test_do_not_pay_taxes_if_informal(firm6, Pi):
    firm = firm6
    firm.n_T = 0
    firm.Pi = Pi
    firm.pay_taxes()    
    economy = firm.model.economy
    economy.pay_taxes.assert_not_called()


@pytest.mark.parametrize('Pi', [0, -25, -50])
def test_do_not_pay_taxes_if_losses(firm6, Pi):
    firm = firm6
    firm.n_T = 1
    firm.Pi = Pi
    firm.pay_taxes()
    economy = firm.model.economy
    economy.pay_taxes.assert_not_called()


@pytest.mark.parametrize('Pi, T, Pi_d', [(25, 5, 10.0), (50, 10.0, 20.0)])
def test_pay_dividends_if_profits(firm6, Pi, T, Pi_d):
    firm = firm6
    firm.rho = 0.5
    firm.Pi = Pi
    firm.T = T
    firm.pay_dividends()
    economy = firm.model.economy
    economy.pay_dividends.assert_called_with(Pi_d, firm, firm.owner)


@pytest.mark.parametrize('Pi', [0, -25, -50])
def test_do_not_pay_dividends_if_losses(firm6, Pi):
    firm = firm6
    firm.Pi = Pi
    firm.pay_dividends()    
    economy = firm.model.economy
    economy.pay_dividends.assert_not_called()


def test_update_net_worth(firm6):
    firm = firm6
    firm.E = 60
    firm.Pi = 40
    firm.T = 15
    firm.Pi_d = 10
    firm.owner = MagicMock()
    firm.update_net_worth()
    assert round(firm.E, 2) == round(60 + 40 - 15 - 10, 2)
    assert round(firm.E, 2) == round(firm.owner.E, 2)

