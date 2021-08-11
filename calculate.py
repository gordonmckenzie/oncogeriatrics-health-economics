import yaml
import numpy as np
from markov_chains.chemotoxicity import cycleChemotoxicity
from markov_chains.mortality import cycleMortality
from markov_chains.treatment_change import cycleTreatmentChange

rng = np.random.default_rng() 

assumptions, utilisation_costs, pretreatment_costs, posttreatment_costs = None,None,None,None

with open("assumptions.yaml", 'r') as stream:
    assumptions = yaml.safe_load(stream)

with open("data/utilisation_costs.yaml", 'r') as stream:
    utilisation_costs = yaml.safe_load(stream)

def calculateCosts(patient, a):

    pretreatment_costs = np.genfromtxt('./templates/pretreatment_costs.tsv', dtype='S70,f8,f8', delimiter='\t')
    posttreatment_costs = np.genfromtxt('./templates/posttreatment_costs.tsv', dtype='S70,f8,f8', delimiter='\t')
   
    arm = 1 if a == 'usual' else 2

    reduced_surgical_complications_effect = 1
    if assumptions['reduced-surgical-complications-effect'] == True:
        reduced_surgical_complications_effect = rng.lognormal(-1.07, 0.97)

    complications_draw = rng.beta(3799, 5703)
    complications_adjusted = (complications_draw * reduced_surgical_complications_effect) if arm == 2 else complications_draw
    complications = True if rng.random() < complications_adjusted else False
    
    ###----Implementation----##
    if arm == 2:
        if assumptions['tablet-based-assessments'] is True:
            pretreatment_costs[0][2] = utilisation_costs['ga-using-tablet-technology'] + utilisation_costs['ga-using-tablet-staff']
        if assumptions['face-to-face-assessments-nurse'] is True:
            pretreatment_costs[3][2] = utilisation_costs['ga-using-nurse-f2f']
        if assumptions['face-to-face-assessments-consultant'] is True:
            pretreatment_costs[1][2] = utilisation_costs['ga-using-consultant']
        if assumptions['face-to-face-assessments-registrar'] is True:
            pretreatment_costs[2][2] = utilisation_costs['ga-using-registrar']
        if assumptions['telephone-assessments'] is True:
            pretreatment_costs[4][2] = utilisation_costs['ga-using-telephone-nurse-led']
    
    ###----Unmet needs----##
    for need in patient:
        # If seen by geriatrician does not need to be referred to geriatrician!
        if need['name'] == 'geriatrician' and need['status'] == True and assumptions['face-to-face-assessments-consultant'] == False and assumptions['face-to-face-assessments-registrar'] == False:
            pretreatment_costs[13][arm] = pretreatment_costs[13][arm] + utilisation_costs['outpatient-physician']
        if need['name'] == 'dietetics' and need['status'] == True:
            pretreatment_costs[6][arm] = utilisation_costs['dietician']
        if need['name'] == 'social_worker' and need['status'] == True:
            pretreatment_costs[7][arm] = utilisation_costs['social-worker']
        if need['name'] == 'ot' and need['status'] == True:
            pretreatment_costs[8][arm] = utilisation_costs['occupational-therapy']
        if need['name'] == 'pt' and need['status'] == True:
            pretreatment_costs[9][arm] = utilisation_costs['physiotherapist']
        if need['name'] == 'mental_health' and need['status'] == True:
            pretreatment_costs[10][arm] = utilisation_costs['cbt-course']
        if need['name'] == 'falls_clinic' and need['status'] == True:
            pretreatment_costs[11][arm] = utilisation_costs['falls-clinic']
        if need['name'] == 'other_physician' and need['status'] == True:
            pretreatment_costs[13][arm] = pretreatment_costs[13][arm] + utilisation_costs['outpatient-physician']
    
    ###----Sum pre-treatment costs----##
    total_pretreatment = sum(cost[arm] for cost in pretreatment_costs)

    t = 0
    ###----Post-treatment costs----###
    if assumptions['only-undergoing-chemotherapy'] == False and assumptions['only-undergoing-surgery'] == False:
        s = rng.dirichlet(assumptions['treatment-distributions'])
        max = np.amax(s)
        t = np.where(s == max)[0][0]

    ###---Differences due to treatment changes---###
    if assumptions['ga-changing-management-at-mdt-level'] == True and arm == 2:
        t, cost_diff = cycleTreatmentChange(t) # t is now changed and there is cost saving/additional costs
        posttreatment_costs[8][arm] = cost_diff

    if assumptions['only-undergoing-chemotherapy'] == False:
        bed_days_draw = rng.gamma(
            assumptions['bed-days-alpha'], 
            assumptions['bed-days-beta']
        ) 
        bed_days = bed_days_draw * assumptions['reduced-los-effect'] if arm == 2 else bed_days_draw

        requiring_itu = rng.binomial(
            1,
            assumptions['requiring-itu'] * assumptions['reduced-itu-admissions-effect'] if arm == 2 else assumptions['requiring-itu']
        ) 

        readmissions_draw = rng.beta(
            assumptions['readmissions-alpha'], 
            assumptions['readmissions-beta']
        ) 
        readmissions = readmissions_draw * assumptions['reduced-post-surgical-readmissions-effect'] if arm == 2 else readmissions_draw

    er_visits_draw = rng.beta(
        assumptions['er-visits-alpha'],
        assumptions['er-visits-beta']
    )
    er_visits = er_visits_draw * assumptions['reduced-er-visits-effect'] if arm == 2 else er_visits_draw

    chemo = False
    if t == 5 or t == 7 or t == 1 or t == 4 or assumptions['only-undergoing-chemotherapy'] == True:
        chemo = True
        chemotox = cycleChemotoxicity(arm)
        if chemotox == 2:
            posttreatment_costs[0][arm] = utilisation_costs['chemotherapy-toxicity-short-stay']
        elif chemotox == 3:
            posttreatment_costs[0][arm] = utilisation_costs['chemotherapy-toxicity-long-stay']
       
    if rng.random() < ((er_visits * assumptions['reduced-er-visits-effect']) if arm == 2 else er_visits):
        posttreatment_costs[7][arm] = utilisation_costs['er-visits']
    
    if t == 5 or t == 7 or t == 2 or t == 6 or assumptions['only-undergoing-surgery'] == True:    
        posttreatment_costs[1][arm] = bed_days * utilisation_costs['excess-bed-day'] # Should balance out but earlier discharge possible with GA (removes excess bed day cost)
        if requiring_itu == 1:
            posttreatment_costs[3][arm] = utilisation_costs['hdu-or-itu-admission']
        if rng.random() < readmissions:
            posttreatment_costs[6][arm] = utilisation_costs['surgical-readmission']

    ###----Sum post-treatment costs----##
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
        'changes_in_management_costs': posttreatment_costs[8][arm],
        'total': total_costs,
        'qalys': qalys
    }