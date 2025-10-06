
import pytest
import agentpy as ap
from mock import MagicMock
from model.agents import Firm


@pytest.fixture
def model():
    model = ap.Model({'seed':0})
    model.labor_market = MagicMock()
    model.good_market = MagicMock()
    model.deposit_market = MagicMock()
    model.credit_market = MagicMock()
    model.economy = MagicMock()
    return model

@pytest.fixture
def firm1(model):
    return Firm(model)


def test_default_real_state(firm1):
    firm = firm1
    assert firm.s_Y == 0
    assert firm.n_W == 0
    assert firm.n_T == 0
    assert firm.N_J == 0
    assert firm.l == 0
    assert firm.l_D == 0


def test_default_nominal_state(firm1):
    firm = firm1
    assert firm.E == 0
    assert firm.L == 0
    assert firm.L_D == 0
    assert firm.L_def == 0
    assert firm.D == 0
    assert firm.M == 0
    assert firm.V == 0
    assert firm.W == 0
    assert firm.w == 0
    assert firm.Q == 0
    assert firm.p_Y == 0
    assert firm.iota_D == 0
    assert firm.iota_L == 0
    assert firm.r_L == 0
    assert firm.Pi == 0
    assert firm.Pi_d == 0
    assert firm.T == 0
    
