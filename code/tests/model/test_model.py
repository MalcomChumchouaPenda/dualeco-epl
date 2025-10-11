
import pytest
import numpy as np

from model.model import DualEcoModel
from model.agents import Household, Firm, Bank
from model.agents import CentralBank, Government
from utils.analysis import sum_params, create_matrices_from_params


@pytest.fixture 
def param_set():
    np.random.seed = 0
    return [{
        'g':np.random.random(),            # taux de croissance
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
        'delta': np.random.random(),      # parametre d'ajustement
        'upsilon_F': np.random.random(),      # parametre d'ajustement des salaires des firmes
        'm':np.random.random(),               # taux de marge brute
        'theta_W':np.random.random(),         # proportion desire de fonds de salaire
        'theta_E':np.random.random(),         # proportion desire de capitaux bancaire (rentabilite)
        'theta_M':np.random.random(),         # proportion desire de liquidite
        'theta_y':np.random.random(),         # proportion desire de sotck d'invendus
        'theta_Zbar':np.random.random(),      # proportion reglementaire des allocations publics
        'theta_Ebar':np.random.random(),      # ratio minimum de capital bancaire
        'theta_Rbar':np.random.random(),      # ratio minimum de liquidite bancaire
        'beta_L':np.random.random(),          # elasticite du taux d'interet du credit au levier financier
        'gamma_L':np.random.random(),         # elasticite de la probabilite de credit au levier financier
        'r_D': np.random.random(),            # taux d'interet sur les depots bancaires
        'r_L': np.random.random(),            # taux d'interet sur les credits bancaires
        'r_B': np.random.random(),            # taux d'interet sur les bons du tresors
        'r_A': np.random.random(),            # taux d'interet sur les avances de la Banque Centrale
    } for _ in range(5)]


@pytest.fixture
def model_set1(param_set):
    models = []
    for params in param_set:
        model = DualEcoModel(params)
        model.init_params()
        model.calc_block_1()
        model.calc_block_2()
        model.calc_block_3()
        model.calc_block_4()
        models.append(model)
    return models


def test_calc_firms_stocks_and_flows(model_set1):
    for model in model_set1:
        stocks, flows = create_matrices_from_params(model.p, digits=2)
        print('stocks\n', stocks, '\nflows\n', flows)
        assert stocks.loc['Y_inv', 'sigma'] > 0
        assert stocks.loc['sigma', 'F'] == 0.0
        assert flows.loc['sigma', 'F'] == 0.0


def test_calc_banks_stocks_and_flows(model_set1):
    for model in model_set1:
        stocks, flows = create_matrices_from_params(model.p, digits=2)
        print('stocks\n', stocks, '\nflows\n', flows)
        assert stocks.loc['sigma', 'B'] == 0
        assert flows.loc['sigma', 'B'] == 0


def test_calc_households_stocks_and_flows(model_set1):
    for model in model_set1:
        stocks, flows = create_matrices_from_params(model.p, digits=2)
        print('stocks\n', stocks, '\nflows\n', flows)
        assert stocks.loc['sigma', 'H'] == 0
        assert flows.loc['sigma', 'H'] == 0


def test_calc_public_sector_stocks_and_flows(model_set1):
    for model in model_set1:
        stocks, flows = create_matrices_from_params(model.p, digits=2)
        print('stocks\n', stocks, '\nflows\n', flows)
        assert stocks.loc['sigma', 'G'] == 0
        assert stocks.loc['sigma', 'CB'] == 0
        assert flows.loc['sigma', 'G'] == 0
        assert flows.loc['sigma', 'CB'] == 0
        

def test_is_globally_stock_consistent(model_set1):
    for model in model_set1:
        stocks, flows = create_matrices_from_params(model.p, digits=2)
        print('stocks\n', stocks, '\nflows\n', flows)
        for key in stocks.index:
            if key not in ['Y_inv', 'V']:
                assert stocks.loc[key, 'sigma'] == 0


def test_is_globally_flow_consistent(model_set1):
    for model in model_set1:
        stocks, flows = create_matrices_from_params(model.p, digits=2)
        print('stocks\n', stocks, '\nflows\n', flows)
        for key in flows.index:
            assert flows.loc[key, 'sigma'] == 0


