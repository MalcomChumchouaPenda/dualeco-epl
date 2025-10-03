import pytest
import agentpy as ap
from model.environment import LaborMarket 


@pytest.fixture
def market():
    model = ap.Model({})
    return LaborMarket(model)


def test_is_network(market):
    assert isinstance(market, ap.Network)


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


def test_hire_worker(market):
    model = market.model
    worker = ap.Agent(model)
    employer = ap.Agent(model)
    market.add_agents([worker, employer])

    market.hire_worker(worker, employer)
    assert market.graph.has_edge(worker, employer)


def test_fire_worker(market):
    model = market.model
    worker = ap.Agent(model)
    employer = ap.Agent(model)
    market.add_agents([worker, employer])
    market.graph.add_edge(worker, employer)

    market.fire_worker(worker, employer)
    assert not market.graph.has_edge(worker, employer)

