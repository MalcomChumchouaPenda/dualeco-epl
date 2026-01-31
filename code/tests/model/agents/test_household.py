import pytest
import numpy as np
import agentpy as ap
from mock import MagicMock
from model.agents import Household


@pytest.fixture
def model():
    return ap.Model()


@pytest.fixture
def default_household(model):
    return Household(model)


def test_default_status(default_household):
    household = default_household
    assert household.s_U == 0
    assert household.s_W == 0
    assert household.s_WG == 0
    assert household.s_E == 0
    assert household.s_EB == 0
    assert household.s_Y == 0
    assert household.n_W == 0


def test_default_stocks(default_household):
    household = default_household
    assert household.E == 0
    assert household.E_star == 0
    assert household.D == 0
    assert household.D_star == 0
    assert household.M == 0
    assert household.V == 0


def test_default_flows(default_household):
    household = default_household
    assert household.Z == 0
    assert household.W == 0
    assert household.C1_star == 0
    assert household.C2_star == 0
    assert household.C1 == 0
    assert household.C2 == 0
    assert household.T == 0
    assert household.iota_D == 0
    assert household.Pi_d == 0


def test_default_prices(default_household):
    household = default_household
    assert household.w == 0


def test_default_params(default_household):
    household = default_household
    assert household.delta == 0
    assert household.upsilon == 0
    assert household.chi_N == 0


# def test_default_links(default_household):
#     household = default_household
#     assert household.bank is None
#     assert household.property is None


@pytest.fixture
def random(model, monkeypatch):
    f = MagicMock()
    monkeypatch.setattr(model, "nprandom", f)
    return f


@pytest.fixture
def exp(monkeypatch):
    f = MagicMock()
    monkeypatch.setattr(np, "exp", f)
    return f


@pytest.fixture
def labor_markets(model):
    empty = ap.AgentList(model)
    markets = {}
    for n_W in (0, 1):
        market = MagicMock()
        market.u = 0.5
        market.upsilon = 0.5 * n_W
        market.employers.random.return_value = empty
        markets[n_W] = market
    return markets


@pytest.fixture
def household2(default_household, random, exp, labor_markets):
    household = default_household
    household.upsilon = 0.25
    household.delta = 0.5
    household.w = 1
    household.model.labor_markets = labor_markets
    random.uniform.return_value = 0.25
    exp.return_value = 0.5
    return household


@pytest.mark.parametrize("choice, expected", [(0, 1), (1, 1.25)])
def test_increase_reservation_wage(household2, random, exp, choice, expected):
    random.choice.return_value = choice
    household = household2
    household.s_U = 0
    household.search_job()
    exp.assert_called_with(-0.25)
    random.choice.assert_called_with([0, 1], p=[0.875, 0.125])
    assert household.w == expected


@pytest.mark.parametrize("choice, expected", [(0, 1), (1, 0.75)])
def test_decrease_reservation_wage(household2, random, exp, choice, expected):
    random.choice.return_value = choice
    household = household2
    household.s_U = 1
    household.search_job()
    exp.assert_called_with(-0.25)
    random.choice.assert_called_with([0, 1], p=[0.125, 0.875])
    assert household.w == expected


@pytest.fixture
def household3(household2, random):
    random.choice.return_value = 0
    household = household2
    household.w = 1.5
    household.s_U = 1
    household.s_E = 0
    household.s_W = 0
    household.chi_N = 1
    return household


@pytest.fixture
def employers(model):
    # employers with wages lower than reservation wage
    group_a = ap.AgentList(model, 2)
    for i, employer in enumerate(group_a):
        employer.w = 0.5 * (i + 1)
        employer.N_v = 1

    # employers with wages higher than reservation wage
    group_b = ap.AgentList(model, 2)
    for i, employer in enumerate(group_b):
        employer.w = i + 1
        employer.N_v = 1

    # employers with no vacancies
    group_c = ap.AgentList(model, 2)
    for i, employer in enumerate(group_c):
        employer.w = i + 1
        employer.N_v = 0
    return {"low_wages": group_a, "high_wages": group_b, "no_vacancies": group_c}