@pytest.fixture
def model_set2(model_set1):
    models = []
    for model in model_set1:
        model.create_households()
        model.create_firms()
        model.create_banks()
        model.create_public_sector()
        models.append(model)
    return models


def test_create_sufficient_households(model_set2):
    for model in model_set2:
        assert sum_params(model.p, 'N') == len(model.households)
        for household in model.households:
            assert isinstance(household, Household)


def test_create_sufficient_owners(model_set2):
    for model in model_set2:
        p = model.p
        households = model.households
        owners = households.select(households.s_E == 1)
        assert sum_params(model.p, 'N_B') == len(owners.select(owners.s_EB == 1))
        assert sum_params(model.p, 'N_E') == len(owners.select(owners.s_EB == 0))
        for s in model.sectors:
            assert sum_params(p, f'N_E{s}') == len(owners.select(owners.s_Y == s))


def test_create_sufficient_workers(model_set2):
    for model in model_set2:
        p = model.p
        households = model.households
        workers = households.select(households.s_W == 1)
        assert sum_params(p, 'N_WG') == len(workers.select(workers.s_WG==1))
        assert sum_params(p, 'N_WG') == len(workers.select(workers.s_Y==0))
        for s in model.sectors:
            assert sum_params(p, f'N_W{s}') == len(workers.select(workers.s_Y==s))


def test_create_sufficient_unemployed(model_set2):
    for model in model_set2:
        p = model.p
        households = model.households
        assert sum_params(p, 'N_U') == len(households.select(households.s_U == 1))


def test_create_firms(model_set2):
    for model in model_set2:
        N = sum_params(model.p, 'N_E')
        assert N == len(model.firms)
        for firm in model.firms:
            assert isinstance(firm, Firm)


def test_create_firms_by_sectors(model_set2):
    for model in model_set2:
        p = model.p
        firms = model.firms
        for s in model.sectors:
            formal = 1 if s == 1 else 0
            group = firms.select(firms.s_Y == s)
            assert p[f'N_E{s}'] == len(group)
            for firm in group:
                assert firm.n_W == formal
                assert firm.n_T == formal


def test_create_banks(model_set2):
    for model in model_set2:
        N = sum_params(model.p, 'N_B')
        assert N == len(model.banks)
        for bank in model_set2[0].banks:
            assert isinstance(bank, Bank)


def test_create_public_sector(model_set2):
    for model in model_set2:
        assert isinstance(model.government, Government)
        assert isinstance(model.central_bank, CentralBank)


@pytest.fixture
def model_set3(model_set2):
    models = []
    for model in model_set2:
        model.create_labor_markets()
        model.create_deposit_market()
        model.create_credit_market()
        model.create_economy()
        models.append(model)
    return model_set2


def test_share_household_stocks(model_set3):
    for model in model_set3:
        p = model.p
        households = model.households
        assert round(p['M_H'], 2) == round(sum(households.M), 2)
        assert round(p['D_H'], 2) == round(sum(households.D), 2)


def test_share_household_flows(model_set3):
    for model in model_set3:
        p = model.p
        households = model.households
        assert round(p['C1'], 2) == round(sum(households.C1), 2)
        assert round(p['C2'], 2) == round(sum(households.C2), 2)
        assert round(p['W_H'], 2) == round(sum(households.W), 2)   
        assert round(p['Z_H'], 2) == round(sum(households.Z), 2)   
        assert round(p['T_H'], 2) == round(sum(households.T), 2)
        assert round(p['iota_DH'], 2) == round(sum(households.iota_D), 2)
        assert round(p['Pi_dH'], 2) == round(sum(households.Pi_d), 2)


def test_share_firm_stocks(model_set3):
    for model in model_set3:
        p = model.p
        firms = model.firms
        for s in model.sectors:
            group = firms.select(firms.s_Y==s)
            assert round(p[f'M_F{s}'], 2) == round(sum(group.M), 2)
            assert round(p[f'D_F{s}'], 2) == round(sum(group.D), 2)
            assert round(p[f'L_F{s}'], 2) == round(sum(group.L), 2)
            assert round(p[f'E_F{s}'], 2) == round(sum(group.E), 2)


