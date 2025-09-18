from scipy import stats
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def get(dati):
    #fitting di una distribuzione normale
    mu, sigma = stats.norm.fit(dati)
    # Test di bontà dell’adattamento (Kolmogorov-Smirnov)
    ks_stat, p_value = stats.kstest(dati, 'norm', args=(mu, sigma))
    print(mu, sigma, ks_stat, p_value)

if __name__ == "__main__":
    #"/home/gronz/PycharmProjects/AIatEdge/dati/gemma3n.csv"
    #"/home/gronz/PycharmProjects/AIatEdge/dati/QwenL4.csv"
    df = pd.read_csv("/home/gronz/PycharmProjects/AIatEdge/dati/gemma3n.csv")
    dati = df["clock_time"]
    sns.histplot(dati, kde=True)
    plt.show()
    get(dati)