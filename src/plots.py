import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_dnf_percent_by_circuits(df, era_name):
    df = df.sort_values('dnf_percent', ascending=False)
    y = df['circuitName']

    acc = df['accident_percent']
    mech = df['mechanical_percent']
    other = df['other_percent']

    plt.figure(figsize = (10,12))

    plt.barh(y, acc, label = 'Accidents / Car Damage')
    plt.barh(y, mech, label = 'Mechanical failure', left=acc)
    plt.barh(y, other, label = 'Other (Reg/Strategic', left=acc+mech)
    plt.xlabel('DNF % (share of starters')
    plt.ylabel('Circuit Name')
    plt.title(f"DNF % by Circuit (stacked by cause) - {era_name}")
    plt.legend()
    plt.gca().invert_yaxis()
    plt.show()
