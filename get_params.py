import numpy as np
import json
from tabulate import tabulate

paramaters = None

with open('./data/parameters.json') as f:
    parameters = json.load(f)

table_cga = []
table_usual = []

for i, p in enumerate(parameters):
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
            g = np.random.default_rng().gamma(shape, scale, 5000)
            if p['arm'] == 'cga':
                table_cga.append([p['name'], round(g.mean(), 2), round(g.std(), 2), f"Gamma ({round(shape)},{round(scale)})"])
            else:
                table_usual.append([p['name'], round(g.mean(), 2), round(g.std(), 2), f"Gamma ({round(shape)},{round(scale)})"])
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
            g = np.random.default_rng().beta(a, b, 5000)
            if p['arm'] == 'cga':
                table_cga.append([p['name'],round(g.mean(), 2), round(g.std(), 2), f"Beta ({round(a)},{round(b)})"])
            else:
                table_usual.append([p['name'], round(g.mean(), 2), round(g.std(), 2), f"Beta ({round(a)},{round(b)})"])
    else:
        if p['arm'] == 'cga':
            table_cga.append([p['name'],0, 0, f"-"])
        else:
            table_usual.append([p['name'], 0, 0, f"-"])

subheader1 = [['Comprehensive Geriatric Assessment', '', '', '']]
subheader2 = [['Usual care', '', '', '']]
table = subheader1 + table_cga + subheader2 + table_usual
print(tabulate(table, headers=['Parameter', 'Mean (%)', 'Standard deviation (%)', 'Distribution in the probabilistic analysis'], tablefmt="tsv"))
