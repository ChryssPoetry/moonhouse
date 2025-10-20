import pandas as pd
import numpy as np

# Load CSV data (parsed from text)
data = pd.read_csv('dataset_purchases.csv')  # Assuming CSV is saved locally or parsed from text

# Inspect data
print(data.head())
print(data.info())
print(data.describe())

# Clean data
data['First payment'] = data['First payment'].replace({'\$': ''}, regex=True).astype(float, errors='ignore')
data['Rebill payment'] = data['Rebill payment'].replace({'\$': ''}, regex=True).astype(float, errors='ignore')
data['first_event_date'] = pd.to_datetime(data['first_event_date'], errors='coerce')

# Fill payment values based on is_trial
data.loc[data['is_trial'] == 1, 'First payment'] = data.loc[data['is_trial'] == 1, 'First payment'].fillna(6.99)
data.loc[data['is_trial'] == 1, 'Rebill payment'] = data.loc[data['is_trial'] == 1, 'Rebill payment'].fillna(29.99)
data.loc[data['is_trial'] == 0, 'First payment'] = data.loc[data['is_trial'] == 0, 'First payment'].fillna(40.00)
data.loc[data['is_trial'] == 0, 'Rebill payment'] = data.loc[data['is_trial'] == 0, 'Rebill payment'].fillna(40.00)

# Aggregate duplicates by user_id, summing renewals
data_agg = data.groupby(['user_id', 'is_trial', 'first_event_date', 'First payment', 'Rebill payment'])['subscription_renewal_amount'].sum().reset_index()

print(data_agg.head())
print(data_agg['is_trial'].value_counts())

# Calculate revenue
data_agg['initial_revenue'] = data_agg['First payment']
data_agg['renewals_revenue'] = data_agg['subscription_renewal_amount'] * data_agg['Rebill payment']
data_agg['total_revenue'] = data_agg['initial_revenue'] + data_agg['renewals_revenue']

# Filter to trial users
trial_users = data_agg[data_agg['is_trial'] == 1].copy()

print(trial_users[['user_id', 'initial_revenue', 'subscription_renewal_amount', 'renewals_revenue', 'total_revenue']].head())
print(f"Trial users count: {len(trial_users)}")
print(f"Avg initial revenue (trial): ${trial_users['initial_revenue'].mean():.2f}")
print(f"Avg renewals revenue (trial): ${trial_users['renewals_revenue'].mean():.2f}")

metric = trial_users['total_revenue'].sum()
print(f"Aggregate Revenue from Trial Users: ${metric:.2f}")

trial_summary = trial_users.groupby('subscription_renewal_amount').agg({
    'user_id': 'count',
    'total_revenue': ['sum', 'mean']
}).round(2)
trial_summary.columns = ['count_users', 'sum_revenue', 'mean_revenue']
trial_summary = trial_summary.reset_index()
print(trial_summary)

data_agg.to_excel('subscriptions_cleaned.xlsx', index=False)
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.bar(trial_summary['subscription_renewal_amount'], trial_summary['count_users'], color='skyblue')
plt.xlabel('Number of Renewals')
plt.ylabel('Number of Users')
plt.title('User Distribution by Renewals (Trial)')
plt.xticks(trial_summary['subscription_renewal_amount'])
plt.show()

plt.figure(figsize=(8, 5))
plt.bar(trial_summary['subscription_renewal_amount'], trial_summary['sum_revenue'], color='lightcoral')
plt.xlabel('Number of Renewals')
plt.ylabel('Total Revenue ($)')
plt.title('Total Revenue by Renewal Segment (Trial)')
plt.xticks(trial_summary['subscription_renewal_amount'])
plt.show()

trial_users['date'] = trial_users['first_event_date'].dt.date
cumulative_revenue = trial_users.groupby('date')['total_revenue'].sum().cumsum()
plt.figure(figsize=(10, 5))
plt.plot(cumulative_revenue.index, cumulative_revenue.values, marker='o', color='navy')
plt.xlabel('First Event Date')
plt.ylabel('Cumulative Revenue ($)')
plt.title('Cumulative Revenue Over Time (Trial)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
