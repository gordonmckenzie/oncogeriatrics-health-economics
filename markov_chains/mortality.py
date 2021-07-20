import numpy as np
import yaml

rng = np.random.default_rng()

assumptions = None
with open("assumptions.yaml", 'r') as stream:
    assumptions = yaml.safe_load(stream)

t = 10 #years

def cycleMortality(patient, arm, complications, chemo):

    initial_qaly = assumptions['initial-qaly']

    chemoMortality, surgicalMortality = False, False

    for param in patient:
        if param['name'] == "QALY_baseline" and param['arm'] == arm:
            initial_qaly = param['status']
        if param['name'] == "chemotherapy_mortality" and param['arm'] == arm and param['status'] == True:
            chemoMortality = True
        if param['name'] == "chemotherapy_mortality" and param['arm'] == arm and param['status'] == True:
            surgicalMortality = True

    risk_of_dying = assumptions['risk-of-dying-all-cancers'] if complications == False else assumptions['risk-of-dying-surgical-complications']
    cumulative_qalys = initial_qaly

    cycle = [[0, 1, initial_qaly, cumulative_qalys]]

    # Risk of chemotherapy mortality
    if chemoMortality != True and surgicalMortality != True:

        for i in range(0,t+1):

            # Chemotherapy toxicity decrement lasts for one year - https://www.sciencedirect.com/science/article/pii/S0959804911004230#b0110
            if i == 1 and chemo == True:
                initial_qaly - assumptions['chemotherapy-qaly-decrement']

            initial_qaly = initial_qaly - (initial_qaly * assumptions['nice-recommended-yearly-discount'])
            
            cumulative_qalys += initial_qaly
            
            if rng.random() < risk_of_dying:
                cycle.append([i+1, 0, initial_qaly, cumulative_qalys])
                break
            else:
                cycle.append([i+1, 1, initial_qaly, cumulative_qalys])

    return cumulative_qalys

###-----TESTING------####

"""
pts = 0
means = []
while pts < 1000:
    dead = []
    mc = 0
    while mc < 1000:
        d = 0
        for i in range(0,t+1):
            initial_qaly = initial_qaly - (initial_qaly * 0.03)
            cumulative_qalys += initial_qaly
            if rng.random() < risk_of_dying:
                d = 1
                patient.append([i+1, 0, initial_qaly, cumulative_qalys])
                break
            else:
                patient.append([i+1, 1, initial_qaly, cumulative_qalys])
        dead.append(d)
        mc += 1
    means.append(np.mean(np.array(dead),axis=0))
    pts += 1

print(np.mean(np.array(means)*100,axis=0))
print(np.std(np.array(means)*100,axis=0))
"""

# print('Year','Alive','QALYs','Cumulative QALYs')
# for row in patient:
#     print(*row)