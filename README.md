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
