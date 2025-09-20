
import pytest
import agentpy as ap
from model.agents import Household


@pytest.fixture
def model():
    model = ap.Model({})
    model.firms = ap.AgentList(model, 2)
    model.households = ap.AgentList(model, 1, Household)
    model.banks = ap.AgentList(model, 2)
    model.government = ap.Agent(model)
    model.central_bank = ap.Agent(model)

    household = model.households[0]
    household.bank = model.banks[0]
    return model
