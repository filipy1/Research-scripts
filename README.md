# Research-scripts
General purpose scripts to aid in the analysis of a clinical trial that uses questionnaires to assess participants.

The scripts are used to create streamlit apps where you can upload CSV files containing trial participant's answers to questionnaires. The CSV file has to be of constructed in the following form: the index has 2 levels - the first is user ID and the second a date when the row's data was collected. Each column's title is a research question and the data itself is each user's answers to the questions in numerical form.

CSV template for the uploaded file:

| First Index   | Second Index  | Question 1    | Question 2    | 
| ------------- | ------------- | ------------- | ------------- | 
| USER ID       | DD/MM/YYYY    | Numerical ans | Numerical ans |
| USER ID       | DD/MM/YYYY    | Numerical ans | Numerical ans |
| USER ID       | DD/MM/YYYY    | Numerical ans | Numerical ans |
| USER ID       | DD/MM/YYYY    | Numerical ans | Numerical ans |