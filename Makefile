install:
	pip install -r requirements.txt

run:
	streamlit run app.py

notebook:
	jupyter notebook notebooks/EmploymentAttritionPrediction_group.ipynb
