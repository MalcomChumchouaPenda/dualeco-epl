
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


def create_matrices():
    stock_matrix = pd.DataFrame(0.0, index=stock_keys, columns=account_keys)
    flow_matrix = pd.DataFrame(0.0, index=flow_keys, columns=account_keys)
    return stock_matrix, flow_matrix

def print_matrices(matrices):
    f = lambda v: round(v, 2)
    print('stocks\n', matrices[0].map(f))
    print('\nflows\n', matrices[1].map(f))


def sum_params(params, prefix):
    return sum([v for k, v in params.items() if k.startswith(prefix)])

def calc_initial_matrices(params):
    stock_matrix, flow_matrix = create_matrices()
    stock_matrix.loc['M', 'H'] = sum_params(params, 'M_H')
    stock_matrix.loc['D', 'H'] = sum_params(params, 'D_H')
    stock_matrix.loc['M', 'F'] = sum_params(params, 'M_F')
    stock_matrix.loc['D', 'F'] = sum_params(params, 'D_F')
    stock_matrix.loc['L', 'F'] = - sum_params(params, 'L_F')
    stock_matrix.loc['M', 'B'] = params['M_B']
    stock_matrix.loc['A', 'B'] = - params['A_B']
    stock_matrix.loc['D', 'B'] = - params['D_B']
    stock_matrix.loc['B', 'B'] = params['B_B']
    stock_matrix.loc['L', 'B'] = params['L_B']
    stock_matrix.loc['M', 'G'] = params['M_G']
    stock_matrix.loc['B', 'G'] = - params['B_G']
    stock_matrix.loc['M', 'CB'] = - params['M_CB']
    stock_matrix.loc['A', 'CB'] = params['A_CB']
    stock_matrix.loc['B', 'CB'] = params['B_CB']
    stock_matrix.loc['V', :] = - stock_matrix.sum()
    stock_matrix.loc['sigma', :] = stock_matrix.sum()
    stock_matrix['sigma'] = stock_matrix.sum(axis=1)
    
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
    flow_matrix.loc['T', 'B'] = - params['T_B']
    flow_matrix.loc['iota_A', 'B'] = - params['iota_AB']
    flow_matrix.loc['iota_B', 'B'] = params['iota_BB']
    flow_matrix.loc['iota_L', 'B'] = params['iota_LB']
    flow_matrix.loc['iota_D', 'B'] = - params['iota_DB']
    flow_matrix.loc['pi_d', 'B'] = - params['pi_dB']
    flow_matrix.loc['DeltaA', 'B'] = params['DeltaA_B']
    flow_matrix.loc['DeltaB', 'B'] = - params['DeltaB_B']
    flow_matrix.loc['DeltaM', 'B'] = - params['DeltaM_B']
    flow_matrix.loc['DeltaL', 'B'] = - params['DeltaL_B']
    flow_matrix.loc['DeltaD', 'B'] = params['DeltaD_B']
    flow_matrix.loc['W', 'G'] = - params['W_G']
    flow_matrix.loc['Z', 'G'] = - params['Z_G']
    flow_matrix.loc['T', 'G'] = params['T_G']
    flow_matrix.loc['iota_B', 'G'] = - params['iota_BG']
    flow_matrix.loc['pi', 'G'] = params['pi_G']
    flow_matrix.loc['DeltaB', 'G'] = params['DeltaB_G']
    flow_matrix.loc['DeltaM', 'G'] = - params['DeltaM_G']
    flow_matrix.loc['iota_A', 'CB'] = params['iota_ACB']
    flow_matrix.loc['iota_B', 'CB'] = params['iota_BCB']
    flow_matrix.loc['pi', 'CB'] = - params['pi_CB']
    flow_matrix.loc['DeltaA', 'CB'] = - params['DeltaA_CB']
    flow_matrix.loc['DeltaB', 'CB'] = - params['DeltaB_CB']
    flow_matrix.loc['DeltaM', 'CB'] = params['DeltaM_CB']
    flow_matrix.loc['sigma', :] = flow_matrix.sum()
    flow_matrix['sigma'] = flow_matrix.sum(axis=1)
    return stock_matrix, flow_matrix
    