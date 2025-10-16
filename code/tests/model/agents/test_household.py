
import pytest
import numpy as np
import agentpy as ap
from mock import MagicMock
from model.agents import Household


@pytest.fixture
def model():
    return ap.Model()

@pytest.fixture
def household1(model):
    return Household(model)


def test_default_status(household1):
    household = household1
    assert household.s_U == 0
    assert household.s_W == 0
    assert household.s_WG == 0
    assert household.s_E == 0
    assert household.s_EB == 0
    assert household.s_Y == 0
    assert household.n_W == 0


def test_default_real_stocks_and_flows(household1):
    household = household1
    assert household.l == 0
    assert household.l_S == 1


def test_default_nominal_stocks_and_flows(household1):
    household = household1
    assert household.E == 0
    assert household.E_D == 0
    assert household.D == 0
    assert household.D_D == 0
    assert household.M == 0
    assert household.V == 0
    assert household.Z == 0
    assert household.W == 0
    assert household.C_D == 0
    assert household.C1 == 0
    assert household.C2 == 0
    assert household.iota_D == 0
    assert household.Pi_d == 0
    assert household.T == 0


def test_default_prices(household1):
    household = household1
    assert household.w_D == 0


def test_default_params(household1):
    household = household1
    assert household.delta == 0
    assert household.upsilon == 0
    assert household.chi_J == 0
    assert household.chi_Y == 0


# def test_default_links(household1):
#     household = household1
#     assert household.bank is None
#     assert household.property is None


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

@pytest.fixture
def labor_markets(model):
    empty = ap.AgentList(model)
    markets = {}
    for n_W in (0, 1):
        market = MagicMock()
        market.u = 0.5
        market.upsilon = 0.5 * n_W
        market.employers.random.return_value = empty
        markets[n_W] = market
    return markets

@pytest.fixture
def household2(household1, random, exp, labor_markets):
    household = household1
    household.upsilon = 0.25
    household.delta = 0.5
    household.w_D = 1
    household.l_S = 1
    household.model.labor_markets = labor_markets
    random.uniform.return_value = 0.25
    exp.return_value = 0.5
    return household


@pytest.mark.parametrize('Pr, s_U, w_D', [(0, 0, 1), (1, 0, 1.25)])    
def test_increase_reservation_wage(household2, random, exp, Pr, s_U, w_D):
    random.choice.return_value = Pr
    household = household2
    household.s_U = s_U
    household.search_job()  
    exp.assert_called_with(-0.25)
    random.choice.assert_called_with([0, 1], p=[0.875, 0.125])
    assert household.w_D == w_D


@pytest.mark.parametrize('Pr, s_U, w_D', [(0, 1, 1), (1, 1, 0.75)])   
def test_decrease_reservation_wage(household2, random, exp, Pr, s_U, w_D):
    random.choice.return_value = Pr
    household = household2
    household.s_U = s_U
    household.search_job()
    exp.assert_called_with(-0.25)
    random.choice.assert_called_with([0, 1], p=[0.125, 0.875])
    assert household.w_D == w_D


@pytest.fixture
def household3(household2, random):
    random.choice.return_value = 0
    household = household2
    household.w_D = 1.5
    household.s_U = 1
    household.s_E = 0
    household.s_W = 0
    household.chi_J = 1
    return household

@pytest.fixture
def employers(model):
    group_a = ap.AgentList(model, 2)
    for i, employer in enumerate(group_a):
        employer.w = 0.5 * (i + 1)
        employer.N_Jc = 1
    group_b = ap.AgentList(model, 2)
    for i, employer in enumerate(group_b):
        employer.w = i + 1
        employer.N_Jc = 1
    group_c = ap.AgentList(model, 2)
    for i, employer in enumerate(group_c):
        employer.w = i + 1
        employer.N_Jc = 0
    return {'a':group_a, 'b':group_b, 'c':group_c}


@pytest.mark.parametrize('g1, g0', [('b', 'a'), ('b', 'b'), ('b', 'c')])
def test_unemployed_prefer_best_formal_job(household3, employers, g1, g0):
    household = household3
    labor_markets = household.model.labor_markets
    labor_markets[1].employers.random.return_value = employers[g1]
    labor_markets[0].employers.random.return_value = employers[g0]
    choice = employers[g1][-1]

    household.search_job()
    labor_markets[1].employers.random.assert_called_with(household.chi_J)
    labor_markets[0].employers.random.assert_not_called()
    labor_markets[1].accept_job.assert_called_with(household, choice)


