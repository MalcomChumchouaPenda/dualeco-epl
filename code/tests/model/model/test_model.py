
import pytest
import numpy as np

from model.model import DualEcoModel
from model import agents as ag
from model import environment as env
from utils.analysis import sum_params, create_matrices_from_params


@pytest.fixture 
def sample():
    np.random.seed = 0
    return [{
        'g':np.random.random(),               # taux de croissance
        'N_E1':np.random.randint(1, 25),      # nombre de entrepreneurs dans le secteur productif 1
        'N_E2':np.random.randint(1, 25),      # nombre de entrepreneurs dans le secteur productif 2
        'N_W1':np.random.randint(1, 25),      # nombre de salaries dans le secteur productif 1
        'N_W2':np.random.randint(1, 25),      # nombre de salaries dans le secteur productif 2
        'N_WG':np.random.randint(1, 25),      # nombre de salaries dans le secteur public
        'N_U':np.random.randint(1, 25),       # nombre de chomeurs dans le secteur public
        'N_B':np.random.randint(1, 10),       # nombre de banques
        'phi1':np.random.uniform(0.5, 2.5),   # productivite initial du secteur productif 1
        'phi2':np.random.uniform(0.5, 2.5),   # productivite initial du secteur productif 2
        'w1':np.random.uniform(0.5, 2.5),     # salaire initial du secteur productif 1
        'w2':np.random.uniform(0.5, 2.5),     # salaire initial du secteur productif 2
        'w_G':np.random.uniform(0.5, 2.5),    # salaire public
        'w_min':np.random.uniform(0.5, 2.5),  # salaire minimum
        'tau': np.random.random(),            # taux d'impots
        'rho': np.random.random(),            # politique de dividende
        'delta': np.random.random(),          # parametre d'ajustement
        'upsilon_F': np.random.random(),      # parametre d'ajustement des salaires des firmes
        'm':np.random.random(),               # taux de marge brute
        'theta_W':np.random.random(),         # proportion desire de fonds de salaire
        'theta_E':np.random.random(),         # proportion desire de capitaux bancaire (rentabilite)
        'theta_M':np.random.random(),         # proportion desire de liquidite
        'theta_y':np.random.random(),         # proportion desire de sotck d'invendus
        'kappa_Z':np.random.random(),         # proportion reglementaire des allocations publics
        'kappa_E':np.random.random(),         # ratio minimum de capital bancaire
        'kappa_R':np.random.random(),         # ratio minimum de liquidite bancaire
        'beta_L':np.random.random(),          # elasticite du taux d'interet du credit au levier financier
        'gamma_L':np.random.random(),         # elasticite de la probabilite de credit au levier financier
        'r_D': np.random.random(),            # taux d'interet sur les depots bancaires
        'r_L': np.random.random(),            # taux d'interet sur les credits bancaires
        'r_B': np.random.random(),            # taux d'interet sur les bons du tresors
        'r_A': np.random.random(),            # taux d'interet sur les avances de la Banque Centrale
    } for _ in range(5)]


@pytest.fixture
def models1(sample):
    models = []
    for params in sample:
        model = DualEcoModel(params)
        model.init_params()
        models.append(model)
    return models


def test_has_empty_stocks_and_flows(models1):
    for model in models1:
        stocks, flows = create_matrices_from_params(model.p, digits=2)
        print('stocks\n', stocks, '\nflows\n', flows)
        for key in flows.index:
            assert flows.loc[key, 'sigma'] == 0
        for key in stocks.index:
            assert stocks.loc[key, 'sigma'] == 0


def test_calc_firms_stocks_and_flows(models1):
    for model in models1:
        model.calc_block_1()
        stocks, flows = create_matrices_from_params(model.p, digits=2)
        print('stocks\n', stocks, '\nflows\n', flows)
        assert stocks.loc['Y_inv', 'sigma'] > 0
        assert stocks.loc['sigma', 'F'] == 0.0
        assert flows.loc['sigma', 'F'] == 0.0


