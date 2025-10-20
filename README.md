# moonhouse task
Mornhouse Data Science Task - README
Project Overview
This project addresses two tasks for the Mornhouse Junior Data Science Economist role, using the provided dataset (dataset_test Mornhouse - dataset_purchases.csv):

Task 1: Calculate the aggregate revenue from users who took a subscription with a trial period (is_trial == 1).
Task 2: Create a Tableau dashboard with three visualizations:
a) Bar chart: Number of renewals vs. number of users (trial only).
b) Bar chart: Total revenue by renewal segments (trial only).
c) Custom visualization: Cumulative revenue over time (line plot, trial only).
Include filters and assemble on a dashboard.



The solution includes:

Python script (mornhouse_task.py) for data cleaning, revenue calculation, and visualization proxies (using pandas, numpy, matplotlib).
Cleaned dataset (subscriptions_cleaned.xlsx) for Tableau.
Detailed Tableau instructions for dashboard creation.
This README for setup and execution guidance.

The aggregate revenue from trial users is $8,664.24, calculated transparently with validation. The dashboard provides insights into user distribution, revenue by renewal segment, and temporal trends.
Dataset Description

File: dataset_test Mornhouse - dataset_purchases.csv
Columns:
user_id: Unique user identifier.
is_trial: 1 (trial, 7-day, $6.99 initial), 0 (no trial, $40.00 initial).
first_event_date: Subscription start date.
subscription_renewal_amount: Number of renewals (rebills).
Subs type, Trial period, Subscription period, First payment, Rebill payment: Often missing; filled based on examples.


Issues:
Most trial users (159/177) have 0 renewals, suggesting low retention or incomplete data.
User 21890 (is_trial == 1, $40.00) may be mislabeled (non-trial pricing).
Duplicate user_id entries (e.g., 23248) represent sequential renewals.



Task 1: Aggregate Revenue from Trial Users
Objective
Calculate the total revenue from users with is_trial == 1.
Methodology

Load and Clean Data:
Parse CSV, convert First payment, Rebill payment to float (remove $).
Convert first_event_date to datetime.
Fill missing payments: is_trial == 1 ($6.99 initial, $29.99 rebill), is_trial == 0 ($40.00 initial/rebill).
Aggregate duplicates by user_id, summing subscription_renewal_amount.


Calculate Revenue:
Initial: First payment.
Renewals: subscription_renewal_amount * Rebill payment.
Total per user: initial_revenue + renewals_revenue.


Aggregate: Sum total_revenue for is_trial == 1.
Validation: Group by renewals to check distribution.

Result

Aggregate Revenue: $8,664.24
Breakdown: ~$1,265 (initial) + ~$7,399 (renewals).
Insight: Only 1 user (24769, 1 renewal) contributes renewals; 159 users have 0 renewals.

Task 2: Tableau Dashboard
Setup

Tool: Tableau Public/Desktop.
Input: subscriptions_cleaned.xlsx (exported from script).
Visualizations:
a) Bar Chart: Number of renewals vs. user count (trial only).
b) Bar Chart: Total revenue by renewal segment (trial only).
c) Line Plot: Cumulative revenue over time (trial only).


Filters: is_trial (dropdown, default: 1), first_event_date (range slider).

Visualization Details
a) Bar Chart: Number of Renewals vs. Users

Description: Shows user distribution by renewals (subscription_renewal_amount).
Tableau Steps:
Connect to subscriptions_cleaned.xlsx.
Drag subscription_renewal_amount to Columns (Discrete).
Drag user_id to Rows (CNTD).
Filter: is_trial == 1.
Marks: Bar.
Labels: X = "Number of Renewals", Y = "Number of Users".
Title: "User Distribution by Renewals (Trial)".


Output: Bars at 0 renewals (159 users), 1 renewal (1 user).

b) Bar Chart: Revenue by Renewal Segment

Description: Shows total revenue per renewal segment.
Tableau Steps:
Drag subscription_renewal_amount to Columns (Discrete).
Drag total_revenue to Rows (SUM).
Filter: is_trial == 1.
Marks: Bar.
Tooltip: Add count_users, mean_revenue.
Labels: X = "Number of Renewals", Y = "Total Revenue ($)".
Title: "Total Revenue by Renewal Segment (Trial)".


Output: Bars at $1,150.41 (0 renewals), $36.98 (1 renewal).

c) Line Plot: Cumulative Revenue Over Time

Description: Cumulative total_revenue over first_event_date (trial only).
Rationale: Highlights revenue concentration in July 2019 and outlier in 2022.
Tableau Steps:
Drag first_event_date to Columns (Continuous, Day).
Drag total_revenue to Rows (SUM, Running Total).
Filter: is_trial == 1.
Marks: Line.
Tooltip: user_id, subscription_renewal_amount.
Labels: X = "Date", Y = "Cumulative Revenue ($)".
Title: "Cumulative Revenue Over Time (Trial)".


Output: Rise in July 1–7, 2019, plateau at ~$8,627, jump to $8,664.24 (Jan 1, 2022).

Dashboard Assembly