@pytest.mark.parametrize('g1, g0', [('a', 'b'), ('c', 'b')])
def test_unemployed_prefer_best_informal_job(household3, employers, g1, g0):
    household = household3
    labor_markets = household.model.labor_markets
    labor_markets[1].employers.random.return_value = employers[g1]
    labor_markets[0].employers.random.return_value = employers[g0]
    choice = employers[g0][-1]

    household.search_job()
    labor_markets[1].employers.random.assert_called_with(household.chi_J)
    labor_markets[0].employers.random.assert_called_with(household.chi_J)
    labor_markets[1].accept_job.assert_not_called()
    labor_markets[0].accept_job.assert_called_with(household, choice)


@pytest.mark.parametrize('g1, g0', [('c', 'c'), ('c', 'a'), ('a', 'c'), ('a', 'a')])
def test_remain_unemployed(household3, employers, g1, g0):
    household = household3
    labor_markets = household.model.labor_markets
    labor_markets[1].employers.random.return_value = employers[g1]
    labor_markets[0].employers.random.return_value = employers[g0]

    household.search_job()
    labor_markets[1].employers.random.assert_called_with(household.chi_J)
    labor_markets[0].employers.random.assert_called_with(household.chi_J)
    labor_markets[1].accept_job.assert_not_called()
    labor_markets[0].accept_job.assert_not_called()


@pytest.fixture
def household4(household3):
    household = household3
    household.s_U = 0
    household.s_E = 0
    household.s_W = 1
    household.n_W = 0
    household._old_employer = MagicMock()
    labor_market = household.model.labor_markets[0]
    labor_market.neighbors.return_value = [household._old_employer]
    return household


@pytest.mark.parametrize('g1, g0', [('b', 'a'), ('b', 'b'), ('b', 'c')])
def test_informal_worker_prefer_formal_job(household4, employers, g1, g0):
    household = household4
    old_employer = household._old_employer
    labor_markets = household.model.labor_markets
    labor_markets[1].employers.random.return_value = employers[g1]
    labor_markets[0].employers.random.return_value = employers[g0]
    choice = employers[g1][-1]

    household.search_job()
    labor_markets[1].employers.random.assert_called_with(household.chi_J)
    labor_markets[0].employers.random.assert_not_called()
    labor_markets[1].accept_job.assert_called_with(household, choice)
    labor_markets[0].accept_job.assert_not_called()
    labor_markets[1].leave_job.assert_not_called()
    labor_markets[0].leave_job.assert_called_with(household, old_employer)


@pytest.mark.parametrize('g1, g0', [('a', 'a'), ('a', 'b'), ('a', 'c'), 
                                    ('c', 'a'), ('c', 'b'), ('c', 'c')])
def test_informal_worker_remain_informal(household4, employers, g1, g0):
    household = household4
    labor_markets = household.model.labor_markets
    labor_markets[1].employers.random.return_value = employers[g1]
    labor_markets[0].employers.random.return_value = employers[g0]

    household.search_job()
    labor_markets[1].employers.random.assert_called_with(household.chi_J)
    labor_markets[0].employers.random.assert_not_called()
    labor_markets[1].accept_job.assert_not_called()
    labor_markets[0].accept_job.assert_not_called()
    labor_markets[1].leave_job.assert_not_called()
    labor_markets[0].leave_job.assert_not_called()


@pytest.fixture
def household5(household3):
    household = household3
    household.s_U = 0
    household.s_E = 1
    household.s_W = 0
    household.n_W = 0
    household._old_employer = MagicMock()
    labor_market = household.model.labor_markets[0]
    labor_market.neighbors.return_value = [household._old_employer]
    return household


