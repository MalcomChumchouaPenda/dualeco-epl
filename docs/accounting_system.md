# Accounting System of SFC-Model of dual economy

Nous supposerons que les firmes et les banques ne sont divises en secteur formel et secteur informel. Nous utilisons plutot le concept de stock/flux formel/informel sur le marche du travail, des depots et du credit.

On considere donc 3 dualismes:
- dualisme technologique de Lewis (marche des biens)
- dualisme du travail de Fields (marche du travail)
- dualisme financier de Stiglitz (marche des depots et du credit)

## Balance Sheet

$$
\begin{aligned}
 & \begin{array}{lcccccc}
    \hline
        & \text{Households (H.)} & \text{Firms (F.)} 
        & \text{Banks (B.)} & \text{Government (G.)} 
        & \text{Central Bank (C.B.)} & \Sigma \\
    \hline
    \text{Inventories} 
        & & +V_{Ft} 
        & & 
        & & +V_{Ft} \\
    \text{HP Money} 
        & +M_{Ht} & +M_{Ft} 
        & +M_{Bt}-A_{Bt} & +M_{gt} 
        & -M_{cbt}+A_{cbt} & 0 \\
    \text{Deposits (formal)} 
        & +D_{H1t} & +D_{F1t} 
        & -D_{B1t} & 
        & & 0 \\
    \text{Deposits (informal)} 
        & +D_{H2t} & +D_{F2t} 
        & -D_{B2t} & 
        & & 0 \\
    \text{Bonds} 
        & & 
        & +B_{Bt} & -B_{gt} 
        & +B_{cbt} & 0 \\
    \text{Loans (formal)} 
        & & -L_{1t} 
        & +L_{1t} & 
        & & 0 \\
    \text{Loans (informal)} 
        & & -L_{2t} 
        & +L_{2t} & 
        & & 0 \\
    \text{Balance} 
        & -V_{Ht} & -E_{Ft} 
        & -E_{Bt} & +S_{gt} 
        & 0 & -V_{Ft}\\
    \hline
    \Sigma & 0 & 0 & 0 & 0 & 0 & 0\\
    \hline
 \end{array}
\end{aligned}
$$


## Transaction Matrix

$$
\begin{aligned}
& \begin{array}{lcccccccc}
    \hline
        & \text{H.} & \text{F. (CA)} & \text{F. (KA)} 
        & \text{B. (CA)} & \text{B. (KA)}  & \text{G.} 
        & \text{C.B. (CA)} & \text{C.B. (KA)} & \Sigma \\
    \hline
        \text{Consumption} 
            & -C_{Ht} & +Q_{Ft} & 
            & & & 
            & & & 0 \\
        \text{Var. of inventories} 
            & & +\Delta V_{Ft} & -\Delta V_{Ft} 
            & & & 
            & & & 0 \\
        \text{Wages (formal)} 
            & +W_{H1t} & -W_{F1t} & 
            & & & -W_{gt} 
            & & & 0 \\
        \text{Wages (informal)} 
            & +W_{H2t} & -W_{F2t} & 
            & & & 
            & & & 0 \\
        \text{Doles} 
            & +G_{Ht}^D & & 
            & & & -G_{gt}^D 
            & & & 0 \\
        \text{Taxes} 
            & -T_{Ht} & -T_{Ft} & 
            &-T_{Bt} & & +T_{gt} 
            & & & 0 \\
        \text{Int. on advances} 
            & & & 
            & -r_{t-1}^A A_{Bt-1} & & 
            & +r_{t-1}^A A_{cbt-1} & & 0 \\
        \text{Int. on bonds} 
            & & & 
            & +r_{t-1}^B B_{Bt-1} & & -r_{t-1}^B B_{gt-1}
            & +r_{t-1}^B B_{cbt-1} & & 0 \\
        \text{Int. on loans (formal)} 
            & & -r_{1t-1}^L L_{F1t-1} & 
            & +r_{1t-1}^L L_{B1t-1} & & 
            & & & 0 \\
        \text{Int. on loans (informal)} 
            & & -r_{2t-1}^L L_{F2t-1} & 
            & +r_{2t-1}^L L_{B2t-1} & & 
            & & & 0 \\
        \text{Int. on deposits (formal)} 
            & +r_{1t-1}^D D_{H1t-1} & +r_{1t-1}^D D_{F1t-1} & 
            & -r_{1t-1}^D D_{B1t-1} & & 
            & & & 0 \\
        \text{Int. on deposits (informal)} 
            & +r_{2t-1}^D D_{H2t-1} & +r_{2t-1}^D D_{F2t-1} & 
            & -r_{2t-1}^D D_{B2t-1} & & 
            & & & 0 \\
        \text{Net Entrepreneurial Profits}
            & +F_{Ht}^d & -F_{Ft}+T_{Ft} & +F_{Ft}-T_{Ft}-F_{Ft}^d
            & -F_{Bt}+T_{Bt} & +F_{Bt}-T_{Bt}-F_{Bt}^d & 
            & & & 0 \\
        \text{Central Bank Profits}
            & & & 
            & & & +F_{gt}
            & -F_{cbt} & +F_{cbt}-F_{cbt}^d & 0 \\
        \text{Var. of advances} 
            & & & 
            & & +\Delta A_{Bt} & 
            & & -\Delta A_{cbt} & 0 \\
        \text{Var. of bonds} 
            & & & 
            & & -\Delta B_{Bt} & +\Delta B_{gt}
            & & -\Delta B_{cbt} & 0 \\
        \text{Var. of HP money} 
            & -\Delta M_{Ht} & & -\Delta M_{Ft}
            & & -\Delta M_{Bt} & -\Delta M_{gt}
            & & +\Delta M_{cbt} & 0 \\
        \text{Var. of loans (formal)} 
            & & & +\Delta L_{F1t}
            & & -\Delta L_{B1t} & 
            & & & 0 \\
        \text{Var. of loans (informal)} 
            & & & +\Delta L_{F2t}
            & & -\Delta L_{B2t} & 
            & & & 0 \\
        \text{Var. of deposits (formal)} 
            & -\Delta D_{H1t} & & -\Delta D_{F1t}
            & & +\Delta D_{B1t} & 
            & & & 0 \\
        \text{Var. of deposits (informal)} 
            & -\Delta D_{H2t} & & -\Delta D_{F2t}
            & & +\Delta D_{B2t} & 
            & & & 0 \\
    \hline
        \Sigma & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

