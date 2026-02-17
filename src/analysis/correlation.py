import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def correlation_analysis(df):

    # Select numeric columns only
    numeric_df = df.select_dtypes(include=['number'])

    # Compute correlation
    corr_matrix = numeric_df.corr()

    print("Correlation Matrix:")
    print(corr_matrix)

    # Plot heatmap
    sns.heatmap(corr_matrix, annot=True)
    plt.title("Correlation Matrix")
    plt.show()

    return corr_matrix