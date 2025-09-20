
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
        'g_ss':np.random.random(),            # taux de croissance
        'N_E1':np.random.randint(1, 25),      # nombre de entrepreneurs dans le secteur productif 1
        'N_E2':np.random.randint(1, 25),      # nombre de entrepreneurs dans le secteur productif 2
        'N_E3':np.random.randint(1, 25),      # nombre de entrepreneurs dans le secteur productif 3
        'N_W1':np.random.randint(1, 25),      # nombre de salaries dans le secteur productif 1
        'N_W2':np.random.randint(1, 25),      # nombre de salaries dans le secteur productif 2
        'N_W3':np.random.randint(1, 25),      # nombre de salaries dans le secteur productif 3
        'N_WG':np.random.randint(1, 25),      # nombre de salaries dans le secteur public
        'N_U':np.random.randint(1, 25),       # nombre de chomeurs dans le secteur public
        'phi1':np.random.uniform(0.5, 2.5),   # productivite initial du secteur productif 1
        'phi2':np.random.uniform(0.5, 2.5),   # productivite initial du secteur productif 2
        'phi3':np.random.uniform(0.5, 2.5),   # productivite initial du secteur productif 3
        'w1':np.random.uniform(0.5, 2.5),     # salaire initial du secteur productif 1
        'w2':np.random.uniform(0.5, 2.5),     # salaire initial du secteur productif 2
        'w3':np.random.uniform(0.5, 2.5),     # salaire initial du secteur productif 3
        'w_G':np.random.uniform(0.5, 2.5),    # salaire public
        'w_min':np.random.uniform(0.5, 2.5),  # salaire minimum
        'tau': np.random.random(),            # taux d'impots
        'rho': np.random.random(),            # politique de dividende
        'm':np.random.random(),               # taux de marge brute
        'alpha_b1':np.random.random(),        # propension a consommer le bien 1 en zone urbaine
        'alpha_a2':np.random.random(),        # propension a consommer le bien 2 en zone rurale
        'theta_W':np.random.random(),         # proportion desire de fonds de salaire
        'theta_E':np.random.random(),         # proportion desire de capitaux bancaire (rentabilite)
        'theta_Ubar':np.random.random(),      # proportion reglementaire des allocations publics
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
        models.append(model)
    return models


def test_initialize_empty_stocks_and_flows(model_set1):
    for model in model_set1:
        stocks, flows = create_matrices_from_params(model.p)
        print('stocks\n', stocks, '\nflows\n', flows) 

        account_keys = ['H', 'F', 'B', 'G', 'CB']
        for key in account_keys:
            assert stocks.loc['sigma', key] == 0.0
            assert flows.loc['sigma', key] == 0.0


def test_calc_firms_stocks_and_flows(model_set1):
    for model in model_set1:
        model.calc_block_1()
        stocks, flows = create_matrices_from_params(model.p, digits=2)
        print('stocks\n', stocks, '\nflows\n', flows)

        assert stocks.loc['sigma', 'F'] == 0.0
        assert flows.loc['sigma', 'F'] == 0.0


def test_calc_households_stocks_and_flows(model_set1):
    for model in model_set1:
        model.calc_block_1()
        model.calc_block_2()
        stocks, flows = create_matrices_from_params(model.p, digits=2)
        print('stocks\n', stocks, '\nflows\n', flows)

        assert stocks.loc['sigma', 'H'] == 0
        assert flows.loc['sigma', 'H'] == 0


def test_calc_banks_stocks_and_flows(model_set1):
    for model in model_set1:
        model.calc_block_1()
        model.calc_block_2()
        model.calc_block_3()
        stocks, flows = create_matrices_from_params(model.p, digits=2)
        print('stocks\n', stocks, '\nflows\n', flows)

        assert stocks.loc['sigma', 'B'] == 0
        assert flows.loc['sigma', 'B'] == 0


def test_calc_public_sector_stocks_and_flows(model_set1):
    for model in model_set1:
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



@pytest.fixture
def model_set2(param_set):
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


def test_create_sufficient_households(model_set2):
    for model in model_set2:
        model.create_households()
        assert sum_params(model.p, 'N') + 1 == len(model.households), "insufficient households"
    
    for household in model_set2[0].households:
        assert isinstance(household, Household)


