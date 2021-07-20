import statsmodels.stats.api as sm

count1 = 1346+1977+311
count2 = 4215 + 4165 + 709

print(round((count1 / count2) * 100, 2))
ll, ul = sm.proportion_confint(count1, count2, method='wilson')
print(round(ll*100, 2), round(ul*100, 2))