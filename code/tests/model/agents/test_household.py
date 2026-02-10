import pytest
import agentpy as ap
from mock import MagicMock
from model.agents import Household



@pytest.fixture
def consumer1():
    model = ap.Model()
    household = Household(model)
    return household


def test_plan_desired_consumptions(consumer1):
    consumer1.alphaY = 0.5
    consumer1.alphaW = 0.2
    consumer1.alpha1 = 0.4
    consumer1.Y_d = 100
    consumer1.W = 50

    consumer1.plan_consumption()

    C_star = consumer1.C1_star + consumer1.C2_star
    assert C_star == pytest.approx(0.5 * 100 + 0.2 * 50)
    assert consumer1.C1_star == pytest.approx(0.4 * C_star)
    assert consumer1.C2_star == pytest.approx(0.6 * C_star)


@pytest.fixture
def goods_market(consumer1):
    suppliers = ap.AgentList(consumer1.model, 10)
    suppliers.pY = 10.0
    suppliers.inv = 20.0
    market = MagicMock()
    market.suppliers = suppliers
    return market


def called_suppliers(market):
    return [call.args[2] for call in market.buy_goods.call_args_list]


def purchase_amounts(market):
    return [call.args[0] for call in market.buy_goods.call_args_list]


def test_buy_goods_at_desired_level(consumer1, goods_market):
    consumer1.M = 2000  # sufficient cash
    consumer1.chiY = 10  # sufficient matching param

    consumer1.buy_goods(2000.0, goods_market)

    assert len(called_suppliers(goods_market)) == consumer1.chiY
    assert sum(purchase_amounts(goods_market)) == pytest.approx(2000.0)


def test_buy_goods_with_limited_suppliers(consumer1, goods_market):
    consumer1.M = 2000  # sufficient cash
    consumer1.chiY = 5  # limited matching param

    consumer1.buy_goods(2000.0, goods_market)

    assert len(called_suppliers(goods_market)) == consumer1.chiY
    assert sum(purchase_amounts(goods_market)) == pytest.approx(1000.0)


def test_buy_goods_with_limited_cash(consumer1, goods_market):
    consumer1.M = 1000  # insufficient cash
    consumer1.chiY = 10  # sufficient matching param

    consumer1.buy_goods(2000.0, goods_market)

    assert len(called_suppliers(goods_market)) < consumer1.chiY
    assert sum(purchase_amounts(goods_market)) == pytest.approx(1000.0)


@pytest.fixture
def consumer2(consumer1):
    consumer1.plan_consumption = MagicMock()
    consumer1.withdraw_deposits = MagicMock()
    consumer1.buy_goods = MagicMock()
    return consumer1


@pytest.fixture
def goods_markets(consumer2):
    markets = {i: MagicMock() for i in range(1, 3)}
    consumer2.region = MagicMock()
    consumer2.region.goods_markets = markets
    return markets


def test_consume_after_planning(consumer2, goods_markets):
    consumer2.C1_star = 100.0
    consumer2.C2_star = 200.0
    consumer2.M = 300.0  # sufficient cash

    consumer2.consume_goods()

    consumer2.plan_consumption.assert_called_once()
    consumer2.buy_goods.assert_any_call(100.0, goods_markets[1])
    consumer2.buy_goods.assert_any_call(200.0, goods_markets[2])


def test_consume_after_withdrawing_deposit(consumer2, goods_markets):
    consumer2.C1_star = 100.0
    consumer2.C2_star = 200.0
    consumer2.M = 100.0  # insufficient cash

    consumer2.consume_goods()

    consumer2.withdraw_deposits.assert_called_once_with(200.0)
    consumer2.buy_goods.assert_any_call(100.0, goods_markets[1])
    consumer2.buy_goods.assert_any_call(200.0, goods_markets[2])
