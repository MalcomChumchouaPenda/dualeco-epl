import pytest
import agentpy as ap
from model.environment import DepositMarket


@pytest.fixture
def market():
    model = ap.Model({})
    return DepositMarket(model)


def test_is_network(market):
    assert isinstance(market, ap.Network)


def test_make_deposits(market):
    model = market.model
    bank = ap.Agent(model)
    bank.D = 0
    bank.M = 0
    client = ap.Agent(model)
    client.D = 0
    client.M = 50

    market.make_deposits(20, client, bank)
    assert client.D == 20
    assert client.M == 30
    assert bank.D == 20
    assert bank.M == 20


def test_withdraw_deposits(market):
    model = market.model
    bank = ap.Agent(model)
    bank.D = 25
    bank.M = 25
    client = ap.Agent(model)
    client.D = 25
    client.M = 0

    market.withdraw_deposits(15, bank, client)
    assert bank.D == 10
    assert bank.M == 10
    assert client.D == 10
    assert client.M == 15


def test_pay_interests(market):
    model = market.model
    bank = ap.Agent(model)
    bank.iota_D = 0
    bank.D = 25
    client = ap.Agent(model)
    client.iota_D = 0
    client.D = 25

    market.pay_interests(5, bank, client)
    assert bank.iota_D == 5
    assert bank.D == 30
    assert client.iota_D == 5
    assert client.D == 30


def test_choose_bank(market):
    model = market.model
    client = ap.Agent(model)
    client.bank = None
    bank1 = ap.Agent(model)
    bank2 = ap.Agent(model)
    market.add_agents([client, bank1, bank2])

    assert client.bank is None
    assert not market.graph.has_edge(client, bank1)
    assert not market.graph.has_edge(client, bank2)

    market.choose_bank(client, bank1)
    assert client.bank is bank1
    assert market.graph.has_edge(client, bank1)
    assert not market.graph.has_edge(client, bank2)

    market.choose_bank(client, bank2)
    assert client.bank is bank2
    assert not market.graph.has_edge(client, bank1)
    assert market.graph.has_edge(client, bank2)
