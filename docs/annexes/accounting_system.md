# Accounting System of dual monetary economy

Nous supposerons que les firmes et les banques ne sont divises en secteur formel et secteur informel. Nous utilisons plutot le concept de stock/flux formel/informel sur le marche du travail, des depots et du credit.

les formes de dualismes considerees sont:
- le dualisme geographique (urbain/rural)
- le dualisme technologique (moderne/traditionnelle)
- le dualisme financier (formel/informel)
- le dualisme du marche du travail (formel/informel)


On considere donc une economie monetaire dual ferme caracterise par:
- des secteurs primaire et secondaire
- des regions ruraux et urbains
- des marches du travail formels et informels
- des marches du credit formels et informels

On repartira les agents en:
- menages urbains (H1) et menages ruraux (H2)
- entreprises urbaines (F1) et entreprises rurales (F2)
- banques formelles (B1) et banques informelles (B2)
- Etat (G) et Banque Centrale (CB)


## Balance Sheet

$$
\begin{aligned}
 & \begin{array}{lccccccccc}
    \hline
        & \text{H1} &  \text{H2}
        & \text{F1} & \text{F2}
        & \text{B1} & \text{B2}
        & \text{G} & \text{CB} 
        & \Sigma \\
    \hline
    \text{Cash Money} 
        & +M_{H1t} & +M_{H2t} 
        & +M_{F1t} & +M_{F2t} 
        & +M_{B1t} & +M_{B2t} 
        & +M_{Gt} & -M_{CBt} 
        & 0 \\
    \text{Cash Advances} 
        & & 
        & & 
        & -A_{B1t} & 
        & & +A_{CBt}
        & 0 \\
    \text{Deposits (formal)} 
        & +D_{H11t} & +D_{H21t} 
        & +D_{F11t} & +D_{F21t} 
        & -D_{B1t} & 
        & & 
        & 0 \\
    \text{Deposits (informal)} 
        & +D_{H12t} & +D_{H22t}  
        & +D_{F12t} & +D_{F22t} 
        & & -D_{B2t} 
        & & 
        & 0 \\
    \text{Bonds} 
        & & 
        & &
        & +B_{B1t} &  
        & -B_{Gt} & +B_{CBt}
        & 0 \\
    \text{Loans (formal)} 
        & &
        & -L_{F11t} & -L_{F21t} 
        & +L_{B1t} &
        & & 
        & 0 \\
    \text{Loans (informal)} 
        & & 
        & -L_{F12t} & -L_{F22t} 
        & & +L_{B2t}
        & &  
        & 0 \\
    \text{Balance} 
        & -V_{H1t} & -V_{H2t} 
        & -E_{F1t} & -E_{F2t} 
        & -E_{B1t} & -E_{B2t} 
        & +V_{Gt} & 0 
        & 0\\
    \text{ } \\
    \hline
    \Sigma & 0 & 0 & 0 & 0 
           & 0 & 0 & 0 & 0
           & 0 \\
    \hline
 \end{array}
\end{aligned}
$$


## Transaction Matrix

