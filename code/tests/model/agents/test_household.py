
import pytest
import agentpy as ap
from mock import MagicMock
from model.agents import Household


@pytest.fixture
def model():
    model = ap.Model({'seed':0})
    model.labor_market = MagicMock()
    model.good_market = MagicMock()
    model.deposit_market = MagicMock()
    model.economy = MagicMock()
    return model

@pytest.fixture
def household1(model):
    return Household(model)


def test_default_real_state(household1):
    household = household1
    assert household.s_U == 0
    assert household.s_W == 0
    assert household.s_WG == 0
    assert household.s_E == 0
    assert household.s_EB == 0
    assert household.s_Y == 0
    assert household.n_W == 0
    assert household.l == 0
    assert household.l_S == 1


def test_default_nominal_state(household1):
    household = household1
    assert household.E == 0
    assert household.E_star == 0
    assert household.D == 0
    assert household.D_star == 0
    assert household.M == 0
    assert household.V == 0
    assert household.Z == 0
    assert household.W == 0
    assert household.w_D == 0
    assert household.C_star == 0
    assert household.C1 == 0
    assert household.C2 == 0
    assert household.iota_D == 0
    assert household.Pi_d == 0
    assert household.T == 0
    
