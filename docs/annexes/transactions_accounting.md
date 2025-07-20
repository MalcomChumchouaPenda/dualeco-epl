
# Transactions accounting in SFC-Model of dual economy: The Monetary Circuit

We consider transactions during the following events:

1. *Production planning*: firms set desired production, labor demand, wages and prices (No transaction).
2. *Credit markets matching*: firms ask credit. banks grant loans and possibly ask cash advances to Central bank.
3. *Labor markets matching*: households set reservation wage. firms and government fires and hires workers (No transaction).
4. *Wages and taxes payment*: Firms pay wages. Households, banks and firms pay taxes.
6. *Profit distribution*: Firms and banks pay dividends. Central bank transfer profit.
5. *Public expenditures*: Government pay wages and doles.
6. *Goods markets matching*: Firms produce and export goods. Households consume and import goods.
6. *Financial debt repayments*: Government repay bonds. Firms repay loans. Banks pay deposit's interests and repay advances.
6. *Bonds market matching*: Government issue bonds. Banks buy bonds. Central Bank buy residuals bonds.
6. *Deposits market matching*: Firms and Households place deposits.
6. *Firms and banks entry-exit*: Defaulted firms and banks exit the market. New firms and banks are created.

## Non negative funds

To ensure some funds are non-negative. If some agents lack of liquid funds, he can use less liquid assets:
- Households use deposits if there is lack of cash (positive cash constraint)
- Firms use deposits if there is lack of cash (positive cash constraint)
- Banks use cash advances if there is lack of reserves (positive reserve constraint)

To pay anything firms and households must withdraw if necessary deposits.

firms withdraw deposits

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & & -\Delta H_{Ft} & +\Delta H_{Bt} & & & & 0 \\
        \text{Var. of deposits (formal)} 
            & & +\Delta D_{F1t} & -\Delta D_{B1t} & & & & 0 \\
        \text{Var. of deposits (informal)} 
            & & +\Delta D_{F2t} & -\Delta D_{B2t} & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$


households withdraw deposits

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & -\Delta H_{Ht} & & +\Delta H_{Bt} & & & & 0 \\
        \text{Var. of deposits (formal)} 
            & +\Delta D_{H1t} & & -\Delta D_{B1t} & & & & 0 \\
        \text{Var. of deposits (informal)} 
            & +\Delta D_{H2t} & & -\Delta D_{B2t} & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$



## Credit markets matching

Banks grant formal loans.

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Var. of advances} 
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & & & & & & & 0 \\
        \text{Var. of loans (formal)} 
            & & +\Delta L_{F1t} & -\Delta L_{B1t} & & & & 0 \\
        \text{Var. of deposits (formal)} 
            & & -\Delta D_{F1t} & +\Delta D_{B1t} & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Banks grant informal loans.

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Var. of advances} 
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & & -\Delta H_{Ft} & +\Delta H_{Bt} & & & & 0 \\
        \text{Var. of loans (informal)} 
            & & +\Delta L_{F2t} & -\Delta L_{B2t} & & & & 0 \\
        \text{Var. of deposits (informal)} 
            & & & & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Banks ask cash advances to Central bank.

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Var. of advances} 
            & & & +\Delta A_{Bt} & & -\Delta A_{CBt} & & 0 \\
        \text{Var. of Cash Money} 
            & & & -\Delta H_{Bt} & & +\Delta H_{CBt} & & 0 \\
        \text{Var. of loans (formal)} 
            & & & & & & & 0 \\
        \text{Var. of deposits (formal)} 
            & & & & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

## Wages and taxes payment

Firms pay formal wages. To balance Firms current and capital account we must use a residual ($F_t$) which represents a loss.

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Wages (formal)} 
            & +W_{H1t} & -W_{F1t} & & & & & 0 \\
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & -\Delta H_{Ht} & +\Delta H_{Ft} & & & & & 0 \\
        \text{Var. of deposits (formal)} 
            & & & & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Firms pay informal wages. 

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Wages (informal)} 
            & +W_{H2t} & -W_{F2t} & & & & & 0 \\
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & -\Delta H_{Ht} & +\Delta H_{Ft} & & & & & 0 \\
        \text{Var. of deposits (informal)} 
            & & & & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Households pay taxes.

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Taxes} 
            & -T_{Ht} & & & +T_{Gt} & & & 0 \\
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & +\Delta H_{Ht} & & & -\Delta H_{Gt} & & & 0 \\
        \text{Var. of deposits (formal)} 
            & & & & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Firms pay taxes.

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Taxes} 
            & & -T_{Ft} & & +T_{Gt} & & & 0 \\
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & & +\Delta H_{Ft} & & -\Delta H_{Gt} & & & 0 \\
        \text{Var. of deposits (formal)} 
            & & & & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Banks pay taxes.

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Taxes} 
            & & & -T_{Bt} & +T_{Gt} & & & 0 \\
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & & & +\Delta H_{Bt} & -\Delta H_{Gt} & & & 0 \\
        \text{Var. of deposits (formal)} 
            & & & & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$