def test_share_firm_net_worth(model_set3):
    for model in model_set3:
        p = model.p
        firms = model.firms
        for s in model.sectors:
            group = firms.select(firms.s_Y==s)
            V = p[f'D_F{s}'] + p[f'M_F{s}'] - p[f'E_F{s}'] - p[f'L_F{s}']
            assert round(V, 2) == round(sum(group.V), 2)


def test_share_firm_production(model_set3):
    for model in model_set3:
        p = model.p
        firms = model.firms
        for s in model.sectors:
            group = firms.select(firms.s_Y==s)
            assert round(sum(group.y_star), 2) == 0
            assert round(sum(group.Y_inv), 2) == round(p[f'Y_inv{s}'], 2) 
            assert round(sum(group.y_inv), 2) == round(p[f'y_inv{s}'], 2) 
            assert round(sum(group.y), 2) == round(p[f'Q{s}'] / p[f'p{s}'], 2)
            assert round(sum(group.q_e), 2) == round(p[f'Q{s}'] / p[f'p{s}'], 2)
            assert round(sum(group.Q), 2) == round(p[f'Q{s}'], 2)  


def test_share_firm_wages_and_labor(model_set3):
    for model in model_set3:
        p = model.p
        firms = model.firms
        for s in model.sectors:
            group = firms.select(firms.s_Y==s)
            assert round(sum(group.N_Jc), 2) == 0
            assert round(sum(group.N_Jd), 2) == 0
            assert round(sum(group.l_D), 2) == 0
            assert round(p[f'W_F{s}'], 2) == round(sum(group.W), 2)  
            assert round(p[f'Q{s}'] / p[f'w{s}'], 2) == round(sum(group.l), 2)


def test_share_firm_interests(model_set3):
    for model in model_set3:
        p = model.p
        firms = model.firms
        for s in model.sectors:
            group = firms.select(firms.s_Y==s)
            assert round(p[f'iota_LF{s}'], 2) == round(sum(group.iota_L), 2)
            assert round(p[f'iota_DF{s}'], 2) == round(sum(group.iota_D), 2)


def test_share_firm_profits_and_taxes(model_set3):
    for model in model_set3:
        p = model.p
        firms = model.firms
        for s in model.sectors:
            group = firms.select(firms.s_Y==s)
            assert round(p[f'Pi_dF{s}'], 2) == round(sum(group.Pi_d), 2)
            assert round(p[f'T_F{s}'], 2) == round(sum(group.T), 2)


def test_share_firm_equities(model_set3):
    for model in model_set3:
        p = model.p
        firms = model.firms
        households = model.households
        owners = households.select(households.s_E == 1)
        for s in model.sectors:
            sector_firms = firms.select(firms.s_Y == s)
            sector_owners = owners.select(owners.s_Y == s)
            assert round(sum(sector_firms.E), 2) == round(sum_params(p, f'E_F{s}'), 2)
            assert round(sum(sector_firms.E), 2) == round(sum(sector_owners.E), 2)
            for firm in sector_firms:
                assert firm.owner in sector_owners
                assert round(firm.E, 2) == round(firm.owner.E, 2)


def test_share_firm_prices(model_set3):
    for model in model_set3:
        p = model.p
        firms = model.firms
        for s in model.sectors:
            group = firms.select(firms.s_Y==s)
            for firm in group:
                assert firm.m == p['m']
                assert firm.w == p[f'w{s}']
                assert firm.p_y == p[f'p{s}']
                if s == 1:
                    assert firm.r_L == p['r_L']


def test_share_firm_behavior_params(model_set3):
    for model in model_set3:
        p = model.p
        firms = model.firms
        for s in model.sectors:
            group = firms.select(firms.s_Y==s)
            for firm in group:
                assert firm.delta == p['delta']
                assert firm.theta_y == p['theta_y']
                assert firm.upsilon == p['upsilon_F']
                assert firm.phi == p[f'phi{s}']


