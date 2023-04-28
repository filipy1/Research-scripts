# Research-scripts
General purpose scripts to aid in the analysis of a clinical trial that uses questionnaires to assess participants.

The scripts are used to create a streamlit multipage app where you can upload CSV/XLSX files containing trial/research participant's answers to questionnaires along with other data. The CSV/XLSX file has to be constructed in the following format: the index has 2 levels - the first is user ID and the second a date when the row's data was collected. Each column's title is a research question and the data itself is each user's answers to the questions in numerical form.

CSV/XLSX template for the uploaded file:

| First Index   | Second Index  | Question 1    | Question 2    | 
| ------------- | ------------- | ------------- | ------------- | 
| USER ID       | DD/MM/YYYY    | Numerical ans | Numerical ans |
| USER ID       | DD/MM/YYYY    | Numerical ans | Numerical ans |
| USER ID       | DD/MM/YYYY    | Numerical ans | Numerical ans |
| USER ID       | DD/MM/YYYY    | Numerical ans | Numerical ans |


## Explanation of Streamlit multipage app usage
For this project I utilized the power of the multipage streamlit feature.
The project is built such that there are 2 copies of each "streamlit app", one is for testing and building new features and the other is inside the "pages" under a different name which is the side bar title to be shown in the app.

Another thing to note is the "Welcome.py" file which is the landing page of the app.