## Profit distribution

Firms pay dividends. 

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Entrepreunarial Profits}
            & +F_{Ht}^d & -F_{Ft}^d & & & & & 0 \\
        \text{Var. of Cash Money} 
            & -\Delta H_{Ht} & +\Delta H_{Ft} & & & & & 0 \\
        \text{Var. of deposits (formal)} 
            & & & & & & & 0 \\
        \text{Var. of deposits (informal)} 
            & & & & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Banks pay dividends. 

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Entrepreunarial Profits}
            & +F_{Ht}^d & & -F_{Bt}^d & & & & 0 \\
        \text{Var. of Cash Money} 
            & -\Delta H_{Ht} & & +\Delta H_{Bt} & & & & 0 \\
        \text{Var. of deposits (formal)} 
            & & & & & & & 0 \\
        \text{Var. of deposits (informal)} 
            & & & & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Central bank transfer profit.

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Central Bank Profit}
            & & & & +F_{Gt} & -F_{CBt}^d & & 0 \\
        \text{Var. of advances} 
            & & & & & & & 0 \\
        \text{Var. of bonds} 
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & & & & -\Delta H_{Gt} & +\Delta H_{CBt} & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

## Public expenditures

Government pay wages.

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Wages (formal)} 
            & +W_{Ht} & & & -W_{Gt} & & & 0 \\
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of bonds} 
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & -\Delta H_{Ht} & & & +\Delta H_{Gt} & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Government pay doles.

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Doles} 
            & +G_{Ht}^D & & & -G_{Gt}^D & & & 0 \\
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of bonds} 
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & -\Delta H_{Ht} & & & +\Delta H_{Gt} & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

## Goods markets matching

Households consume goods.

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Consumption} 
            & -C_{Ht} & + C_{Ft} & & & & & 0 \\
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & +\Delta H_{Ht} & -\Delta H_{Ft} & & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$


Households import goods.

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Imports} 
            & -M_{Ht} & & & & & + M_{Wt} & 0 \\
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & +\Delta H_{Ht} & & & & -\Delta H_{CBt} & & 0 \\
        \text{Var. of Foreign Reserves} 
            & & & & & +\Delta R_{CBt}^f & -\Delta R_{Wt}^f & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Firms export goods.

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Exports} 
            & & +X_{Ht} & & & & -X_{Wt} & 0 \\
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & & -\Delta H_{Ht} & & & +\Delta H_{CBt} & & 0 \\
        \text{Var. of Foreign Reserves} 
            & & & & & -\Delta R_{CBt}^f & +\Delta R_{Wt}^f & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

## Financial debt repayments

Government repay bonds to Banks. 

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Int. on bonds} 
            & & & +r_{t-1}^B B_{Bt-1} & -r_{t-1}^B B_{Gt-1} & & & 0 \\
        \text{Entrepreneurial Profit}
            & & & & & & & 0 \\
        \text{Var. of bonds} 
            & & & +\Delta B_{Bt} & -\Delta B_{Gt} & & & 0 \\
        \text{Var. of Cash Money} 
            & & & -\Delta H_{Bt} & +\Delta H_{Gt} & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Government repay bonds to Central bank. 

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Int. on bonds} 
            & & & & -r_{t-1}^B B_{Gt-1} & +r_{t-1}^B B_{CBt-1} & & 0 \\
        \text{Central Bank Profit}
            & & & & & & & 0 \\
        \text{Var. of bonds} 
            & & & & -\Delta B_{Gt} & +\Delta B_{CBt} & & 0 \\
        \text{Var. of Cash Money} 
            & & & & +\Delta H_{Gt} & -\Delta H_{CBt} & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Firms repay formal loans. 

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Int. on loans (formal)} 
            & & -r_{t-1}^L L_{F1t-1} & +r_{t-1}^L L_{B1t-1} & & & & 0 \\
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & & +\Delta H_{Ft} & -\Delta H_{Bt} & & & & 0 \\
        \text{Var. of loans (formal)} 
            & & -\Delta L_{F1t} & +\Delta L_{B1t} & & & & 0 \\
        \text{Var. of deposits (formal)} 
            & & & & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Firms repay informal loans. 

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Int. on loans (informal)} 
            & & -r_{t-1}^L L_{F2t-1} & +r_{t-1}^L L_{B2t-1} & & & & 0 \\
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & & +\Delta H_{Ft} & -\Delta H_{Bt} & & & & 0 \\
        \text{Var. of loans (informal)} 
            & & -\Delta L_{F2t} & +\Delta L_{B2t} & & & & 0 \\
        \text{Var. of deposits (informal)} 
            & & & & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Banks pay interest on formal deposit of households

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Int. on deposits (formal)} 
            & +r_{t-1}^D D_{H1t-1} & & -r_{t-1}^D D_{B1t-1} & & & & 0 \\
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & & & & & & & 0 \\
        \text{Var. of deposits (formal)} 
            & -\Delta D_{H1t} & & +\Delta D_{B1t} & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Banks pay interest on informal deposit of households

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Int. on deposits (informal)} 
            & +r_{t-1}^D D_{H2t-1} & & -r_{t-1}^D D_{B2t-1} & & & & 0 \\
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & & & & & & & 0 \\
        \text{Var. of deposits (informal)} 
            & -\Delta D_{H2t} & & +\Delta D_{B2t} & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Banks pay interest on formal deposit of firms

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Int. on deposits (formal)} 
            & & +r_{t-1}^D D_{F1t-1} & -r_{t-1}^D D_{B1t-1} & & & & 0 \\
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & & & & & & & 0 \\
        \text{Var. of deposits (formal)} 
            & & -\Delta D_{F1t} & +\Delta D_{B1t} & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Banks pay interest on informal deposit of firms

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Int. on deposits (informal)} 
            & & +r_{t-1}^D D_{F2t-1} & -r_{t-1}^D D_{B2t-1} & & & & 0 \\
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & & & & & & & 0 \\
        \text{Var. of deposits (informal)} 
            & & -\Delta D_{F2t} & +\Delta D_{B2t} & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$


