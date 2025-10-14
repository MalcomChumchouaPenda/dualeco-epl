
import pytest
import agentpy as ap
from model.environment import GoodMarket 


@pytest.fixture
def market():
    model = ap.Model({})
    return GoodMarket(model)


def test_is_space(market):
    assert isinstance(market, ap.Space)
    assert market.shape == (1, 1)

def test_default_state(market):
    assert market.s_Y == 0


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