def test_calc_banks_stocks_and_flows(models1):
    for model in models1:
        model.calc_block_1()
        model.calc_block_2()
        stocks, flows = create_matrices_from_params(model.p, digits=2)
        print('stocks\n', stocks, '\nflows\n', flows)
        assert stocks.loc['sigma', 'B'] == 0
        assert flows.loc['sigma', 'B'] == 0


def test_calc_households_stocks_and_flows(models1):
    for model in models1:
        model.calc_block_1()
        model.calc_block_2()
        model.calc_block_3()
        stocks, flows = create_matrices_from_params(model.p, digits=2)
        print('stocks\n', stocks, '\nflows\n', flows)
        assert stocks.loc['sigma', 'H'] == 0
        assert flows.loc['sigma', 'H'] == 0


def test_calc_public_sector_stocks_and_flows(models1):
    for model in models1:
        model.calc_block_1()
        model.calc_block_2()
        model.calc_block_3()
        model.calc_block_4()
        stocks, flows = create_matrices_from_params(model.p, digits=2)
        print('stocks\n', stocks, '\nflows\n', flows)
        assert stocks.loc['sigma', 'G'] == 0
        assert stocks.loc['sigma', 'CB'] == 0
        assert flows.loc['sigma', 'G'] == 0
        assert flows.loc['sigma', 'CB'] == 0
        

def test_is_globally_stock_consistent(models1):
    for model in models1:
        model.calc_block_1()
        model.calc_block_2()
        model.calc_block_3()
        model.calc_block_4()
        stocks, flows = create_matrices_from_params(model.p, digits=2)
        print('stocks\n', stocks, '\nflows\n', flows)
        for key in stocks.index:
            if key not in ['Y_inv', 'V']:
                assert stocks.loc[key, 'sigma'] == 0


def test_is_globally_flow_consistent(models1):
    for model in models1:
        model.calc_block_1()
        model.calc_block_2()
        model.calc_block_3()
        model.calc_block_4()
        stocks, flows = create_matrices_from_params(model.p, digits=2)
        print('stocks\n', stocks, '\nflows\n', flows)
        for key in flows.index:
            assert flows.loc[key, 'sigma'] == 0


@pytest.fixture
def models2(models1):
    models = []
    for model in models1:
        model.calc_block_1()
        model.calc_block_2()
        model.calc_block_3()
        model.calc_block_4()
        models.append(model)
    return models


def test_create_sufficient_households(models2):
    for model in models2:
        model.create_households()
        p = model.p
        assert sum_params(p, 'N') == len(model.households)
        for household in model.households:
            assert isinstance(household, ag.Household)
            assert household.delta == p['delta']


def test_create_sufficient_owners(models2):
    for model in models2:
        model.create_households()
        p = model.p
        households = model.households
        owners = households.select(households.s_E == 1)
        assert sum_params(p, 'N_B') == len(owners.select(owners.s_EB == 1))
        assert sum_params(p, 'N_E') == len(owners.select(owners.s_EB == 0))
        for s in model.sectors:
            assert sum_params(p, f'N_E{s}') == len(owners.select(owners.s_Y == s))


def test_create_sufficient_workers(models2):
    for model in models2:
        model.create_households()
        p = model.p
        households = model.households
        workers = households.select(households.s_W == 1)
        assert sum_params(p, 'N_WG') == len(workers.select(workers.s_WG==1))
        assert sum_params(p, 'N_WG') == len(workers.select(workers.s_Y==0))
        for s in model.sectors:
            assert sum_params(p, f'N_W{s}') == len(workers.select(workers.s_Y==s))


def test_create_sufficient_unemployed(models2):
    for model in models2:
        model.create_households()
        p = model.p
        households = model.households
        assert sum_params(p, 'N_U') == len(households.select(households.s_U == 1))


def test_create_firms(models2):
    for model in models2:
        model.create_firms()
        p = model.p
        N = sum_params(p, 'N_E')
        assert N == len(model.firms)
        for firm in model.firms:
            assert isinstance(firm, ag.Firm)
            assert firm.m == p['m']
            assert firm.delta == p['delta']
            assert firm.theta_y == p['theta_y']
            assert firm.upsilon_F == p['upsilon_F']