Banks repay advances.

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Int. on advances} 
            & & & -r_{t-1}^A A_{Bt-1} & & +r_{t-1}^A A_{CBt-1} & & 0 \\
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Central Bank Profit}
            & & & & & & & 0 \\
        \text{Var. of advances} 
            & & & -\Delta A_{Bt} & & +\Delta A_{CBt} & & 0 \\
        \text{Var. of Cash Money} 
            & & & +\Delta H_{Bt} & & -\Delta H_{CBt} & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

## Bonds market matching

Banks buy bonds. 

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of bonds} 
            & & & -\Delta B_{Bt} & +\Delta B_{Gt} & & & 0 \\
        \text{Var. of Cash Money} 
            & & & +\Delta H_{Bt} & -\Delta H_{Gt} & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Central Bank buy residuals bonds.

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Central Bank Profit}
            & & & & & & & 0 \\
        \text{Var. of bonds} 
            & & & -\Delta B_{Bt} & & +\Delta B_{CBt} & & 0 \\
        \text{Var. of Cash Money} 
            & & & +\Delta H_{Bt} & & -\Delta H_{CBt} & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$


## Deposit market matching

firms place deposits

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & & +\Delta H_{Ft} & -\Delta H_{Bt} & & & & 0 \\
        \text{Var. of deposits (formal)} 
            & & -\Delta D_{F1t} & +\Delta D_{B1t} & & & & 0 \\
        \text{Var. of deposits (informal)} 
            & & -\Delta D_{F2t} & +\Delta D_{B2t} & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$


households place deposits

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & +\Delta H_{Ht} & & -\Delta H_{Bt} & & & & 0 \\
        \text{Var. of deposits (formal)} 
            & -\Delta D_{H1t} & & +\Delta D_{B1t} & & & & 0 \\
        \text{Var. of deposits (informal)} 
            & -\Delta D_{H2t} & & +\Delta D_{B2t} & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

## Firms and banks entry-exit
### Firms exit process

Defaulted firms reimburse residual loans (step 1 of exit) by:
1. using deposits
2. using cash
3. registering capital loss

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Entrepreunarial Profits}
            & & +F_{Ft}^d & -F_{Bt}^d & & & & 0 \\
        \text{Var. of Cash Money} 
            & & +\Delta H_{Ft} & -\Delta H_{Bt} & & & & 0 \\
        \text{Var. of loans (formal)} 
            & & -\Delta L_{F1t} & +\Delta L_{B1t} & & & & 0 \\
        \text{Var. of loans (informal)} 
            & & -\Delta L_{F2t} & +\Delta L_{B2t} & & & & 0 \\
        \text{Var. of deposits (formal)} 
            & & +\Delta D_{F1t} & -\Delta D_{B1t} & & & & 0 \\
        \text{Var. of deposits (informal)} 
            & & +\Delta D_{F2t} & -\Delta D_{B2t} & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Defaulted firms transfer residual deposit (step 2 of exit)

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & & -\Delta H_{Ft} & +\Delta H_{Bt} & & & & 0 \\
        \text{Var. of deposits (formal)} 
            & & +\Delta D_{F1t} & -\Delta D_{B1t} & & & & 0 \\
        \text{Var. of deposits (informal)} 
            & & +\Delta D_{F2t} & -\Delta D_{B2t} & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Defaulted firms transfer residual cash (step 3 of exit)

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Entrepreunarial Profits}
            & +F_{Ht}^d & -F_{Ft}^d  & & & & & 0 \\
        \text{Var. of Cash Money} 
            & -\Delta H_{Ht} & +\Delta H_{Ft} & & & & & 0 \\
        \text{Var. of deposits (formal)} 
            & & & & & & & 0 \\
        \text{Var. of deposits (informal)} 
            & & & & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

