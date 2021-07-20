import yaml
import numpy as np
from pgmpy.models import MarkovChain as MC
#from pgmpy.factors.discrete import State

assumptions = None
with open("assumptions.yaml", 'r') as stream:
    assumptions = yaml.safe_load(stream)

def cycleChemotoxicity(arm):
    model = MC(['no_toxicity','toxicity', 'readmission', 'short_stay', 'long_stay'], [2, 2, 2, 2, 2])
    model.add_transition_model(
        'no_toxicity', {
            0: {0: assumptions['chemotherapy-toxicity'][arm], 1: 1 - assumptions['chemotherapy-toxicity'][arm]}, 
            1: {0: assumptions['chemotherapy-toxicity'][arm], 1: 1 - assumptions['chemotherapy-toxicity'][arm]}
        })
    model.add_transition_model(
        'toxicity', {
            0: {0: 1 - assumptions['chemotherapy-toxicity'][arm], 1: assumptions['chemotherapy-toxicity'][arm]}, 
            1: {0: 1 - assumptions['chemotherapy-toxicity'][arm], 1: assumptions['chemotherapy-toxicity'][arm]}
        })
    model.add_transition_model(
        'readmission', {
            0: {0: 1 - assumptions['readmission-for-chemotherapy'][arm] * assumptions['chemotherapy-toxicity'][arm], 1: assumptions['readmission-for-chemotherapy'][arm] * assumptions['chemotherapy-toxicity'][arm]}, 
            1: {0: 1 - assumptions['readmission-for-chemotherapy'][arm] * assumptions['chemotherapy-toxicity'][arm], 1: assumptions['readmission-for-chemotherapy'][arm] * assumptions['chemotherapy-toxicity'][arm]}
        })
    model.add_transition_model(
        'short_stay', {
            0: {0: 1 - assumptions['readmission-for-chemotherapy'][arm] * assumptions['chemotherapy-toxicity'][arm] * assumptions['short-stay-following-chemotherapy-admission'][arm], 1: assumptions['readmission-for-chemotherapy'][arm] * assumptions['chemotherapy-toxicity'][arm] * assumptions['short-stay-following-chemotherapy-admission'][arm]}, 
            1: {0: 1 - assumptions['readmission-for-chemotherapy'][arm] * assumptions['chemotherapy-toxicity'][arm] * assumptions['short-stay-following-chemotherapy-admission'][arm], 1: assumptions['readmission-for-chemotherapy'][arm] * assumptions['chemotherapy-toxicity'][arm] * assumptions['short-stay-following-chemotherapy-admission'][arm]}, 
        })
    model.add_transition_model(
        'long_stay', {
            0: {0: 1 - assumptions['readmission-for-chemotherapy'][arm] * assumptions['chemotherapy-toxicity'][arm] * assumptions['long-stay-following-chemotherapy-admission'][arm], 1: assumptions['readmission-for-chemotherapy'][arm] * assumptions['chemotherapy-toxicity'][arm] * assumptions['long-stay-following-chemotherapy-admission'][arm]}, 
            1: {0: 1, 1: 0}
        })
    #model.set_start_state([State('no_toxicity', 0),State('toxicity', 0), State('readmission', 0), State('short_stay', 0), State('long_stay', 0)])
    #print(model.sample())
    #checks = model.sample(size=5000)
    #print(np.mean(checks, axis=0))
    arr = np.array(model.sample())
    #print(np.max(np.nonzero(arr)))
    state = 0
    try:
        state = np.max(np.nonzero(arr))
    except: 
        pass

    return state