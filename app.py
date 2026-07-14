
from __future__ import annotations

import io
import sqlite3
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Customer Churn Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {display:none !important;}
    header[data-testid="stHeader"] {background: transparent;}
    .stApp {background:#eef1f5;}
    .block-container {
        max-width: 1600px;
        padding: .7rem 1rem 2rem 1rem;
    }
    h1,h2,h3,h4,p {font-family: Inter, "Segoe UI", Arial, sans-serif;}
    .app-shell {
        background:#d9dde3;
        border:1px solid #c8cdd5;
        border-radius:4px;
        padding:10px;
        box-shadow:0 10px 32px rgba(15,23,42,.10);
    }
    .topbar {
        background:#ffffff;
        border:1px solid #d7dbe1;
        padding:10px 14px;
        display:flex;
        align-items:center;
        justify-content:space-between;
        margin-bottom:8px;
    }
    .topbar-title {
        font-size:1.15rem;
        font-weight:800;
        color:#243447;
        letter-spacing:.01em;
    }
    .topbar-subtitle {font-size:.78rem;color:#758195;margin-top:2px;}
    .section-label {
        background:#ffffff;
        border:1px solid #d7dbe1;
        font-weight:800;
        color:#334155;
        padding:8px 10px;
        margin-bottom:8px;
        font-size:.95rem;
    }
    .nav-card {
        background:#ffffff;
        border:1px solid #d7dbe1;
        min-height:710px;
        padding:8px;
    }
    .brand-box {
        border-bottom:1px solid #e4e7ec;
        padding:10px 8px 18px 8px;
        margin-bottom:8px;
        text-align:center;
    }
    .brand-mark {
        width:38px;height:38px;border-radius:50%;
        background:linear-gradient(135deg,#0ea5e9,#14b8a6);
        color:#fff;display:inline-flex;align-items:center;justify-content:center;
        font-weight:900;margin-bottom:6px;
    }
    .brand-title {font-size:.86rem;font-weight:800;color:#253246;}
    .metric-card {
        background:#fff;
        border:1px solid #d9dde3;
        padding:12px 14px;
        min-height:96px;
        box-shadow:0 2px 8px rgba(15,23,42,.04);
    }
    .metric-title {font-size:.78rem;color:#667085;font-weight:700;}
    .metric-value {font-size:1.65rem;color:#263445;font-weight:850;margin:4px 0;}
    .metric-sub {font-size:.72rem;color:#8a94a3;}
    .chart-card {
        background:#fff;
        border:1px solid #d9dde3;
        padding:8px;
        box-shadow:0 2px 8px rgba(15,23,42,.04);
    }
    div[data-testid="stPlotlyChart"] {
        background:#fff;
        border:1px solid #d9dde3;
        padding:2px;
        box-shadow:0 2px 8px rgba(15,23,42,.04);
    }
    div[data-testid="stMetric"] {
        background:#fff;
        border:1px solid #d9dde3;
        padding:10px 12px;
        border-radius:0;
    }
    div[role="radiogroup"] {
        background:#fff;
        border:none;
        padding:0;
    }
    div[role="radiogroup"] label {
        width:100%;
        padding:8px 7px;
        border-radius:0;
        border-bottom:1px solid #edf0f3;
        margin:0;
        font-size:.84rem;
    }
    div[role="radiogroup"] label:hover {background:#f0f4f8;}
    .stSelectbox, .stMultiSelect, .stDateInput {
        background:#fff;
    }
    .stButton button, .stDownloadButton button {
        border-radius:0;
        font-weight:700;
    }
    .stDataFrame {border:1px solid #d9dde3;}
    .small-note {font-size:.72rem;color:#52606d;}

    /* High-contrast Streamlit controls */
    .stApp, .stApp p, .stApp span, .stApp label {color:#1f2937;}
    div[data-baseweb="select"] > div {
        background:#ffffff !important;
        color:#111827 !important;
        border-color:#9ca3af !important;
    }
    div[data-baseweb="select"] span {color:#111827 !important;}
    div[data-baseweb="popover"] {color:#111827 !important;}
    ul[role="listbox"] {background:#ffffff !important;}
    li[role="option"] {background:#ffffff !important;color:#111827 !important;}
    li[role="option"]:hover {background:#eaf2ff !important;}
    input, textarea {background:#ffffff !important;color:#111827 !important;}
    [data-testid="stFileUploaderDropzone"] {
        background:#ffffff !important;
        color:#111827 !important;
        border:1px dashed #7c8798 !important;
    }
    [data-testid="stFileUploaderDropzone"] small,
    [data-testid="stFileUploaderDropzone"] span,
    [data-testid="stFileUploaderDropzone"] p {color:#374151 !important;}
    [data-testid="stFileUploaderDropzone"] button {
        background:#0f4c81 !important;
        color:#ffffff !important;
        border:1px solid #0f4c81 !important;
    }
    div[role="radiogroup"] label, div[role="radiogroup"] label span {
        color:#1f2937 !important;
        opacity:1 !important;
    }
    .stCaption, [data-testid="stCaptionContainer"] {color:#475569 !important;}

    /* KPI cards: force readable values in every browser/theme */
    div[data-testid="stMetric"] {
        background:#ffffff !important;
        border:1px solid #cbd5e1 !important;
        padding:12px 14px !important;
        border-radius:4px !important;
        box-shadow:0 2px 8px rgba(15,23,42,.06) !important;
    }
    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] label p,
    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] p {
        color:#334155 !important;
        opacity:1 !important;
        font-weight:700 !important;
    }
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] > div,
    div[data-testid="stMetricValue"] p {
        color:#0f172a !important;
        opacity:1 !important;
        font-size:1.65rem !important;
        font-weight:850 !important;
        line-height:1.15 !important;
        -webkit-text-fill-color:#0f172a !important;
    }
    div[data-testid="stMetricDelta"],
    div[data-testid="stMetricDelta"] p {
        color:#475569 !important;
        opacity:1 !important;
    }
    [data-baseweb="tag"]{
    background:#E2F3E8 !important;
    border:1px solid #6AA84F !important;
}

    [data-baseweb="tag"] span{
        color:#38761D !important;
}

    /* Download button - Power BI style */
    div.stDownloadButton > button {
        background:#2563EB !important;
        color:#FFFFFF !important;
        border:1px solid #1D4ED8 !important;
        border-radius:6px !important;
        padding:0.55rem 1rem !important;
        font-weight:700 !important;
        box-shadow:0 2px 5px rgba(37,99,235,.20) !important;
    }
    div.stDownloadButton > button:hover {
        background:#1D4ED8 !important;
        border-color:#1E40AF !important;
        color:#FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)




REQUIRED_COLUMNS = {
    "customerid",
    "subscription_start_date",
    "plan_type",
    "contract_type",
    "monthly_charges",
    "churn_score",
}


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )
    return df


def clean_customer(customer: pd.DataFrame) -> pd.DataFrame:
    customer = normalize_columns(customer)
    customer = customer.rename(columns={"name": "customer_name"})
    customer = customer.drop(columns=["interests", "pincode"], errors="ignore")

    if "gender" in customer.columns:
        customer["gender"] = customer["gender"].replace(
            {"Men": "Male", "Women": "Female", "M": "Male", "F": "Female"}
        )

    if "dob" in customer.columns:
        customer["dob"] = pd.to_datetime(customer["dob"], errors="coerce")

    if {"state", "country"}.issubset(customer.columns):
        state_country = (
            customer.dropna(subset=["state", "country"])
            .drop_duplicates("state")
            .set_index("state")["country"]
            .to_dict()
        )
        customer["country"] = customer["country"].fillna(
            customer["state"].map(state_country)
        )

    return customer


def clean_subscription(subscription: pd.DataFrame) -> pd.DataFrame:
    subscription = normalize_columns(subscription)

    for col in [
        "subscription_start_date",
        "renewal_date",
        "cancellation_date",
    ]:
        if col in subscription.columns:
            subscription[col] = pd.to_datetime(subscription[col], errors="coerce")

    if "cancellation_date" in subscription.columns:
        subscription["churn_flag"] = (
            subscription["cancellation_date"].notna().astype(int)
        )
    elif "churn_flag" not in subscription.columns:
        subscription["churn_flag"] = 0

    return subscription


def clean_support(support: pd.DataFrame) -> pd.DataFrame:
    support = normalize_columns(support)
    support = support.drop(columns=["col_1", "comment"], errors="ignore")

    if "complaint_date" in support.columns:
        support["complaint_date"] = pd.to_datetime(
            support["complaint_date"], errors="coerce"
        )

    if "customerid" in support.columns:
        support["complaint_count"] = support.groupby("customerid")[
            "customerid"
        ].transform("count")

        sort_col = "complaint_date" if "complaint_date" in support.columns else "customerid"
        support = (
            support.sort_values(sort_col)
            .drop_duplicates("customerid", keep="last")
        )

    return support


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(df)

    date_cols = [
        "subscription_start_date",
        "renewal_date",
        "cancellation_date",
        "complaint_date",
        "dob",
    ]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    if "churn_flag" not in df.columns and "cancellation_date" in df.columns:
        df["churn_flag"] = df["cancellation_date"].notna().astype(int)

    if "escalations" in df.columns:
        df["escalation_label"] = df["escalations"].astype(str).str.upper()
        df["escalation_flag"] = (
            df["escalation_label"].isin(["Y", "YES", "1", "TRUE"]).astype(int)
        )
    else:
        df["escalation_label"] = "N"
        df["escalation_flag"] = 0

    if {"subscription_start_date", "cancellation_date"}.issubset(df.columns):
        today = pd.Timestamp.today().normalize()
        end_date = df["cancellation_date"].fillna(today)
        df["tenure_days"] = (
            end_date - df["subscription_start_date"]
        ).dt.days.clip(lower=0)

    if "churn_score" in df.columns:
        df["churn_risk"] = pd.cut(
            pd.to_numeric(df["churn_score"], errors="coerce"),
            bins=[-np.inf, 49, 69, np.inf],
            labels=["Low", "Medium", "High"],
        )

    if "monthly_charges" in df.columns:
        df["monthly_charges"] = pd.to_numeric(
            df["monthly_charges"], errors="coerce"
        )

    if "cltv" in df.columns:
        df["cltv"] = pd.to_numeric(df["cltv"], errors="coerce")

    if "complaint_count" in df.columns:
        df["complaint_count"] = pd.to_numeric(
            df["complaint_count"], errors="coerce"
        ).fillna(0)

    if "csat_score" in df.columns:
        df["csat_score"] = pd.to_numeric(df["csat_score"], errors="coerce")

    return df


def load_excel(uploaded_file) -> pd.DataFrame:
    excel = pd.ExcelFile(uploaded_file)
    sheets = {
        name.lower().strip(): pd.read_excel(uploaded_file, sheet_name=name)
        for name in excel.sheet_names
    }

    customer_key = next((k for k in sheets if "customer" in k), None)
    subscription_key = next((k for k in sheets if "subscription" in k), None)
    support_key = next((k for k in sheets if "support" in k), None)

    if customer_key and subscription_key:
        customer = clean_customer(sheets[customer_key])
        subscription = clean_subscription(sheets[subscription_key])

        df = subscription.merge(customer, on="customerid", how="left")

        if support_key:
            support = clean_support(sheets[support_key])
            df = df.merge(support, on="customerid", how="left")

        return engineer_features(df)

    first_sheet = next(iter(sheets.values()))
    return engineer_features(first_sheet)


@st.cache_data(show_spinner=False)
def load_uploaded_file(file_name: str, file_bytes: bytes) -> pd.DataFrame:
    buffer = io.BytesIO(file_bytes)

    if file_name.lower().endswith(".csv"):
        return engineer_features(pd.read_csv(buffer))

    if file_name.lower().endswith((".xlsx", ".xls")):
        return load_excel(buffer)

    raise ValueError("Please upload a CSV, XLSX, or XLS file.")


def format_currency(value: float) -> str:
    return f"₹{value:,.2f}"


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df.copy()

    # Power BI-style filter heading
    st.markdown(
        """
        <div style="
            background:#FFFFFF;
            border:1px solid #D1D5DB;
            border-left:5px solid #2563EB;
            padding:14px 18px;
            border-radius:6px;
            margin-bottom:14px;
            box-shadow:0 2px 6px rgba(0,0,0,0.05);
        ">
            <h4 style="margin:0;color:#1F2937;font-size:18px;font-weight:700;">
                🔎 Dashboard Filters
            </h4>
            <p style="margin:5px 0 0 0;color:#6B7280;font-size:13px;">
                Use these filters to update all KPIs, charts and tables.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    filter_specs = [
        ("Plan Type", "plan_type", c1),
        ("Contract Type", "contract_type", c2),
        ("State", "state", c3),
        ("Gender", "gender", c4),
        ("Churn Risk", "churn_risk", c5),
    ]

    selections = {}
    for label, column_name, container in filter_specs:
        if column_name in filtered.columns:
            options = sorted(
                filtered[column_name].dropna().astype(str).unique().tolist()
            )
            selections[column_name] = container.multiselect(
                label=label,
                options=options,
                default=options,
                key=f"filter_{column_name}",
            )

    c6, c7 = st.columns([1, 1.35])

    score_range = None
    if "churn_score" in filtered.columns:
        churn_scores = pd.to_numeric(filtered["churn_score"], errors="coerce")
        valid_scores = churn_scores.dropna()
        if not valid_scores.empty:
            minimum_score = int(valid_scores.min())
            maximum_score = int(valid_scores.max())
            score_range = c6.slider(
                label="Churn Score",
                min_value=minimum_score,
                max_value=maximum_score,
                value=(minimum_score, maximum_score),
                key="filter_churn_score",
            )

    selected_dates = None
    if "subscription_start_date" in filtered.columns:
        filtered["subscription_start_date"] = pd.to_datetime(
            filtered["subscription_start_date"], errors="coerce"
        )
        valid_dates = filtered["subscription_start_date"].dropna()
        if not valid_dates.empty:
            minimum_date = valid_dates.min().date()
            maximum_date = valid_dates.max().date()
            selected_dates = c7.date_input(
                label="Subscription Start Date",
                value=(minimum_date, maximum_date),
                min_value=minimum_date,
                max_value=maximum_date,
                key="filter_subscription_date",
            )

    for column_name, selected_values in selections.items():
        if selected_values:
            filtered = filtered[
                filtered[column_name].astype(str).isin(selected_values)
            ]
        else:
            filtered = filtered.iloc[0:0]

    if score_range is not None and "churn_score" in filtered.columns:
        filtered_scores = pd.to_numeric(filtered["churn_score"], errors="coerce")
        filtered = filtered[
            filtered_scores.between(score_range[0], score_range[1])
        ]

    if (
        isinstance(selected_dates, (tuple, list))
        and len(selected_dates) == 2
        and "subscription_start_date" in filtered.columns
    ):
        start_date, end_date = selected_dates
        filtered = filtered[
            filtered["subscription_start_date"].dt.date.between(start_date, end_date)
        ]

    info_col, download_col = st.columns([3, 1])

    with info_col:
        st.caption(f"Showing {len(filtered):,} of {len(df):,} customer records")

    with download_col:
        csv_data = filtered.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="⬇ Download Filtered Data",
            data=csv_data,
            file_name=f"filtered_customer_churn_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
            disabled=filtered.empty,
            key="download_filtered_data",
        )

    return filtered


def kpi_cards(df: pd.DataFrame) -> None:
    customers = df["customerid"].nunique() if "customerid" in df.columns else len(df)
    churn_rate = df["churn_flag"].mean() * 100 if "churn_flag" in df.columns else 0
    retention_rate = 100 - churn_rate
    arpu = df["monthly_charges"].mean() if "monthly_charges" in df.columns else 0
    revenue_risk = (
        df.loc[df["churn_flag"] == 1, "monthly_charges"].sum()
        if {"churn_flag", "monthly_charges"}.issubset(df.columns)
        else 0
    )
    avg_tenure = df["tenure_days"].mean() if "tenure_days" in df.columns else 0

    cols = st.columns(6)
    cols[0].metric("Customers", f"{customers:,}")
    cols[1].metric("Churn Rate", f"{churn_rate:.1f}%")
    cols[2].metric("Retention Rate", f"{retention_rate:.1f}%")
    cols[3].metric("ARPU", format_currency(arpu))
    cols[4].metric("Revenue at Risk", format_currency(revenue_risk))
    cols[5].metric("Avg. Tenure", f"{avg_tenure:,.0f} days")


def overview_page(df: pd.DataFrame) -> None:
    kpi_cards(df)
    st.markdown("### Churn Overview")

    col1, col2 = st.columns(2)

    with col1:
        if "churn_flag" in df.columns:
            counts = (
                df["churn_flag"]
                .map({0: "Retained", 1: "Churned"})
                .value_counts()
                .rename_axis("status")
                .reset_index(name="customers")
            )
            fig = px.pie(
                counts,
                names="status",
                values="customers",
                hole=0.58,
                title="Customer Status",
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if {"plan_type", "churn_flag"}.issubset(df.columns):
            plan = (
                df.groupby("plan_type", dropna=False)["churn_flag"]
                .mean()
                .mul(100)
                .reset_index(name="churn_rate")
            )
            fig = px.bar(
                plan,
                x="plan_type",
                y="churn_rate",
                text_auto=".1f",
                title="Churn Rate by Plan Type",
                labels={"plan_type": "Plan Type", "churn_rate": "Churn Rate (%)"},
            )
            st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        if {"contract_type", "churn_flag"}.issubset(df.columns):
            contract = (
                df.groupby("contract_type", dropna=False)["churn_flag"]
                .mean()
                .mul(100)
                .reset_index(name="churn_rate")
            )
            fig = px.bar(
                contract,
                x="contract_type",
                y="churn_rate",
                text_auto=".1f",
                title="Churn Rate by Contract Type",
            )
            st.plotly_chart(fig, use_container_width=True)

    with col4:
        if "churn_risk" in df.columns:
            risk = (
                df["churn_risk"]
                .astype(str)
                .value_counts()
                .rename_axis("risk")
                .reset_index(name="customers")
            )
            fig = px.bar(
                risk,
                x="risk",
                y="customers",
                text_auto=True,
                title="Customers by Churn Risk",
                category_orders={"risk": ["Low", "Medium", "High"]},
            )
            st.plotly_chart(fig, use_container_width=True)


def trend_page(df: pd.DataFrame) -> None:
    st.markdown("### Churn Trends")

    if {"cancellation_date", "churn_flag"}.issubset(df.columns):
        churned = df[df["churn_flag"] == 1].dropna(subset=["cancellation_date"]).copy()
        if not churned.empty:
            churned["month"] = churned["cancellation_date"].dt.to_period("M").astype(str)
            trend = churned.groupby("month").size().reset_index(name="churned_customers")
            fig = px.line(
                trend,
                x="month",
                y="churned_customers",
                markers=True,
                title="Monthly Churn Trend",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No cancellation records are available for the selected filters.")

    col1, col2 = st.columns(2)

    with col1:
        if {"state", "churn_flag"}.issubset(df.columns):
            state = (
                df.groupby("state")["churn_flag"]
                .mean()
                .mul(100)
                .sort_values(ascending=False)
                .head(15)
                .reset_index(name="churn_rate")
            )
            fig = px.bar(
                state,
                x="state",
                y="churn_rate",
                text_auto=".1f",
                title="Top States by Churn Rate",
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if {"subscription_type", "churn_flag"}.issubset(df.columns):
            source = (
                df.groupby("subscription_type")["churn_flag"]
                .mean()
                .mul(100)
                .reset_index(name="churn_rate")
            )
            fig = px.bar(
                source,
                x="subscription_type",
                y="churn_rate",
                text_auto=".1f",
                title="Churn by Acquisition Source",
            )
            st.plotly_chart(fig, use_container_width=True)


def revenue_page(df: pd.DataFrame) -> None:
    st.markdown("### Revenue & Customer Value")

    col1, col2 = st.columns(2)

    with col1:
        if {"plan_type", "monthly_charges"}.issubset(df.columns):
            revenue = (
                df.groupby("plan_type")["monthly_charges"]
                .sum()
                .reset_index(name="monthly_revenue")
            )
            fig = px.bar(
                revenue,
                x="plan_type",
                y="monthly_revenue",
                text_auto=".2s",
                title="Monthly Revenue by Plan",
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if {"churn_flag", "monthly_charges"}.issubset(df.columns):
            temp = df.copy()
            temp["status"] = temp["churn_flag"].map({0: "Retained", 1: "Churned"})
            fig = px.box(
                temp,
                x="status",
                y="monthly_charges",
                points="outliers",
                title="Monthly Charges by Customer Status",
            )
            st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        if {"cltv", "churn_score"}.issubset(df.columns):
            fig = px.scatter(
                df,
                x="churn_score",
                y="cltv",
                color="churn_risk" if "churn_risk" in df.columns else None,
                hover_data=["customerid"] if "customerid" in df.columns else None,
                title="CLTV vs Churn Score",
            )
            st.plotly_chart(fig, use_container_width=True)

    with col4:
        if {"plan_type", "cltv"}.issubset(df.columns):
            cltv = (
                df.groupby("plan_type")["cltv"]
                .mean()
                .reset_index(name="average_cltv")
            )
            fig = px.bar(
                cltv,
                x="plan_type",
                y="average_cltv",
                text_auto=".2f",
                title="Average CLTV by Plan",
            )
            st.plotly_chart(fig, use_container_width=True)


def support_page(df: pd.DataFrame) -> None:
    st.markdown("### Customer Support Analysis")

    col1, col2, col3 = st.columns(3)
    escalation_rate = (
        df["escalation_flag"].mean() * 100 if "escalation_flag" in df.columns else 0
    )
    avg_complaints = (
        df["complaint_count"].sum()
        / max(df["customerid"].nunique(), 1)
        if {"complaint_count", "customerid"}.issubset(df.columns)
        else 0
    )
    avg_csat = df["csat_score"].mean() if "csat_score" in df.columns else 0

    col1.metric("Escalation Rate", f"{escalation_rate:.1f}%")
    col2.metric("Avg. Complaints/User", f"{avg_complaints:.2f}")
    col3.metric("Average CSAT", f"{avg_csat:.1f}")

    chart1, chart2 = st.columns(2)

    with chart1:
        if {"escalation_flag", "churn_flag"}.issubset(df.columns):
            esc = (
                df.groupby("escalation_flag")["churn_flag"]
                .mean()
                .mul(100)
                .reset_index(name="churn_rate")
            )
            esc["escalation"] = esc["escalation_flag"].map(
                {0: "No Escalation", 1: "Escalated"}
            )
            fig = px.bar(
                esc,
                x="escalation",
                y="churn_rate",
                text_auto=".1f",
                title="Churn Rate: Escalated vs Non-Escalated",
            )
            st.plotly_chart(fig, use_container_width=True)

    with chart2:
        if {"csat_score", "churn_flag"}.issubset(df.columns):
            temp = df.dropna(subset=["csat_score"]).copy()
            temp["status"] = temp["churn_flag"].map({0: "Retained", 1: "Churned"})
            fig = px.box(
                temp,
                x="status",
                y="csat_score",
                title="CSAT Distribution by Churn Status",
            )
            st.plotly_chart(fig, use_container_width=True)


def customer_explorer_page(df: pd.DataFrame) -> None:
    st.markdown("### Customer Explorer")

    search = st.text_input("Search by Customer ID or Name")
    table = df.copy()

    if search:
        mask = pd.Series(False, index=table.index)
        if "customerid" in table.columns:
            mask |= table["customerid"].astype(str).str.contains(
                search, case=False, na=False
            )
        if "customer_name" in table.columns:
            mask |= table["customer_name"].astype(str).str.contains(
                search, case=False, na=False
            )
        table = table[mask]

    preferred = [
        "customerid",
        "customer_name",
        "state",
        "gender",
        "plan_type",
        "contract_type",
        "monthly_charges",
        "cltv",
        "churn_score",
        "churn_risk",
        "churn_flag",
        "complaint_count",
        "csat_score",
        "tenure_days",
    ]
    visible = [c for c in preferred if c in table.columns]
    st.dataframe(table[visible], use_container_width=True, hide_index=True)

    csv = table.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered customer data",
        data=csv,
        file_name="filtered_churn_customers.csv",
        mime="text/csv",
    )


def insights_page(df: pd.DataFrame) -> None:
    st.markdown("### Automated Business Insights")

    insights = []

    if {"plan_type", "churn_flag"}.issubset(df.columns):
        s = df.groupby("plan_type")["churn_flag"].mean().sort_values(ascending=False)
        if not s.empty:
            insights.append(
                f"**{s.index[0]}** has the highest plan-level churn rate at "
                f"**{s.iloc[0] * 100:.1f}%**."
            )

    if {"contract_type", "churn_flag"}.issubset(df.columns):
        s = df.groupby("contract_type")["churn_flag"].mean().sort_values(ascending=False)
        if not s.empty:
            insights.append(
                f"Customers on **{s.index[0]}** contracts show the greatest churn risk "
                f"at **{s.iloc[0] * 100:.1f}%**."
            )

    if {"escalation_flag", "churn_flag"}.issubset(df.columns):
        rates = df.groupby("escalation_flag")["churn_flag"].mean()
        if 1 in rates.index and 0 in rates.index:
            uplift = (rates.loc[1] - rates.loc[0]) * 100
            insights.append(
                f"Escalated customers have a churn rate difference of "
                f"**{uplift:+.1f} percentage points** versus non-escalated customers."
            )

    if {"churn_flag", "monthly_charges"}.issubset(df.columns):
        risk = df.loc[df["churn_flag"] == 1, "monthly_charges"].sum()
        insights.append(
            f"Current monthly revenue exposed to churn is approximately "
            f"**{format_currency(risk)}**."
        )

    if not insights:
        st.info("Not enough columns are available to generate insights.")
    else:
        for item in insights:
            st.markdown(
                f'<div class="insight-card">{item}</div>',
                unsafe_allow_html=True,
            )

    if {"churn_score", "churn_flag", "monthly_charges"}.issubset(df.columns):
        high_risk = df[
            (pd.to_numeric(df["churn_score"], errors="coerce") >= 70)
            & (df["churn_flag"] == 0)
        ].copy()
        high_risk = high_risk.sort_values(
            ["churn_score", "monthly_charges"], ascending=False
        )

        st.markdown("#### Priority Retention List")
        cols = [
            c
            for c in [
                "customerid",
                "customer_name",
                "plan_type",
                "contract_type",
                "monthly_charges",
                "cltv",
                "churn_score",
                "complaint_count",
                "csat_score",
            ]
            if c in high_risk.columns
        ]
        st.dataframe(high_risk[cols].head(25), use_container_width=True, hide_index=True)



def styled_fig(fig, height=290):
    text_color = "#0f172a"
    muted_color = "#334155"
    grid_color = "#d8dee8"

    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=58, r=24, t=62, b=58),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family="Segoe UI, Arial", size=12, color=text_color),
        title=dict(
            font=dict(size=15, color="#0f172a", family="Segoe UI, Arial"),
            x=0.02,
            xanchor="left",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=11, color=text_color),
            bgcolor="rgba(255,255,255,.95)",
        ),
        hoverlabel=dict(
            bgcolor="#0f2742",
            bordercolor="#0f2742",
            font_color="#ffffff",
            font_size=12,
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        showline=True,
        linecolor="#94a3b8",
        tickfont=dict(color=muted_color, size=11),
        title_font=dict(color=text_color, size=12),
        automargin=True,
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=grid_color,
        zeroline=False,
        showline=True,
        linecolor="#94a3b8",
        tickfont=dict(color=muted_color, size=11),
        title_font=dict(color=text_color, size=12),
        automargin=True,
    )

    # Text labels are supported by bar, scatter, pie and similar traces.
    # Box traces do not support the textfont property.
    fig.update_traces(
        selector=dict(type="bar"),
        textfont=dict(color="#0f172a", size=11),
        marker_line_color="#ffffff",
        marker_line_width=0.8,
    )
    fig.update_traces(
        selector=dict(type="scatter"),
        marker_line_color="#ffffff",
        marker_line_width=0.7,
    )
    fig.update_traces(
        selector=dict(type="pie"),
        textfont=dict(color="#0f172a", size=11),
        marker_line_color="#ffffff",
        marker_line_width=1,
    )
    fig.update_traces(
        selector=dict(type="box"),
        line=dict(color="#075985", width=2),
        fillcolor="rgba(56, 189, 248, 0.35)",
        marker=dict(color="#0369a1"),
    )

    return fig



def powerbi_dashboard(df: pd.DataFrame) -> None:
    customers = df["customerid"].nunique() if "customerid" in df.columns else len(df)
    churn_rate = df["churn_flag"].mean() * 100 if "churn_flag" in df.columns else 0
    retained = customers - int(df["churn_flag"].sum()) if "churn_flag" in df.columns else customers
    arpu = df["monthly_charges"].mean() if "monthly_charges" in df.columns else 0
    revenue = df["monthly_charges"].sum() if "monthly_charges" in df.columns else 0
    risk_revenue = (
        df.loc[df["churn_flag"] == 1, "monthly_charges"].sum()
        if {"churn_flag", "monthly_charges"}.issubset(df.columns)
        else 0
    )

    m1, m2, m3, m4 = st.columns(4)
    metric_values = [
        ("Total Customers", f"{customers:,}", f"Retained: {retained:,}"),
        ("Churn Rate", f"{churn_rate:.1f}%", "Selected customer segment"),
        ("Monthly Revenue", format_currency(revenue), f"ARPU: {format_currency(arpu)}"),
        ("Revenue at Risk", format_currency(risk_revenue), "From churned customers"),
    ]
    for container, (title, value, sub) in zip([m1, m2, m3, m4], metric_values):
        container.markdown(
            f'<div class="metric-card"><div class="metric-title">{title}</div>'
            f'<div class="metric-value">{value}</div><div class="metric-sub">{sub}</div></div>',
            unsafe_allow_html=True,
        )

    st.write("")
    r1c1, r1c2 = st.columns([1, 2])

    with r1c1:
        if {"plan_type", "churn_flag"}.issubset(df.columns):
            plan = (
                df.groupby("plan_type")["churn_flag"]
                .mean().mul(100).reset_index(name="churn_rate")
            )
            fig = px.bar(
                plan, x="plan_type", y="churn_rate",
                text_auto=".1f", title="Churn Rate by Plan",
                color="churn_rate", color_continuous_scale=[(0, "#9ecae1"), (1, "#08519c")]
            )
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(styled_fig(fig, 275), use_container_width=True)

    with r1c2:
        if {"cancellation_date", "churn_flag"}.issubset(df.columns):
            churned = df[df["churn_flag"] == 1].dropna(subset=["cancellation_date"]).copy()
            if not churned.empty:
                churned["month"] = churned["cancellation_date"].dt.to_period("M").astype(str)
                trend = churned.groupby("month").size().reset_index(name="customers")
                fig = px.bar(
                    trend, x="month", y="customers", text_auto=True,
                    title="Monthly Churn Movement",
                    color="customers", color_continuous_scale=[(0, "#99d8c9"), (1, "#006d5b")]
                )
                fig.update_coloraxes(showscale=False)
                st.plotly_chart(styled_fig(fig, 275), use_container_width=True)
            else:
                st.info("No cancellation dates found for this selection.")

    r2c1, r2c2, r2c3 = st.columns([1.15, 1.25, 1])

    with r2c1:
        if {"contract_type", "churn_flag"}.issubset(df.columns):
            contract = (
                df.groupby("contract_type")["churn_flag"]
                .mean().mul(100).reset_index(name="churn_rate")
            )
            fig = px.bar(
                contract, x="contract_type", y="churn_rate",
                text_auto=".1f", title="Churn by Contract",
                color="churn_rate", color_continuous_scale=[(0, "#9ecae1"), (1, "#08519c")]
            )
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(styled_fig(fig, 260), use_container_width=True)

    with r2c2:
        if {"state", "churn_flag"}.issubset(df.columns):
            state = (
                df.groupby("state")["churn_flag"]
                .mean().mul(100).sort_values(ascending=False)
                .head(10).reset_index(name="churn_rate")
            )
            fig = px.bar(
                state, x="state", y="churn_rate",
                text_auto=".1f", title="Top States by Churn",
                color="churn_rate", color_continuous_scale=[(0, "#99d8c9"), (1, "#006d5b")]
            )
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(styled_fig(fig, 260), use_container_width=True)

    with r2c3:
        if "churn_flag" in df.columns:
            counts = (
                df["churn_flag"].map({0:"Retained",1:"Churned"})
                .value_counts().rename_axis("status").reset_index(name="customers")
            )
            fig = px.pie(
                counts, names="status", values="customers",
                hole=.58, title="Customer Mix"
            )
            fig.update_layout(showlegend=True)
            st.plotly_chart(styled_fig(fig, 260), use_container_width=True)

    r3c1, r3c2, r3c3 = st.columns([1.3, 1, 1])

    with r3c1:
        if {"monthly_charges", "churn_flag"}.issubset(df.columns):
            temp = df.copy()
            temp["status"] = temp["churn_flag"].map({0:"Retained",1:"Churned"})
            fig = px.box(
                temp, x="status", y="monthly_charges",
                points=False, title="Monthly Charges by Status"
            )
            st.plotly_chart(styled_fig(fig, 245), use_container_width=True)

    with r3c2:
        if {"churn_score", "cltv"}.issubset(df.columns):
            fig = px.scatter(
                df, x="churn_score", y="cltv",
                color="churn_risk" if "churn_risk" in df.columns else None,
                title="CLTV vs Churn Score",
                hover_data=["customerid"] if "customerid" in df.columns else None
            )
            st.plotly_chart(styled_fig(fig, 245), use_container_width=True)

    with r3c3:
        if {"escalation_flag", "churn_flag"}.issubset(df.columns):
            esc = (
                df.groupby("escalation_flag")["churn_flag"]
                .mean().mul(100).reset_index(name="churn_rate")
            )
            esc["escalation"] = esc["escalation_flag"].map({0:"No",1:"Yes"})
            fig = px.bar(
                esc, x="escalation", y="churn_rate",
                text_auto=".1f", title="Escalation Impact",
                color="churn_rate", color_continuous_scale=[(0, "#fcae91"), (1, "#99000d")]
            )
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(styled_fig(fig, 245), use_container_width=True)


st.markdown('<div class="app-shell">', unsafe_allow_html=True)

st.markdown(
    """
    <div class="topbar">
        <div>
            <div class="topbar-title">Customer Churn Analytics Dashboard</div>
            <div class="topbar-subtitle">Interactive business intelligence view for retention, revenue and customer risk</div>
        </div>
        <div class="small-note">Power BI-style layout • Streamlit</div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, main = st.columns([0.18, 0.82], gap="small")

with left:
    st.markdown(
        """
        <div class="brand-box">
            <div class="brand-mark">CC</div>
            <div class="brand-title">Churn Analytics</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section = st.radio(
        "Navigation",
        ["Indicators", "Filter Data", "Monthly Dashboard", "Customer Table"],
        label_visibility="collapsed",
    )

    uploaded_file = st.file_uploader(
        "Upload data",
        type=["csv", "xlsx", "xls"],
        label_visibility="visible",
    )

with main:
    if uploaded_file is None:
        st.markdown('<div class="section-label">Upload a churn dataset to open the dashboard</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.info("CSV, XLSX and XLS supported")
        c2.info("Automatic data cleaning and feature creation")
        c3.info("Interactive KPIs, filters and charts")
        st.stop()

    try:
        data = load_uploaded_file(uploaded_file.name, uploaded_file.getvalue())
    except Exception as exc:
        st.error(f"Unable to load the file: {exc}")
        st.stop()

    if section == "Filter Data":
        st.markdown('<div class="section-label">Filter Data</div>', unsafe_allow_html=True)
        filtered_df = filter_data(data)
        if filtered_df.empty:
            st.warning("No customer records match the selected filters.")
        else:
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    elif section == "Customer Table":
        st.markdown('<div class="section-label">Customer Table</div>', unsafe_allow_html=True)
        filtered_df = filter_data(data)
        customer_explorer_page(filtered_df)

    elif section == "Indicators":
        st.markdown('<div class="section-label">Indicators</div>', unsafe_allow_html=True)
        filtered_df = filter_data(data)
        kpi_cards(filtered_df)
        insights_page(filtered_df)

    else:
        top_filter_1, top_filter_2, top_filter_3 = st.columns([1,1,1])
        month_choice = "All"
        if "cancellation_date" in data.columns:
            valid = data["cancellation_date"].dropna()
            months = sorted(valid.dt.to_period("M").astype(str).unique()) if not valid.empty else []
            month_choice = top_filter_1.selectbox("Select Month", ["All"] + months)
        plan_choice = "All"
        if "plan_type" in data.columns:
            plan_choice = top_filter_2.selectbox(
                "Plan", ["All"] + sorted(data["plan_type"].dropna().astype(str).unique())
            )
        contract_choice = "All"
        if "contract_type" in data.columns:
            contract_choice = top_filter_3.selectbox(
                "Contract", ["All"] + sorted(data["contract_type"].dropna().astype(str).unique())
            )

        filtered_df = data.copy()
        if month_choice != "All" and "cancellation_date" in filtered_df.columns:
            filtered_df = filtered_df[
                filtered_df["cancellation_date"].dt.to_period("M").astype(str) == month_choice
            ]
        if plan_choice != "All":
            filtered_df = filtered_df[filtered_df["plan_type"].astype(str) == plan_choice]
        if contract_choice != "All":
            filtered_df = filtered_df[filtered_df["contract_type"].astype(str) == contract_choice]

        st.markdown('<div class="section-label">Monthly Dashboard</div>', unsafe_allow_html=True)
        if filtered_df.empty:
            st.warning("No records match the selected filters.")
        else:
            powerbi_dashboard(filtered_df)

st.markdown('</div>', unsafe_allow_html=True)
