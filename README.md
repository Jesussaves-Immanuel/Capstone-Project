# Employee Attrition Prediction System

A Streamlit web application that predicts employee attrition risk using a trained Random Forest machine learning model. This project includes data exploration, model training via Jupyter notebook, and an interactive corporate intelligence dashboard.

## Project Structure

```
Capstone Project/
├── app.py                              # Streamlit dashboard application
├── notebooks/
│   └── EmploymentAttritionPrediction_group.ipynb   # Training & evaluation notebook
├── data/
│   └── raw/
│       └── attrition_data.csv          # IBM HR employee dataset
├── models/
│   ├── attrition_model.joblib          # Trained Random Forest model
│   ├── scaler.joblib                   # StandardScaler artifact
│   └── feature_columns.joblib          # Feature column names
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
├── Makefile                            # Build and run commands
└── setup.py                            # Package setup metadata
```

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Training Data

Ensure your dataset (`attrition_data.csv`) is in `data/raw/`.

### 3. Train the Model

Open and run the Jupyter notebook to train and save the model artifacts:

```bash
make notebook
```

Or manually run:
```bash
jupyter notebook notebooks/EmploymentAttritionPrediction_group.ipynb
```

Execute all cells to:
- Load and explore the data
- Preprocess features (encoding, scaling)
- Handle class imbalance with SMOTE
- Train a Random Forest Classifier
- Save model artifacts to `models/`

### 4. Launch the Streamlit App

```bash
make run
```

Or directly:
```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501` with these features:
- **Data Explorer** - Inspect dataset distributions and attrition patterns
- **Batch Prediction** - Upload CSV/XLSX to score multiple employees
- **Individual Prediction** - Score a single employee with guided inputs
- **Info** - Documentation and feature requirements

## Model Details

- **Algorithm**: Random Forest Classifier
- **Features**: MonthlyIncome, JobSatisfaction, YearsAtCompany, OverTime, WorkLifeBalance, DistanceFromHome
- **Target**: Attrition (Yes/No)
- **Class Imbalance**: Handled with SMOTE
- **Optimization**: Threshold tuned to maximize Recall (~68%)
- **Performance**: ~90.8% accuracy on test set

## Project Features

✅ Data exploration with Altair visualizations  
✅ Batch upload for workforce-wide predictions  
✅ Individual employee risk scoring  
✅ Feature importance analysis with drilldowns  
✅ Retention strategy recommendations (action buckets)  
✅ Dark-theme glassmorphism UI  
✅ CSV export of predictions  

## Required Files for App

The Streamlit app requires these model artifacts in `models/`:
- `attrition_model.joblib` - Trained model
- `scaler.joblib` - Feature scaler
- `feature_columns.joblib` - Feature names (optional, inferred from model)

If these files are missing, the app will display an error message.

## Notebook Workflow

The notebook (`EmploymentAttritionPrediction_group.ipynb`) handles the complete ML pipeline:
1. **Import & Setup** - Load libraries and configure visualization
2. **Data Loading** - Read from `data/raw/attrition_data.csv`
3. **EDA** - Analyze distributions, missing values, class imbalance
4. **Preprocessing** - Encode categorical features, scale numerical features
5. **Train/Test Split** - 80/20 split with stratification
6. **SMOTE** - Oversample minority class for balance
7. **Model Training** - Random Forest with cross-validation
8. **Evaluation** - Confusion matrix, classification report, ROC-AUC
9. **Feature Importance** - Identify key attrition drivers
10. **Model Export** - Save artifacts to `models/`

## How to Use the App

### Data Explorer
1. Upload a CSV/XLSX file with employee data
2. View global attrition rate and category distributions
3. Inspect the dataset preview

### Batch Prediction
1. Upload a dataset with the 6 required features
2. Review summary metrics (total employees, high-risk count)
3. Explore model insights and feature importance
4. Check retention strategy recommendations
5. Download results as CSV

### Individual Prediction
1. Enter an employee's details via sliders/dropdowns
2. Click "Predict Attrition Risk"
3. View risk probability and interpretation
4. Review input summary

## Dependencies

See `requirements.txt` for a complete list. Key packages:
- Streamlit (dashboard)
- scikit-learn (ML model)
- pandas, numpy (data processing)
- joblib (model serialization)
- Altair (visualizations)
- imbalanced-learn (SMOTE)

## Notes

- The notebook must be run before launching the app (to generate model files)
- The app auto-detects model files and displays an error if missing
- Predictions use probability-based scoring (0-100% risk scale)
- The model is optimized for recall (catching at-risk employees)

## Author

Student Project - Thrive Africa Capstone Group 14
