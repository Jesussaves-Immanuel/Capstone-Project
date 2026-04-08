import streamlit as st
import pandas as pd
import numpy as np
import joblib
import altair as alt
from pathlib import Path
import io

# Page configuration
st.set_page_config(
    page_title="Employee Attrition Prediction",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme and glassmorphism
st.markdown("""
    <style>
    body, .main, .block-container {
        background: radial-gradient(circle at top left, rgba(229, 57, 70, 0.14), transparent 20%),
                    radial-gradient(circle at top right, rgba(255, 121, 198, 0.12), transparent 18%),
                    linear-gradient(180deg, #071020 0%, #0d1732 100%);
        color: #e8f1ff;
    }

    .css-18ni7ap.e8zbici2 { background: transparent; }

    h1 {
        color: #ffffff;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 6px;
        font-weight: 700;
    }

    .subtitle {
        text-align: center;
        color: #c7d0f0;
        font-size: 1rem;
        margin-bottom: 35px;
        line-height: 1.6;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }

    .hero-card, .glass-card, .info-card, .summary-card {
        background: rgba(11, 18, 40, 0.72);
        border: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border-radius: 28px;
        box-shadow: 0 30px 80px rgba(0,0,0,0.25);
    }

    .hero-card {
        padding: 28px 36px;
        margin-bottom: 30px;
    }

    .section-title {
        color: #f7f9ff;
        margin-bottom: 12px;
        font-size: 1.5rem;
        font-weight: 700;
    }

    .section-description {
        color: #b7c1e0;
        line-height: 1.75;
        margin-bottom: 20px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 55px;
        padding: 0 22px;
        background-color: rgba(255,255,255,0.03);
        border-radius: 16px 16px 0 0;
        color: #b0b8d8;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        color: #ffffff;
        background-color: rgba(230, 57, 70, 0.20);
        border-bottom: 3px solid #e63946;
    }

    .stFileUploader, .stTextArea, .stNumberInput, .stSelectbox {
        border-radius: 22px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
    }

    .stButton > button {
        background: linear-gradient(135deg, #e63946 0%, #ff5c8a 100%);
        color: #ffffff;
        font-weight: 700;
        border-radius: 18px;
        height: 52px;
        box-shadow: 0 12px 35px rgba(230, 57, 70, 0.28);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 15px 45px rgba(230, 57, 70, 0.32);
    }

    .css-1n76uvr.e1fqkh3o1 {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 22px !important;
    }

    .stMetric > div {
        background: rgba(255,255,255,0.06);
        border-radius: 18px;
        padding: 18px 22px;
        min-height: 120px;
    }

    .stMarkdown {
        color: #d4d9f0;
    }

    .reportview-container .markdown-text-container p {
        color: #c5d1f2;
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
    "<div class='hero-card'><h1>Employee Attrition Prediction</h1><p class='subtitle'>Predict employee attrition risk with a polished HR analytics interface. Use batch uploads for dataset-wide scoring or evaluate a single employee with guided input controls.</p></div>",
    unsafe_allow_html=True
)

if not model_loaded:
    st.error("⚠️ Model files not found. Please ensure 'attrition_model.joblib' and 'scaler.joblib' are in the 'models/' directory.")
    st.stop()

# Sidebar navigation
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
        with st.container():
            st.markdown("#### Global Attrition Overview")
            if 'Attrition' in df_explore.columns:
                attrition_rate = df_explore['Attrition'].map({'Yes': 1, 'No': 0}).mean() * 100
                st.metric("Global Attrition Rate", f"{attrition_rate:.1f}%")
            else:
                st.info("The dataset does not include an Attrition column for global rate calculation.")

        categories = ['Department', 'JobRole', 'BusinessTravel']
        card_cols = st.columns(3)
        for col, category in zip(card_cols, categories):
            with col:
                if category in df_explore.columns:
                    st.markdown(f"#### {category}")
                    st.altair_chart(make_horizontal_bar_chart(df_explore, category, category, color='#8A2BE2'), use_container_width=True)
                else:
                    st.markdown(f"#### {category}")
                    st.info(f"Upload data with the `{category}` column to view this chart.")

        st.markdown("#### Dataset Preview")
        st.dataframe(df_explore.head(10), use_container_width=True)

elif nav_selection == "Batch Prediction":
    st.markdown("### 📦 Workforce Intelligence Dashboard")
    st.markdown("**Global business view**: Upload your employee dataset, review model-driven attrition risk, and explore retention strategies with clear guidance for HR teams.")
    st.markdown("Use the walkthrough below to interpret risk scores, feature drivers, and action buckets even if you're new to HR analytics.")

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
                    st.info("**Global Impact**: Maintain operational efficiency and team knowledge")

                with benefit_cols[2]:
                    st.markdown("#### 🛡️ Risk Mitigation")
                    risk_reduction = 100 - risk_percentage
                    st.metric("Retention Confidence", f"{risk_reduction:.1f}%", help="Percentage of workforce likely to remain stable")
                    st.info("**Strategic Impact**: Reduce business continuity risks worldwide")

                # Model Performance & Global Business Context
                st.markdown("### 📊 AI Model Performance")
                perf_col1, perf_col2 = st.columns([2, 1])
                with perf_col1:
                    accuracy = 90.8
                    st.markdown("<div class='glass-card' style='padding: 24px;'>", unsafe_allow_html=True)
                    st.markdown("#### Workforce Analytics")
                    st.markdown(f"**Model Accuracy:** {accuracy:.1f}%")
                    st.markdown("**Trained on:** IBM HR Dataset (adapted for workforce patterns)")
                    st.markdown("**Optimized for:** Recall (68% - catches at-risk employees)")
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
    st.markdown("Enter employee details below to compute attrition risk for a single employee.")

    left_col, right_col = st.columns([1, 1])
    with left_col:
        monthly_income = st.slider("💰 Monthly Income ($)", min_value=1000, max_value=20000, value=5000, step=100)
        years_at_company = st.slider("📅 Years at Company", min_value=0, max_value=40, value=5, step=1)
        distance_from_home = st.slider("🏠 Distance From Home (km)", min_value=1, max_value=50, value=10, step=1)
    with right_col:
        job_satisfaction = st.slider("😊 Job Satisfaction", min_value=1, max_value=4, value=3, step=1)
        work_life_balance = st.slider("⚖️ Work-Life Balance", min_value=1, max_value=4, value=3, step=1)
        overtime = st.selectbox("⏰ Overtime Status", ["No", "Yes"], index=0)

    overtime_binary = 1 if overtime == "Yes" else 0

    if st.button("🔍 Predict Attrition Risk"):
        try:
            input_df = pd.DataFrame([{
                'MonthlyIncome': monthly_income,
                'JobSatisfaction': job_satisfaction,
                'YearsAtCompany': years_at_company,
                'OverTime': overtime_binary,
                'WorkLifeBalance': work_life_balance,
                'DistanceFromHome': distance_from_home
            }])
            
            # Use the same preprocessing as batch prediction
            input_df_processed = preprocess_for_prediction(input_df)
            probability = model.predict_proba(input_df_processed)[0, 1] * 100
            prediction = int(probability >= 50)

            st.markdown("---")
            if prediction == 1:
                st.error(f"🚨 High risk of attrition detected ({probability:.1f}% probability). Consider retention actions.")
            else:
                st.success(f"✅ Low risk of attrition detected ({probability:.1f}% probability). Employee is likely to stay.")

            with st.expander("📋 Input Summary"):
                st.write(f"**Monthly Income:** ${monthly_income}")
                st.write(f"**Job Satisfaction:** {job_satisfaction}/4")
                st.write(f"**Years at Company:** {years_at_company}")
                st.write(f"**OverTime:** {overtime}")
                st.write(f"**Work-Life Balance:** {work_life_balance}/4")
                st.write(f"**Distance From Home:** {distance_from_home} km")
                st.write(f"**Predicted Attrition Probability:** {probability:.1f}%")
        except Exception as e:
            st.error(f"❌ Individual prediction failed: {str(e)}")

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
