import pytest
import agentpy as ap
from mock import MagicMock
from model.agents import CentralBank


@pytest.fixture
def model():
    model = ap.Model({"seed": 0})
    model.bond_market = MagicMock()
    model.economy = MagicMock()
    return model


@pytest.fixture
def central_bank1(model):
    return CentralBank(model)


def test_default_state(central_bank1):
    central_bank = central_bank1
    assert central_bank.M == 0
    assert central_bank.B == 0
    assert central_bank.A == 0
    assert central_bank.iota_B == 0
    assert central_bank.iota_A == 0
    assert central_bank.Pi == 0
