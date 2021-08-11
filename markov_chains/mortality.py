import numpy as np
import yaml, math

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

    #risk_of_dying = assumptions['risk-of-dying-all-cancers'] if complications == False else assumptions['risk-of-dying-surgical-complications']
    cumulative_qalys = initial_qaly

    #cycle = [[0, 1, initial_qaly, cumulative_qalys]]

    #alive = 1 # Testing

    year = 0

    # Risk of chemotherapy mortality
    if chemoMortality != True and surgicalMortality != True:

        for i in range(0,t):

            # Chemotherapy toxicity decrement lasts for one year - https://www.sciencedirect.com/science/article/pii/S0959804911004230#b0110
            if i == 1 and chemo == True:
                initial_qaly - rng.beta(assumptions['chemotherapy-qaly-decrement-alpha'], assumptions['chemotherapy-qaly-decrement-beta'])
            
            if rng.random() < (getTransitionProbability(i) if complications == False else getTransitionProbability(i, True)):
                #alive = 0 # Testing
                break

            initial_qaly = initial_qaly - (initial_qaly * assumptions['nice-recommended-yearly-discount'])
            
            cumulative_qalys += initial_qaly

            year += 1   
        
        #cycle.append([year, alive, initial_qaly, cumulative_qalys])

    #return [year, alive, initial_qaly, cumulative_qalys] # Testing

    return cumulative_qalys

####------TESTING--------####
# pts = 0
# test = []
# while pts < 5000:
#     patient = [
#         {"name": "QALY_baseline", "status": 0.62, "arm": 'usual'},
#         {"name": "chemotherapy_mortality", "status": True if rng.random() < 0.03 else False, "arm": 'usual'}, 
#         {"name": "surgical_mortality", "status": True if rng.random() < 0.01 else False, "arm": 'usual'},
#         {"name": "QALY_baseline", "status": 0.62, "arm": 'cga'},
#         {"name": "chemotherapy_mortality", "status": True if rng.random() < 0.03 else False, "arm": 'cga'}, 
#         {"name": "surgical_mortality", "status": True if rng.random() < 0.01 else False, "arm": 'cga'},
#     ]
#     test.append(cycleMortality(patient, 'cga' if rng.random() < 0.5 else 'usual', True if rng.random() < 0.3 else False, True if rng.random() < 0.3 else False))
#     pts += 1 

# print('Year','        Alive', '        Average final QALY', ' Cumulative QALYs')
# print(np.mean(np.array(test),axis=0))

###-----TESTING------####

# pts = 0
# initial_qaly = assumptions['initial-qaly']
# means = []
# patients = []
# while pts < 5000:
#     d = 0
#     year = 0
#     cumulative_qalys = 0
#     for i in range(0,t):
#         if rng.random() < (tps_cancer[i] if rng.random() < 0.2 else tps_cancer_comps[i]): # Dead
#             d = 1
#             break
#         cumulative_qalys += (initial_qaly - (initial_qaly * 0.03))
#         year += 1     
#     patients.append([year, d, cumulative_qalys]) # Alive
#     pts += 1    

# print(np.mean(np.array(means),axis=0))
# print(np.std(np.array(means),axis=0))

#print(np.mean(np.array(patients),axis=0))
# print('Year','Dead','Cumulative QALYs')
# for row in patients:
#     print(*row)