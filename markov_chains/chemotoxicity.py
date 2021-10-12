import yaml
import numpy as np

assumptions = None
with open("assumptions.yaml", 'r') as stream:
    assumptions = yaml.safe_load(stream)

rng = np.random.default_rng()

def cycleChemotoxicity(arm):

    # Distributions
    toxicity_draw = rng.beta(12,11)
    readmission = rng.beta(9,61)
    los = rng.gamma(1, 1/0.277)

    reduced_chemotherapy_toxicity_effect = 1
    if assumptions['reduced-chemotherapy-toxicity-effect'] == True:
        reduced_chemotherapy_toxicity_effect = rng.lognormal(-0.53, 0.85)

    state = 0

    if rng.random() < ((toxicity_draw * reduced_chemotherapy_toxicity_effect) if arm == 2 else toxicity_draw):
        state = 1
        if rng.random() < readmission:
            if los <= 1:
                state = 2
            else: 
                state = 3

    return state