@pytest.mark.parametrize(
    "formal, informal",
    [
        ("high_wages", "low_wages"),  # high formal wages + low informal wages
        ("high_wages", "high_wages"),  # high formal wages + high informal wages
        ("high_wages", "no_vacancies"),
    ],
)  # high formal wages + no informal vacancies
def test_unemployed_prefer_best_formal_job(household3, employers, formal, informal):
    household = household3
    labor_markets = household.model.labor_markets
    labor_markets[1].employers.random.return_value = employers[formal]
    labor_markets[0].employers.random.return_value = employers[informal]

    household.search_job()
    labor_markets[1].employers.random.assert_called_with(household.chi_N)
    labor_markets[0].employers.random.assert_not_called()
    labor_markets[1].accept_job.assert_called_with(household, employers[formal][-1])


@pytest.mark.parametrize(
    "formal, informal",
    [
        ("low_wages", "high_wages"),  # low formal wages + high informal wages
        ("no_vacancies", "high_wages"),
    ],
)
def test_unemployed_prefer_best_informal_job(household3, employers, formal, informal):
    household = household3
    labor_markets = household.model.labor_markets
    labor_markets[1].employers.random.return_value = employers[formal]
    labor_markets[0].employers.random.return_value = employers[informal]

    household.search_job()
    labor_markets[1].employers.random.assert_called_with(household.chi_N)
    labor_markets[0].employers.random.assert_called_with(household.chi_N)
    labor_markets[1].accept_job.assert_not_called()
    labor_markets[0].accept_job.assert_called_with(household, employers[informal][-1])


@pytest.mark.parametrize(
    "formal, informal",
    [
        ("no_vacancies", "no_vacancies"),
        ("no_vacancies", "low_wages"),
        ("low_wages", "no_vacancies"),
        ("low_wages", "low_wages"),
    ],
)
def test_remain_unemployed(household3, employers, formal, informal):
    household = household3
    labor_markets = household.model.labor_markets
    labor_markets[1].employers.random.return_value = employers[formal]
    labor_markets[0].employers.random.return_value = employers[informal]

    household.search_job()
    labor_markets[1].employers.random.assert_called_with(household.chi_N)
    labor_markets[0].employers.random.assert_called_with(household.chi_N)
    labor_markets[1].accept_job.assert_not_called()
    labor_markets[0].accept_job.assert_not_called()


@pytest.fixture
def household4(household3):
    household = household3
    household.s_U = 0
    household.s_E = 0
    household.s_W = 1
    household.n_W = 0
    household._old_employer = MagicMock()
    labor_market = household.model.labor_markets[0]
    labor_market.neighbors.return_value = [household._old_employer]
    return household


@pytest.mark.parametrize(
    "formal, informal",
    [
        ("high_wages", "low_wages"),
        ("high_wages", "high_wages"),
        ("high_wages", "no_vacancies"),
    ],
)
def test_informal_worker_prefer_formal_job(household4, employers, formal, informal):
    household = household4
    old_employer = household._old_employer
    labor_markets = household.model.labor_markets
    labor_markets[1].employers.random.return_value = employers[formal]
    labor_markets[0].employers.random.return_value = employers[informal]

    household.search_job()
    labor_markets[1].employers.random.assert_called_with(household.chi_N)
    labor_markets[0].employers.random.assert_not_called()
    labor_markets[1].accept_job.assert_called_with(household, employers[formal][-1])
    labor_markets[0].accept_job.assert_not_called()
    labor_markets[1].leave_job.assert_not_called()
    labor_markets[0].leave_job.assert_called_with(household, old_employer)


@pytest.mark.parametrize(
    "formal, informal",
    [
        ("low_wages", "low_wages"),
        ("low_wages", "high_wages"),
        ("low_wages", "no_vacancies"),
        ("no_vacancies", "low_wages"),
        ("no_vacancies", "high_wages"),
        ("no_vacancies", "no_vacancies"),
    ],
)
def test_informal_worker_remain_informal(household4, employers, formal, informal):
    household = household4
    labor_markets = household.model.labor_markets
    labor_markets[1].employers.random.return_value = employers[formal]
    labor_markets[0].employers.random.return_value = employers[informal]

    household.search_job()
    labor_markets[1].employers.random.assert_called_with(household.chi_N)
    labor_markets[0].employers.random.assert_not_called()
    labor_markets[1].accept_job.assert_not_called()
    labor_markets[0].accept_job.assert_not_called()
    labor_markets[1].leave_job.assert_not_called()
    labor_markets[0].leave_job.assert_not_called()