def test_create_firms_by_sectors(models2):
    for model in models2:
        model.create_firms()
        p = model.p
        firms = model.firms
        for s in model.sectors:
            formal = 1 if s == 1 else 0
            group = firms.select(firms.s_Y == s)
            assert p[f'N_E{s}'] == len(group)
            for firm in group:
                assert firm.n_W == formal
                assert firm.n_T == formal
                assert firm.phi == p[f'phi{s}']


def test_create_banks(models2):
    for model in models2:
        model.create_banks()
        p = model.p
        N = sum_params(p, 'N_B')
        assert N == len(model.banks)
        for bank in model.banks:
            assert isinstance(bank, ag.Bank)
            assert bank.delta == p['delta']
            assert bank.kappa_E == p['kappa_E']
            assert bank.kappa_R == p['kappa_R']
            assert bank.gamma_L == p['gamma_L']
            assert bank.beta_L == p['beta_L']


def test_create_public_sector(models2):
    for model in models2:
        model.create_public_sector()
        assert isinstance(model.government, ag.Government)
        assert isinstance(model.central_bank, ag.CentralBank)


@pytest.fixture
def models3(models2):
    models = []
    for model in models2:
        model.create_households()
        model.create_firms()
        model.create_banks()
        model.create_public_sector()
        models.append(model)
    return models


def test_create_good_markets(models3):
    for model in models3:
        model.create_good_markets()
        firms = model.firms
        for s, market in model.good_markets.items():
            agents = market.agents.to_list()
            group = firms.select(firms.s_Y == s)
            assert isinstance(market, env.GoodMarket)
            assert market.s_Y == s
            assert set(group) == set(agents)
            assert set(group) == set(market.suppliers)


def test_create_labor_markets(models3):
    for model in models3:
        model.create_labor_markets()
        for n, market in model.labor_markets.items():
            assert isinstance(market, env.LaborMarket)
            assert market.n_W == n


def test_populate_formal_labor_market(models3):
    for model in models3:
        model.create_labor_markets()
        market = model.labor_markets[1]
        agents = market.agents.to_list()
        workers = market.workers
        employers = market.employers
        government = model.government
        firms = model.firms
        households = model.households
        group = firms.select(firms.s_Y == 1)
        assert set(group).issubset(set(agents))
        assert set(group).issubset(set(employers))
        assert set(households).issubset(set(agents))
        assert not set(households).issubset(set(employers))
        assert set(households) == set(workers)
        assert government in set(agents)
        assert government in set(employers)
        assert len(agents) == len(households + group) + 1


def test_setup_formal_labor_networks(models3):
    for model in models3:
        model.create_labor_markets()
        p = model.p
        min_ratio = (p['N_E1'] + p['N_W1']) // p['N_E1']
        max_ratio = min_ratio + 1
        market = model.labor_markets[1]
        government = model.government
        firms = model.firms
        for firm in firms.select(firms.s_Y==1):
            employees = market.neighbors(firm).to_list()
            assert len(employees) in [min_ratio, max_ratio]
        assert len(market.neighbors(government).to_list()) == p['N_WG']


def test_populate_informal_labor_market(models3):
    for model in models3:
        model.create_labor_markets()
        market = model.labor_markets[0]
        agents = market.agents.to_list()
        employers = market.employers
        firms = model.firms
        households = model.households
        group = firms.select(firms.s_Y == 2)
        assert set(group) == set(employers)
        assert set(group).issubset(set(agents))
        assert set(households).issubset(set(agents))
        assert not set(households).issubset(set(employers))
        assert len(agents) == len(households + group)


def test_setup_informal_labor_networks(models3):
    for model in models3:
        model.create_labor_markets()
        p = model.p
        min_ratio = (p['N_E2'] + p['N_W2']) // p['N_E2']
        max_ratio = min_ratio + 1
        market = model.labor_markets[0]
        firms = model.firms
        group = firms.select(firms.s_Y == 2)
        for firm in group:
            employees = market.neighbors(firm).to_list()
            assert len(employees) in [min_ratio, max_ratio]


