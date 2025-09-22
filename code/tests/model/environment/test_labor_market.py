import pytest
import agentpy as ap
from model.environment import LaborMarket 


@pytest.fixture
def market():
    model = ap.Model({})
    return LaborMarket(model)


def test_pay_wages(market):
    model = market.model
    employer = ap.Agent(model)
    employer.W = 0
    employer.M = 50
    worker = ap.Agent(model)
    worker.W = 0
    worker.M = 0

    market.pay_wages(20, employer, worker)
    assert employer.W == 20
    assert employer.M == 30
    assert worker.W == 20
    assert worker.M == 20

