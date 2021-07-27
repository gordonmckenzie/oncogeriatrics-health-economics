#import yaml
import numpy as np
# import pandas as pd
# from pgmpy.models import MarkovChain as MC
# from pgmpy.factors.discrete import State
# from scipy import stats

# assumptions = None
# with open("assumptions.yaml", 'r') as stream:
#     assumptions = yaml.safe_load(stream)

rng = np.random.default_rng()

def cycleChemotoxicity(toxicity_effect=1):

    # Distributions
    toxicity = rng.beta(12,11)
    readmission = rng.beta(9,61)
    los = rng.gamma(1, 1/0.277)

    state = 0

    if (rng.random() < toxicity) * toxicity_effect:
        state = 1
        if rng.random() < readmission:
            if los < 5:
                state = 2
            else: 
                state = 3

    return state

    """
    model = MC(['no_toxicity','toxicity', 'readmission'], [2, 2, 2])
    model.add_transition_model(
        'no_toxicity', {
            0: {0: toxicity, 1: 1 - toxicity},
            1: {0: toxicity, 1: 1 - toxicity}
        })
    model.add_transition_model(
        'toxicity', {
            0: {0: 1 - (readmission * toxicity), 1: readmission * toxicity},
            1: {0: 1 - (readmission * toxicity), 1: readmission * toxicity}
        })
    model.add_transition_model(
        'readmission', {
            0: {0: 1, 1: 0},
            1: {0: 1, 1: 0}
        })
    model.add_transition_model(
        'short_stay', {
            0: {0: 0 if los <5 else 1, 1: 1 if los <5 else 0}, 
            1: {0: 0 if los <5 else 1, 1: 1 if los <5 else 0}, 
        })
    model.add_transition_model(
        'long_stay', {
            0: {0: 0 if los >=5 else 1, 1: 1 if los >=5 else 0}, 
            1: {0: 1, 1: 0}
        })
    """
    #model.set_start_state([State('no_toxicity', 1),State('toxicity', 0), State('readmission', 0)])
    # print(model.sample())
    # checks = model.sample(size=5000)
    # print(stats.mode(checks))
    # print(np.mean(checks, axis=0))
    arr = model.sample().values[0]
    # print(arr)
    state = 0
    if np.count_nonzero(arr) != 0:
        state = next(i for i in range(len(arr)-1, -1, -1) if arr[i] == 1)

    # if state == 0: 
    #     return 'NO_TOXICITY'
    # elif state == 1: 
    #     return 'TOXICITY'
    # else:
    #     if los <5:
    #         return 'SHORT_STAY'
    #     else:
    #         return 'LONG_STAY'
    if state == 2:
        if los <5:
            state = 3
        else:
            state = 4
    
    return state
    #print(np.max(np.nonzero(arr)))
    # state = 0
    # try:
    #     state = np.max(np.nonzero(arr))
    # except: 
    #     pass

    # return state

# states = []
# for i in range(0,5000):
#     x = cycleChemotoxicity(0.5)
#     states.append(x)

# print(np.array(states).mean())

