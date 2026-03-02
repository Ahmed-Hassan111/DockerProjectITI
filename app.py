import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os



################# Data Collection #################

BASE_URL = "https://dummyjson.com/users"

def fetch_users_batch(limit=30, skip=0):
    url = f"{BASE_URL}?limit={limit}&skip={skip}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["users"]


MAX_USERS = 100

all_users = []
limit = 30
skip = 0

while len(all_users) < MAX_USERS:
    batch = fetch_users_batch(limit=limit, skip=skip)
    if not batch:
        break

    all_users.extend(batch)
    skip += limit

df = pd.json_normalize(all_users[:MAX_USERS])

os.makedirs("output", exist_ok=True)

df.to_csv("output/users.csv", index=False)

df =pd.read_csv("output/users.csv")

################# Basic Data Exploration #################
# Shape (rows, columns)
print("Shape:", df.shape)

# Column names
print("\nColumns:", df.columns.tolist())

# Data types
print("\nData Types:")
print(df.dtypes)

# Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Duplicate rows
print("\nDuplicate Rows:", df.duplicated().sum())

# Summary statistics for numeric columns
print("\nSummary Statistics:")
print(df.describe())

# Value counts for categorical columns
print("\nGender Distribution:")
print(df['gender'].value_counts())

print("\nBlood Group Distribution:")
print(df['bloodGroup'].value_counts().head(10))

print("\nEye Color Distribution:")
print(df['eyeColor'].value_counts())

print("\nRole Distribution:")
print(df['role'].value_counts())


################# Data Cleaning / Preparation #################

# Need to drop maidName in my vision this is not in right order and not important for my analysis
df.drop(columns=['maidenName'], inplace=True)

# birthdte should be in datetime format
df['birthDate'] = pd.to_datetime(df['birthDate'], errors='coerce')

# Need to clean senstive data and unwanted in analysis
sensitive_cols = [
    'password', 'ssn', 'ein', 
    'bank.cardNumber','userAgent', 'bank.iban',
    'crypto.wallet', 'macAddress', 'ip'
]
df.drop(columns=sensitive_cols, inplace=True)

# Check nulls in data 
print(df.isnull().sum()) #there is no nulls in data 

# If there is null in age, hight, weight
df['age'].fillna(df['age'].median(), inplace=True)
df['height'].fillna(df['height'].mean(), inplace=True)
df['weight'].fillna(df['weight'].mean(), inplace=True)

# Checking if age is correct by calculating age from birthdate and comparing it with age column in data
today = pd.to_datetime("today")
df['calculated_age'] = (today - df['birthDate']).dt.days // 365

print("\nCalculated Age:")
print(df[['age', 'calculated_age']].head(30))


################# Insights #################

# 1. Average age of users? 
average_age = df['age'].mean()
print(f"Average Age: {average_age:.2f}")

#2. Average age by gender? 
average_age_by_gender = df.groupby('gender')['age'].mean()
print("\nAverage Age by Gender:")
print(average_age_by_gender)

#3. Number of users per gender
users_per_gender = df['gender'].value_counts()
print("\nNumber of Users per Gender:")
print(users_per_gender)

#4. Top 10 cities with the most users? 
top_cities = df['address.city'].value_counts().head(10)
print("\nTop 10 Cities with the Most Users:")
print(top_cities)

#5. Average height and weight overall? 
average_height = df['height'].mean()
average_weight = df['weight'].mean()
print(f"\nAverage Height: {average_height:.2f}")
print(f"Average Weight: {average_weight:.2f}")


#6. Is there any obvious relationship between age and height/weight
correlation_age_height = df['age'].corr(df['height'])
correlation_age_weight = df['age'].corr(df['weight'])
print(f"\nCorrelation between Age and Height: {correlation_age_height:.2f}")
print(f"Correlation between Age and Weight: {correlation_age_weight:.2f}")
# used corr func to find correlation between age and height/weight, the values are close to 0 which indicates a weak relationship between age and height/weight in this dataset.

# will see all of this 6 insghts as visualizations using python libraries like matplotlib or seaborn in next steps.
################# Visualization #################

sns.set(style="darkgrid")

# 1. average age of users
plt.figure()
sns.histplot(df['age'], kde=True)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Count")
os.makedirs("output", exist_ok=True)
plt.savefig("output/age_distribution.png")
plt.close()


#2. Average age by gender? 
plt.figure()
sns.barplot(x=average_age_by_gender.index, y=average_age_by_gender.values)
plt.title("Average Age by Gender")
plt.xlabel("Gender")
plt.ylabel("Average Age")
os.makedirs("output", exist_ok=True)
plt.savefig("output/avg-age-per-gender.png")
plt.close()



#3. Number of users per gender
plt.figure()
sns.countplot(x='gender', data=df)
plt.title("Number of Users per Gender")
plt.xlabel("Gender")
plt.ylabel("Count")
os.makedirs("output", exist_ok=True)
plt.savefig("output/user-per-gender.png")
plt.close()


#4. Top 10 cities with the most users? 
plt.figure(figsize=(10, 6))
sns.barplot(x=top_cities.index, y=top_cities.values)
plt.title("Top 10 Cities with the Most Users")
plt.xlabel("City")
plt.ylabel("Count")
plt.xticks(rotation=45)
os.makedirs("output", exist_ok=True)
plt.savefig("output/Top10Cities.png")
plt.close()


#5. Average height and weight overall
plt.figure()
sns.barplot(x=['Height', 'Weight'], y=[average_height, average_weight])
plt.title("Average Height and Weight")
plt.xlabel("Metric")
plt.ylabel("Average Value")
os.makedirs("output", exist_ok=True)
plt.savefig("output/Avg-H-W.png")
plt.close()


#6. Is there any obvious relationship between age and height/weight digram for age vs height and age vs weight
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
sns.regplot(x='age', y='height', data=df)
plt.title("Age vs Height")
plt.xlabel("Age")
plt.ylabel("Height")

plt.subplot(1, 2, 2)
sns.regplot(x='age', y='weight', data=df)
plt.title("Age vs Weight")
plt.xlabel("Age")
plt.ylabel("Weight")

plt.tight_layout()
os.makedirs("output", exist_ok=True)
plt.savefig("output/finalimg.png")
plt.close()
