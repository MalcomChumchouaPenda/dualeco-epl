
import pytest
import agentpy as ap
from model.agents import CentralBank


@pytest.fixture
def model():
    model = ap.Model({})
    model.firms = ap.AgentList(model, 2)
    model.households = ap.AgentList(model, 2)
    model.banks = ap.AgentList(model, 2)
    model.government = ap.Agent(model)
    model.central_bank = CentralBank(model)
    return model