def test_create_sufficient_owners(model_set2):
    for model in model_set2:
        model.create_households()

        p = model.p
        households = model.households
        owners = households.select(households.s_E == 1)
        assert 1 == len(owners.select(owners.s_EB == 1)), "abnormal number of bank owners"
        assert sum_params(model.p, 'N_E') == len(owners.select(owners.s_EB==0)), "abnormal number of firm owners"
        for s in model.sectors:
            assert sum_params(p, f'N_E{s}') == len(owners.select(owners.s==s)), f"abnormal number of firm owners type {s}"


def test_create_sufficient_workers(model_set2):
    for model in model_set2:
        model.create_households()

        p = model.p
        households = model.households
        workers = households.select(households.s_W == 1)
        assert sum_params(p, 'N_WG') == len(workers.select(workers.s_WG==1)), "abnormal number of public workers"
        assert sum_params(p, 'N_WG') == len(workers.select(workers.s==0)), "abnormal number of public workers"
        for s in model.sectors:
            assert sum_params(p, f'N_W{s}') == len(workers.select(workers.s==s)), f"abnormal number of firm workers type {s}"


def test_create_sufficient_unemployed(model_set2):
    for model in model_set2:
        model.create_households()

        p = model.p
        households = model.households
        assert sum_params(p, 'N_U') == len(households.select(households.s_U == 1)), "abnormal number of public workers"


def test_create_households_by_regions(model_set2):
    for model in model_set2:
        model.create_households()

        p = model.p
        households = model.households
        Na = p['N_E1'] + p['N_W1']
        N = sum_params(p, 'N_')
        Nb = N - Na
        assert Na == len(households.select(households.z == 'a')), "abnormal number of rural households"
        assert Nb == len(households.select(households.z == 'b')), "abnormal number of urban households"


def test_create_firms(model_set2):
    for model in model_set2:
        model.create_firms()
        N = sum_params(model.p, 'N_E')
        assert N == len(model.firms)

    for firm in model_set2[0].firms:
        assert isinstance(firm, Firm)


def test_create_firms_by_sectors(model_set2):
    for model in model_set2:
        model.create_firms()

        p = model.p
        firms = model.firms
        for s in model.sectors:
            assert p[f'N_E{s}'] == len(firms.select(firms.s == s)), f"adnormal number of firms in {s}"


def test_create_firms_by_regions(model_set2):
    for model in model_set2:
        model.create_firms()

        p = model.p
        firms = model.firms
        Na = p['N_E1']
        Nb = p['N_E2'] + p['N_E3']
        assert Na == len(firms.select(firms.z == 'a')), "abnormal number of firms in rural region"
        assert Nb == len(firms.select(firms.z == 'b')), "abnormal number of firms in urban region"


def test_create_unique_bank(model_set2):
    for model in model_set2:
        model.create_bank()
        assert isinstance(model.bank, Bank)


def test_create_public_sector(model_set2):
    for model in model_set2:
        model.create_public_sector()
        assert isinstance(model.government, Government)
        assert isinstance(model.central_bank, CentralBank)


def test_share_household_stocks(model_set2):
    for model in model_set2:
        model.create_households()

        p = model.p
        households = model.households
        for z in model.regions:
            group = households.select(households.z==z)
            assert round(p[f'M_H{z}'], 2) == round(sum(group.M), 2)
            assert round(p[f'D_H{z}'], 2) == round(sum(group.D), 2)


def test_share_household_flows(model_set2):
    for model in model_set2:
        model.create_households()

        p = model.p
        households = model.households
        for z in model.regions:
            group = households.select(households.z==z)
            assert round(p[f'C{z}'], 2) == round(sum(group.C), 2)
            assert round(p[f'W_H{z}'], 2) == round(sum(group.W), 2)   
            assert round(p[f'Z_H{z}'], 2) == round(sum(group.Z), 2)   
            assert round(p[f'T_H{z}'], 2) == round(sum(group.T), 2)
            assert round(p[f'iota_DH{z}'], 2) == round(sum(group.iota_D), 2)
            assert round(p[f'pi_dH{z}'], 2) == round(sum(group.pi_d), 2)


def test_share_firm_stocks(model_set2):
    for model in model_set2:
        model.create_firms()

        p = model.p
        firms = model.firms
        for s in model.sectors:
            group = firms.select(firms.s==s)
            assert round(p[f'M_F{s}'], 2) == round(sum(group.M), 2)
            assert round(p[f'D_F{s}'], 2) == round(sum(group.D), 2)
            assert round(p[f'L_F{s}'], 2) == round(sum(group.L), 2)


