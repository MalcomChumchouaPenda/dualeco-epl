import pytest
import agentpy as ap
from mock import MagicMock
from model.agents import Government


@pytest.fixture
def model():
    model = ap.Model({'seed':0})
    model.labor_market = MagicMock()
    model.bond_market = MagicMock()
    model.economy = MagicMock()
    return model

@pytest.fixture
def government1(model):
    return Government(model)


def test_default_state(government1):
    government = government1
    assert government.M == 0
    assert government.B == 0
    assert government.B_S == 0
    assert government.iota_B == 0
    assert government.Pi == 0
    assert government.T == 0
    assert government.Z == 0
    assert government.W == 0
    assert government.w == 0

