# Research-scripts
General purpose scripts to aid in the analysis of a clinical trial (or any other type of trial) that uses basic tabular data to assess participants.

The scripts are used to create a streamlit multipage app where you can upload CSV/XLSX files containing trial/research participant's answers to questionnaires along with other data. The CSV/XLSX file has to be constructed in the following format: the index has 2 levels - the first is user ID and the second a date when the row's data was collected. Each column's title is a research question and the data itself is each user's answers to the questions in numerical form.

CSV/XLSX template for the uploaded file:

| First Index   | Second Index  | Question 1    | Question 2    | 
| ------------- | ------------- | ------------- | ------------- | 
| USER ID       | DD/MM/YYYY    | Numerical ans | Numerical ans |
| USER ID       | DD/MM/YYYY    | Numerical ans | Numerical ans |
| USER ID       | DD/MM/YYYY    | Numerical ans | Numerical ans |
| USER ID       | DD/MM/YYYY    | Numerical ans | Numerical ans |


## Explanation of Streamlit multipage app usage
For this project I utilized the power of the multi-page streamlit feature.
The project is built such that there are 2 copies of each "streamlit app". One set of copies is in the "test_script" folder so you are able to run each app individually and change it as you see fit, the second set of copies is under the "pages" (specifically titled like this) folder and is meant to be the final product to be used in the multi-page app.
Another thing to note is the "Welcome.py" file which is the landing page of the app.

### Also added dockerfile support

### Usage example -
https://user-images.githubusercontent.com/91021054/235315833-d8b1e9e5-14c1-435b-8116-7b5f66eb15f0.mov