$$
\begin{aligned}
& \begin{array}{lccccccccccc}
    \hline
        & \text{H1} &  \text{H2}
        & \text{F1} & \text{F2}
        & \text{B1} & \text{B2}
        & \text{G} & \text{CB} 
        & \Sigma \\
    \hline
        \text{Consumption (primary)} 
            & -C_{H11t} & -C_{H21t} 
            & & +Q_{F2t} 
            & & 
            & & 
            & 0 \\
        \text{Consumption (secondary)} 
            & -C_{H12t} & -C_{H22t} 
            & +Q_{F1t} & 
            & & 
            & & 
            & 0 \\
        \text{Wages (formal)} 
            & +W_{H11t} & +W_{H21t}
            & -W_{F1t} & 
            & & 
            & -W_{Gt} & 
            & 0 \\
        \text{Wages (informal)} 
            & +W_{H12t} & +W_{H22t} 
            & & -W_{F2t} 
            & &
            & & 
            & 0 \\
        \text{Doles} 
            & +G_{H1t}^D & +G_{H2t}^D 
            & & 
            & &
            & -G_{Gt}^D & 
            & 0 \\
        \text{Taxes} 
            & -T_{H1t} & -T_{H2t} 
            & -T_{F1t} & -T_{F2t}  
            & -T_{B1t} & 
            & +T_{Gt} & 
            & 0 \\
        \text{Int. on advances} 
            & & 
            & &
            & -R_{B1t}^A &  
            & & +R_{CBt}^A
            & 0 \\
        \text{Int. on bonds} 
            & &
            & & 
            & +R_{B1t}^B & 
            & -R_{Gt}^B & +R_{CBt}^B
            & 0 \\
        \text{Int. on loans (formal)} 
            & & 
            & -R_{F11t}^L & -R_{F21t}^L
            & +R_{B1t}^L &
            & & 
            & 0 \\
        \text{Int. on loans (informal)} 
            & & 
            & -R_{F12t}^L & -R_{F22t}^L
            & & +R_{B2t}^L
            & & 
            & 0 \\
        \text{Int. on deposits (formal)} 
            & +R_{H11t}^D & +R_{H21t}^D 
            & +R_{F11t}^D & +R_{F21t}^D 
            & -R_{B1t}^D & 
            & & 
            & 0 \\
        \text{Int. on deposits (informal)} 
            & +R_{H12t}^D & +R_{H22t}^D 
            & +R_{F12t}^D & +R_{F22t}^D 
            & & -R_{B2t}^D
            & & 
            & 0 \\
        \text{Entrepreneurial Profits}
            & +F_{H1t}^d & +F_{H2t}^d
            & -F_{F1t}^d & -F_{F2t}^d 
            & -F_{B1t}^d & -F_{B2t}^d 
            & & 
            & 0 \\
        \text{Central Bank Profits}
            & & 
            & &
            & &
            & +F_{Gt} & -F_{CBt} 
            & 0 \\
        \text{Var. of advances} 
            & & 
            & & 
            & +\Delta A_{B1t} & 
            & & -\Delta A_{CBt}
            & 0 \\
        \text{Var. of bonds} 
            & & 
            & & 
            & -\Delta B_{B1t} & 
            & +\Delta B_{Gt} & -\Delta B_{CBt}
            & 0 \\
        \text{Var. of Cash Money} 
            & -\Delta M_{H1t} & -\Delta M_{H2t} 
            & -\Delta M_{F1t} & -\Delta M_{F2t}
            & -\Delta M_{B1t} & -\Delta M_{B2t}
            & -\Delta M_{Gt} & +\Delta M_{CBt}
            & 0 \\
        \text{Var. of loans (formal)} 
            & & 
            & +\Delta L_{F11t} & +\Delta L_{F21t}
            & -\Delta L_{B1t} & 
            & & 
            & 0 \\
        \text{Var. of loans (informal)} 
            & & 
            & +\Delta L_{F12t} & +\Delta L_{F22t} 
            & & -\Delta L_{B2t} 
            & &
            & 0 \\
        \text{Var. of deposits (formal)} 
            & -\Delta D_{H11t} & -\Delta D_{H21t}
            & -\Delta D_{F11t} & -\Delta D_{F21t}
            & +\Delta D_{B1t} & 
            & & 
            & 0 \\
        \text{Var. of deposits (informal)} 
            & -\Delta D_{H12t} & -\Delta D_{H22t}
            & -\Delta D_{F12t} & -\Delta D_{F22t}
            & & +\Delta D_{B2t} 
            & & 
            & 0 \\
        \text{ } \\
    \hline
        \Sigma 
            & 0 & 0 & 0 & 0 
            & 0 & 0 & 0 & 0
            & 0 \\
    \hline
\end{array}
\end{aligned}
$$

