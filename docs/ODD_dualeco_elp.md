---
title: A simple Agent-Based Model of Dual Economy for employment protection legislation evaluation
author: Malcom Chumchoua Penda
date: August 29, 2025
---

# A simple Agent-Based Model of Dual Economy for employment protection legislation evaluation
**Malcom Chumchoua Penda$^1$**   
<sup>$^1$ GRETA, Laboratoire d'Economie Theorique et Appliquee, Universite de Douala<sup>

**August 29, 2025**

<br>

## 1. Overview

### 1.1 Purpose and Patterns

### 1.2 Entities, State Variables, and Scales

### 1.3 Process overview and scheduling


## 2. Design Concepts

### 2.1. Basic Principles

### 2.2. Emergence

### 2.3. Adaptation

### 2.4 Objectives

### 2.5. Learning

### 2.6. Prediction

### 2.7. Sensing

### 2.8. Interaction

### 2.9. Stochasticity

### 2.10. Collectives

### 2.11. Observation



## 3. Details

### 3.1. Initialization

#### 3.1.1 Initialization of stocks, flows and prices

we adopted the following six-step strategy proposed by Caiani et al. [\[1\]](#1). :  
1. We derive an aggregate version of the model.
2. We constrain the aggregate model to be in a real stationary state associated with a nominal steady growth equal to gss. This imply that while all real quantities are constant, all prices and wages are growing at the same rate gss.19
3. We numerically solve the constrained model by setting exogenously reasonable values for the parameters for which some empirical information is available (e.g. unemployment rate, mark-ups, interest rates, and income and profit tax rates) or that we want to control (e.g. technological coefficients, number of agents in each sector, distribution of workers across sectors, loans and capital durations). We then obtain the initial values for each stock and flow variable of the aggregate steady state, as well as the values of some behavioral parameters, which are hence compatible with the steady/stationary state (e.g. the propensity to consume out of income, target capacity utilization and profit rates, initial capital and liquidity targets for banks).
4. We distribute each sector's aggregate values uniformly across agents' in that sector. In this way we derive the total value of each type of stock held by agents (e.g. households' and firms' deposits, total outstanding loans and real capital for each firm, total loans, and reserves and bonds for individual banks) and agents' past values to be used for expectations (e.g. past sales, past wages, and past profits).
5. To determine the original amount, outstanding values, age of durable stocks we assume that, in each of the periods before the simulation starts, firms have obtained a loan and consumption firms have also acquired new capital batches to replace old capital and maintain their productive capacity. We further assume that the real value (i.e. corrected for inflation) of each of these loans and capital batches was constant. Knowing the constant inflation rate gss and the amortization schedules for capital goods and loans, we can then derive the outstanding value for each of these stocks, so that the sum of these values is exactly equal to the amount determined in the previous step.
6. In order to set the initial network configuration, we randomly assign a previous period supplier (required for the matching mechanism) to each demand agent on each market, ensuring that each supplier has the same number of customers. Similarly, we assign to households' and firms' deposits, and to firms' loans a randomly selected bank, sot that each bank has the same number (and amount) of deposits and loans with the same number of agents.  The procedure20 just explained generates an important symmetry condition on agents' initial characteristics: that is, we start from a situation of perfect homogeneity between agents in order to limit as much as possible any possible bias embedded in asymmetric initial conditions, and we let heterogeneity emerge as a consequence of cumulative effects triggered by the stochastic factors embedded in agents' adaptive rules. Furthermore, by setting initial values based on SS

As explained in Section 4 our procedure is based on the imposition of a real stationary state coupled with a nominal steady state growth (i.e. inflation) at the macroeconomic level. More precisely, we first declare a set of exogenous parameters, aggregate variables, and stock-flow norms that we fix at reasonable values (see Section A.4). Then we employ the accounting identities and the steady state (SS hereafter) conditions to find a numerical solution to the system. For tractability and explanatory reasons we divided the SS system of equations in three sub-systems: the first block contains the equations which refer to capital good producers (Section A.1), the second presents the set of equations related to consumption firms (Section A.2), and the third (Section A.3) refers to households, banks and the public sector (government and central bank). Once the first block of the system is solved, its solution are employed to solve the second subsystem, whose solutions in turn are used to solve the third one.

##### 3.1.1.1 Firms equations

notons:

$$\zeta_1 = \frac{1} {1+g_{ss}} \tag{1}$$
$$\zeta_2 = \frac{g_{ss}} {1+g_{ss}} = 1-\zeta_1 \tag{2}$$

for each type $j$ of firms:

$$N_{Fj} = \sum\nolimits_{i} {N_{Fji}} \tag{3}$$
$$y_{Fj} = \phi_j N_{Fj} \tag{3}$$ 
$$W_{Fj} = w_j N_{Fj} \tag{3}$$
$$ p_j = { (1+m) W_{Fj} }/{ y_{Fj} } \tag{3}$$
$$ C_{Fj} = p_j  y_{Fj}  \tag{3}$$
$$ L_{Fj} =a_{Fj}^{D}{{f}^{L}} C_{Fj}  \tag{3}$$ 
$$ D_{Fj} =a_{Fj}^{D} {{\theta }^{W}}W_{Fj}  -{{M}_{Fj}} \tag{3}$$
$$ F_{Fj} = C_{Fj} +{{\zeta }_{1}}{{r}^{D}} D_{Fj} -W_{Fj}  -{{\zeta }_{1}}{{r}^{L}} L_{Fj}  \tag{3}$$ 
 $$ T_{Fj} =\tau n_{Fj}^{\tau } F_{Fj}  \tag{3}$$
 $$F_{Fj}^{d}=\rho   F_{Fj} - T_{Fj}   \tag{3}$$
 $$ F_{Fj} - T_{Fj} -F_{Fj}^{d}={{\zeta }_{2}} D_{Fj} +{{\zeta }_{2}}{{M}_{Fj}}-{{\zeta }_{2}} L_{Fj}  \tag{3}$$


##### 3.1.1.2 Households equations

$${W_{Hi}}={w_{G}}{N_{Gi}}+\sum\nolimits_j{w_j {N_{Fji}}}        \tag{1}$$
 $${{Z}_{Hi}}={N_{Gi}}+\sum\nolimits_{j}{{N_{Fji}}}          \tag{2}$$
 $${{J}_{Hi}}=a_{Hi}^{J}{{\kappa }^{J}}{{w}^{\min }}{{Z}_{Hi}}          \tag{3}$$
 $$R_{F}^{L}=\sum\nolimits_{j}{{{\zeta }_{1}}{{r}^{L}} L_{Fj} }           \tag{4}$$
 $$F_{B}^{d}=\rho R_{F}^{L}             \tag{5}$$
 $$F_{Hi}^{d}=\sum\nolimits_{j}{a_{Fji}^{F}F_{Fkj}^{d}}+a_{Bi}^{F}F_{B}^{d}      \tag{6}$$
 $$Y_{Hi}^{N}={W_{Hi}}+F_{Hi}^{d}+{{J}_{Hi}}        \tag{7}$$
 
 $$f_{Hi}^{C}={Y_{Hi}^{N}}/{\sum\nolimits_{i}{Y_{Hi}^{N}}}\;         \tag{8}$$
 $${{C}_{H}}=\sum\nolimits_{j}{ C_{Fj} }           \tag{9}$$
 $${{C}_{Hi}}=f_{Hi}^{C}{{C}_{H}}           \tag{10}$$
 
 $${ y_{Hi}}=Y_{Hi}^{N}+{{\zeta }_{1}}{{r}^{D}}{{D}_{Hi}}        \tag{11}$$
 $${{T}_{Hi}}=\tau n_{Hi}^{\tau } { y_{Hi}}-{{J}_{Hi}}         \tag{12}$$
 $$Y_{Hi}^{d}={ y_{Hi}}-{{T}_{Hi}}           \tag{13}$$
 $${{\zeta }_{2}}{{M}_{Hi}}+{{\zeta }_{2}}{{D}_{Hi}}=Y_{Hi}^{d}-{{C}_{Hi}}      \tag{14}$$
 $${{\zeta }_{2}}{{D}_{Hi}}=a_{Hi}^{D} Y_{Hi}^{d}-{{C}_{Hi}}        \tag{15}$$

##### 3.1.1.3 Banks, Government and Central Bank equations

 $${{D}_{B}}={{D}_{H}}+{{D}_{F}}             \tag{1}$$
 $${{L}_{B}}=\sum\nolimits_{j}{{{L}_{Fj}}}             \tag{2}$$
 $${{A}_{B}}=0              \tag{3}$$
 $${{F}_{H}}=\sum\nolimits_{j}{ C_{Fj} }           \tag{11}$$
 $${{F}_{B}}={{\zeta }_{1}}{{r}^{L}}{{L}_{B}}+{{\zeta }_{1}}{{r}^{B}}{{B}_{B}}-{{\zeta }_{1}}{{r}^{D}}{{D}_{B}}    \tag{4}$$
 $${{T}_{B}}=\tau {{F}_{B}}               \tag{5}$$
 $${{E}_{B}}={{L}_{B}}+{{B}_{B}}+{{M}_{B}}-{{D}_{B}}        \tag{6}$$
 $${{E}_{B}}={{\theta }^{E}} {{L}_{B}}+{{B}_{B}}+{{M}_{B}}         \tag{7}$$
 
 $${W_{G}}={w_{G}}\sum\nolimits_{i}{{N_{Gi}}}           \tag{8}$$
 $${{J}_{G}}=\sum\nolimits_{i}{{{J}_{Hi}}}              \tag{9}$$
 $${{M}_{G}}=0              \tag{10}$$
 $${{A}_{CB}}={{A}_{B}}              \tag{11}$$
 $${{F}_{CB}}={{F}_{G}}              \tag{12}$$
 $${{M}_{CB}}={{B}_{CB}}             \tag{13}$$
 $${{T}_{G}}={{T}_{H}}+{{T}_{F}}+{{T}_{B}}           \tag{14}$$
 $${{B}_{G}}={{B}_{B}}+{{B}_{CB}}            \tag{15}$$
 
 $${{\zeta }_{2}}{{B}_{G}}={W_{G}}+{{J}_{G}}+{{\zeta }_{1}}{{r}^{B}}{{B}_{G}}-{{T}_{G}}-{{F}_{G}}   \tag{16}$$


### 3.2. Input Data

### 3.3. Submodels

## References
<a id="1">[1]</a> 
Caiani et al., “Agent Based-Stock Flow Consistent Macroeconomics: Towards a Benchmark Model.”