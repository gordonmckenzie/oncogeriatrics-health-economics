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

#other care; chemotherapy only; surgery only; radiotherapy only; chemotherapy and radiotherapy; surgery and chemotherapy; surgery and radiotherapy; surgery, radiotherapy and chemotherapy
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

    for k,v in initial_state_map.items():
        if v == change:
            change_map = k
    
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
