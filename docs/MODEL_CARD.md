# Model Card

## Current Status

This repository currently provides a customer churn **analytics dashboard**. It does not train or serve a machine-learning model.

## Churn Definition

When `cancellation_date` is available, the dashboard treats:

- `churn_flag = 1` when a cancellation date exists
- `churn_flag = 0` when no cancellation date exists

## Churn Risk

When `churn_score` is available, risk groups are generated as follows:

- Low: score up to 49
- Medium: score from 50 to 69
- High: score 70 or above

## Intended Use

- Exploratory customer churn analysis
- Retention planning
- Portfolio and educational demonstrations

## Not Intended For

- Fully automated customer treatment decisions
- Credit, insurance, employment or other high-impact decisions
- Production use without validation, monitoring and governance