### Formal banks exit process

Defaulted formal banks collect residual loans (step 1 of exit). 

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Entrepreunarial Profits}
            & & +F_{Ft}^d & -F_{Bt}^d & & & & 0 \\
        \text{Var. of Cash Money} 
            & & +\Delta H_{Ft} & -\Delta H_{Bt} & & & & 0 \\
        \text{Var. of loans (formal)} 
            & & -\Delta L_{F1t} & +\Delta L_{B1t} & & & & 0 \\
        \text{Var. of deposits (formal)} 
            & & +\Delta D_{F1t} & -\Delta D_{B1t} & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$


Defaulted formal banks reimburse residual deposits (step 2 of exit) 

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & -\Delta H_{Ht} & -\Delta H_{Ft} & +\Delta H_{Bt} & & & & 0 \\
        \text{Var. of deposits (formal)} 
            & +\Delta D_{H1t} & +\Delta D_{F1t} & -\Delta D_{B1t} & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

Defaulted formal banks transfer bonds to central bank (step 3 of exit) 

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of bonds} 
            & & & +\Delta B_{Bt} & & -\Delta B_{CBt} & & 0 \\
        \text{Var. of Cash Money} 
            & & & -\Delta H_{Bt} & & +\Delta H_{CBt} & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$


Defaulted formal banks reimburse residuals cash advances (step 4 of exit). 

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of advances} 
            & & & -\Delta A_{Bt} & & +\Delta A_{CBt} & & 0 \\
        \text{Var. of Cash Money} 
            & & & +\Delta H_{Bt} & & -\Delta H_{CBt} & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$


Defaulted formal banks reimburse residual reserves (step 5 of exit). 

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Entrepreunarial Profits}
            & +F_{Ht}^d & & -F_{Bt}^d & & & & 0 \\
        \text{Central Bank Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & -\Delta H_{Ht} &  & +\Delta H_{Bt} & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$


### Informal banks exit process

Defaulted informal banks collect residual loans (step 1 of exit). 

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Entrepreunarial Profits}
            & & +F_{Ft}^d  & -F_{Bt}^d & & & & 0 \\
        \text{Var. of Cash Money} 
            & & +\Delta H_{Ft} & -\Delta H_{Bt} & & & & 0 \\
        \text{Var. of loans (informal)} 
            & & -\Delta L_{F2t} & +\Delta L_{B2t} & & & & 0 \\
        \text{Var. of deposits (informal)} 
            & & +\Delta D_{F2t} & -\Delta D_{B2t} & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$


Defaulted informal banks reimburse residual deposits (step 2 of exit) 

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Entrepreunarial Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & -\Delta H_{Ht} & -\Delta H_{Ft} & +\Delta H_{Bt} & & & & 0 \\
        \text{Var. of deposits (informal)} 
            & +\Delta D_{H2t} & +\Delta D_{F2t} & -\Delta D_{B2t} & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$


Defaulted informal banks reimburse residual reserves (step 3 of exit). 

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Entrepreunarial Profits}
            & +F_{Ht}^d & & -F_{Bt}^d & & & & 0 \\
        \text{Central Bank Profits}
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & -\Delta H_{Ht} & & +\Delta H_{Bt} & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$


### Firms entry process

New firm are created.

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Var. of inventories} 
            & & & & & & & 0 \\
        \text{Entrepreunarial Profits}
            & +F_{Ht}^d & -F_{Ft}^d & & & & & 0 \\
        \text{Var. of Cash Money} 
            & -\Delta H_{Ht} & +\Delta H_{Ft} & & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$


### Banks entry process

New banks are created.

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks}  
        & \text{Government} & \text{Central Bank} & \text{Rest of World}
        & \Sigma \\
    \hline
        \text{Entrepreunarial Profits}
            & +F_{Ht}^d & & -F_{Bt}^d & & & & 0 \\
        \text{Var. of advances} 
            & & & & & & & 0 \\
        \text{Var. of Cash Money} 
            & -\Delta H_{Ht}^d & & +\Delta H_{Bt}^d & & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$
