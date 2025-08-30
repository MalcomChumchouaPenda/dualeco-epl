# Accounting System of dual monetary economy

On considere une economie monetaire duale fermee avec deux secteurs geographiques:
- un secteur rural
- un secteur urbain

Chaque secteur geographique $k$ contient:
- un marche des biens unique
- des marches du travail formel et informel

Dans l'economie tout entiere, on a:
- un systeme bancaire unique
- une administration publique commune

les secteurs institutionnelles sont:
- les menages
- les entreprises
- les banques
- l'etat
- la Banque Centrale

$$
E = mc^2 \tag{1}
$$

Dans chaque secteur geographique, le secteur des menages est desagrege en 5 sous-secteurs $j$ :
- les entrepreneurs formels
- les entrepreneurs informels
- les salaries formels
- les salaries informels
- les chomeurs

De meme, dans chaque secteur geographique, le secteur des entreprises est desagrege en 2 sous-secteurs $j$ :
- les entreprises formels
- les entreprises informels


## Balance Sheet

$$
\begin{aligned}
 & \begin{array}{lcccccccc}
    \hline
        & \text{Households}
        & \text{Firms}  
        & \text{Banks} & \text{Government} & \text{C. Bank} & \Sigma \\
    \hline
    \text{HP Money} 
        & +\sum\nolimits_{i} M_{Hit}
        & +\sum\nolimits_{j} M_{Fjt}
        & +M_{Bt} & +M_{Gt} & -M_{CBt} & 0 \\
    \text{Cash Advances} 
        & & 
        & -A_{Bt} & & +A_{CBt} & 0 \\
    \text{Deposits} 
        & +\sum\nolimits_{i} D_{Hit}
        & +\sum\nolimits_{j} D_{Fjt}
        & -D_{Bt} & & & 0 \\
    \text{Bonds} 
        & & 
        & +B_{Bt} & -B_{Gt} & +B_{CBt} & 0 \\
    \text{Loans} 
        & 
        & -\sum\nolimits_{j} L_{Fjt}
        & +L_{Bt} & & & 0 \\
    \text{Balance} 
        & -\sum\nolimits_{i} V_{Hit}
        & -\sum\nolimits_{j} E_{Fjt}
        & -E_{Bt} & +V_{Gt} & 0 & 0\\
    \hline
    \Sigma & 0 & 0
           & 0 & 0 & 0 & 0\\
    \hline
 \end{array}
\end{aligned}
$$


## Transaction Matrix

$$
\begin{aligned}
& \begin{array}{lcccccccccc}
    \hline
        & \text{Households}
        & \text{Firms}  
        & \text{Banks} & \text{Government} & \text{C. Bank} & \Sigma \\
    \hline
        \text{Consumption} 
            & -\sum\nolimits_{i} C_{Hit}  
            & +\sum\nolimits_{j} Q_{Fjt}
            & & & & 0 \\
        \text{Wages} 
            & +\sum\nolimits_{i} W_{Hit}
            & -\sum\nolimits_{j} W_{Fjt}
            & & -W_{Gt} & & 0 \\
        \text{Doles} 
            & +\sum\nolimits_{i} J_{Hit}
            & 
            & & -J_{Gt} & & 0 \\
        \text{Taxes} 
            & -\sum\nolimits_{i} T_{Hit}
            & -\sum\nolimits_{j} T_{Fjt} 
            & -T_{Bt} & +T_{Gt} & & 0 \\
        \text{Int. on advances} 
            & & 
            & -R_{Bt}^A & & +R_{CBt}^A & 0 \\
        \text{Int. on bonds} 
            & & 
            & +R_{Bt}^B & -R_{Gt}^B & +R_{CBt}^B & 0 \\
        \text{Int. on loans} 
            & 
            & -\sum\nolimits_{j} R_{Fjt}^L 
            & +R_{Bt}^L & & & 0 \\
        \text{Int. on deposits} 
            & +\sum\nolimits_{i} R_{Hit}^D 
            & +\sum\nolimits_{j} R_{Fjt}^D 
            & -R_{Bt}^D & & & 0 \\
        \text{Entrepreneurial Profits}
            & +\sum\nolimits_{i} F_{Hit}^d 
            & -\sum\nolimits_{j} F_{Fjt}^d 
            & -F_{Bt}^d & & & 0 \\
        \text{Central Bank Profits}
            & & 
            & & +F_{Gt} & -F_{CBt} & 0 \\
        \text{Var. of advances} 
            & & 
            & +\Delta A_{Bt} & & -\Delta A_{CBt} & 0 \\
        \text{Var. of bonds} 
            & & 
            & -\Delta B_{Bt} & +\Delta B_{Gt} & -\Delta B_{CBt} & 0 \\
        \text{Var. of HP money} 
            & -\sum\nolimits_{i} \Delta M_{Hit}
            & -\sum\nolimits_{j} \Delta M_{Fjt}
            & -\Delta M_{Bt} & -\Delta M_{Gt} & +\Delta M_{CBt} & 0 \\
        \text{Var. of loans} 
            & 
            & +\sum\nolimits_{j} \Delta L_{Fjt}  
            & -\Delta L_{Bt} & & & 0 \\
        \text{Var. of deposits} 
            & -\sum\nolimits_{i} \Delta D_{Hit} 
            & -\sum\nolimits_{j} \Delta D_{Fjt}
            & +\Delta D_{Bt} & & & 0 \\
    \hline
        \Sigma 
            & 0 & 0 
            & 0 & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

