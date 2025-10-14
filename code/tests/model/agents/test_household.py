
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


@pytest.fixture
def random(model, monkeypatch):
    f = MagicMock()
    monkeypatch.setattr(model, 'nprandom', f)
    return f

@pytest.fixture
def labor_market():
    market = MagicMock()
    market.upsilon = 0.5
    market.u = 0.5
    return market

@pytest.fixture
def exp(monkeypatch):
    f = MagicMock()
    monkeypatch.setattr(np, 'exp', f)
    return f

@pytest.fixture
def household2(household1, random, exp, labor_market):
    household = household1
    household.upsilon = 0.25
    household.delta = 0.5
    household.w_D = 1
    household.l_S = 1
    household.model.labor_market = labor_market
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


@pytest.mark.parametrize('Pr, s_U, w_D', [(0, 11, 1), (1, 11, 0.75)])   
def test_decrease_reservation_wage(household2, random, exp, Pr, s_U, w_D):
    random.choice.return_value = Pr
    household = household2
    household.s_U = s_U
    household.search_job()
    exp.assert_called_with(-0.25)
    random.choice.assert_called_with([0, 1], p=[0.125, 0.875])
    assert household.w_D == w_D


