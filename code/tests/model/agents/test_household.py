import pytest
import agentpy as ap
from mock import MagicMock
from model.agents import Household


@pytest.fixture
def model():
    return ap.Model()


@pytest.fixture
def consumer1(model):
    return Household(model)


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
def goods_market1(model):
    suppliers = ap.AgentList(model, 5)
    suppliers.pY = ap.AttrIter([1.0, 0.5, 0.25, 0.5, 1.5])
    market = MagicMock()
    market.search_suppliers.return_value = suppliers
    return market


@pytest.fixture
def consumer2(model):
    household = Household(model)
    household.chiY = 10
    return household


def test_search_producers_in_goods_market(consumer2, goods_market1):
    suppliers = consumer2.search_producers(goods_market1)
    goods_market1.search_suppliers.assert_called_with(consumer2.chiY)
    assert set(goods_market1.search_suppliers.return_value) == set(suppliers)
    assert len(goods_market1.search_suppliers.return_value) == len(suppliers)


def test_search_and_rank_producers_by_prices(consumer2, goods_market1):
    suppliers = consumer2.search_producers(goods_market1)
    for i in range(1, len(suppliers)):
        assert suppliers[i - 1].pY <= suppliers[i].pY


@pytest.fixture
def consumer3(model):
    suppliers = ap.AgentList(model, 10)
    suppliers.pY = 10.0
    suppliers.inv = 20.0
    household = Household(model)
    household.search_producers = MagicMock()
    household.search_producers.return_value = suppliers
    return household


@pytest.fixture
def goods_market2():
    return MagicMock()


def goods_purchases(market):
    return [call.args[0] for call in market.buy_goods.call_args_list]


def test_buy_goods_at_desired_level(consumer3, goods_market2):
    consumer3.M = 2000.0
    consumer3.buy_goods(2000.0, goods_market2)
    assert sum(goods_purchases(goods_market2)) == pytest.approx(2000.0)


def test_buy_goods_with_limited_suppliers(consumer3, goods_market2):
    consumer3.M = 3000.0
    consumer3.buy_goods(3000.0, goods_market2)
    assert sum(goods_purchases(goods_market2)) == pytest.approx(2000.0)


def test_buy_goods_with_limited_cash(consumer3, goods_market2):
    consumer3.M = 1000.0
    consumer3.buy_goods(2000.0, goods_market2)
    assert sum(goods_purchases(goods_market2)) == pytest.approx(1000.0)


@pytest.fixture
def goods_markets():
    return {1: MagicMock(), 2: MagicMock()}


@pytest.fixture
def consumer4(model, goods_markets):
    household = Household(model)
    household.plan_consumption = MagicMock()
    household.withdraw_deposits = MagicMock()
    household.buy_goods = MagicMock()
    household.region = MagicMock()
    household.region.goods_markets = goods_markets
    return household


def test_consume_after_planning(consumer4):
    consumer4.C1_star = 100.0
    consumer4.C2_star = 200.0
    consumer4.M = 300.0

    consumer4.consume_goods()
    consumer4.plan_consumption.assert_called_once()


def test_consume_each_goods_types(consumer4, goods_markets):
    consumer4.C1_star = 100.0
    consumer4.C2_star = 200.0
    consumer4.M = 300.0

    consumer4.consume_goods()
    consumer4.buy_goods.assert_any_call(100.0, goods_markets[1])
    consumer4.buy_goods.assert_any_call(200.0, goods_markets[2])


def test_consume_after_withdrawing_deposit(consumer4):
    consumer4.C1_star = 100.0
    consumer4.C2_star = 200.0
    consumer4.M = 50.0

    consumer4.consume_goods()
    consumer4.withdraw_deposits.assert_called_once_with(250.0)
