
import pytest
import agentpy as ap
from model.agents import Firm


@pytest.fixture
def model():
    model = ap.Model({})
    model.firms = ap.AgentList(model, 1, Firm)
    model.households = ap.AgentList(model, 2)
    model.banks = ap.AgentList(model, 2)
    model.government = ap.Agent(model)
    model.central_bank = ap.Agent(model)

    firm = model.firms[0]
    firm.bank = model.banks[0]
    return model





