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


@pytest.fixture
def firm(model):
    firm = ap.Agent(model)
    firm.p_Y = 0.5
    firm.y_inv = 100.0
    firm.Q = 0.0
    firm.M = 0.0
    return firm


@pytest.fixture
def client(model):
    client = ap.Agent(model)
    client.C1 = 0.0
    client.C2 = 0.0
    client.M = 50.0
    return client


def test_consume_goods_of_type1(market, client, firm):
    market.s_Y = 1
    market.consume_goods(25.0, client, firm)
    assert abs(firm.y_inv - 50.0) < 1e-6
    assert abs(firm.Q - 25.0) < 1e-6
    assert abs(firm.M - 25.0) < 1e-6
    assert abs(client.C1 - 25.0) < 1e-6
    assert abs(client.C2 - 0.0) < 1e-6
    assert abs(client.M - 25.0) < 1e-6


def test_consume_goods_of_type2(market, client, firm):
    market.s_Y = 2
    market.consume_goods(25.0, client, firm)
    assert abs(firm.y_inv - 50.0) < 1e-6
    assert abs(firm.Q - 25.0) < 1e-6
    assert abs(firm.M - 25.0) < 1e-6
    assert abs(client.C1 - 0.0) < 1e-6
    assert abs(client.C2 - 25.0) < 1e-6
    assert abs(client.M - 25.0) < 1e-6