def test_create_bond_market(models3):
    for model in models3:
        model.create_bond_market()
        market = model.bond_market
        agents = market.agents.to_list()
        banks = model.banks
        government = model.government
        central_bank = model.central_bank
        assert isinstance(market, env.BondMarket)
        assert government in set(agents)
        assert central_bank in set(agents)
        assert set(banks).issubset(set(agents))
        assert len(agents) == len(banks) + 2


def test_create_deposit_market(models3):
    for model in models3:
        model.create_deposit_market()
        market = model.deposit_market
        agents = market.agents.to_list()
        banks = model.banks
        firms = model.firms
        formal_firms = firms.select(firms.s_Y==1)
        households = model.households
        assert isinstance(market, env.DepositMarket)
        assert set(households).issubset(set(agents))
        assert set(formal_firms).issubset(set(agents))
        assert set(banks).issubset(set(agents))
        assert len(agents) == len(households + formal_firms + banks)


def test_setup_initial_deposit_networks(models3):
    for model in models3:
        model.create_deposit_market()
        market = model.deposit_market
        banks = model.banks
        firms = model.firms
        formal_firms = firms.select(firms.s_Y==1)
        households = model.households
        num_clients = len(households + formal_firms)
        min_ratio = num_clients // len(banks)
        max_ratio = min_ratio + 1
        for bank in banks:
            clients = market.neighbors(bank).to_list()
            assert len(clients) in [min_ratio, max_ratio]
            for client in clients:
                assert client.bank == bank
        

def test_create_credit_market(models3):
    for model in models3:
        model.create_deposit_market()
        model.create_credit_market()
        market = model.credit_market
        agents = market.agents.to_list()
        banks = model.banks
        firms = model.firms
        formal_firms = firms.select(firms.s_Y==1)
        assert isinstance(market, env.CreditMarket)
        assert set(formal_firms).issubset(set(agents))
        assert set(banks).issubset(set(agents))
        assert len(agents) == len(formal_firms + banks)


def test_setup_initial_credit_networks(models3):
    for model in models3:
        model.create_deposit_market()
        model.create_credit_market()
        market = model.credit_market
        banks = model.banks
        firms = model.firms
        formal_firms = firms.select(firms.s_Y==1)
        min_ratio = len(formal_firms) // len(banks)
        max_ratio = min_ratio + 1
        for bank in banks:
            clients = market.neighbors(bank).to_list()
            assert len(clients) in [min_ratio, max_ratio]
            for client in clients:
                assert client.bank == bank
            


def test_create_economy(models3):
    for model in models3:
        model.create_economy()
        firms = model.firms
        households = model.households
        agents = model.economy.agents.to_list()
        assert set(households).issubset(set(agents))
        assert set(firms).issubset(set(agents))
        assert len(agents) == len(firms + households)


def test_setup_initial_firms_ownership(models3):
    for model in models3:
        model.create_economy()
        firms = model.firms
        households = model.households
        owners = households.select(households.s_E == 1)
        for s in model.sectors:
            sector_firms = firms.select(firms.s_Y == s)
            sector_owners = owners.select(owners.s_Y == s)
            for firm in sector_firms:
                assert firm.owner in sector_owners


def test_setup_initial_banks_ownership(models3):
    for model in models3:
        model.create_economy()
        banks = model.banks
        households = model.households
        owners = households.select(households.s_EB == 1)
        for bank in banks:
            assert bank.owner in owners


@pytest.fixture
def models4(models3):
    models = []
    for model in models3:
        model.create_good_markets()
        model.create_labor_markets()
        model.create_deposit_market()
        model.create_credit_market()
        model.create_bond_market()
        model.create_economy()
        models.append(model)
    return models


def test_share_initial_firm_equities(models4):
    for model in models4:
        model.share_initial_equities()
        p = model.p
        firms = model.firms
        households = model.households
        for s in model.sectors:
            owners = households.select(households.s_E == 1)
            owners = owners.select(owners.s_Y == s)
            group = firms.select(firms.s_Y == s)
            assert round(sum(group.E), 2) == round(p[f'E_F{s}'], 2)
            assert round(sum(group.E), 2) == round(sum(owners.E), 2)
            for firm in group:
                assert round(firm.E, 2) == round(firm.owner.E, 2)


