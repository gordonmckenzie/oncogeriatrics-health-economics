#import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng()

# from pgmpy.models import MarkovChain as MC
# model = MC()

# model.add_variables_from(['single', 'multiple'], [2, 1])
# model.add_variables_from(['multiple', 'single'], [1, 1])
# model.add_variables_from(['multiple', 'bsc'], [1, 1])
# model.add_variables_from(['bsc', 'single'], [1, 1])
# model.add_variables_from(['single', 'bsc'], [2, 1])

# model.add_transition_model('single', {0:{0: 1, 1: 0}})

"""
other care; 
chemotherapy only; 
surgery only; 
radiotherapy only; 
chemotherapy and radiotherapy; 
surgery and chemotherapy; 
surgery and radiotherapy; 
surgery, radiotherapy and chemotherapy
"""
initial_state_map = {
    0: 'bsc',
    1: 'single',
    2: 'single',
    3: 'single',
    4: 'multiple',
    5: 'multiple',
    6: 'multiple',
    7: 'multiple'
}

#matrix
# transitionMatrix = [
#     ['single', 'multiple', 0.010667, 948.4582227],  
#     ['multiple', 'single', 0.016, -948.4582227],
#     ['multiple', 'bsc', 0.010666667, 5100.836111],
#     ['bsc', 'single', 0.008, -6049.294334],
#     ['single', 'bsc', 0.130666667, 6049.294334],
# ]

transitionName = [["single","multiple","bsc"],["multiple","single","bsc"],["bsc","single"]]
transitionMatrix = [[0.858666333, 0.010667, 0.130666667], [0.973333333, 0.016, 0.010666667], [0.992, 0.008]]
costMatrix = [[0, 948.4582227, 6049.294334], [0, -948.4582227, 5100.836111], [0, -6049.294334]]

def cycleTreatmentChange(initial_state):

    start_state = initial_state_map[initial_state]
    cost_diff = 0
    change = 0
    change_map = 0
    
    for i, tn in enumerate(transitionName):
        if tn[0] == start_state:
            change = rng.choice(transitionName[i],replace=True,p=transitionMatrix[i])
            for ii,t in enumerate(tn):
                if t == change:
                    cost_diff = costMatrix[i][ii]
                    pass

    # This will capture most decisions initially
    for k,v in initial_state_map.items():
        if v == change:
            change_map = k
    
    # If multiple treatment includes chemotherapy and surgery and the change is to single modality, 
    # this will almost always involve other care (e.g. hormonal therapy) or radiotherapy
    # Since radiotherpy has no further effects, allocation to 0 is the same
    if initial_state in [4,5,6,7] and change == "single":
        change_map = 0

    # If the initial state was other (e.g. BSC) and single treatment is proposed,
    # this will almost always be hormonal or radiotherapy so 0 again is appropriate 
    if initial_state == 0 and change == "single":
        change_map = 0
    
    # If the initial state was surgery only and now multiple treatments are proposed, 
    # this may include the addition of chemotherapy or chemo and radiotherapy
    # reflecting states 5 and 7 in a 2:1 ratio 
    if initial_state == 2 and change == "multiple":
        change_map = rng.choice([5,7], p=[0.33, 0.67])

    # If the initial state was other (e.g. hormonal therapy in this case) and now the decision is multiple therapies,
    # this may include chemotherapy in about 50% of cases
    if initial_state == 0 and change == "multiple":
        change_map = rng.choice([0, 1])
    
    return change_map, cost_diff

# test = []

# for _ in range(0,5000):
#     delta = cycleTreatmentChange(7)
#     test.append(delta)

# a = np.array(test)
# unique, counts = np.unique(a, return_counts=True)
# s = sum(counts)
# means = [count / s for count, _ in zip(counts, unique)]
# print(means)
