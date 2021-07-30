import numpy as np
import pandas as pd
import json, yaml, sys
from calculate import calculateCosts
from tabulate import tabulate

paramaters, assumptions = None, None

with open('./data/parameters.json') as f:
    parameters = json.load(f)

with open("assumptions.yaml", 'r') as stream:
    assumptions = yaml.safe_load(stream)

rng = np.random.default_rng()

def isPresent(r):
    if rng.random() < r:
        return True
    else:
        return False

usual = []
cga = []
parameter_values_usual = []
parameter_values_cga = []
arms = ['usual', 'cga']

for arm in arms:
    if assumptions['progress'] == True:
        sys.stdout.write("\r")
        sys.stdout.flush()
    i = 0

    while i < assumptions['simulations']:

        #https://github.com/tqdm/tqdm
        if assumptions['progress'] == True:
            sys.stdout.write(f"\rSimulating {arm} arm: {round((i / (assumptions['simulations'])) * 100)}% complete")
            sys.stdout.flush()

        simulation = []

        #---Parameter estimations---#
        for p in parameters:
            if p['arm'] == arm:
                g = 0
                if p['mean'] != 0:
                    if p['distribution'] == 'gamma':
                        scale,shape = 0,0
                        #https://math.stackexchange.com/questions/2873763/is-it-possible-to-determine-shape-and-scale-for-a-gamma-distribution-from-a-mean
                        if 'sd' in p:
                            scale = p['sd']**2 / p['mean']
                        elif 'ci_95_ll' in p:
                            sd = (p['ci_95_ul'] - p['ci_95_ll']) / 3.92
                            scale = sd**2 / p['mean']
                        elif 'll_range' in p:
                            #Range rule for standard deviation
                            sd = (p['ul_range'] - p['ll_range']) / 4
                            scale = sd**2 / p['mean']
                        shape = p['mean']**2 / sd**2
                        g = np.random.default_rng().gamma(shape, scale)
                    elif p['distribution'] == 'beta':
                        a,b = 0,0
                        #https://stats.stackexchange.com/questions/12232/calculating-the-parameters-of-a-beta-distribution-using-the-mean-and-variance
                        if 'sd' in p:
                            a = (((1 - p['mean']) / p['sd']**2) - (1 / p['mean'])) * p['mean']**2
                        elif 'ci_95_ll' in p:
                            sd = (p['ci_95_ul'] - p['ci_95_ll']) / 3.92
                            a = (((1 - p['mean']) / sd**2) - (1 / p['mean'])) * p['mean']**2
                        elif 'll_range' in p:
                            #Range rule for standard deviation
                            sd = (p['ul_range'] - p['ll_range']) / 4
                            a = (((1 - p['mean']) / sd**2) - (1 / p['mean'])) * p['mean']**2
                        b = a * (1 / (p['mean']) - 1)
                        g = np.random.default_rng().beta(a, b)
                # Tests
                # print(np.mean(g), np.std(g))
                # print(np.percentile(g, 2.5),  np.percentile(g, 97.5))
                if len(p['name']) > 4 and p['name'][3] != "QALY":
                    simulation.append({'name': p['name'], 'arm': p['arm'], 'status': isPresent(g)})
                else:
                    simulation.append({'name': p['name'], 'arm': p['arm'], 'status': g})

        costs = calculateCosts(simulation, arm)
        parameter_values_usual.append(simulation) if arm == 'usual' else parameter_values_cga.append(simulation)
        usual.append(list(costs.values())) if arm == 'usual' else cga.append(list(costs.values()))

        i += 1

u = pd.DataFrame(usual, columns=['total_pretreatment', 'total_posttreatment', 'chemotherapy_toxicity', 'er_visits', 'postoperative_bed_days', 'other_postoperative', 'total_costs', 'qalys'])
c = pd.DataFrame(cga, columns=['total_pretreatment', 'total_posttreatment', 'chemotherapy_toxicity', 'er_visits', 'postoperative_bed_days', 'other_postoperative', 'total_costs', 'qalys'])

# print("\r")
# print(u.mean())
# print(c.mean())
#dif = np.subtract(cga, usual)
dif = c - u

#dif.to_csv('test.csv')

means = dif.mean(axis=0)
ci_ll = np.percentile(dif, 2.5, axis=0)
ci_ul = np.percentile(dif, 97.5, axis=0)

strings = [
    'Difference in pretreatment costs per patient (£)', 
    'Difference in posttreatment costs per patient (£)',
    'Difference in chemotherapy toxicity costs per patient (£)',
    'Difference in emergency department visits per patient (£)',
    'Difference in postoperative bed day costs per patient (£)',
    'Difference in other postoperative costs per patient (£)',
    'Difference in total pre- and post-treatment costs per patient (£)',
    'Difference in discounted QALYs per patient over 10 years'
]

t = []
for i,m in enumerate(means):
    t.append([strings[i], f"{round(means[i],2):,} ({round(ci_ll[i],2):,} to {round(ci_ul[i],2):,})"])

print("\n")
print(tabulate(t, headers=['', 'Mean (2.5th and 97.5th percentile values)'], tablefmt="tsv"))

t2 =[]
t2.append('Incremental net benefit (INB) of CGA compared to standard care (QALYs)')
cet = [13000,20000,30000]

for c in cet:
    inb_m = means[7] - (means[6] / c)
    inb_ll = ci_ll[7] - (ci_ll[6] / c)
    inb_ul = ci_ul[7] - (ci_ul[6] / c)
    t2.append(f"{round(inb_m,2):,} ({round(inb_ll,2):,} to {round(inb_ul,2):,})")

print("\n")
print(tabulate([t2], headers=['', 'CET = £13,000', 'CET = £20,000', 'CET = £30,000'], tablefmt="tsv"))