def test_share_initial_bank_equities(models4):
    for model in models4:
        model.share_initial_equities()
        p = model.p
        banks = model.banks
        households = model.households
        owners = households.select(households.s_EB == 1)
        assert round(sum(banks.E), 2) == round(p[f'E_B'], 2)
        assert round(sum(banks.E), 2) == round(sum(owners.E), 2)
        for bank in banks:
            assert round(bank.E, 2) == round(bank.owner.E, 2)


def test_share_initial_firm_credits(models4):
    for model in models4:
        model.share_initial_equities()
        model.share_initial_credits()
        p = model.p
        firms = model.firms
        for s in model.sectors:
            group = firms.select(firms.s_Y==s) 
            assert round(p[f'L_F{s}'], 2) == round(sum(group.L), 2)
            assert round(p[f'iota_LF{s}'], 2) == round(sum(group.iota_L), 2)


def test_share_initial_bank_credits(models4):
    for model in models4:
        model.share_initial_equities()
        model.share_initial_credits()
        p = model.p
        banks = model.banks
        credit_market = model.credit_market
        assert round(p['L_B'], 2) == round(sum(banks.L), 2)
        assert round(p['iota_LB'], 2) == round(sum(banks.iota_L), 2)
        for bank in banks:
            clients = credit_market.neighbors(bank).to_list()
            assert round(sum(clients.L), 2) == round(bank.L, 2)
            assert round(sum(clients.iota_L), 2) == round(bank.iota_L, 2)


def test_share_initial_household_deposits(models4):
    for model in models4:
        model.share_initial_equities()
        model.share_initial_credits()
        model.share_initial_deposits()
        p = model.p
        households = model.households
        assert round(p['D_H'], 2) == round(sum(households.D), 2)
        assert round(p['iota_DH'], 2) == round(sum(households.iota_D), 2)


def test_share_initial_firm_deposits(models4):
    for model in models4:
        model.share_initial_equities()
        model.share_initial_credits()
        model.share_initial_deposits()
        p = model.p
        firms = model.firms
        for s in model.sectors:
            group = firms.select(firms.s_Y==s) 
            assert round(p[f'D_F{s}'], 2) == round(sum(group.D), 2)
            assert round(p[f'iota_DF{s}'], 2) == round(sum(group.iota_D), 2)


def test_share_initial_bank_deposits(models4):
    for model in models4:
        model.share_initial_equities()
        model.share_initial_credits()
        model.share_initial_deposits()
        p = model.p
        banks = model.banks
        deposit_market = model.deposit_market
        assert round(p['D_B'], 2) == round(sum(banks.D), 2)
        assert round(p['iota_DB'], 2) == round(sum(banks.iota_D), 2)
        for bank in banks:
            clients = deposit_market.neighbors(bank).to_list()
            assert round(sum(clients.D), 2) == round(bank.D, 2)
            assert round(sum(clients.iota_D), 2) == round(bank.iota_D, 2)


def test_share_initial_bonds(models4):
    for model in models4:
        model.share_initial_equities()
        model.share_initial_credits()
        model.share_initial_deposits()
        model.share_initial_bonds()
        p = model.p
        banks = model.banks
        government = model.government
        central_bank = model.central_bank
        assert round(p['B_B'], 2) == round(sum(banks.B), 2)
        assert round(p['B_G'], 2) == round(government.B, 2)
        assert round(p['B_CB'], 2) == round(central_bank.B, 2)
        assert round(p['iota_BB'], 2) == round(sum(banks.iota_B), 2)
        assert round(p['iota_BG'], 2) == round(government.iota_B, 2)
        assert round(p['iota_BCB'], 2) == round(central_bank.iota_B, 2)
        assert government.r_B == p['r_B']


def test_share_initial_private_sector_cash(models4):
    for model in models4:
        model.share_initial_equities()
        model.share_initial_credits()
        model.share_initial_deposits()
        model.share_initial_bonds()
        model.share_initial_cash()
        p = model.p
        households = model.households
        banks = model.banks
        firms = model.firms
        for s in model.sectors:
            group = firms.select(firms.s_Y==s)
            assert round(p[f'M_F{s}'], 2) == round(sum(group.M), 2)
        assert round(p['M_H'], 2) == round(sum(households.M), 2)
        assert round(p['M_B'], 2) == round(sum(banks.M), 2)
        assert round(p['A_B'], 2) == round(sum(banks.A), 2)
        assert round(p['iota_AB'], 2) == round(sum(banks.iota_A), 2)
        assert set(banks.r_A) == {p['r_A']}


