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

we adopted the following six-step strategy {cite:p}`perez2011python`:  
1. We derive an aggregate version of the model.
2. We constrain the aggregate model to be in a real stationary state associated with a nominal steady growth equal to gss. This imply that while all real quantities are constant, all prices and wages are growing at the same rate gss.19
3. We numerically solve the constrained model by setting exogenously reasonable values for the parameters for which some empirical information is available (e.g. unemployment rate, mark-ups, interest rates, and income and profit tax rates) or that we want to control (e.g. technological coefficients, number of agents in each sector, distribution of workers across sectors, loans and capital durations). We then obtain the initial values for each stock and flow variable of the aggregate steady state, as well as the values of some behavioral parameters, which are hence compatible with the steady/stationary state (e.g. the propensity to consume out of income, target capacity utilization and profit rates, initial capital and liquidity targets for banks).
4. We distribute each sector's aggregate values uniformly across agents' in that sector. In this way we derive the total value of each type of stock held by agents (e.g. households' and firms' deposits, total outstanding loans and real capital for each firm, total loans, and reserves and bonds for individual banks) and agents' past values to be used for expectations (e.g. past sales, past wages, and past profits).
5. To determine the original amount, outstanding values, age of durable stocks we assume that, in each of the periods before the simulation starts, firms have obtained a loan and consumption firms have also acquired new capital batches to replace old capital and maintain their productive capacity. We further assume that the real value (i.e. corrected for inflation) of each of these loans and capital batches was constant. Knowing the constant inflation rate gss and the amortization schedules for capital goods and loans, we can then derive the outstanding value for each of these stocks, so that the sum of these values is exactly equal to the amount determined in the previous step.
6. In order to set the initial network configuration, we randomly assign a previous period supplier (required for the matching mechanism) to each demand agent on each market, ensuring that each supplier has the same number of customers. Similarly, we assign to households' and firms' deposits, and to firms' loans a randomly selected bank, sot that each bank has the same number (and amount) of deposits and loans with the same number of agents.  The procedure20 just explained generates an important symmetry condition on agents' initial characteristics: that is, we start from a situation of perfect homogeneity between agents in order to limit as much as possible any possible bias embedded in asymmetric initial conditions, and we let heterogeneity emerge as a consequence of cumulative effects triggered by the stochastic factors embedded in agents' adaptive rules. Furthermore, by setting initial values based on SS

### 3.2. Input Data

### 3.3. Submodels

## References
```{bibliography}
```