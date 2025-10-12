
import pytest
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