def test_share_initial_public_sector_cash(models4):
    for model in models4:
        model.share_initial_equities()
        model.share_initial_credits()
        model.share_initial_deposits()
        model.share_initial_bonds()
        model.share_initial_cash()
        p = model.p
        government = model.government
        central_bank = model.central_bank
        assert round(p['M_G'], 2) == round(government.M, 2)
        assert round(p['M_CB'], 2) == round(central_bank.M, 2)
        assert round(p['A_CB'], 2) == round(central_bank.A, 2)
        assert round(p['iota_ACB'], 2) == round(central_bank.iota_A, 2)


def test_share_initial_production(models4):
    for model in models4:
        model.share_initial_equities()
        model.share_initial_credits()
        model.share_initial_deposits()
        model.share_initial_bonds()
        model.share_initial_cash()
        model.share_initial_production()
        p = model.p
        firms = model.firms
        for s in model.sectors:
            group = firms.select(firms.s_Y==s)
            assert round(sum(group.y_D), 2) == 0
            assert round(sum(group.Y_inv), 2) == round(p[f'Y_inv{s}'], 2) 
            assert round(sum(group.y_inv), 2) == round(p[f'y_inv{s}'], 2) 
            assert round(sum(group.y), 2) == round(p[f'Q{s}'] / p[f'p{s}'], 2)
            assert round(sum(group.q_e), 2) == round(p[f'Q{s}'] / p[f'p{s}'], 2)
            assert round(sum(group.Q), 2) == round(p[f'Q{s}'], 2)  
            assert set(group.p_Y) == {p[f'p{s}']}


@pytest.fixture
def models5(models4):
    models = []
    for model in models4:
        model.share_initial_equities()
        model.share_initial_credits()
        model.share_initial_deposits()
        model.share_initial_bonds()
        model.share_initial_cash()
        model.share_initial_production()
        models.append(model)
    return models


def test_share_initial_household_wages(models5):
    for model in models5:
        model.share_initial_wages()
        p = model.p
        households = model.households
        unemployed = households.select(households.s_U == 1)
        public_workers = households.select(households.s_WG == 1)
        for s in model.sectors:
            sector_workers = households.select(households.s_Y == s)
            assert round(sum(sector_workers.W), 2) == round(p[f'W_F{s}'], 2)
            assert set(sector_workers.w_D) == {p[f'w{s}']} 
        assert round(sum(public_workers.W), 2) == round(p['W_G'], 2) 
        assert round(sum(households.W), 2) == round(p['W_H'], 2)   
        assert set(public_workers.w_D) == {p['w_G']}
        assert set(unemployed.w_D) == {p['w_min']}


def test_share_initial_firm_wages(models5):
    for model in models5:
        model.share_initial_wages()
        p = model.p
        firms = model.firms
        for s in model.sectors:
            group = firms.select(firms.s_Y==s)
            assert round(sum(group.N_Jc), 2) == 0
            assert round(sum(group.N_Jd), 2) == 0
            assert round(sum(group.l_D), 2) == 0
            assert round(sum(group.W), 2) == round(p[f'W_F{s}'], 2)  
            assert round(sum(group.l), 2) == round(p[f'Q{s}'] / p[f'w{s}'], 2)
            assert set(group.w) == {p[f'w{s}']}


def test_share_initial_public_wages(models5):
    for model in models5:
        model.share_initial_wages()
        p = model.p
        government = model.government 
        assert round(government.W, 2) == round(p['W_G'], 2)
        assert government.w == p['w_G']


def test_share_initial_transfers(models5):
    for model in models5:
        model.share_initial_wages()
        model.share_initial_transfers()
        p = model.p
        households = model.households
        unemployed = households.select(households.s_U == 1) 
        assert round(p['Z_H'], 2) == round(sum(households.Z), 2)   
        assert round(p['Z_G'], 2) == round(sum(unemployed.Z), 2) 