def test_share_bank_financial_stocks(model_set3):
    for model in model_set3:
        p = model.p
        banks = model.banks
        assert round(p['M_B'], 2) == round(sum(banks.M), 2)
        assert round(p['A_B'], 2) == round(sum(banks.A), 2)
        assert round(p['D_B'], 2) == round(sum(banks.D), 2)
        assert round(p['B_B'], 2) == round(sum(banks.B), 2)
        assert round(p['L_B'], 2) == round(sum(banks.L), 2)


def test_share_bank_financial_flows(model_set3):
    for model in model_set3:
        p = model.p
        banks = model.banks
        assert round(p['T_B'], 2) == round(sum(banks.T), 2)
        assert round(p['iota_AB'], 2) == round(sum(banks.iota_A), 2)
        assert round(p['iota_BB'], 2) == round(sum(banks.iota_B), 2)
        assert round(p['iota_LB'], 2) == round(sum(banks.iota_L), 2)
        assert round(p['iota_DB'], 2) == round(sum(banks.iota_D), 2)
        assert round(p['Pi_dB'], 2) == round(sum(banks.Pi_d), 2)


def test_share_bank_equities(model_set3):
    for model in model_set3:
        p = model.p
        banks = model.banks
        households = model.households
        owners = households.select(households.s_EB == 1)
        assert round(sum(banks.E), 2) == round(sum_params(p, 'E_B'), 2)
        assert round(sum(banks.E), 2) == round(sum(owners.E), 2)
        for bank in banks:
            assert bank.owner in owners
            assert round(bank.E, 2) == round(bank.owner.E, 2)


def test_share_bank_behavior_params(model_set3):
    for model in model_set3:
        p = model.p
        for bank in model.banks:
            assert bank.delta == p['delta']
            assert bank.theta_Ebar == p['theta_Ebar']
            assert bank.theta_Rbar == p['theta_Rbar']
            assert bank.gamma_L == p['gamma_L']
            assert bank.beta_L == p['beta_L']


def test_share_public_sector_stocks(model_set3):
    for model in model_set3:
        p = model.p
        government = model.government
        assert round(p['M_G'], 2) == round(government.M, 2)
        assert round(p['B_G'], 2) == round(government.B, 2)
        
        central_bank = model.central_bank
        assert round(p['M_CB'], 2) == round(central_bank.M, 2)
        assert round(p['A_CB'], 2) == round(central_bank.A, 2)
        assert round(p['B_CB'], 2) == round(central_bank.B, 2)


def test_share_public_sector_flows(model_set3):
    for model in model_set3:
        p = model.p
        government = model.government 
        assert round(p['W_G'], 2) == round(government.W, 2)
        assert round(p['Z_G'], 2) == round(government.Z, 2)
        assert round(p['T_G'], 2) == round(government.T, 2)
        assert round(p['iota_BG'], 2) == round(government.iota_B, 2)
        assert round(p['Pi_G'], 2) == round(government.Pi, 2)
        
        central_bank = model.central_bank 
        assert round(p['iota_ACB'], 2) == round(central_bank.iota_A, 2)
        assert round(p['iota_BCB'], 2) == round(central_bank.iota_B, 2)
        assert round(p['Pi_CB'], 2) == round(central_bank.Pi, 2)


def test_share_consumption_prices(model_set3):
    for model in model_set3:
        p = model.p
        firms = model.firms
        for s in model.sectors:
            group = firms.select(firms.s_Y == s)
            assert group[0].p_y == p[f'p{s}']


def test_share_reservation_wages(model_set3):
    for model in model_set3:
        p = model.p
        households = model.households
        for s in model.sectors:
            group1 = households.select(households.s_Y == s)
            assert group1[0].w_D == p[f'w{s}']

        group2 = households.select(households.s_WG == 1)
        group3 = households.select(households.s_U == 1)
        assert group2[0].w_D == p['w_G']
        assert group3[0].w_D == p['w_min']

        gov = model.government
        assert gov.w == p['w_G']