@pytest.mark.parametrize('g1, g0', [('b', 'a'), ('b', 'b'), ('b', 'c')])
def test_informal_entrepreneur_prefer_formal_job(household5, employers, g1, g0):
    household = household5
    old_employer = household._old_employer
    labor_markets = household.model.labor_markets
    labor_markets[1].employers.random.return_value = employers[g1]
    labor_markets[0].employers.random.return_value = employers[g0]
    choice = employers[g1][-1]

    household.search_job()
    labor_markets[1].employers.random.assert_called_with(household.chi_J)
    labor_markets[0].employers.random.assert_not_called()
    labor_markets[1].accept_job.assert_called_with(household, choice)
    labor_markets[0].accept_job.assert_not_called()
    labor_markets[1].leave_job.assert_not_called()
    labor_markets[0].leave_job.assert_called_with(household, old_employer)


@pytest.mark.parametrize('g1, g0', [('a', 'a'), ('a', 'b'), ('a', 'c'), 
                                    ('c', 'a'), ('c', 'b'), ('c', 'c')])
def test_informal_entrepreneur_remain_informal(household5, employers, g1, g0):
    household = household5
    labor_markets = household.model.labor_markets
    labor_markets[1].employers.random.return_value = employers[g1]
    labor_markets[0].employers.random.return_value = employers[g0]

    household.search_job()
    labor_markets[1].employers.random.assert_called_with(household.chi_J)
    labor_markets[0].employers.random.assert_not_called()
    labor_markets[1].accept_job.assert_not_called()
    labor_markets[0].accept_job.assert_not_called()
    labor_markets[1].leave_job.assert_not_called()
    labor_markets[0].leave_job.assert_not_called()


@pytest.fixture
def household6(household3):
    household = household3
    household.s_U = 0
    household.n_W = 1
    household._old_employer = MagicMock()
    labor_market = household.model.labor_markets[0]
    labor_market.neighbors.return_value = [household._old_employer]
    return household


@pytest.mark.parametrize('g1, g0', [('a', 'a'), ('a', 'b'), ('a', 'c'), 
                                    ('b', 'a'), ('b', 'b'), ('b', 'c'), 
                                    ('c', 'a'), ('c', 'b'), ('c', 'c')])
def test_no_search_from_informal_entrepreneur(household6, employers, g1, g0):
    household = household6
    household.s_E = 1
    household.s_W = 0
    labor_markets = household.model.labor_markets
    labor_markets[1].employers.random.return_value = employers[g1]
    labor_markets[0].employers.random.return_value = employers[g0]

    household.search_job()
    labor_markets[1].employers.random.assert_not_called()
    labor_markets[0].employers.random.assert_not_called()
    labor_markets[1].accept_job.assert_not_called()
    labor_markets[0].accept_job.assert_not_called()
    labor_markets[1].leave_job.assert_not_called()
    labor_markets[0].leave_job.assert_not_called()


@pytest.mark.parametrize('g1, g0', [('a', 'a'), ('a', 'b'), ('a', 'c'), 
                                    ('b', 'a'), ('b', 'b'), ('b', 'c'), 
                                    ('c', 'a'), ('c', 'b'), ('c', 'c')])
def test_no_search_from_informal_worker(household6, employers, g1, g0):
    household = household6
    household.s_E = 0
    household.s_W = 1
    labor_markets = household.model.labor_markets
    labor_markets[1].employers.random.return_value = employers[g1]
    labor_markets[0].employers.random.return_value = employers[g0]

    household.search_job()
    labor_markets[1].employers.random.assert_not_called()
    labor_markets[0].employers.random.assert_not_called()
    labor_markets[1].accept_job.assert_not_called()
    labor_markets[0].accept_job.assert_not_called()
    labor_markets[1].leave_job.assert_not_called()
    labor_markets[0].leave_job.assert_not_called()



@pytest.fixture
def economy():
    economy = MagicMock()
    economy.tau = 0.1
    return economy    

@pytest.fixture
def government(model):
    return ap.Agent(model)

@pytest.fixture
def household7(household1, economy, government):
    household = household1
    household.W = 100
    household.Pi_d = 50
    household.iota_D = 50
    household.model.economy = economy
    household.model.government = government
    return household


def test_compute_taxable_income(household7):
    household = household7
    household.pay_taxes()
    assert household.Y == 200

def test_pay_taxes(household7, government):
    household = household7
    household.pay_taxes()
    economy = household.model.economy
    economy.pay_taxes.assert_called_with(20, household, government)