def test_share_initial_firms_profits(models5):
    for model in models5:
        model.share_initial_wages()
        model.share_initial_transfers()
        model.share_initial_profits()
        p = model.p
        households = model.households
        owners = households.select(households.s_E == 1)
        firms = model.firms
        for s in model.sectors:
            sector_firms = firms.select(firms.s_Y == s)
            sector_owners = owners.select(owners.s_Y == s)
            assert round(p[f'Pi_dF{s}'], 2) == round(sum(sector_firms.Pi_d), 2)
            assert round(p[f'Pi_dF{s}'], 2) == round(sum(sector_owners.Pi_d), 2)


def test_share_initial_banks_profits(models5):
    for model in models5:
        model.share_initial_wages()
        model.share_initial_transfers()
        model.share_initial_profits()
        p = model.p
        banks = model.banks
        households = model.households
        owners = households.select(households.s_EB == 1)
        assert round(p['Pi_dB'], 2) == round(sum(owners.Pi_d), 2)
        assert round(p['Pi_dB'], 2) == round(sum(banks.Pi_d), 2) 
        assert round(p['Pi_dH'], 2) == round(sum(households.Pi_d), 2)


def test_share_initial_central_bank_profits(models5):
    for model in models5:
        model.share_initial_wages()
        model.share_initial_transfers()
        model.share_initial_profits()
        p = model.p
        government = model.government 
        central_bank = model.central_bank 
        assert round(p['Pi_CB'], 2) == round(central_bank.Pi, 2)
        assert round(p['Pi_G'], 2) == round(government.Pi, 2)


def test_share_initial_household_taxes(models5):
    for model in models5:
        model.share_initial_wages()
        model.share_initial_transfers()
        model.share_initial_profits()
        model.share_initial_taxes()
        p = model.p
        households = model.households
        Y = households.W + households.iota_D + households.Pi_d
        for y, household in zip(Y, households):
            assert round(household.T / p['T_H'], 2) == round(y / sum(Y), 2)
        assert round(p['T_H'], 2) == round(sum(households.T), 2)


def test_share_initial_firm_taxes(models5):
    for model in models5:
        model.share_initial_wages()
        model.share_initial_transfers()
        model.share_initial_profits()
        model.share_initial_taxes()
        p = model.p
        firms = model.firms
        for s in model.sectors:
            group = firms.select(firms.s_Y==s)
            assert round(p[f'T_F{s}'], 2) == round(sum(group.T), 2)


def test_share_initial_bank_taxes(models5):
    for model in models5:
        model.share_initial_wages()
        model.share_initial_transfers()
        model.share_initial_profits()
        model.share_initial_taxes()
        p = model.p
        banks = model.banks
        assert round(p['T_B'], 2) == round(sum(banks.T), 2)


def test_share_initial_government_taxes(models5):
    for model in models5:
        model.share_initial_wages()
        model.share_initial_transfers()
        model.share_initial_profits()
        model.share_initial_taxes()
        p = model.p
        government = model.government 
        assert round(p['T_G'], 2) == round(government.T, 2)


def test_share_initial_consumption(models5):
    for model in models5:
        model.share_initial_wages()
        model.share_initial_transfers()
        model.share_initial_profits()
        model.share_initial_taxes()
        model.share_initial_consumption()
        p = model.p
        households = model.households
        Y = households.W + households.iota_D + households.Pi_d
        Y_d = Y - households.T + households.Z 
        for y_d, household in zip(Y_d, households):
            assert round(household.C1 / p['C1'], 2) == round(y_d / sum(Y_d), 2)
            assert round(household.C2 / p['C2'], 2) == round(y_d / sum(Y_d), 2)
        assert round(p['C1'], 2) == round(sum(households.C1), 2)
        assert round(p['C2'], 2) == round(sum(households.C2), 2)


# def test_share_initial_prices(models5):
#     for model in models5:
#         model.share_initial_wages()
#         model.share_initial_transfers()
#         model.share_initial_profits()
#         model.share_initial_taxes()
#         model.share_initial_consumption()
#         model.share_initial_prices()
#         assert False

