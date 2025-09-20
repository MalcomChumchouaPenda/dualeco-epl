
import pandas as pd
import numpy as np


# definition des secteurs institutionnels
account_keys = ['H', 'F', 'B', 'G', 'CB']
account_names = ['Households', 'Firms', 'Banks', 
                 'Government', 'Central Bank']

# definitions des stocks
stock_keys = ['M', 'A', 'D', 'B', 'L']
stock_names = ['HP Money', 'Cash Advances', 
               'Deposits', 'Bonds', 'Loans']

# definitions des flux
flow_keys = ['C', 'W', 'Z', 'T', 'iota_A', 'iota_B', 'iota_L', 'iota_D', 
             'pi_d', 'pi', 'DeltaA', 'DeltaB', 'DeltaM', 'DeltaL', 'DeltaD']
flow_names = ['Consumption', 'Wages', 'Doles', 'Taxes',  'Int. on advances', 
              'Int. on bonds', 'Int. on loans', 'Int on deposits', 'Entrepreneurial Profits', 
              'Central Bank Profits', 'Var. of advances', 'Var. of bonds', 'Var. of HP Money', 
              'var. of loans', 'Var. of deposits']


def print_matrices(matrices):
    f = lambda v: round(v, 2)
    print('stocks\n', matrices[0].map(f))
    print('\nflows\n', matrices[1].map(f))


def sum_params(params, prefix):
    return sum([v for k, v in params.items() if k.startswith(prefix)])


def create_matrices_from_params(params, digits=None):
    stock_matrix = pd.DataFrame(0.0, index=stock_keys, columns=account_keys)
    stock_matrix.loc['M', 'H'] = sum_params(params, 'M_H')
    stock_matrix.loc['D', 'H'] = sum_params(params, 'D_H')
    stock_matrix.loc['M', 'F'] = sum_params(params, 'M_F')
    stock_matrix.loc['D', 'F'] = sum_params(params, 'D_F')
    stock_matrix.loc['L', 'F'] = - sum_params(params, 'L_F')
    stock_matrix.loc['M', 'B'] = params.get('M_B', 0)
    stock_matrix.loc['A', 'B'] = - params.get('A_B', 0)
    stock_matrix.loc['D', 'B'] = - params.get('D_B', 0)
    stock_matrix.loc['B', 'B'] = params.get('B_B', 0)
    stock_matrix.loc['L', 'B'] = params.get('L_B', 0)
    stock_matrix.loc['M', 'G'] = params.get('M_G', 0)
    stock_matrix.loc['B', 'G'] = - params.get('B_G', 0)
    stock_matrix.loc['M', 'CB'] = - params.get('M_CB', 0)
    stock_matrix.loc['A', 'CB'] = params.get('A_CB', 0)
    stock_matrix.loc['B', 'CB'] = params.get('B_CB', 0)
    stock_matrix.loc['V', :] = - stock_matrix.sum()
    stock_matrix.loc['sigma', :] = stock_matrix.sum()
    stock_matrix['sigma'] = stock_matrix.sum(axis=1)
    
    flow_matrix = pd.DataFrame(0.0, index=flow_keys, columns=account_keys)
    flow_matrix.loc['C', 'H'] = - sum_params(params, 'C')
    flow_matrix.loc['W', 'H'] = sum_params(params, 'W_H')
    flow_matrix.loc['Z', 'H'] = sum_params(params, 'Z_H')
    flow_matrix.loc['T', 'H'] = - sum_params(params, 'T_H')
    flow_matrix.loc['iota_D', 'H'] = sum_params(params, 'iota_DH')
    flow_matrix.loc['pi_d', 'H'] = sum_params(params, 'pi_dH')
    flow_matrix.loc['DeltaM', 'H'] = - sum_params(params, 'DeltaM_H')
    flow_matrix.loc['DeltaD', 'H'] = - sum_params(params, 'DeltaD_H')
    flow_matrix.loc['C', 'F'] = sum_params(params, 'Q')
    flow_matrix.loc['W', 'F'] = - sum_params(params, 'W_F')
    flow_matrix.loc['T', 'F'] = - sum_params(params, 'T_F')
    flow_matrix.loc['iota_L', 'F'] = - sum_params(params, 'iota_LF')
    flow_matrix.loc['iota_D', 'F'] = sum_params(params, 'iota_DF')
    flow_matrix.loc['pi_d', 'F'] = - sum_params(params, 'pi_dF')
    flow_matrix.loc['DeltaM', 'F'] = - sum_params(params, 'DeltaM_F')
    flow_matrix.loc['DeltaL', 'F'] = sum_params(params, 'DeltaL_F')
    flow_matrix.loc['DeltaD', 'F'] = - sum_params(params, 'DeltaD_F')
    flow_matrix.loc['T', 'B'] = - params.get('T_B', 0)
    flow_matrix.loc['iota_A', 'B'] = - params.get('iota_AB', 0)
    flow_matrix.loc['iota_B', 'B'] = params.get('iota_BB', 0)
    flow_matrix.loc['iota_L', 'B'] = params.get('iota_LB', 0)
    flow_matrix.loc['iota_D', 'B'] = - params.get('iota_DB', 0)
    flow_matrix.loc['pi_d', 'B'] = - params.get('pi_dB', 0)
    flow_matrix.loc['DeltaA', 'B'] = params.get('DeltaA_B', 0)
    flow_matrix.loc['DeltaB', 'B'] = - params.get('DeltaB_B', 0)
    flow_matrix.loc['DeltaM', 'B'] = - params.get('DeltaM_B', 0)
    flow_matrix.loc['DeltaL', 'B'] = - params.get('DeltaL_B', 0)
    flow_matrix.loc['DeltaD', 'B'] = params.get('DeltaD_B', 0)
    flow_matrix.loc['W', 'G'] = - params.get('W_G', 0)
    flow_matrix.loc['Z', 'G'] = - params.get('Z_G', 0)
    flow_matrix.loc['T', 'G'] = params.get('T_G', 0)
    flow_matrix.loc['iota_B', 'G'] = - params.get('iota_BG', 0)
    flow_matrix.loc['pi', 'G'] = params.get('pi_G', 0)
    flow_matrix.loc['DeltaB', 'G'] = params.get('DeltaB_G', 0)
    flow_matrix.loc['DeltaM', 'G'] = - params.get('DeltaM_G', 0)
    flow_matrix.loc['iota_A', 'CB'] = params.get('iota_ACB', 0)
    flow_matrix.loc['iota_B', 'CB'] = params.get('iota_BCB', 0)
    flow_matrix.loc['pi', 'CB'] = - params.get('pi_CB', 0)
    flow_matrix.loc['DeltaA', 'CB'] = - params.get('DeltaA_CB', 0)
    flow_matrix.loc['DeltaB', 'CB'] = - params.get('DeltaB_CB', 0)
    flow_matrix.loc['DeltaM', 'CB'] = params.get('DeltaM_CB', 0)
    flow_matrix.loc['sigma', :] = flow_matrix.sum()
    flow_matrix['sigma'] = flow_matrix.sum(axis=1)

    if digits is not None:
        f = lambda x: round(x, digits)
        stock_matrix = stock_matrix.map(f)
        flow_matrix = flow_matrix.map(f)
    return stock_matrix, flow_matrix


def create_matrices_from_output(output, t, model_name='DualEcoModel', digits=None):
    variables = output.variables[model_name]
    variables = variables.loc[t].to_dict()
    return create_matrices_from_params(variables, digits=digits)


