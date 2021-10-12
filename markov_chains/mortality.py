import numpy as np
import yaml

rng = np.random.default_rng()

assumptions = None
with open("assumptions.yaml", 'r') as stream:
    assumptions = yaml.safe_load(stream)

t = 10 # Total length of time in years

def getTransitionProbability(year=0, complications=False):
    survival = assumptions['10-year-survival-probabilities']
    mu_0, mu_1 = 0,0
    if complications == True:
        mu_0 = survival[1][year]
        mu_1 = survival[1][year+1]
    else:
        mu_0 = survival[0][year]
        mu_1 = survival[0][year+1]

    tp = 1 - (mu_1 / mu_0)

    return tp

def cycleMortality(patient, arm, complications, chemo):

    initial_qaly = rng.beta(assumptions['initial-qaly-alpha'], assumptions['initial-qaly-beta'])

    chemoMortality, surgicalMortality = False, False

    for param in patient:
        if param['name'] == "chemotherapy_mortality" and param['arm'] == arm and param['status'] == True:
            chemoMortality = True
        if param['name'] == "surgical_mortality" and param['arm'] == arm and param['status'] == True:
            surgicalMortality = True

    cumulative_qalys = initial_qaly

    year = 0

    # Risk of chemotherapy mortality
    if chemoMortality != True and surgicalMortality != True:

        for i in range(0,t):

            # Chemotherapy toxicity decrement lasts for one year - https://www.sciencedirect.com/science/article/pii/S0959804911004230#b0110
            if i == 1 and chemo == True:
                initial_qaly - rng.beta(assumptions['chemotherapy-qaly-decrement-alpha'], assumptions['chemotherapy-qaly-decrement-beta'])
            
            if rng.random() < (getTransitionProbability(i) if complications == False else getTransitionProbability(i, True)):
                break

            initial_qaly = initial_qaly - (initial_qaly * assumptions['nice-recommended-yearly-discount'])
            
            cumulative_qalys += initial_qaly

            year += 1   

    return cumulative_qalys
