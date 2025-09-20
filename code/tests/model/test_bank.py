
import pytest
import agentpy as ap
from model.agents import Bank


@pytest.fixture
def model1():
    model = ap.Model({})
    model.firms = ap.AgentList(model, 3)
    model.households = ap.AgentList(model, 2)
    model.banks = ap.AgentList(model, 1, Bank)
    model.government = ap.Agent(model)
    model.central_bank = ap.Agent(model)
    return model

