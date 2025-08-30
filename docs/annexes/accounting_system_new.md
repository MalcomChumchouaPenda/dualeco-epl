# Accounting System of dual monetary economy


on considere une economie constituee de:
- 02 secteurs: rural et urbain
- 02 secteurs urbains: formel et informel
- 02 secteurs informels: avance et retarde

les formes de dualismes considerees sont:
- le dualisme geographique (urbain/rural)
- le dualisme technologique (avancee/retarde)
- le dualisme du marche du travail (formel/informel)

On a donc 04 secteurs $k$ dans lequel sont regroupes les entreprises:
- un secteur rural ($k = 1$)
- un secteur urbain formel ($k = 2$)
- un secteur urbain informel avancee ($k = 3$)
- un secteur urbain informel retardee ($k = 4$)

|     | Secteur 1 | Secteur 2 | Secteur 3 | Secteur 4 |
| --- | ---       | ---       | ---       | ---       |
| Region          | Rural | Urbain | Urbain    | Urbain    |
| Type de travail | Informel | Formel | Informel | Informel |
| Acces au credit | Non | Oui | Oui | Non |
| Biens produits  | Agricoles | Manufacturees | Manufacturees | Intermediaires |
| Technologie     | Retardee | Avancee | Avancee | Retardee |


On a egalement 06 categories $z$ de menages:

| Categorie | Secteur   | Statut       | Description             |
|:-:| ---               | ---          | ---                     |
| 1 | rural             | entrepreneur | paysans                 |
| 2 | urbain formel     | entrepreneur | entrepreneurs formels   |
| 3 | urbain informel   | entrepreneur | entrepreneurs informels |
| 4 | urbain formel     | salaries     | salaries formels        |
| 5 | urbain informel   | salaries     | salaries informels      |
| 6 | urbain            | *aucun*      | chomeurs                |



## Balance Sheet

$$
\begin{aligned}
 & \begin{array}{lcccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks} 
        & \text{Government} & \text{Central Bank} & \Sigma \\
    \hline
    \text{Cash Money} 
        & +\sum{M_{Hzt}} & +\sum{M_{Fkt}} & +M_{Bt} 
        & +M_{Gt} & -M_{CBt} & 0 \\
    \text{Cash Advances} 
        & & & -A_{Bt} 
        & & +A_{CBt} & 0 \\
    \text{Deposits} 
        & +\sum{D_{Hzt}} & +\sum{D_{Fkt}} & -D_{Bt} 
        & & & 0 \\
    \text{Bonds} 
        & & & +B_{Bt} 
        & -B_{Gt} & +B_{CBt} & 0 \\
    \text{Loans} 
        & & -\sum{L_{Fkt}} & +L_{Bt}
        & & & 0 \\
    \text{Balance} 
        & -\sum{V_{Hzt}} & -\sum{E_{Fkt}} & -E_{Bt} 
        & +V_{Gt} & 0 & 0\\
    \hline
    \Sigma & 0 & 0 & 0
           & 0 & 0 & 0 \\
    \hline
 \end{array}
\end{aligned}
$$


## Transaction Matrix

$$
\begin{aligned}
& \begin{array}{lcccccccccc}
    \hline
        & \text{Households} & \text{Firms} & \text{Banks} 
        & \text{Government} & \text{Central Bank} & \Sigma \\
    \hline
        \text{Consumption (goods 1)} 
            & -\sum{C_{H1zt}} & +\sum{Q_{F1kt}} & 
            & & & 0 \\
        \text{Consumption (goods 2)} 
            & -\sum{C_{H2zt}} & +\sum{Q_{F2kt}} & 
            & & & 0 \\
        \text{Consumption (goods 3)} 
            & -\sum{C_{H3zt}} & +\sum{Q_{F3kt}} & 
            & & & 0 \\
        \text{Wages (formal)} 
            & +\sum{W_{H1zt}} & -\sum{W_{F1kt}} & 
            & -W_{Gt} & & 0 \\
        \text{Wages (informal)} 
            & +\sum{W_{H0zt}} & -\sum{W_{F0kt}} & 
            & & & 0 \\
        \text{Doles} 
            & +\sum{G_{Hzt}^D} & &
            & -G_{Gt}^D & & 0 \\
        \text{Taxes} 
            & -\sum{T_{Hzt}} & -\sum{T_{Fkt}} & -T_{Bt}
            & +T_{Gt} & & 0 \\
        \text{Int. on advances} 
            & & & -R_{Bt}^A
            & & +R_{CBt}^A & 0 \\
        \text{Int. on bonds} 
            & & & +R_{Bt}^B 
            & -R_{Gt}^B & +R_{CBt}^B & 0 \\
        \text{Int. on loans} 
            & & -\sum{R_{Fkt}^L} & +R_{Bt}^L 
            & & & 0 \\
        \text{Int. on deposits} 
            & +\sum{R_{Hzt}^D} & +\sum{R_{Fkt}^D} & -R_{Bt}^D 
            & & & 0 \\
        \text{Entrepreneurial Profits}
            & +\sum{F_{Hzt}^d} & -\sum{F_{Fkt}^d} & -F_{Bt}^d 
            & & & 0 \\
        \text{Central Bank Profits}
            & & & 
            & +F_{Gt} & -F_{CBt} & 0 \\
        \text{Var. of advances} 
            & & & +\Delta A_{Bt}
            & & -\Delta A_{CBt} & 0 \\
        \text{Var. of bonds} 
            & & & -\Delta B_{Bt} 
            & +\Delta B_{Gt} & -\Delta B_{CBt} & 0 \\
        \text{Var. of cash money} 
            & -\sum{\Delta M_{Hzt}} & -\sum{\Delta M_{Fkt}} & -\Delta M_{Bt} 
            & -\Delta M_{Gt} & +\Delta M_{CBt} & 0 \\
        \text{Var. of loans} 
            & & +\sum{\Delta L_{Fkt}} & -\Delta L_{Bt} 
            & & & 0 \\
        \text{Var. of deposits} 
            & -\sum{\Delta D_{Hzt}} & -\sum{\Delta D_{Fkt}} & +\Delta D_{Bt} 
            & & & 0 \\
    \hline
        \Sigma 
            & 0 & 0 & 0
            & 0 & 0 & 0 \\
    \hline
\end{array}
\end{aligned}
$$

