import numpy as np
import yaml, sys
from calculate import calculateCosts
from tabulate import tabulate

paramaters, assumptions = None, None

with open('./data/parameters.yaml', 'r') as stream:
    parameters = yaml.safe_load(stream)

with open("assumptions.yaml", 'r') as stream:
    assumptions = yaml.safe_load(stream)

rng = np.random.default_rng()

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
            if p['distribution'] == 'beta':
                a,b = 0,0
                _arm = 'both' if 'both' in p['stats'] else arm
                if p['stats'][_arm]['mean'] != 0:
                    mu = p['stats'][_arm]['mean']
                    ul = p['stats'][_arm]['ul_range']
                    ll = p['stats'][_arm]['ll_range']
                    sd = (ul - ll) / 3.92
                    a = (((1 - mu) / sd**2) - (1 / mu)) * mu**2
                    b = a * ((1 / mu) - 1)
                    g = rng.beta(a, b)
                    pr = rng.binomial(1,g)
                    r = True if pr == 1 else False
                    simulation.append({'name': p['name'], 'arm': arm, 'status': r})
                else:
                    simulation.append({'name': p['name'], 'arm': arm, 'status': False})

        costs = calculateCosts(simulation, arm)
        parameter_values_usual.append(simulation) if arm == 'usual' else parameter_values_cga.append(simulation)
        usual.append(list(costs.values())) if arm == 'usual' else cga.append(list(costs.values()))

        i += 1

# u = pd.DataFrame(usual, columns=['total_pretreatment', 'total_posttreatment', 'chemotherapy_toxicity', 'er_visits', 'postoperative_bed_days', 'other_postoperative', 'total_costs', 'qalys'])
# c = pd.DataFrame(cga, columns=['total_pretreatment', 'total_posttreatment', 'chemotherapy_toxicity', 'er_visits', 'postoperative_bed_days', 'other_postoperative', 'total_costs', 'qalys'])

dif = np.subtract(cga, usual)

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
    'Difference in treatment management changes (£)',
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
    inb_m = means[8] - (means[7] / c)
    inb_ll = ci_ll[8] - (ci_ll[7] / c)
    inb_ul = ci_ul[8] - (ci_ul[7] / c)
    t2.append(f"{round(inb_m,2):,} ({round(inb_ll,2):,} to {round(inb_ul,2):,})")

print("\n")
print(tabulate([t2], headers=['', 'CET = £13,000', 'CET = £20,000', 'CET = £30,000'], tablefmt="tsv"))


