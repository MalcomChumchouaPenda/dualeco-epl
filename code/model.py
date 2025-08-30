def calc_block_1(params):
    p = params.copy()
    p['zeta_1'] = 1/(1+p['g_ss'])
    p['zeta_2'] = 1-p['zeta_1']
    for j in range(1, p['Z_j']+1):
        p[f'N_F{j}'] = sum([p[f'N_F{j}{i}'] for i in range(1, p['Z_i']+1)])
        p[f'y_F{j}'] = p[f'phi_{j}'] * p[f'N_F{j}']
        p[f'W_F{j}'] = p[f'w_{j}'] * p[f'N_F{j}']
        if p[f'y_F{j}'] == 0:
            p[f'p_{j}'] = (1+p['m']) * p[f'w_{j}']
        else:
            p[f'p_{j}'] = (1+p['m']) * p[f'W_F{j}']/p[f'y_F{j}']
        p[f'D_F{j}'] = p[f'a_D_F{j}'] * p['theta_W'] * p[f'W_F{j}']
        p[f'W_F{j}'] = p[f'w_{j}'] * p[f'N_F{j}']
        p[f'C_F{j}'] = p[f'p_{j}'] * p[f'y_F{j}']
        p[f'L_F{j}'] = p[f'a_D_F{j}'] * p['f_L'] * p[f'C_F{j}']

        A = np.array([
            [1, p[f'a_D_F{j}'], 0, 0, 0],
            [-p['zeta_1']*p['r_D'], 0, 1, 0, 0],
            [0, 0, p['tau']*p[f'n_tau_F{j}'], -1, 0],
            [0, 0, p['rho'], -p['rho'], -1],
            [-p['zeta_2'], -p['zeta_2'], 1, -1, -1]
        ])
        B = np.array([
            p['theta_W'] * p[f'W_F{j}',
            p[f'C_F{j}']-p[f'W_F{j}']+p['zeta_1']*p['r_L']*p[f'L_F{j}'],
            0,
            0,
            p['zeta_2']*p[f'L_F{j}']            
        ])
        X = np.linalg.solve(A, B)
        
        p[f'D_F{j}'] = X[0]
        p[f'M_F{j}'] = X[1]
        p[f'F_F{j}'] = X[2]
        p[f'L_F{j}'] = X[3]
        p[f'F_d_F{j}'] = X[4]
        
        p[f'R_L_F{j}'] = p['zeta_1']*p['r_L'] * p[f'L_F{j}']
        p[f'R_D_F{j}'] = p['zeta_1']*p['r_D'] * p[f'D_F{j}']
        p[f'Delta_L_F{j}'] = p['zeta_2'] * p[f'L_F{j}']
        p[f'Delta_D_F{j}'] = p['zeta_2'] * p[f'D_F{j}']
        p[f'Delta_M_F{j}'] = p['zeta_2'] * p[f'M_F{j}'] 
    return p