def test_share_firm_flows(model_set2):
    for model in model_set2:
        model.create_firms()

        p = model.p
        firms = model.firms
        for s in model.sectors:
            group = firms.select(firms.s==s)
            assert round(p[f'Q{s}'], 2) == round(sum(group.Q), 2)
            assert round(p[f'W_F{s}'], 2) == round(sum(group.W), 2)    
            assert round(p[f'T_F{s}'], 2) == round(sum(group.T), 2)
            assert round(p[f'iota_LF{s}'], 2) == round(sum(group.iota_L), 2)
            assert round(p[f'iota_DF{s}'], 2) == round(sum(group.iota_D), 2)
            assert round(p[f'pi_dF{s}'], 2) == round(sum(group.pi_d), 2)


def test_share_bank_stocks(model_set2):
    for model in model_set2:
        model.create_bank()

        p = model.p
        bank = model.bank
        assert round(p['M_B'], 2) == round(bank.M, 2)
        assert round(p['A_B'], 2) == round(bank.A, 2)
        assert round(p['D_B'], 2) == round(bank.D, 2)
        assert round(p['B_B'], 2) == round(bank.B, 2)
        assert round(p['L_B'], 2) == round(bank.L, 2)


def test_share_bank_flows(model_set2):
    for model in model_set2:
        model.create_bank()

        p = model.p
        bank = model.bank 
        assert round(p['T_B'], 2) == round(bank.T, 2)
        assert round(p['iota_AB'], 2) == round(bank.iota_A, 2)
        assert round(p['iota_BB'], 2) == round(bank.iota_B, 2)
        assert round(p['iota_LB'], 2) == round(bank.iota_L, 2)
        assert round(p['iota_DB'], 2) == round(bank.iota_D, 2)
        assert round(p['pi_dB'], 2) == round(bank.pi_d, 2)


def test_share_public_sector_stocks(model_set2):
    for model in model_set2:
        model.create_public_sector()

        p = model.p
        government = model.government
        assert round(p['M_G'], 2) == round(government.M, 2)
        assert round(p['B_G'], 2) == round(government.B, 2)
        
        central_bank = model.central_bank
        assert round(p['M_CB'], 2) == round(central_bank.M, 2)
        assert round(p['A_CB'], 2) == round(central_bank.A, 2)
        assert round(p['B_CB'], 2) == round(central_bank.B, 2)


def test_share_public_sector_flows(model_set2):
    for model in model_set2:
        model.create_public_sector()

        p = model.p
        government = model.government 
        assert round(p['W_G'], 2) == round(government.W, 2)
        assert round(p['Z_G'], 2) == round(government.Z, 2)
        assert round(p['T_G'], 2) == round(government.T, 2)
        assert round(p['iota_BG'], 2) == round(government.iota_B, 2)
        assert round(p['pi_G'], 2) == round(government.pi, 2)
        
        central_bank = model.central_bank 
        assert round(p['iota_ACB'], 2) == round(central_bank.iota_A, 2)
        assert round(p['iota_BCB'], 2) == round(central_bank.iota_B, 2)
        assert round(p['pi_CB'], 2) == round(central_bank.pi, 2)



@pytest.fixture
def model_set3(model_set2):
    for model in model_set2:
        model.create_households()
        model.create_firms()
        model.create_bank()
        model.create_public_sector()
    return model_set2


def test_share_consumption_prices(model_set3):
    for model in model_set3:
        p = model.p
        firms = model.firms
        for s in model.sectors:
            group = firms.select(firms.s == s)
            assert group[0].p_y == p[f'p{s}']


def test_share_reservation_wages(model_set3):
    for model in model_set3:
        p = model.p
        households = model.households
        for s in model.sectors:
            group1 = households.select(households.s == s)
            assert group1[0].w_D == p[f'w{s}']

        group2 = households.select(households.s_WG == 1)
        group3 = households.select(households.s_U == 1)
        assert group2[0].w_D == p['w_G']
        assert group3[0].w_D == p['w_min']

        gov = model.government
        assert gov.w == p['w_G']


def test_share_interest_rates(model_set3):
    for model in model_set3:
        p = model.p
        households = model.households
        household = households.select(households.z == 'a')
        assert household.r_D == p['r_D']

        firms = model.firms
        firm = firms.select(firms.s == 2)[0]
        assert firm.r_D == p['r_D']
        assert firm.r_L == p['r_L']

        bank = model.bank
        assert bank.r_D == p['r_D']
        assert bank.r_L == p['r_L']
        assert bank.r_A == p['r_A']
        assert bank.r_B == p['r_B']

        gov = model.government
        assert gov.r_B == p['r_B']

        central_bank = model.central_bank
        assert central_bank.r_A == p['r_A']
        assert central_bank.r_B == p['r_B']


