
import pytest
import agentpy as ap
from model.environment import GoodMarket 


@pytest.fixture
def model():
    return ap.Model({})

@pytest.fixture
def market(model):
    return GoodMarket(model)


def test_is_space(market):
    assert isinstance(market, ap.Space)
    assert market.shape == (1, 1)

def test_default_state(market):
    assert market.s_Y == 0
    assert len(market.suppliers) == 0


@pytest.fixture
def suppliers(model):
    suppliers = ap.AgentList(model, 5)
    return suppliers


def test_add_suppliers(market, suppliers):
    market.add_suppliers(suppliers)
    agents = market.agents.to_list()
    assert len(suppliers) == len(market.suppliers)
    assert set(suppliers).issubset(set(agents))

def test_remove_supplier(market, suppliers):
    supplier = suppliers[0]
    market.add_suppliers(suppliers)
    market.remove_supplier(supplier)
    agents = market.agents.to_list()
    assert len(suppliers) - 1 == len(market.suppliers)
    assert supplier not in market.suppliers
    assert supplier not in agents


def test_consume_goods(market):
    model = market.model
    firm = ap.Agent(model)
    firm.Q = 0
    firm.M = 0
    client = ap.Agent(model)
    client.C = 0
    client.M = 50

    market.consume_goods(25, client, firm)
    assert firm.Q == 25
    assert firm.M == 25
    assert client.C == 25
    assert client.M == 25

