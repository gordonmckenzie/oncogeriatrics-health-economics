import yaml
import numpy as np
from markov_chains.chemotoxicity import cycleChemotoxicity
from markov_chains.mortality import cycleMortality

rng = np.random.default_rng()

assumptions, pretreatment_costs, posttreatment_costs = None,None,None

with open("assumptions.yaml", 'r') as stream:
    assumptions = yaml.safe_load(stream)

def calculateCosts(patient, a):

    pretreatment_costs = np.genfromtxt('./templates/pretreatment_costs.tsv',dtype='S70,f8,f8', delimiter='\t')
    posttreatment_costs = np.genfromtxt('./templates/posttreatment_costs.tsv',dtype='S70,f8,f8', delimiter='\t')
    utilisation_costs = np.genfromtxt('./data/utilisation_costs.tsv',dtype='S70,S20,f8,S20,f8,f8,S300', delimiter='\t')

    arm = 1 if a == 'usual' else 2

    complications = False

    for param in patient:
        if param['name'] == "major_surgical_complication" and param['arm'] == a and param['status'] == True:
            complications = True
    
    ###----Implementation----##
    if arm == 2:
        if assumptions['tablet-based-assessments'] is True:
            pretreatment_costs[0][2] = utilisation_costs[0][5]
        if assumptions['face-to-face-assessments'] is True:
            pretreatment_costs[3][2] = utilisation_costs[3][5]
        if assumptions['telephone-assessments'] is True:
            pretreatment_costs[3][2] = utilisation_costs[4][5]
    
    ###----Unmet needs----##
    for need in patient:
        if need['name'] == 'geriatrician' and need['status'] == True:
            pretreatment_costs[1][arm] = utilisation_costs[1][5]
        if need['name'] == 'dietetics' and need['status'] == True:
            pretreatment_costs[6][arm] = utilisation_costs[6][5]
        if need['name'] == 'social_worker' and need['status'] == True:
            pretreatment_costs[7][arm] = utilisation_costs[7][5]
        if need['name'] == 'ot' and need['status'] == True:
            pretreatment_costs[8][arm] = utilisation_costs[8][5]
        if need['name'] == 'pt' and need['status'] == True:
            pretreatment_costs[9][arm] = utilisation_costs[9][5]
        if need['name'] == 'mental_health' and need['status'] == True:
            pretreatment_costs[10][arm] = utilisation_costs[11][5]
        if need['name'] == 'falls_clinic' and need['status'] == True:
            pretreatment_costs[11][arm] = utilisation_costs[10][5]
        if need['name'] == 'other_physician' and need['status'] == True:
            pretreatment_costs[13][arm] = utilisation_costs[12][5]
    
    ###----Sum pre-treatment costs----##
    total_pretreatment = sum(cost[arm] for cost in pretreatment_costs)
    
    ###----Post-treatment costs----###
    s = np.random.dirichlet( #Decision making in health economic analysis, https://www.cancerdata.nhs.uk/treatments
        (0.335175413, 0.083228036, 0.209740598, 0.147376245, 0.049030028, 0.074862494, 0.072866805, 0.027720381)
        )
    max = np.amax(s)
    t = np.where(s == max)[0][0]

    chemo = False
    if t == 5 or t == 7 or t == 1 or t == 4:
        chemo = True
        chemotox = cycleChemotoxicity(a)
        if chemotox == 3:
            posttreatment_costs[0][arm] = utilisation_costs[19][5]
        elif chemotox == 4:
            posttreatment_costs[0][arm] = utilisation_costs[20][5]
       
        if rng.random() < assumptions['er-visits'][a]:
            posttreatment_costs[7][arm] = utilisation_costs[21][5]
    
    if t == 5 or t == 7 or t == 2 or t == 6:    
        posttreatment_costs[1][arm] = assumptions['bed-days'][a] * assumptions['cost-per-excess-bed-day'][a]
        if rng.random() < assumptions['requiring-itu'][a]:
            posttreatment_costs[3][arm] = utilisation_costs[16][5]
        if rng.random() < assumptions['readmissions'][a]:
            posttreatment_costs[6][arm] = utilisation_costs[22][5]

    ###----Sum pre-treatment costs----##
    total_posttreatment = sum(cost[arm] for cost in posttreatment_costs)
    total_posttreatment = 0 if np.isnan(total_posttreatment) else total_posttreatment

    ###----Sum total costs----##
    total_costs = total_pretreatment + total_posttreatment

    ###----QALYs--------------##
    qalys = cycleMortality(patient, arm, complications, chemo)

    return {
        'total_pretreatment': total_pretreatment,
        'total_posttreatment': total_posttreatment,
        'chemotherapy_toxicity': posttreatment_costs[0][arm],
        'er_visits': posttreatment_costs[7][arm],
        'postoperative_bed_days': posttreatment_costs[1][arm],
        'other_postoperative': posttreatment_costs[3][arm] + posttreatment_costs[6][arm],
        'total': total_costs,
        'qalys': qalys
    }