@pytest.fixture
def household5(household3):
    household = household3
    household.s_U = 0
    household.s_E = 1
    household.s_W = 0
    household.n_W = 0
    household._old_employer = MagicMock()
    labor_market = household.model.labor_markets[0]
    labor_market.neighbors.return_value = [household._old_employer]
    return household


@pytest.mark.parametrize(
    "formal, informal",
    [
        ("high_wages", "low_wages"),
        ("high_wages", "high_wages"),
        ("high_wages", "no_vacancies"),
    ],
)
def test_informal_entrepreneur_prefer_formal_job(
    household5, employers, formal, informal
):
    household = household5
    old_employer = household._old_employer
    labor_markets = household.model.labor_markets
    labor_markets[1].employers.random.return_value = employers[formal]
    labor_markets[0].employers.random.return_value = employers[informal]

    household.search_job()
    labor_markets[1].employers.random.assert_called_with(household.chi_N)
    labor_markets[0].employers.random.assert_not_called()
    labor_markets[1].accept_job.assert_called_with(household, employers[formal][-1])
    labor_markets[0].accept_job.assert_not_called()
    labor_markets[1].leave_job.assert_not_called()
    labor_markets[0].leave_job.assert_called_with(household, old_employer)


@pytest.mark.parametrize(
    "formal, informal",
    [
        ("low_wages", "low_wages"),
        ("low_wages", "high_wages"),
        ("low_wages", "no_vacancies"),
        ("no_vacancies", "low_wages"),
        ("no_vacancies", "high_wages"),
        ("no_vacancies", "no_vacancies"),
    ],
)
def test_informal_entrepreneur_remain_informal(household5, employers, formal, informal):
    household = household5
    labor_markets = household.model.labor_markets
    labor_markets[1].employers.random.return_value = employers[formal]
    labor_markets[0].employers.random.return_value = employers[informal]

    household.search_job()
    labor_markets[1].employers.random.assert_called_with(household.chi_N)
    labor_markets[0].employers.random.assert_not_called()
    labor_markets[1].accept_job.assert_not_called()
    labor_markets[0].accept_job.assert_not_called()
    labor_markets[1].leave_job.assert_not_called()
    labor_markets[0].leave_job.assert_not_called()


@pytest.fixture
def household6(household3):
    household = household3
    household.s_U = 0
    household.n_W = 1
    household._old_employer = MagicMock()
    labor_market = household.model.labor_markets[0]
    labor_market.neighbors.return_value = [household._old_employer]
    return household


@pytest.mark.parametrize(
    "formal, informal",
    [
        ("low_wages", "low_wages"),
        ("low_wages", "high_wages"),
        ("low_wages", "no_vacancies"),
        ("high_wages", "low_wages"),
        ("high_wages", "high_wages"),
        ("high_wages", "no_vacancies"),
        ("no_vacancies", "low_wages"),
        ("no_vacancies", "high_wages"),
        ("no_vacancies", "no_vacancies"),
    ],
)
def test_no_search_from_formal_entrepreneur(household6, employers, formal, informal):
    household = household6
    household.s_E = 1
    household.s_W = 0
    labor_markets = household.model.labor_markets
    labor_markets[1].employers.random.return_value = employers[formal]
    labor_markets[0].employers.random.return_value = employers[informal]

    household.search_job()
    labor_markets[1].employers.random.assert_not_called()
    labor_markets[0].employers.random.assert_not_called()
    labor_markets[1].accept_job.assert_not_called()
    labor_markets[0].accept_job.assert_not_called()
    labor_markets[1].leave_job.assert_not_called()
    labor_markets[0].leave_job.assert_not_called()


