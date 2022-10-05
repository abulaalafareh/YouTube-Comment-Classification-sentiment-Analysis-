# YouTube-Comment-Classification-sentiment-Analysis-

This project was made as our final year project group members being me and https://github.com/Abdullahniazi 

Basic Introduction:

  This project is youtube comment classification. In this project we scrape and classify youtube comments into different categories based on their sentiments
  total sentiments being 16. We decided to get of the bubble of only positive, negative and neutral Sentiment and decided to increase the horizons for sentiment
  analysis.
  
Categories:
  1. Appreciation
  2. Recommendation
  3. sad
  4. hate
  5. greeting
  6. blessing
  7. Quotation
  8. wish
  9. Question
  10. Love
  11. Excitement
  12. Request
  13. Links
  14. Others
  15. Positive
  16. Negative

Working:
  steps:
  1. Scrape YouTube Save them to database
  2. Perform Sentiment Analysis on each comment and save to database
  3. Show in tabels
  
Models:
  We used different ML and DL models including Logistic Regression, SVM, KNN, Random Forest Classifier and BERT.
  Every model had accuracy around 75%-80% but the one which performed best on real time data was BERT.
  Total dataset was around 4700 which was mostly manually labeled as we could not find most of the categories data on the internet.
  Current BERT model was trained on a single epoch.
  
  The model which is present in this repository is a logistic Regression Model because we did not find it feasible to upload BERT model
  as it was around 1.2gb. Instead Logistic Regression model is uploaded. Logistic Regression predictions cannot be compared to that of BERT but still
  are quite good.
  
 
Requirments
  Libraries:
  1. pip install Tkinter
  2. pip install Joblib
  3. pip install functools
  4. pip install operator
  5. pip install string
  6. pip install sqlite3
  7. pip install pandas
  8. pip install --upgrade google-api-python-client
