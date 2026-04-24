# Employee Attrition Prediction System

A Streamlit dashboard for predicting employee attrition risk using a trained Random Forest model. This repository contains the production app, dataset, model artifacts, and supporting notebook used for training, evaluation, and insights.

## Project Overview

This project is designed to help HR teams identify employees who are at higher risk of leaving the organization. It includes:
- A Streamlit web dashboard for interactive data exploration and prediction
- A Jupyter notebook for model training, evaluation, and artifact generation
- Prebuilt model files for immediate use in the app
- Support for batch and single-record attrition scoring

## Repository Structure

```
app.py                                # Streamlit HR dashboard application
notebooks/
  └── EmploymentAttritionPrediction_group.ipynb   # Model training and analysis notebook
dataset/
  └── raw/
      └── attrition_data.csv          # Source employee attrition dataset
models/
  ├── attrition_model.joblib          # Trained model artifact
  ├── scaler.joblib                   # Feature scaler artifact
  └── feature_columns.joblib          # Feature metadata
presentation_slide/                   # Project presentation files
report/                               # Final report documents
requirements.txt                      # Python dependency list
README.md                             # Project documentation
Makefile                              # Run commands
setup.py                              # Package setup metadata
```

## Prerequisites

- Python 3.8 or newer
- `pip` installed
- Optional: a virtual environment for dependency isolation

## Installation

1. Open a terminal in the project root.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the App

Start the Streamlit dashboard with:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal (typically `http://localhost:8501`).

## Recommended Workflow

1. Confirm that `dataset/raw/attrition_data.csv` exists.
2. If you want to refresh or retrain the model, run the notebook:

```bash
jupyter notebook notebooks/EmploymentAttritionPrediction_group.ipynb
```

3. Launch the dashboard and navigate between:
   - **Data Explorer**
   - **Batch Prediction**
   - **Individual Prediction**
   - **Info**

## Model Artifacts

The app depends on the following files in `models/`:
- `attrition_model.joblib`
- `scaler.joblib`
- `feature_columns.joblib`

If the model or scaler files are missing, the app displays an error and stops.

## App Features

- **Data Explorer**: visualize employee distributions, attrition rates, department summaries, and other HR metrics using uploaded CSV/XLSX data.
- **Batch Prediction**: score multiple employee records at once and export prediction results.
- **Individual Prediction**: enter one employee profile and receive an attrition risk score.
- **Info view**: learn about required input features and the model pipeline.

## Prediction Inputs

The current prediction pipeline requires these features:
- `MonthlyIncome`
- `JobSatisfaction`
- `YearsAtCompany`
- `OverTime`
- `WorkLifeBalance`
- `DistanceFromHome`

The app preprocesses these values, scales numeric features, and applies the saved Random Forest model.

## Notebook Workflow

The notebook contains the full ML pipeline and covers:
1. data loading from `dataset/raw/attrition_data.csv`
2. exploratory data analysis
3. preprocessing and feature engineering
4. handling class imbalance
5. model training and evaluation
6. saving artifacts for deployment

## Dependencies

Key libraries used in this project:
- `streamlit`
- `pandas`
- `numpy`
- `scikit-learn`
- `joblib`
- `altair`
- `imbalanced-learn`
- `openpyxl`

## Notes

- Keep source data in `dataset/raw/`.
- Re-run the notebook if model inputs or preprocessing change.
- The dashboard is styled for a polished HR analytics experience but can be extended for other business use cases.

## Authors

Thrive Africa Capstone Group 14
