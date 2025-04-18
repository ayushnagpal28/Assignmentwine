# -*- coding: utf-8 -*-
"""Assignment8.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1V3Jod-FQuidbmB0l1LEQP6pwKxD6Liu7
"""

from google.colab import drive
drive.mount('/content/drive')

import os
print(os.listdir("/content/drive/My Drive/"))

import pandas as pd

file_path = "/content/drive/My Drive/studentperformance.csv"
df = pd.read_csv(file_path)


print(df.head())

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, f_oneway

print(df.info())
print(df.head())

correlation_matrix = df[['math score', 'reading score', 'writing score']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
plt.title("Correlation Between Scores")
plt.show()

sns.boxplot(x="test preparation course", y="math score", data=df)
plt.title("Effect of Test Preparation on Math Score")
plt.show()

prep_yes = df[df["test preparation course"] == "completed"]["math score"]
prep_no = df[df["test preparation course"] == "none"]["math score"]

t_stat, p_value = ttest_ind(prep_yes, prep_no)
print(f"T-test for Test Prep Effect on Math Score: t-stat={t_stat}, p-value={p_value}")

sns.boxplot(x="parental level of education", y="math score", data=df)
plt.xticks(rotation=45)
plt.title("Effect of Parental Education on Math Score")
plt.show()

groups = [df[df["parental level of education"] == level]["math score"] for level in df["parental level of education"].unique()]
anova_stat, anova_p = f_oneway(*groups)
print(f"ANOVA Test for Parental Education Effect: F-stat={anova_stat}, p-value={anova_p}")

sns.boxplot(x="gender", y="math score", data=df)
plt.title("Gender Comparison: Math Scores")
plt.show()

male_scores = df[df["gender"] == "male"]["math score"]
female_scores = df[df["gender"] == "female"]["math score"]

t_stat_gender, p_value_gender = ttest_ind(male_scores, female_scores)
print(f"T-test for Gender Effect on Math Score: t-stat={t_stat_gender}, p-value={p_value_gender}")

df = pd.get_dummies(df, columns=['race/ethnicity', 'lunch', 'test preparation course'], drop_first=True)

education_order = {
    "some high school": 0,
    "high school": 1,
    "some college": 2,
    "associate's degree": 3,
    "bachelor's degree": 4,
    "master's degree": 5
}
df["parental level of education"] = df["parental level of education"].map(education_order)

df["total score"] = df["math score"] + df["reading score"] + df["writing score"]
df["average score"] = df["total score"] / 3

df["performance_category"] = pd.cut(df["average score"], bins=[0, 50, 75, 100], labels=["Low", "Medium", "High"])

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
df[['math score', 'reading score', 'writing score', 'total score', 'average score']] = scaler.fit_transform(
    df[['math score', 'reading score', 'writing score', 'total score', 'average score']]
)

X = df.drop(columns=['math score', 'reading score', 'writing score', 'performance_category'])
y = df['performance_category']

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


file_path = "/content/drive/My Drive/wine.csv"
wine_data = pd.read_csv(file_path)


print("First 5 rows of the dataset:")
print(wine_data.head())


print("\nDataset Columns:")
print(wine_data.columns)


print("\nMissing Values in Dataset:")
print(wine_data.isnull().sum())


print("\nSummary Statistics:")
print(wine_data.describe())


plt.figure(figsize=(12, 6))
sns.heatmap(wine_data.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Feature Correlation Heatmap")
plt.show()


correlation = wine_data.corr()['quality'].sort_values(ascending=False)
print("\nFeature Correlations with Wine Quality:")
print(correlation)


top_features = correlation[1:6]
plt.figure(figsize=(8, 4))
sns.barplot(x=top_features.index, y=top_features.values, palette="coolwarm")
plt.title("Top 5 Features Influencing Wine Quality")
plt.xlabel("Features")
plt.ylabel("Correlation with Quality")
plt.show()


features = top_features.index.tolist()
plt.figure(figsize=(12, 8))

for i, feature in enumerate(features, 1):
    plt.subplot(2, 3, i)
    sns.boxplot(x=wine_data['quality'], y=wine_data[feature], palette='coolwarm')
    plt.title(f"{feature} vs Wine Quality")

plt.tight_layout()
plt.show()

print("Missing Values in Each Column:")
print(wine_data.isnull().sum())

wine_data_cleaned = wine_data.dropna()

wine_data.fillna(wine_data.mean(), inplace=True)

wine_data.fillna(wine_data.mode().iloc[0], inplace=True)

from sklearn.impute import KNNImputer
imputer = KNNImputer(n_neighbors=5)
wine_data_imputed = pd.DataFrame(imputer.fit_transform(wine_data), columns=wine_data.columns)

from scipy.stats import shapiro
plt.figure(figsize=(15, 10))
df.hist(bins=30, figsize=(15, 10), color='blue', edgecolor='black')
plt.suptitle("Feature Distributions", fontsize=16)
plt.show()

non_normal_features = []
alpha = 0.05

for col in df.select_dtypes(include=['float64', 'int64']).columns:
    stat, p = shapiro(df[col].dropna())
    if p < alpha:
        non_normal_features.append(col)
        print(f"Feature '{col}' is not normally distributed (p-value = {p:.5f})")

print("\nNon-Normal Features:", non_normal_features)

import os
df_transformed = df.copy()

for col in non_normal_features:
    if (df[col] > 0).all():
        df_transformed[col + "_log"] = np.log1p(df[col])
        df_transformed[col + "_sqrt"] = np.sqrt(df[col])
        df_transformed[col + "_boxcox"], _ = boxcox(df[col] + 1)

plt.figure(figsize=(15, 10))
df_transformed.hist(bins=30, figsize=(15, 10), color='green', edgecolor='black')
plt.suptitle("Transformed Feature Distributions", fontsize=16)
plt.show()
os.makedirs("/mnt/data", exist_ok=True)
df_transformed.to_csv("/mnt/data/wine_transformed.csv", index=False)