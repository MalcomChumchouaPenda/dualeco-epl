
import pytest
import agentpy as ap
from mock import MagicMock
from model.agents import Household


#--------------------------------------
# CONSUMPTION BEHAVIORS TESTING
#---------------------------------------

@pytest.fixture
def consumer1():
    model = ap.Model()
    h = Household(model)
    h.alphaY = 0.5
    h.alphaW = 0.2
    h.alpha1 = 0.4
    h.Y_d = 100
    h.W = 50
    return h


def test_plan_desired_consumption(consumer1):
    h = consumer1
    h.plan_consumption()
    assert h.C_star == pytest.approx(0.5*100 + 0.2*50)
    assert h.C1_star == pytest.approx(0.4*h.C_star)
    assert h.C2_star == pytest.approx(0.6*h.C_star)


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
    market = goods_market
    h = consumer1
    h.M = 2000                   # sufficient cash
    h.chiY = 10                  # sufficient matching param  
    h.buy_goods(2000.0, market)
    assert len(called_suppliers(market)) == h.chiY
    assert sum(purchase_amounts(market)) == pytest.approx(2000.0)

def test_buy_goods_with_limited_suppliers(consumer1, goods_market):
    market = goods_market
    h = consumer1
    h = consumer1
    h.M = 2000                  # sufficient cash
    h.chiY = 5                  # limited matching param
    h.buy_goods(2000.0, market)
    assert len(called_suppliers(market)) == h.chiY
    assert sum(purchase_amounts(market)) == pytest.approx(1000.0)

def test_buy_goods_with_limited_cash(consumer1, goods_market):
    market = goods_market
    h = consumer1
    h.M = 1000                     # insufficient cash
    h.chiY = 10                    # sufficient matching param
    h.buy_goods(2000.0, market)
    assert len(called_suppliers(market)) < h.chiY
    assert sum(purchase_amounts(market)) == pytest.approx(1000.0)
    

@pytest.fixture
def consumer2(consumer1):
    h = consumer1
    h.C_star = 300.0
    h.C1_star = 100.0
    h.C2_star = 200.0
    h.plan_consumption = MagicMock()
    h.withdraw_deposits = MagicMock()
    h.buy_goods = MagicMock()
    h.region = MagicMock()
    return h

@pytest.fixture
def goods_markets(consumer2):
    markets = {i:MagicMock() for i in range(1,3)}
    consumer2.region.goods_markets = markets
    return markets


def test_consume_after_planning(consumer2, goods_markets):
    h = consumer2
    h.M = 300.0  
    h.D = 0.0  
    h.consume_goods()
    h.plan_consumption.assert_called_once()
    h.buy_goods.assert_any_call(h.C1_star, goods_markets[1])
    h.buy_goods.assert_any_call(h.C2_star, goods_markets[2])

def test_consume_after_withdrawing_deposit(consumer2, goods_markets):
    h = consumer2
    h.M = 100.0  
    h.D = 100.0  
    h.consume_goods()
    h.withdraw_deposits.assert_called_once_with(100.0)
    h.buy_goods.assert_any_call(h.C1_star, goods_markets[1])
    h.buy_goods.assert_any_call(h.C2_star, goods_markets[2])

