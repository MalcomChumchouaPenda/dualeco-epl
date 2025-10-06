import pytest
import agentpy as ap
from model.environment import LaborMarket 


@pytest.fixture
def model():
    return ap.Model({})

@pytest.fixture
def market(model):
    return LaborMarket(model)


def test_is_network(market):
    assert isinstance(market, ap.Network)


@pytest.fixture
def firm(model):
    return ap.Agent(model)

@pytest.fixture
def private_worker(model):
    worker = ap.Agent(model)
    worker.s_WG = 0
    worker.s_W = 1
    worker.s_U = 0
    worker.s_E = 0
    worker.s_EB = 0
    worker.property = None
    return worker


@pytest.mark.parametrize('s_Y, n_W', [(1, 1), (1, 0), (2, 1), (2, 0)])
def test_pay_private_wages(market, firm, private_worker, s_Y, n_W):
    employee = private_worker
    employee.s_Y = s_Y
    employee.n_W = n_W
    employee.W = 0
    employee.M = 0
    employer = firm
    employer.s_Y = s_Y
    employer.n_W = n_W
    employer.W = 0
    employer.M = 50
    market.pay_wages(20, employer, employee)

    assert employer.W == 20
    assert employer.M == 30
    assert employee.W == 20
    assert employee.M == 20


@pytest.fixture
def government(model):
    government = ap.Agent(model)
    government.n_W = 1
    return government

@pytest.fixture
def public_worker(model):
    worker = ap.Agent(model)
    worker.s_WG = 1
    worker.s_W = 1
    worker.s_U = 0
    worker.s_E = 0
    worker.s_EB = 0
    worker.n_W = 1
    worker.property = None
    return worker


def test_pay_public_wages(market, government, public_worker):
    employer = government
    employer.W = 0
    employer.M = 50
    employee = public_worker
    employee.W = 0
    employee.M = 0
    market.pay_wages(20, employer, employee)

    assert employer.W == 20
    assert employer.M == 30
    assert employee.W == 20
    assert employee.M == 20


@pytest.fixture
def unemployed(model):
    unemployed = ap.Agent(model)
    unemployed.s_WG = 0
    unemployed.s_W = 0
    unemployed.s_U = 1
    unemployed.s_E = 0
    unemployed.s_EB = 0
    unemployed.s_Y = 0
    unemployed.n_W = 0
    unemployed.property = None
    return unemployed


@pytest.mark.parametrize('s_Y, n_W', [(1, 1), (1, 0), (2, 1), (2, 0)])
def test_accept_private_job(market, firm, unemployed, s_Y, n_W):
    employer = firm
    employer.N_J = 1
    employer.s_Y = s_Y
    employer.n_W = n_W
    worker = unemployed
    market.add_agents([worker, employer])

    market.accept_job(worker, employer)
    assert market.graph.has_edge(worker, employer)
    assert employer.N_J == 0
    assert worker.s_WG == 0
    assert worker.s_W == 1
    assert worker.s_E == 0
    assert worker.s_U == 0
    assert worker.s_Y == s_Y
    assert worker.n_W == n_W


def test_accept_public_job(market, government, unemployed):
    employer = government
    employer.N_J = 1
    worker = unemployed
    market.add_agents([worker, employer])

    market.accept_job(worker, employer)
    assert market.graph.has_edge(worker, employer)
    assert employer.N_J == 0
    assert worker.s_WG == 1
    assert worker.s_W == 1
    assert worker.s_E == 0
    assert worker.s_U == 0
    assert worker.s_Y == 0
    assert worker.n_W == 1


@pytest.fixture
def self_employed(model):
    firm = ap.Agent(model)
    self_employed = ap.Agent(model)
    self_employed.s_WG = 0
    self_employed.s_W = 0
    self_employed.s_U = 0
    self_employed.s_E = 1
    self_employed.s_EB = 0
    self_employed.property = firm
    return self_employed


@pytest.mark.parametrize('s_Y, n_W', [(1, 1), (1, 0), (2, 1), (2, 0)])
def test_accept_own_job(market, self_employed, s_Y, n_W):
    employer = self_employed.property
    employer.N_J = 1
    employer.s_Y = s_Y
    employer.n_W = n_W
    worker = self_employed
    worker.s_Y = 0
    worker.n_W = 0
    market.add_agents([worker, employer])

    market.accept_job(worker, employer)
    assert market.graph.has_edge(worker, employer)
    assert employer.N_J == 0
    assert worker.s_WG == 0
    assert worker.s_W == 0
    assert worker.s_E == 1
    assert worker.s_U == 0
    assert worker.s_Y == s_Y
    assert worker.n_W == n_W


@pytest.mark.parametrize('s_Y, n_W', [(1, 1), (1, 0), (2, 1), (2, 0)])
def test_leave_private_job(market, firm, private_worker, s_Y, n_W):
    worker = private_worker
    worker.s_Y = s_Y
    worker.n_W = n_W
    employer = firm
    employer.s_Y = s_Y
    employer.n_W = n_W
    employer.N_J = 1
    market.add_agents([worker, employer])
    market.graph.add_edge(worker, employer)

    market.leave_job(worker, employer)
    assert not market.graph.has_edge(worker, employer)
    assert employer.N_J == 1
    assert worker.s_WG == 0
    assert worker.s_W == 0
    assert worker.s_U == 1
    assert worker.s_E == 0
    assert worker.s_EB == 0
    assert worker.s_Y == 0
    assert worker.n_W == 0


def test_leave_public_job(market, government, public_worker):
    worker = public_worker
    employer = government
    employer.N_J = 1
    market.add_agents([worker, employer])
    market.graph.add_edge(worker, employer)

    market.leave_job(worker, employer)
    assert not market.graph.has_edge(worker, employer)
    assert employer.N_J == 1
    assert worker.s_WG == 0
    assert worker.s_W == 0
    assert worker.s_U == 1
    assert worker.s_E == 0
    assert worker.s_EB == 0
    assert worker.s_Y == 0
    assert worker.n_W == 0


@pytest.mark.parametrize('s_Y, n_W', [(1, 1), (1, 0), (2, 1), (2, 0)])
def test_leave_own_job(market, self_employed, s_Y, n_W):
    worker = self_employed
    worker.s_Y = s_Y
    worker.n_W = n_W
    employer = worker.property
    employer.s_Y = s_Y
    employer.n_W = n_W
    employer.N_J = 1
    market.add_agents([worker, employer])
    market.graph.add_edge(worker, employer)

    market.leave_job(worker, employer)
    assert not market.graph.has_edge(worker, employer)
    assert employer.N_J == 1
    assert worker.s_WG == 0
    assert worker.s_W == 0
    assert worker.s_U == 1
    assert worker.s_E == 0
    assert worker.s_EB == 0
    assert worker.s_Y == 0
    assert worker.n_W == 0