# ! must place interest rate on a common market
def test_share_interest_rates(model_set3):
    for model in model_set3:
        p = model.p
        households = model.households
        household = households[0]
        assert household.r_D == p['r_D']

        firms = model.firms
        firm = firms.select(firms.s_Y == 1)[0]
        assert firm.r_D == p['r_D']
        assert firm.r_L == p['r_L']

        bank = model.banks[0]
        assert bank.r_D == p['r_D']
        assert bank.r_L == p['r_L']
        assert bank.r_A == p['r_A']
        assert bank.r_B == p['r_B']

        gov = model.government
        assert gov.r_B == p['r_B']

        central_bank = model.central_bank
        assert central_bank.r_A == p['r_A']
        assert central_bank.r_B == p['r_B']


def test_create_formal_labor_networks(model_set3):
    for model in model_set3:
        market = model.labor_markets[1]
        agents = market.agents.to_list()
        government = model.government
        firms = model.firms
        firms = firms.select(firms.s_Y==1)
        households = model.households
        assert government in set(agents)
        assert set(households).issubset(set(agents))
        assert set(firms).issubset(set(agents))
        assert len(agents) == len(households + firms) + 1

        p = model.p
        num_employers = p['N_E1']
        num_employees = p['N_E1'] + p['N_W1']
        min_ratio = num_employees // num_employers
        max_ratio = min_ratio + 1
        for firm in firms:
            employees = market.neighbors(firm).to_list()
            assert len(employees) in [min_ratio, max_ratio]
        assert len(market.neighbors(government).to_list()) == p['N_WG']


def test_create_informal_labor_networks(model_set3):
    for model in model_set3:
        model.create_labor_markets()

        market = model.labor_markets[2]
        agents = market.agents.to_list()
        firms = model.firms
        firms = firms.select(firms.s_Y==2)
        households = model.households
        assert set(households).issubset(set(agents))
        assert set(firms).issubset(set(agents))
        assert len(agents) == len(households + firms)

        p = model.p
        num_employers = p['N_E2']
        num_employees = p['N_E2'] + p['N_W2']
        min_ratio = num_employees // num_employers
        max_ratio = min_ratio + 1
        for firm in firms:
            employees = market.neighbors(firm).to_list()
            assert len(employees) in [min_ratio, max_ratio]


def test_create_deposit_networks(model_set3):
    for model in model_set3:
        market = model.deposit_market
        agents = market.agents.to_list()
        banks = model.banks
        firms = model.firms
        formal_firms = firms.select(firms.s_Y==1)
        households = model.households
        assert set(households).issubset(set(agents))
        assert set(formal_firms).issubset(set(agents))
        assert set(banks).issubset(set(agents))
        assert len(agents) == len(households + formal_firms + banks)
        
        p = model.p
        num_bank = p['N_B']
        num_clients = len(households + formal_firms)
        min_ratio = num_clients // num_bank
        max_ratio = min_ratio + 1
        for bank in banks:
            clients = market.neighbors(bank).to_list()
            assert len(clients) in [min_ratio, max_ratio]
            assert round(sum(clients.D), 2) == round(bank.D, 2)
            assert round(sum(clients.iota_D), 2) == round(bank.iota_D, 2)


def test_create_credit_networks(model_set3):
    for model in model_set3:
        market = model.credit_market
        agents = market.agents.to_list()
        banks = model.banks
        firms = model.firms
        formal_firms = firms.select(firms.s_Y==1)
        assert set(formal_firms).issubset(set(agents))
        assert set(banks).issubset(set(agents))
        assert len(agents) == len(formal_firms + banks)
        
        p = model.p
        num_bank = p['N_B']
        num_firms = p['N_E1']
        min_ratio = num_firms // num_bank
        max_ratio = min_ratio + 1
        for bank in banks:
            clients = market.neighbors(bank).to_list()
            assert len(clients) in [min_ratio, max_ratio]
            assert round(sum(clients.L), 2) == round(bank.L, 2)
            assert round(sum(clients.iota_L), 2) == round(bank.iota_L, 2)


def test_create_economy(model_set3):
    for model in model_set3:
        firms = model.firms
        households = model.households
        agents = model.economy.agents.to_list()
        assert set(households).issubset(set(agents))
        assert set(firms).issubset(set(agents))
        assert len(agents) == len(firms + households)