def test_create_rural_labor_networks(model_set3):
    for model in model_set3:
        model.create_labor_markets()
        
        market = model.labor_markets[1]
        agents = market.agents.to_list()
        households = model.households
        households = households.select(households.z=='a')
        firms = model.firms
        firms = firms.select(firms.z=='a')
        assert set(households).issubset(set(agents))
        assert set(firms).issubset(set(agents))
        assert len(agents) == len(households) + len(firms)

        p = model.p
        num_employers = p['N_E1']
        num_employees = p['N_E1'] + p['N_W1']
        min_ratio = num_employees // num_employers
        max_ratio = min_ratio + 1
        assert len(market.neighbors(firms[0]).to_list()) in [min_ratio, max_ratio]
        assert len(market.neighbors(firms[-1]).to_list()) in [min_ratio, max_ratio]
        

def test_create_formal_urban_labor_networks(model_set3):
    for model in model_set3:
        model.create_labor_markets()

        market = model.labor_markets[2]
        agents = market.agents.to_list()
        government = model.government
        firms = model.firms
        firms = firms.select(firms.s==2)
        households = model.households
        households = households.select(households.z=='b')
        assert government in set(agents)
        assert set(households).issubset(set(agents))
        assert set(firms).issubset(set(agents))
        assert len(agents) == len(households + firms) + 1

        p = model.p
        num_employers = p['N_E2']
        num_employees = p['N_E2'] + p['N_W2']
        min_ratio = num_employees // num_employers
        max_ratio = min_ratio + 1
        assert len(market.neighbors(firms[0]).to_list()) in [min_ratio, max_ratio]
        assert len(market.neighbors(firms[-1]).to_list()) in [min_ratio, max_ratio]
        assert len(market.neighbors(government).to_list()) == p['N_WG']


def test_create_informal_urban_labor_networks(model_set3):
    for model in model_set3:
        model.create_labor_markets()

        market = model.labor_markets[3]
        agents = market.agents.to_list()
        firms = model.firms
        firms = firms.select(firms.s==3)
        households = model.households
        households = households.select(households.z=='b')
        assert set(households).issubset(set(agents))
        assert set(firms).issubset(set(agents))
        assert len(agents) == len(households + firms)

        p = model.p
        num_employers = p['N_E3']
        num_employees = p['N_E3'] + p['N_W3']
        min_ratio = num_employees // num_employers
        max_ratio = min_ratio + 1
        assert len(market.neighbors(firms[0]).to_list()) in [min_ratio, max_ratio]
        assert len(market.neighbors(firms[-1]).to_list()) in [min_ratio, max_ratio]


def test_create_deposit_networks(model_set3):
    for model in model_set3:
        model.create_deposit_market()

        market = model.deposit_market
        agents = market.agents.to_list()
        bank = model.bank
        firms = model.firms
        firms = firms.select(firms.s==2)
        households = model.households
        households = households.select(households.z=='b')
        assert set(households).issubset(set(agents))
        assert set(firms).issubset(set(agents))
        assert bank in agents
        assert len(agents) == len(households + firms) + 1
        assert len(market.neighbors(bank).to_list()) == len(households + firms)


def test_create_credit_networks(model_set3):
    for model in model_set3:
        model.create_credit_market()

        market = model.credit_market
        agents = market.agents.to_list()
        bank = model.bank
        firms = model.firms
        firms = firms.select(firms.s==2)
        assert set(firms).issubset(set(agents))
        assert bank in agents
        assert len(agents) == len(firms) + 1
        assert len(market.neighbors(bank).to_list()) == len(firms)

def test_create_regional_spaces(model_set3):
    for model in model_set3:
        model.create_region_spaces()

        firms = model.firms
        households = model.households
        rural_households = households.select(households.z=='a')
        rural_firms = firms.select(firms.z=='a')
        rural_space = model.region_spaces['a']
        rural_agents = rural_space.agents.to_list()
        assert set(rural_households).issubset(set(rural_agents))
        assert set(rural_firms).issubset(set(rural_agents))
        assert len(rural_agents) == len(rural_firms + rural_households)

        urban_households = households.select(households.z=='a')
        urban_firms = firms.select(firms.z=='a')
        urban_space = model.region_spaces['a']
        urban_agents = urban_space.agents.to_list()
        assert set(urban_households).issubset(set(urban_agents))
        assert set(urban_firms).issubset(set(urban_agents))
        assert len(urban_agents) == len(urban_firms + urban_households)

