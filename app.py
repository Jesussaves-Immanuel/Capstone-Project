import streamlit as st
import pandas as pd
import numpy as np
import joblib
import altair as alt
from pathlib import Path
import io

# Page configuration
st.set_page_config(
    page_title="Golden Palms HR Dashboard",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Golden Palms admin dashboard
st.markdown("""
    <style>
    body, .main, .block-container {
        background: linear-gradient(180deg, #051223 0%, #0d172c 45%, #121f3f 100%);
        color: #f8f4e6;
        font-family: 'Inter', sans-serif;
    }

    .css-18ni7ap.e8zbici2 { background: transparent; }

    h1, h2, h3, h4, h5, h6 {
        color: #f8f4e6;
        font-family: 'Inter', sans-serif;
    }

    .subtitle {
        text-align: center;
        color: #d3c4a8;
        font-size: 1rem;
        margin-bottom: 35px;
        line-height: 1.7;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }

    .hero-card, .glass-card, .info-card, .summary-card, .brand-card {
        background: rgba(8, 15, 34, 0.80);
        border: 1px solid rgba(255, 215, 0, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 28px;
        box-shadow: 0 25px 60px rgba(0,0,0,0.35);
    }

    .hero-card {
        padding: 32px 42px;
        margin-bottom: 30px;
    }

    .brand-card {
        padding: 18px 22px;
        margin-bottom: 18px;
    }

    .section-title {
        color: #f8f4e6;
        margin-bottom: 12px;
        font-size: 1.6rem;
        font-weight: 700;
    }

    .section-description {
        color: #bdb897;
        line-height: 1.75;
        margin-bottom: 22px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 52px;
        padding: 0 24px;
        background-color: rgba(255,255,255,0.04);
        border-radius: 16px 16px 0 0;
        color: #d3c4a8;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        color: #fff;
        background-color: rgba(255,215,0,0.18);
        border-bottom: 3px solid #ffc700;
    }

    .stFileUploader, .stTextArea, .stNumberInput, .stSelectbox {
        border-radius: 20px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,215,0,0.14);
    }

    .stButton > button {
        background: linear-gradient(135deg, #d4af37 0%, #ffd966 100%);
        color: #081223;
        font-weight: 700;
        border-radius: 18px;
        height: 52px;
        box-shadow: 0 12px 35px rgba(255,215,0,0.22);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 15px 45px rgba(255,215,0,0.30);
    }

    .css-1n76uvr.e1fqkh3o1 {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,215,0,0.16) !important;
        border-radius: 22px !important;
    }

    .stMetric > div {
        background: rgba(255,255,255,0.05);
        border-radius: 22px;
        padding: 22px 24px;
        min-height: 140px;
        color: #f8f4e6;
    }

    .stMetric > div > div {
        color: #f8f4e6;
    }

    .stMarkdown {
        color: #e4decd;
    }

    .reportview-container .markdown-text-container p {
        color: #d3c4a8;
    }

    .profile-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,215,0,0.14);
        border-radius: 24px;
        padding: 18px;
        margin-bottom: 16px;
        transition: transform 0.15s ease;
    }

    .profile-card:hover {
        transform: translateY(-3px);
    }

    .profile-image {
        width: 100%;
        height: 170px;
        object-fit: cover;
        border-radius: 16px;
        margin-bottom: 14px;
        border: 2px solid rgba(255,255,255,0.22);
        box-shadow: 0 10px 24px rgba(0,0,0,0.18);
    }

    .profile-name {
        color: #fff;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .profile-details {
        color: #d3c4a8;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .summary-badge {
        background: rgba(255,215,0,0.15);
        color: #fff;
        padding: 6px 12px;
        border-radius: 999px;
        display: inline-block;
        font-size: 0.85rem;
        margin-bottom: 10px;
    }

    .summary-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,215,0,0.14);
        border-radius: 24px;
        padding: 22px;
        min-height: 170px;
    }

    .summary-card h4 {
        color: #ffd966;
        margin-bottom: 14px;
    }

    .summary-card .metric-number {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .summary-card .metric-label {
        color: #d3c4a8;
        font-size: 0.95rem;
    }

    .dashboard-grid {
        display: flex;
        gap: 24px;
        flex-wrap: wrap;
        margin-bottom: 22px;
    }

    .kpi-card {
        background: #152243;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 24px;
        overflow: hidden;
        min-height: 240px;
    }

    .kpi-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 18px 20px;
        color: #ffffff;
        font-weight: 700;
        letter-spacing: 0.02em;
    }

    .kpi-teal {
        background: linear-gradient(135deg, #127a8f 0%, #28c7b8 100%);
    }

    .kpi-mint {
        background: linear-gradient(135deg, #24c78a 0%, #8ef0c8 100%);
    }

    .kpi-amber {
        background: linear-gradient(135deg, #f3b872 0%, #ffd347 100%);
    }

    .kpi-coral {
        background: linear-gradient(135deg, #f16d50 0%, #ff9b72 100%);
    }

    .kpi-body {
        padding: 20px;
    }

    .kpi-main {
        color: #ffffff;
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .kpi-subtitle {
        color: #cdd2e0;
        margin-bottom: 16px;
        font-size: 0.95rem;
    }

    .kpi-split {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 14px;
    }

    .kpi-split div {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 14px 12px;
        text-align: center;
    }

    .kpi-label {
        color: #b9c6d9;
        font-size: 0.82rem;
        margin-bottom: 6px;
    }

    .kpi-value {
        color: #ffffff;
        font-size: 1.4rem;
        font-weight: 700;
    }

    .chart-row {
        display: flex;
        gap: 24px;
        flex-wrap: wrap;
        margin-bottom: 28px;
    }

    .chart-card {
        background: #16264a;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 26px;
        padding: 20px;
    }

    .prediction-card,
    .result-card,
    .input-card,
    .guide-card {
        background: rgba(8, 15, 34, 0.92);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.20);
        margin-bottom: 16px;
    }

    .prediction-card h4,
    .guide-card h4,
    .result-card h4,
    .input-card h4 {
        color: #f8f4e6;
        margin-bottom: 12px;
        font-size: 1.15rem;
        letter-spacing: 0.01em;
    }

    .prediction-card p,
    .guide-card p,
    .result-card p,
    .input-card p {
        color: #cfd6e7;
        line-height: 1.7;
    }

    .prediction-badge {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(255,255,255,0.08);
        color: #f8f4e6;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .result-score {
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .result-summary {
        color: #d3c4a8;
        margin-bottom: 14px;
    }

    .result-bar {
        background: linear-gradient(90deg, #28c7b8, #8ef0c8);
        border-radius: 14px;
        height: 12px;
        margin-top: 14px;
    }

    .guide-list {
        list-style-type: none;
        padding-left: 0;
        color: #d3c4a8;
    }

    .guide-list li {
        margin-bottom: 10px;
    }

    .guide-list li::before {
        content: '•';
        color: #ffd966;
        display: inline-block;
        width: 1em;
    }

    .chart-title {
        color: #f8f4e6;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 14px;
    }

    .sidebar .sidebar-content {
        background: rgba(5, 18, 35, 0.95);
    }

    .sidebar .stSidebar {
        border-right: 1px solid rgba(255,215,0,0.12);
    }
    </style>
    """, unsafe_allow_html=True)

# Helper functions

def load_dataset(uploaded_file):
    if uploaded_file is None:
        return None
    try:
        if uploaded_file.name.lower().endswith('.csv'):
            return pd.read_csv(uploaded_file)
        return pd.read_excel(uploaded_file)
    except Exception:
        return None


def preprocess_for_prediction(df):
    """Preprocess data exactly as done in the notebook"""
    df_processed = df.copy()
    
    # Encode OverTime to binary
    if df_processed['OverTime'].dtype == 'object':
        df_processed['OverTime'] = df_processed['OverTime'].map({'Yes': 1, 'No': 0})
    
    # Scale numerical features (same as notebook)
    numerical_features = ['MonthlyIncome', 'YearsAtCompany', 'DistanceFromHome']
    df_processed[numerical_features] = scaler.transform(df_processed[numerical_features])
    
    # Return in correct feature order
    required_features = ['MonthlyIncome', 'JobSatisfaction', 'YearsAtCompany', 
                        'OverTime', 'WorkLifeBalance', 'DistanceFromHome']
    return df_processed[required_features]


def make_horizontal_bar_chart(df, field, title, color='#8A2BE2'):
    counts = df[field].value_counts().reset_index()
    counts.columns = [field, 'count']
    chart = alt.Chart(counts).mark_bar(cornerRadiusTopLeft=8, cornerRadiusBottomLeft=8).encode(
        x=alt.X('count:Q', title='Count'),
        y=alt.Y(f'{field}:N', sort='-x', title=''),
        color=alt.value(color),
        tooltip=[field, 'count']
    ).properties(height=220)
    return chart


def make_performance_chart(score, baseline=55):
    data = pd.DataFrame({
        'Category': ['Model', 'Baseline'],
        'Accuracy': [score, baseline]
    })
    chart = alt.Chart(data).mark_bar(cornerRadiusTopLeft=8, cornerRadiusBottomLeft=8).encode(
        x=alt.X('Accuracy:Q', title='Accuracy (%)'),
        y=alt.Y('Category:N', sort='-x', title=''),
        color=alt.Color('Category:N', scale=alt.Scale(range=['#8A2BE2', '#7b7f99'])),
        tooltip=['Category', 'Accuracy']
    ).properties(height=180)
    return chart


def make_org_stacked_bar_chart(df):
    df_plot = df.copy()
    if 'Gender' in df_plot.columns:
        df_plot['Gender'] = df_plot['Gender'].astype(str).replace({'F': 'Female', 'M': 'Male', 'f': 'Female', 'm': 'Male'})
    else:
        df_plot['Gender'] = 'Unknown'

    if 'Department' in df_plot.columns:
        org_field = 'Department'
    elif 'JobRole' in df_plot.columns:
        org_field = 'JobRole'
    elif 'BusinessTravel' in df_plot.columns:
        org_field = 'BusinessTravel'
    else:
        org_field = 'Organization'
        df_plot[org_field] = 'All'

    counts = df_plot.groupby([org_field, 'Gender']).size().reset_index(name='Count')
    totals = counts.groupby(org_field, as_index=False)['Count'].sum().rename(columns={'Count': 'Total'})

    bar = alt.Chart(counts).mark_bar(cornerRadiusTopLeft=8, cornerRadiusBottomLeft=8).encode(
        y=alt.Y(f'{org_field}:N', sort=alt.SortField('Total', order='descending'), title='Organization'),
        x=alt.X('Count:Q', title='Employees'),
        color=alt.Color('Gender:N', scale=alt.Scale(domain=['Male', 'Female', 'Unknown'], range=['#2ab7c8', '#9be8d3', '#7b7f99'])),
        tooltip=[org_field, 'Gender', 'Count']
    ).properties(height=320)

    labels = alt.Chart(totals).mark_text(dx=5, dy=4, color='#ffffff', align='left').encode(
        y=alt.Y(f'{org_field}:N', sort=alt.SortField('Total', order='descending')),
        x=alt.X('Total:Q'),
        text=alt.Text('Total:Q')
    )

    chart = alt.layer(bar, labels).configure_view(
        stroke='#2f3b5a',
        strokeWidth=1,
        fill='#121f3f'
    ).configure_axis(
        labelColor='#f8f4e6',
        titleColor='#f8f4e6'
    ).configure_legend(
        labelColor='#f8f4e6',
        titleColor='#f8f4e6'
    )
    return chart


def make_termination_donut_chart(df):
    df_plot = df.copy()
    if 'Attrition' in df_plot.columns:
        df_plot = df_plot[df_plot['Attrition'].map({'Yes': 1, 'No': 0}).fillna(0) == 1]

    if 'Department' in df_plot.columns:
        org_field = 'Department'
    elif 'Branch' in df_plot.columns:
        org_field = 'Branch'
    elif 'BusinessTravel' in df_plot.columns:
        org_field = 'BusinessTravel'
    else:
        org_field = 'Organization'
        df_plot[org_field] = 'All'

    data = df_plot.groupby(org_field).size().reset_index(name='Terminations')
    if data.empty and 'Department' in df.columns:
        data = df.groupby('Department').size().reset_index(name='Terminations')
    data['Label'] = data[org_field] + ': ' + data['Terminations'].astype(str)

    chart = alt.Chart(data).mark_arc(innerRadius=70, outerRadius=110).encode(
        theta=alt.Theta('Terminations:Q', stack=True),
        color=alt.Color(f'{org_field}:N', scale=alt.Scale(range=['#2ab7c8', '#9be8d3', '#f2c94c', '#f07c5a', '#8b9de2'])),
        tooltip=[org_field, 'Terminations']
    ).properties(width=360, height=320)

    labels = alt.Chart(data).mark_text(radius=145, size=12, color='#ffffff').encode(
        theta=alt.Theta('Terminations:Q', stack=True),
        text=alt.Text('Label:N')
    )
    return alt.layer(chart, labels).configure_view(
        stroke='#2f3b5a',
        strokeWidth=1,
        fill='#121f3f'
    ).configure_legend(
        labelColor='#f8f4e6',
        titleColor='#f8f4e6'
    )


def get_feature_importance_cards(model, feature_names):
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    return importance_df


def feature_drilldown_chart(df, feature):
    df_plot = df.copy()
    if feature == 'OverTime':
        if df_plot[feature].dtype != 'object':
            df_plot[feature] = df_plot[feature].map({1: 'Yes', 0: 'No'})
        chart = alt.Chart(df_plot).mark_bar().encode(
            x=alt.X(f'{feature}:N', title=feature),
            y=alt.Y('count():Q', title='Count'),
            color=alt.Color('Attrition:N', scale=alt.Scale(range=['#8A2BE2', '#E63946'])),
            tooltip=[feature, 'count()', 'Attrition']
        ).properties(height=240)
        return chart

    if df_plot[feature].dtype == 'object':
        chart = alt.Chart(df_plot).mark_bar().encode(
            x=alt.X(f'{feature}:N', title=feature),
            y=alt.Y('count():Q', title='Count'),
            color=alt.Color('Attrition:N', scale=alt.Scale(range=['#8A2BE2', '#E63946'])),
            tooltip=[feature, 'count()', 'Attrition']
        ).properties(height=240)
        return chart

    chart = alt.Chart(df_plot).mark_bar().encode(
        x=alt.X(f'{feature}:Q', bin=alt.Bin(maxbins=20), title=feature),
        y=alt.Y('count():Q', title='Count'),
        color=alt.Color('Attrition:N', scale=alt.Scale(range=['#8A2BE2', '#E63946'])),
        tooltip=[alt.Tooltip(f'{feature}:Q'), 'count()', 'Attrition']
    ).properties(height=240)
    return chart


def compute_action_buckets(df):
    high_priority = df[df['RiskScore'] > 80]
    watchlist = df[(df['RiskScore'] >= 50) & (df['RiskScore'] <= 80)]
    stable = df[df['RiskScore'] < 50]
    return high_priority, watchlist, stable

# Try to load model and scaler from models directory
import os
from pathlib import Path

try:
    # Get the directory where this script is located
    BASE_DIR = Path(__file__).parent
    MODEL_PATH = BASE_DIR / "models" / "attrition_model.joblib"
    SCALER_PATH = BASE_DIR / "models" / "scaler.joblib"
    
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    model_loaded = True
except FileNotFoundError:
    model_loaded = False
except Exception as e:
    model_loaded = False

# Main Title
st.markdown(
    "<div class='hero-card'><div style='display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;'>"
    "<div><h1>Golden Palms Industries Ltd</h1>"
    "<p class='subtitle'>HR Attrition Intelligence Dashboard built by AkwaabaTech Solutions — ready for admin decision-making and people analytics.</p></div>"
    "<div style='text-align:right; min-width:220px; margin-top:12px;'>"
    "<div style='font-size:0.95rem; color:#d3c4a8; letter-spacing:0.1em;'>AKWAABATECH SOLUTIONS</div>"
    "<div style='font-size:1.15rem; color:#ffd966; font-weight:700; margin-top:6px;'>GOLDEN PALMS HR</div>"
    "<div style='margin-top:8px; color:#c7b377;'>Admin Executive Dashboard</div>"
    "</div></div></div>",
    unsafe_allow_html=True
)

if not model_loaded:
    st.error("⚠️ Model files not found. Please ensure 'attrition_model.joblib' and 'scaler.joblib' are in the 'models/' directory.")
    st.stop()

# Sidebar navigation
st.sidebar.markdown("<div class='brand-card'><h3 style='margin:0; color:#ffd966;'>Golden Palms Admin</h3><p style='margin:4px 0 0; color:#d3c4a8;'>AkwaabaTech workforce solution</p></div>", unsafe_allow_html=True)
st.sidebar.markdown("## 🎯 Navigation")
nav_selection = st.sidebar.radio(
    "Choose a view",
    ["Data Explorer", "Batch Prediction", "Individual Prediction", "Info"],
    index=1
)

if "uploaded_df" not in st.session_state:
    st.session_state.uploaded_df = None

st.sidebar.markdown("---")
st.sidebar.markdown("## 📄 Upload Dataset")
uploaded_file = st.sidebar.file_uploader(
    "Upload employee attrition data",
    type=["csv", "xlsx"],
    help="Use the same file for Data Explorer and Batch Prediction."
)

if uploaded_file is not None:
    df_uploaded = load_dataset(uploaded_file)
    if df_uploaded is not None:
        st.session_state.uploaded_df = df_uploaded
    else:
        st.sidebar.error("Unable to read the uploaded file. Please check the format.")

st.sidebar.markdown("---")
st.sidebar.markdown("**High-level navigation for the employee attrition intelligence dashboard.**")

required_features = ['MonthlyIncome', 'JobSatisfaction', 'YearsAtCompany', 'OverTime', 'WorkLifeBalance', 'DistanceFromHome']

if nav_selection == "Data Explorer":
    st.markdown("### 🧠 Data Explorer")
    st.markdown("Explore data distributions and understand attrition drivers in your dataset.")

    df_explore = st.session_state.uploaded_df
    if df_explore is None:
        st.warning("Upload a dataset in the sidebar to populate the Data Explorer.")
    else:
        total_employees = len(df_explore)
        gender_counts = {'Female': 0, 'Male': 0}
        if 'Gender' in df_explore.columns:
            gender_series = df_explore['Gender'].astype(str).replace({'F': 'Female', 'M': 'Male', 'f': 'Female', 'm': 'Male'})
            gender_counts['Female'] = int((gender_series == 'Female').sum())
            gender_counts['Male'] = int((gender_series == 'Male').sum())

        department_counts = {}
        if 'Department' in df_explore.columns:
            department_counts = df_explore['Department'].value_counts().to_dict()
        elif 'JobRole' in df_explore.columns:
            department_counts = df_explore['JobRole'].value_counts().to_dict()

        education_counts = {}
        if 'EducationField' in df_explore.columns:
            education_counts = df_explore['EducationField'].value_counts().to_dict()

        branch_field = None
        for candidate in ['Branch', 'Company', 'BusinessTravel', 'BusinessUnit']:
            if candidate in df_explore.columns:
                branch_field = candidate
                break

        branch_counts = df_explore[branch_field].value_counts().to_dict() if branch_field else {}

        def top_two(counts):
            items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            if len(items) < 2:
                items += [('N/A', 0)] * (2 - len(items))
            return items[:2]

        top_depts = top_two(department_counts)
        top_eds = top_two(education_counts)
        top_branches = top_two(branch_counts)

        kpi_cols = st.columns(4, gap='large')

        kpis = [
            {
                'title': 'Demographics',
                'header_class': 'kpi-teal',
                'icon': '👥',
                'main': f"{total_employees}",
                'subtitle': 'Head Count',
                'split': [('Female', gender_counts['Female']), ('Male', gender_counts['Male'])]
            },
            {
                'title': 'Departments',
                'header_class': 'kpi-mint',
                'icon': '🏢',
                'main': f"{len(department_counts)}" if department_counts else 'N/A',
                'subtitle': 'Department Count',
                'split': [(top_depts[0][0], top_depts[0][1]), (top_depts[1][0], top_depts[1][1])]
            },
            {
                'title': 'Education',
                'header_class': 'kpi-amber',
                'icon': '🎓',
                'main': f"{len(education_counts)}" if education_counts else 'N/A',
                'subtitle': 'Education Fields',
                'split': [(top_eds[0][0], top_eds[0][1]), (top_eds[1][0], top_eds[1][1])]
            },
            {
                'title': 'Branches',
                'header_class': 'kpi-coral',
                'icon': '🌐',
                'main': f"{len(branch_counts)}" if branch_counts else 'N/A',
                'subtitle': branch_field if branch_field else 'Company Branches',
                'split': [(top_branches[0][0], top_branches[0][1]), (top_branches[1][0], top_branches[1][1])]
            }
        ]

        for col, kpi in zip(kpi_cols, kpis):
            with col:
                st.markdown(
                    f"<div class='kpi-card'>"
                    f"<div class='kpi-header {kpi['header_class']}'><span>{kpi['icon']} {kpi['title']}</span></div>"
                    f"<div class='kpi-body'>"
                    f"<div class='kpi-main'>{kpi['main']}</div>"
                    f"<div class='kpi-subtitle'>{kpi['subtitle']}</div>"
                    f"<div class='kpi-split'>"
                    f"<div><div class='kpi-label'>{kpi['split'][0][0]}</div><div class='kpi-value'>{kpi['split'][0][1]}</div></div>"
                    f"<div><div class='kpi-label'>{kpi['split'][1][0]}</div><div class='kpi-value'>{kpi['split'][1][1]}</div></div>"
                    f"</div></div></div>",
                    unsafe_allow_html=True
                )

        st.markdown("---")
        st.markdown("### Department Insights")
        left_chart_col, right_chart_col = st.columns([2, 1], gap='large')
        with left_chart_col:
            st.markdown("<div class='chart-card'><div class='chart-title'>Employee by Department</div>", unsafe_allow_html=True)
            st.altair_chart(make_org_stacked_bar_chart(df_explore), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with right_chart_col:
            st.markdown("<div class='chart-card'><div class='chart-title'>Department Graph Overview</div>", unsafe_allow_html=True)
            st.altair_chart(make_termination_donut_chart(df_explore), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        avg_income = df_explore['MonthlyIncome'].mean() if 'MonthlyIncome' in df_explore.columns else None
        overtime_pct = df_explore['OverTime'].map({'Yes': 1, 'No': 0}).mean() * 100 if 'OverTime' in df_explore.columns else None

        categories = ['JobRole', 'BusinessTravel']
        card_cols = st.columns(2, gap='large')
        for col, category in zip(card_cols, categories):
            with col:
                if category in df_explore.columns:
                    st.markdown(f"#### {category}")
                    st.altair_chart(make_horizontal_bar_chart(df_explore, category, category, color='#8A2BE2'), use_container_width=True)
                else:
                    st.markdown(f"#### {category}")
                    st.info(f"Upload data with the `{category}` column to view this chart.")

        st.markdown("#### Employee Records")
        st.markdown("**Representative employee profiles for admin review. Includes Ghanaian and international talent.**")
        employee_profiles = [
            {
                'name': 'Kwame Mensah',
                'title': 'Sales Executive',
                    'department': 'Sales',
                    'income': '$5,200',
                    'tenure': '4 years',
                    'overtime': 'Yes',
                    'balance': '3/4',
                    'image': 'https://randomuser.me/api/portraits/men/34.jpg'
                },
                {
                    'name': 'Akosua Boateng',
                    'title': 'HR Specialist',
                    'department': 'Human Resources',
                    'income': '$4,750',
                    'tenure': '2 years',
                    'overtime': 'No',
                    'balance': '4/4',
                    'image': 'https://randomuser.me/api/portraits/women/44.jpg'
                },
                {
                    'name': 'Liam Johnson',
                    'title': 'Operations Manager',
                    'department': 'Operations',
                    'income': '$6,500',
                    'tenure': '6 years',
                    'overtime': 'Yes',
                    'balance': '2/4',
                    'image': 'https://randomuser.me/api/portraits/men/76.jpg'
                },
                {
                    'name': 'Emma Smith',
                    'title': 'Customer Success Lead',
                    'department': 'Service',
                    'income': '$5,900',
                    'tenure': '3 years',
                    'overtime': 'No',
                    'balance': '4/4',
                    'image': 'https://randomuser.me/api/portraits/women/68.jpg'
                },
                {
                    'name': 'Pierre Laurent',
                    'title': 'Finance Analyst',
                    'department': 'Finance',
                    'income': '$5,100',
                    'tenure': '5 years',
                    'overtime': 'Yes',
                    'balance': '3/4',
                    'image': 'https://randomuser.me/api/portraits/men/22.jpg'
                },
                {
                    'name': 'Sofia Martinez',
                    'title': 'Talent Partner',
                    'department': 'People Ops',
                    'income': '$5,300',
                    'tenure': '4 years',
                    'overtime': 'No',
                    'balance': '4/4',
                    'image': 'https://randomuser.me/api/portraits/women/15.jpg'
                },
            ]

        for i in range(0, len(employee_profiles), 3):
            row = employee_profiles[i:i+3]
            cols = st.columns(len(row), gap='large')
            for col, profile in zip(cols, row):
                with col:
                    st.markdown(
                        f"<div class='profile-card'>"
                        f"<img class='profile-image' src='{profile['image']}' alt='profile image'/>"
                        f"<div class='profile-name'>{profile['name']}</div>"
                        f"<div class='profile-details'>"
                        f"<strong>{profile['title']}</strong><br>"
                        f"Department: {profile['department']}<br>"
                        f"Income: {profile['income']}<br>"
                        f"Tenure: {profile['tenure']}<br>"
                        f"Overtime: {profile['overtime']}<br>"
                        f"Work-Life Balance: {profile['balance']}"
                        f"</div></div>",
                        unsafe_allow_html=True
                    )

        st.markdown("#### Dataset Preview")
        st.dataframe(df_explore.head(10), use_container_width=True)

elif nav_selection == "Batch Prediction":
    st.markdown("### 📦 Golden Palms Attrition Intelligence")
    st.markdown("**Admin view**: Upload your employee dataset, score the workforce, and turn AI insights into retention actions for leadership.")
    st.markdown("Designed for HR admins: clear reporting, ready-to-use actions, and executive-ready analytics.")

    df_input = st.session_state.uploaded_df
    if df_input is None:
        st.warning("Upload a dataset in the sidebar to begin batch prediction.")
    else:
        missing_features = [f for f in required_features if f not in df_input.columns]
        if missing_features:
            st.error(f"Missing required features: {', '.join(missing_features)}")
            st.info(f"Required columns: {', '.join(required_features)}")
        else:
            with st.expander("📋 Dataset Overview"):
                st.dataframe(df_input.head(10), use_container_width=True)

            df_predict = df_input[required_features].copy()
            df_predict = preprocess_for_prediction(df_predict)
            try:
                # df_predict is already preprocessed and scaled
                probabilities = model.predict_proba(df_predict)[:, 1]
                predictions = (probabilities >= 0.5).astype(int)

                df_results = df_input.copy()
                df_results['RiskScore'] = np.round(probabilities * 100, 1)
                df_results['Attrition_Risk'] = predictions
                df_results['Prediction'] = df_results['Attrition_Risk'].map({
                    1: '🚨 High Risk (Likely to Leave)',
                    0: '✅ Low Risk (Likely to Stay)'
                })

                high_risk = int((predictions == 1).sum())
                low_risk = int((predictions == 0).sum())
                risk_percentage = (high_risk / len(predictions)) * 100

                # Global Business Impact Header
                st.markdown("---")
                st.markdown("## 💼 Workforce Risk Summary")
                st.markdown("**Quick HR guide**: Identify risk levels, understand what drives attrition, and prioritize actions for your teams.")

                # Key Metrics with Global Context
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("👥 Total Workforce", len(predictions))
                col2.metric("🚨 At-Risk Employees", high_risk, f"{risk_percentage:.1f}%")
                col3.metric("✅ Stable Employees", low_risk)
                col4.metric("📊 Attrition Rate", f"{risk_percentage:.1f}%")
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("**How to read this page:**")
                st.markdown("- **Risk Score** shows the probability of attrition for each employee.")
                st.markdown("- **At-Risk Employees** are those most likely to leave soon.")
                st.markdown("- **Stable Employees** are likely to stay.")
                st.markdown("- **Feature drivers** explain the model's top factors.")
                st.markdown("- **Action buckets** tell you where to focus retention efforts.")
                st.markdown("- **Note**: The attrition rate here is model-predicted, while Data Explorer shows actual historical attrition.")

                with st.expander("🧭 Beginner HR Walkthrough"):
                    st.markdown("1. Upload your workforce file using the sidebar.")
                    st.markdown("2. Review the Risk Summary to identify whether you have an urgent retention issue.")
                    st.markdown("3. Use the Feature Drivers section to see which factors matter most.")
                    st.markdown("4. Open each drilldown to compare attrition vs retention for that feature.")
                    st.markdown("5. Use Workforce Segmentation to decide who needs immediate action, monitoring, or development support.")

                # Global Business Benefits
                st.markdown("### 🌍 Business Benefits")

                benefit_cols = st.columns(3)
                with benefit_cols[0]:
                    st.markdown("#### 💰 Cost Savings")
                    avg_salary = df_input['MonthlyIncome'].mean() if 'MonthlyIncome' in df_input.columns else 5000
                    annual_turnover_cost = (avg_salary * 12) * (high_risk / len(predictions))
                    st.metric("Estimated Turnover Cost", f"{annual_turnover_cost:,.0f}", help="Based on average monthly salary × 12 months × attrition risk share.")
                    st.info("**Impact**: Understand the financial value of retention.")

                with benefit_cols[1]:
                    st.markdown("#### 📈 Productivity Gains")
                    productivity_gain = (high_risk * 0.25)  # Assuming 25% productivity per retained employee
                    st.metric("Productivity Boost", f"{productivity_gain:.0f} FTE", help="Full-Time Equivalent productivity gained through retention")
                    st.info("**Impact**: Maintain operational efficiency and team knowledge.")

                with benefit_cols[2]:
                    st.markdown("#### 🛡️ Risk Mitigation")
                    risk_reduction = 100 - risk_percentage
                    st.metric("Retention Confidence", f"{risk_reduction:.1f}%", help="Percentage of workforce likely to remain stable")
                    st.info("**Strategic Impact**: Reduce business continuity risks worldwide.")

                # Model Performance & Global Business Context
                st.markdown("### 📊 AI Model Performance")
                perf_col1, perf_col2 = st.columns([2, 1])
                with perf_col1:
                    accuracy = 90.8
                    st.markdown("<div class='glass-card' style='padding: 24px;'>", unsafe_allow_html=True)
                    st.markdown("#### Workforce Analytics")
                    st.markdown(f"**Model Accuracy:** {accuracy:.1f}% - How often the model predicts correctly")
                    st.markdown("**Trained on:** IBM HR Dataset (adapted for workforce patterns) - Large dataset of employee data")
                    st.markdown("**Optimized for:** Recall (68% - catches at-risk employees) - Prioritizes finding employees who might leave")
                    st.markdown("**AUC Score:** 72.2% - Measures model's ability to distinguish between stayers and leavers")
                    st.altair_chart(make_performance_chart(accuracy), use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                with perf_col2:
                    st.markdown("<div class='glass-card' style='padding: 24px;'>", unsafe_allow_html=True)
                    st.markdown("#### Global Business Context")
                    st.markdown("**Why this matters:**")
                    st.markdown("- Talent retention affects productivity and cost.")
                    st.markdown("- High attrition hurts continuity.")
                    st.markdown("- Data-driven HR supports better decisions.")
                    st.markdown("- Retention matters across industries.")
                    st.markdown("</div>", unsafe_allow_html=True)

                # Feature Importance with Global Context
                importance_df = get_feature_importance_cards(model, required_features)
                st.markdown("### 🎯 Key Attrition Drivers")
                st.markdown("**Feature explanations**: Higher importance means the model sees this factor as more predictive of attrition. Use drilldowns to compare attrition vs retention groups.")
                st.markdown("**How to read drilldowns:** More red bars mean a feature value has higher attrition counts. More blue bars mean retention is stronger for that group.")

                driver_cols = st.columns(2)
                for i, (_, row) in enumerate(importance_df.iterrows()):
                    col = driver_cols[i % 2]
                    with col:
                        st.markdown(f"#### {row.Feature}")
                        st.progress(row.Importance)
                        st.markdown(f"**Impact:** {row.Importance:.1%}")

                        # Add global insights
                        if row.Feature == 'MonthlyIncome':
                            st.info("💡 **Pro tip**: Competitive compensation is a strong retention factor.")
                        elif row.Feature == 'OverTime':
                            st.info("💡 **Pro tip**: Excess overtime often leads to burnout and attrition.")
                        elif row.Feature == 'YearsAtCompany':
                            st.info("💡 **Pro tip**: Retaining experienced staff preserves institutional knowledge.")
                        elif row.Feature == 'JobSatisfaction':
                            st.info("💡 **Pro tip**: Higher satisfaction generally reduces attrition risk.")
                        elif row.Feature == 'WorkLifeBalance':
                            st.info("💡 **Pro tip**: Better balance supports employee well-being and retention.")
                        elif row.Feature == 'DistanceFromHome':
                            st.info("💡 **Pro tip**: Long commutes can increase the chance of leaving.")

                # Add comprehensive analytics section
                st.markdown("#### 📊 In-Depth Attrition Analytics")
                st.markdown("**Business insights**: Understand how each factor contributes to your company's attrition patterns. These charts help identify specific areas for intervention.")

                # Risk Score Distribution in accordion
                with st.expander("📈 Risk Score Distribution"):
                    st.markdown("**How your workforce's attrition risk is distributed across employees**")
                    risk_chart = alt.Chart(df_results).mark_bar().encode(
                        x=alt.X('RiskScore:Q', bin=alt.Bin(maxbins=20), title='Risk Score (%)'),
                        y=alt.Y('count():Q', title='Number of Employees'),
                        color=alt.value('#8A2BE2')
                    ).properties(height=200)
                    st.altair_chart(risk_chart, use_container_width=True)
                    st.markdown("*Peaks at higher scores indicate more employees at risk. Use this to understand your overall risk profile.*")

                # Feature-specific analytics in accordions
                if 'Attrition' in df_input.columns:
                    for feature in required_features:
                        with st.expander(f"🔍 {feature} Patterns"):
                            st.markdown(f"**Explore how {feature} behaves for employees who stay vs leave.**")
                            feature_chart = feature_drilldown_chart(df_input[[feature, 'Attrition']].copy(), feature)
                            st.altair_chart(feature_chart, use_container_width=True)

                            if feature in ['MonthlyIncome', 'YearsAtCompany', 'DistanceFromHome']:
                                corr = df_results[feature].corr(df_results['RiskScore'])
                                st.markdown(f"**Correlation with Risk Score:** {corr:.3f}")
                                if abs(corr) > 0.3:
                                    direction = "higher risk" if corr > 0 else "lower risk"
                                    st.info(f"📈 Strong relationship: {feature} correlates with {direction}.")
                            else:
                                avg_risk = df_results.groupby(feature)['RiskScore'].mean().reset_index()
                                st.markdown("**Average Risk by Category:**")
                                st.dataframe(avg_risk.style.highlight_max(axis=0), use_container_width=True)
                else:
                    st.info("Upload data with 'Attrition' column for detailed feature analysis.")

                # Strategic Recommendations
                st.markdown("### 🎯 Strategic Recommendations")
                st.markdown("**Actionable insights for your workforce retention strategy**")

                rec_cols = st.columns(2)
                with rec_cols[0]:
                    st.markdown("#### Immediate Actions (Next 30 Days)")
                    st.markdown("1. **Identify High-Risk Employees** - Focus retention efforts")
                    st.markdown("2. **Compensation Review** - Address salary competitiveness")
                    st.markdown("3. **Work-Life Balance Audit** - Reduce overtime where possible")
                    st.markdown("4. **Stay Interviews** - Understand employee concerns")

                with rec_cols[1]:
                    st.markdown("#### Long-term Strategy (3-6 Months)")
                    st.markdown("1. **Talent Development** - Invest in career growth")
                    st.markdown("2. **Performance Management** - Regular feedback systems")
                    st.markdown("3. **Workplace Culture** - Build engagement and satisfaction")
                    st.markdown("4. **Succession Planning** - Prepare for key role transitions")

                # Export Results
                st.markdown("### 💾 Export Workforce Intelligence")
                csv = df_results.to_csv(index=False)
                st.download_button(
                    label="📊 Download Complete Analysis",
                    data=csv,
                    file_name="workforce_attrition_analysis.csv",
                    mime="text/csv",
                    help="Export full workforce analysis with risk scores and recommendations"
                )

                with st.expander("🔍 Detailed Results Preview"):
                    display_df = df_results[required_features + ['RiskScore', 'Prediction']].copy()
                    st.dataframe(display_df, use_container_width=True)

                high_priority, watchlist, stable = compute_action_buckets(df_results)
                st.markdown("### 👥 Workforce Segmentation")
                st.markdown("**Risk-based retention buckets for easy HR action planning**")
                strat_col1, strat_col2, strat_col3 = st.columns(3)

                strat_col1.markdown("<div style='border: 2px solid #E63946; border-radius: 18px; padding: 20px;'> <h4 style='color:#ffffff;'>High Priority</h4> <p style='color:#f5c6cb;'>Risk > 80%</p> <p style='color:#f5c6cb;'>Immediate Stay Interview</p> <p style='color:#f5c6cb;'>Employees: {}</p> </div>".format(len(high_priority)), unsafe_allow_html=True)
                strat_col2.markdown("<div style='border: 2px solid #ffbf00; border-radius: 18px; padding: 20px;'> <h4 style='color:#ffffff;'>Watchlist</h4> <p style='color:#f9f7d9;'>Risk 50-80%</p> <p style='color:#f9f7d9;'>Work-Life Balance Review</p> <p style='color:#f9f7d9;'>Employees: {}</p> </div>".format(len(watchlist)), unsafe_allow_html=True)
                strat_col3.markdown("<div style='border: 2px solid #2ecc71; border-radius: 18px; padding: 20px;'> <h4 style='color:#ffffff;'>Stable</h4> <p style='color:#d4f5e7;'>Risk < 50%</p> <p style='color:#d4f5e7;'>Recognition / Growth Path</p> <p style='color:#d4f5e7;'>Employees: {}</p> </div>".format(len(stable)), unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.info("**Troubleshooting**: Ensure your dataset contains the required columns and model files are properly trained.")

elif nav_selection == "Individual Prediction":
    st.markdown("### 👤 Individual Prediction")
    st.markdown("Refresh the page with a clean employee risk scoring experience and expert retention guidance.")

    left_panel, right_panel = st.columns([1.3, 0.95], gap='large')
    with left_panel:
        st.markdown("<div class='input-card'><h4>Employee Profile</h4><p>Enter the employee's details to calculate a tailored attrition risk score.</p></div>", unsafe_allow_html=True)

        input_grid = st.columns(2, gap='large')
        with input_grid[0]:
            monthly_income = st.slider("💰 Monthly Income ($)", min_value=1000, max_value=20000, value=4500, step=100)
            job_satisfaction = st.slider("😊 Job Satisfaction", min_value=1, max_value=4, value=3, step=1)
            overtime = st.selectbox("⏰ Overtime Status", ["No", "Yes"], index=0)
        with input_grid[1]:
            years_at_company = st.slider("📅 Years at Company", min_value=0, max_value=40, value=4, step=1)
            work_life_balance = st.slider("⚖️ Work-Life Balance", min_value=1, max_value=4, value=3, step=1)
            distance_from_home = st.slider("🏠 Distance From Home (km)", min_value=1, max_value=50, value=12, step=1)

        overtime_binary = 1 if overtime == "Yes" else 0
        st.markdown("<div class='prediction-card'><h4>Quick Score</h4><p>Submit the employee profile to generate a live attrition score and retention recommendation.</p></div>", unsafe_allow_html=True)
        predict_button = st.button("🔍 Generate Score", key="individual_predict")

        if predict_button:
            try:
                input_df = pd.DataFrame([{
                    'MonthlyIncome': monthly_income,
                    'JobSatisfaction': job_satisfaction,
                    'YearsAtCompany': years_at_company,
                    'OverTime': overtime_binary,
                    'WorkLifeBalance': work_life_balance,
                    'DistanceFromHome': distance_from_home
                }])

                input_df_processed = preprocess_for_prediction(input_df)
                probability = model.predict_proba(input_df_processed)[0, 1] * 100
                prediction = "High Risk" if probability >= 50 else "Low Risk"
                color_hex = "#f16d50" if probability >= 50 else "#2ecc71"
                message = (
                    "High risk of voluntary attrition — prioritize engagement and retention support." if probability >= 50 else
                    "Low attrition risk, but continue monitoring job satisfaction and work-life balance."
                )

                st.markdown(
                    f"<div class='result-card'>"
                    f"<h4>Attrition Score</h4>"
                    f"<div class='prediction-badge' style='background:{color_hex}20; color:{color_hex};'>{prediction}</div>"
                    f"<div class='result-score'>{probability:.1f}%</div>"
                    f"<div class='result-summary'>{message}</div>"
                    f"<div class='result-bar' style='width:{probability:.1f}%;'></div>"
                    f"</div>",
                    unsafe_allow_html=True
                )

                with st.expander("📋 Employee Input Summary"):
                    st.markdown(f"**Monthly Income:** ${monthly_income}")
                    st.markdown(f"**Job Satisfaction:** {job_satisfaction}/4")
                    st.markdown(f"**Years at Company:** {years_at_company}")
                    st.markdown(f"**OverTime:** {overtime}")
                    st.markdown(f"**Work-Life Balance:** {work_life_balance}/4")
                    st.markdown(f"**Distance From Home:** {distance_from_home} km")
                    st.markdown(f"**Predicted Attrition Probability:** {probability:.1f}%")
            except Exception as e:
                st.error(f"❌ Unable to score this employee: {str(e)}")

    with right_panel:
        st.markdown("<div class='guide-card'><h4>Retention Intelligence</h4><ul class='guide-list'><li>Use this score to identify employees who need engagement and support.</li><li>High risk often correlates with overtime, low satisfaction, and long commutes.</li><li>Pair the score with development conversations and manager check-ins.</li></ul></div>", unsafe_allow_html=True)
        st.markdown("<div class='guide-card'><h4>Recommended Actions</h4><ul class='guide-list'><li>Schedule a stay interview for high-risk employees.</li><li>Review compensation and career path signals.</li><li>Track overtime and work-life balance over the next 30 days.</li></ul></div>", unsafe_allow_html=True)

else:
    st.markdown("### ℹ️ App Information")
    st.markdown("""
    #### About This App
    Use this tool to predict employee attrition risk using machine learning. Choose between data exploration, batch predictions, and individual employee scoring.

    #### How It Works
    - **Data Explorer**: Inspect key categorical distributions and global attrition rate.
    - **Batch Prediction**: Upload a dataset to score your workforce and get retention recommendations.
    - **Individual Prediction**: Evaluate one employee at a time.

    #### Required Features for Batch Prediction
    Your dataset should include:
    - **MonthlyIncome**
    - **JobSatisfaction**
    - **YearsAtCompany**
    - **OverTime** (Yes/No)
    - **WorkLifeBalance**
    - **DistanceFromHome**

    #### Output Notes
    - The model predicts attrition risk using a Random Forest classifier.
    - Predictions include risk score, action buckets, and model insights.
    - Use the Data Explorer to validate feature distributions and category balance.
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #707070; font-size: 0.85em;'>"
    "Made with Streamlit | Employee Attrition Prediction System"
    "</div>",
    unsafe_allow_html=True
)
