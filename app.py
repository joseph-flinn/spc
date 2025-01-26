import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

from rules import rules


def generate_control_chart(data, mean, std, suffix=""):
    plt.style.use('_mpl-gallery')
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = range(1, len(data)+1)
    ax.plot(x, data, 'o-')
    
    ax.plot(x, [mean]*len(x), color='green', label='mean')
    ax.plot(x, [mean + std]*len(x), color='purple', label='URL')
    ax.plot(x, [mean - std]*len(x), color='purple', label='LRL')
    ax.plot(x, [mean + (2*std)]*len(x), color='yellow', label='UWL')
    ax.plot(x, [mean - (2*std)]*len(x), color='yellow', label='LWL')
    ax.plot(x, [mean + (3*std)]*len(x), color='red', label='UCL')
    ax.plot(x, [mean - (3*std)]*len(x), color='red', label='LCL')
    
    ax.set_xlim(1, len(data)+1)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    
    plt.title(f"Control Chart - {datafile}")
    plt.legend()
    plt.savefig(f"images/control-chart{suffix}.png", bbox_inches='tight')


# ===== Load the dataset =====
datafile = "datasets/three.csv"
data = list(pd.read_csv(datafile)['Value'])

mean = np.mean(data, axis=0)
std = np.std(data, axis=0)

# ===== Generate control chart image =====
generate_control_chart(data, mean, std, suffix=f"-{datafile.split('.')[0].split('/')[1]}")

# ===== Run all rules =====
issues = []

for rule in rules:
    issues = issues + rule.run(data, mean, std, verbose=False)

print("===== Detected Events =====")
for issue in issues:
    print(f"Rule: {issue[0]}, Point: {issue[1]}")