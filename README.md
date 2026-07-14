# Customer Churn Analytics Dashboard

An interactive, Power BI-style customer churn dashboard built with **Python, Streamlit, Pandas and Plotly**.  
The application lets users upload customer data, apply filters, review churn KPIs, explore customer segments and download the filtered results.

## Features

- Upload CSV, XLSX or XLS customer churn data
- Automatically clean column names and convert date fields
- Create useful fields such as:
  - Churn status
  - Churn-risk group
  - Customer tenure
  - Escalation flag
  - Complaint count
- Filter customers by:
  - Plan type
  - Contract type
  - State
  - Gender
  - Churn risk
  - Churn-score range
  - Subscription-date range
- View business KPIs:
  - Total customers
  - Churn rate
  - Retention rate
  - Average revenue per user
  - Revenue at risk
  - Average tenure
- Analyze churn by plan, contract, state and month
- Review CLTV, monthly charges, support escalations and CSAT
- Search customer records
- Download the filtered dataset as CSV
- View automatically generated retention insights

## Dashboard Pages

1. **Indicators** – KPIs, automated insights and priority-retention customers
2. **Filter Data** – complete filtered dataset with CSV download
3. **Monthly Dashboard** – compact Power BI-style visual dashboard
4. **Customer Table** – searchable customer-level view

## Project Structure

```text
customer-churn-analytics-dashboard/
├── .streamlit/
│   └── config.toml
├── data/
│   └── README.md
├── docs/
│   ├── MODEL_CARD.md
│   └── ETHICS.md
├── screenshots/
│   └── README.md
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Expected Data Columns

The dashboard works best when the uploaded file contains these columns:

| Column | Description |
|---|---|
| `customerid` | Unique customer identifier |
| `subscription_start_date` | Subscription start date |
| `plan_type` | Basic, Standard, Premium, etc. |
| `contract_type` | Monthly, Annual, etc. |
| `monthly_charges` | Customer's monthly charge |
| `churn_score` | Numerical churn-risk score |
| `cancellation_date` | Date of cancellation, if applicable |
| `cltv` | Customer lifetime value |
| `state` | Customer state |
| `gender` | Customer gender |
| `escalations` | Support escalation indicator |
| `csat_score` | Customer satisfaction score |

The application also supports an Excel workbook with separate sheets whose names include:

- `customer`
- `subscription`
- `support`

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/customer-churn-analytics-dashboard.git
cd customer-churn-analytics-dashboard
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the dashboard

```bash
streamlit run app.py
```
## Business Use Cases

- Identify high-risk customers
- Prioritize retention campaigns
- Compare churn across plans and contracts
- Estimate monthly revenue exposed to churn
- Study the relationship between complaints, escalations and churn
- Export filtered customer lists for further action

## Limitations

- Dashboard quality depends on the uploaded data
- Churn is inferred from cancellation information when available
- Churn-risk groups are created from score thresholds
- The project currently focuses on analytics and does not train a prediction model
- Production use would require authentication, monitoring and privacy controls

## Future Improvements

- Add an XGBoost churn-prediction model
- Add SHAP explanations
- Connect the dashboard to FastAPI
- Add role-based login
- Store prediction history in a database
- Add automated model monitoring
- Add Docker and CI/CD


