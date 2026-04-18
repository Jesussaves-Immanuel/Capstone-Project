# Employee Attrition Prediction System

A Streamlit web application that predicts employee attrition risk using a trained Random Forest model. The project includes data exploration, model training in a Jupyter notebook, and a dashboard for both batch and individual employee predictions.

## Current Project Structure

```
Machine Learning and Ai-Capstone Project-Group 14/
├── app.py                              # Streamlit dashboard application
├── notebooks/
│   └── EmploymentAttritionPrediction_group.ipynb   # Training and evaluation notebook
├── dataset/
│   └── raw/
│       └── attrition_data.csv          # IBM HR employee dataset
├── models/
│   ├── attrition_model.joblib          # Trained model artifact
│   ├── scaler.joblib                   # Scaler artifact
│   └── feature_columns.joblib          # Feature name metadata
├── presentation_slide/                 # Project presentation files
├── report/                            # Final report documents
├── requirements.txt                    # Python dependencies
├── README.md                           # Project documentation
├── Makefile                            # Build and run commands
└── setup.py                            # Package setup metadata
```

> Recent update: the dataset folder was reorganized to `dataset/raw/` and the README now reflects the current repository structure.

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Your Dataset

Ensure `attrition_data.csv` is located in `dataset/raw/`.

### 3. Train or Update the Model

Run the notebook to retrain or refresh the model artifacts:

```bash
make notebook
```

Or manually run:

```bash
jupyter notebook notebooks/EmploymentAttritionPrediction_group.ipynb
```

### 4. Launch the Streamlit App

```bash
make run
```

Or run directly:

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` and provides:
- **Data Explorer** for dataset summaries and attrition insights
- **Batch Prediction** for scoring employee datasets
- **Individual Prediction** for single employee risk assessment
- **Model and input guidance** for required features

## App Requirements

The Streamlit application uses these files from `models/`:
- `attrition_model.joblib`
- `scaler.joblib`
- `feature_columns.joblib`

If any model artifacts are missing, the app will show an error message.

## Model Overview

- **Algorithm**: Random Forest Classifier
- **Target**: `Attrition` (Yes / No)
- **Key steps**: feature encoding, scaling, class imbalance handling, model training, and export
- **Prediction output**: attrition risk probability and category label

## Notebook Workflow

The notebook handles the full ML pipeline:
1. Load libraries and configure environment
2. Read data from `dataset/raw/attrition_data.csv`
3. Explore and visualize the dataset
4. Preprocess features and encode categories
5. Handle class imbalance with SMOTE
6. Train the model and evaluate performance
7. Save model artifacts to `models/`

## How to Use the App

### Data Explorer
- Upload a CSV/XLSX dataset
- View attrition rates and distribution charts
- Inspect the dataset preview and clean-up summary

### Batch Prediction
- Upload employee data with the required features
- Review predictions and high-risk employee counts
- Download prediction results as CSV

### Individual Prediction
- Enter employee details using the form controls
- Click `Predict Attrition Risk`
- View risk probability and recommended interpretation

## Dependencies

Install from `requirements.txt`. Key libraries include:
- `streamlit`
- `scikit-learn`
- `pandas`
- `numpy`
- `joblib`
- `altair`
- `imbalanced-learn`

## Notes

- Keep the dataset path updated to `dataset/raw/`
- Re-run the notebook if model artifacts are regenerated
- The app uses the saved model files in `models/`

## Author

Thrive Africa Capstone Group 14