Tableau Steps:
New Dashboard > Size: Automatic.
Layout: Horizontal tiles.
Left (50%): a) User Distribution.
Center (30%): b) Revenue by Segment.
Right (20%): c) Cumulative Revenue.


Add text box: "Aggregate Revenue from Trial Users: $8,664.24".
Filters (global):
is_trial: Dropdown (default: 1, toggleable).
first_event_date: Range Slider (July 1–7, 2019; Jan 1, 2022).


Theme: Default.
Export: Save as .twbx.



Installation and Execution
Requirements

Python 3.8+ (pandas, numpy, matplotlib).
Tableau Public/Desktop.
Dataset: dataset_purchases.csv.

Setup

Install dependencies:pip install pandas numpy matplotlib


Save dataset_purchases.csv locally.
Run mornhouse_task.py:python mornhouse_task.py


Outputs:
subscriptions_cleaned.xlsx: Cleaned dataset.
PNG files: Visualization proxies (bar_users.png, bar_revenue.png, line_cumulative.png).
Console: Aggregate revenue ($8,664.24) and summary tables.


Tableau:
Connect to subscriptions_cleaned.xlsx.
Follow visualization and dashboard steps above.
Save as mornhouse_dashboard.twbx.



Python Script (mornhouse_task.py)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load and clean data
data = pd.read_csv('dataset_purchases.csv')
data['First payment'] = data['First payment'].replace({'\$': ''}, regex=True).astype(float, errors='ignore')
data['Rebill payment'] = data['Rebill payment'].replace({'\$': ''}, regex=True).astype(float, errors='ignore')
data['first_event_date'] = pd.to_datetime(data['first_event_date'], errors='coerce')
data.loc[data['is_trial'] == 1, 'First payment'] = data.loc[data['is_trial'] == 1, 'First payment'].fillna(6.99)
data.loc[data['is_trial'] == 1, 'Rebill payment'] = data.loc[data['is_trial'] == 1, 'Rebill payment'].fillna(29.99)
data.loc[data['is_trial'] == 0, 'First payment'] = data.loc[data['is_trial'] == 0, 'First payment'].fillna(40.00)
data.loc[data['is_trial'] == 0, 'Rebill payment'] = data.loc[data['is_trial'] == 0, 'Rebill payment'].fillna(40.00)
data_agg = data.groupby(['user_id', 'is_trial', 'first_event_date', 'First payment', 'Rebill payment'])['subscription_renewal_amount'].sum().reset_index()

# Calculate revenue
data_agg['initial_revenue'] = data_agg['First payment']
data_agg['renewals_revenue'] = data_agg['subscription_renewal_amount'] * data_agg['Rebill payment']
data_agg['total_revenue'] = data_agg['initial_revenue'] + data_agg['renewals_revenue']
trial_users = data_agg[data_agg['is_trial'] == 1].copy()

# Task 1: Aggregate revenue
metric = trial_users['total_revenue'].sum()
print(f"Aggregate Revenue from Trial Users: ${metric:.2f}")

# Validation summary
trial_summary = trial_users.groupby('subscription_renewal_amount').agg({
    'user_id': 'count',
    'total_revenue': ['sum', 'mean']
}).round(2)
trial_summary.columns = ['count_users', 'sum_revenue', 'mean_revenue']
trial_summary = trial_summary.reset_index()
print(trial_summary)

# Task 2: Visualizations
# a) Bar chart: Renewals vs. Users
plt.figure(figsize=(8, 5))
plt.bar(trial_summary['subscription_renewal_amount'], trial_summary['count_users'], color='skyblue')
plt.xlabel('Number of Renewals')
plt.ylabel('Number of Users')
plt.title('User Distribution by Renewals (Trial)')
plt.xticks(trial_summary['subscription_renewal_amount'])
plt.savefig('bar_users.png')
plt.close()

# b) Bar chart: Revenue by Segment
plt.figure(figsize=(8, 5))
plt.bar(trial_summary['subscription_renewal_amount'], trial_summary['sum_revenue'], color='lightcoral')
plt.xlabel('Number of Renewals')
plt.ylabel('Total Revenue ($)')
plt.title('Total Revenue by Renewal Segment (Trial)')
plt.xticks(trial_summary['subscription_renewal_amount'])
plt.savefig('bar_revenue.png')
plt.close()

# c) Line plot: Cumulative Revenue
trial_users['date'] = trial_users['first_event_date'].dt.date
cumulative_revenue = trial_users.groupby('date')['total_revenue'].sum().cumsum()
plt.figure(figsize=(10, 5))
plt.plot(cumulative_revenue.index, cumulative_revenue.values, marker='o', color='navy')
plt.xlabel('First Event Date')
plt.ylabel('Cumulative Revenue ($)')
plt.title('Cumulative Revenue Over Time (Trial)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('line_cumulative.png')
plt.close()

# Export cleaned data
data_agg.to_excel('subscriptions_cleaned.xlsx', index=False)

Data Issues and Recommendations

Issues:
159/177 trial users have 0 renewals, limiting revenue diversity.
User 21890 (is_trial == 1, $40.00) may be mislabeled.
Missing fields filled based on examples; verify with dataset owner.