@pytest.mark.parametrize(
    "formal, informal",
    [
        ("low_wages", "low_wages"),
        ("low_wages", "high_wages"),
        ("low_wages", "no_vacancies"),
        ("high_wages", "low_wages"),
        ("high_wages", "high_wages"),
        ("high_wages", "no_vacancies"),
        ("no_vacancies", "low_wages"),
        ("no_vacancies", "high_wages"),
        ("no_vacancies", "no_vacancies"),
    ],
)  # no formal vacancies + high informal wages
def test_no_search_from_formal_worker(household6, employers, formal, informal):
    household = household6
    household.s_E = 0
    household.s_W = 1
    labor_markets = household.model.labor_markets
    labor_markets[1].employers.random.return_value = employers[formal]
    labor_markets[0].employers.random.return_value = employers[informal]

    household.search_job()
    labor_markets[1].employers.random.assert_not_called()
    labor_markets[0].employers.random.assert_not_called()
    labor_markets[1].accept_job.assert_not_called()
    labor_markets[0].accept_job.assert_not_called()
    labor_markets[1].leave_job.assert_not_called()
    labor_markets[0].leave_job.assert_not_called()


@pytest.fixture
def household_as_tax_payer(default_household):
    household = default_household
    household.W = 100
    household.Pi_d = 50
    household.iota_D = 50

    economy = MagicMock()
    economy.tau = 0.1
    government = ap.Agent(household.model)
    model = household.model
    model.economy = economy
    model.government = government
    return household


def test_compute_taxable_income(household_as_tax_payer):
    household = household_as_tax_payer
    household.pay_taxes()
    assert household.Y == 200


def test_pay_taxes(household_as_tax_payer):
    household = household_as_tax_payer
    household.pay_taxes()
    gov = household.model.government
    economy = household.model.economy
    economy.pay_taxes.assert_called_with(20, household, gov)


@pytest.fixture
def household_as_consumer(default_household):
    household = default_household
    household.alphaY = 0.8
    household.alphaV = 0.2
    household.alphaC1 = 0.6
    household.chiY = 2
    household.Y = 1000
    household.Z = 300
    household.T = 200
    household.D = 3000
    household.M = 2000

    model = household.model
    model.goods_markets = {}
    for sector in (1, 2):
        market = MagicMock()
        market.suppliers = ap.AgentList(model, 4)
        market.suppliers.p_Y = 1
        market.suppliers.y_inv = 1000
        model.goods_markets[sector] = market
    return household


def test_set_desired_consumption(household_as_consumer):
    household = household_as_consumer
    expected_C_star = 0.8 * 1100 + 0.2 * 5000
    expected_C1_star = 0.6 * expected_C_star
    expected_C2_star = 0.4 * expected_C_star

    household.consume_goods()
    C1_star = household.C1_star
    C2_star = household.C2_star
    assert abs(C1_star - expected_C1_star) < 1e-6
    assert abs(C2_star - expected_C2_star) < 1e-6


def test_sample_goods_suppliers(household_as_consumer):
    household = household_as_consumer
    household.D = 3000
    household.M = 2000
    market1 = household.model.goods_markets[1]
    market2 = household.model.goods_markets[2]

    household.consume_goods()
    called_suppliers1 = [call.args[2] for call in market1.consume_goods.call_args_list]
    called_suppliers2 = [call.args[2] for call in market2.consume_goods.call_args_list]
    assert len(set(called_suppliers1)) == household.chiY
    assert len(set(called_suppliers2)) == household.chiY


def test_consume_at_desired_level(household_as_consumer):
    household = household_as_consumer
    household.D = 3000
    household.M = 2000
    market1 = household.model.goods_markets[1]
    market2 = household.model.goods_markets[2]

    household.consume_goods()
    purchased_amount1 = [call.args[0] for call in market1.consume_goods.call_args_list]
    purchased_amount2 = [call.args[0] for call in market2.consume_goods.call_args_list]
    assert abs(sum(purchased_amount1) - household.C1_star) < 1e-6
    assert abs(sum(purchased_amount2) - household.C2_star) < 1e-6
