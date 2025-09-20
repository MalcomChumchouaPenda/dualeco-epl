
import pytest
import agentpy as ap
from model.agents import Government


@pytest.fixture
def model():
    model = ap.Model({})
    model.firms = ap.AgentList(model, 2)
    model.households = ap.AgentList(model, 2)
    model.banks = ap.AgentList(model, 2)
    model.government = Government(model)
    model.central_bank = ap.Agent(model)
    return model


