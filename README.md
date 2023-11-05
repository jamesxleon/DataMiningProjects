# Proyecto 5 : Data Classification using Naive Bayes and kNN

### A note on the dataset: 

We are working with 27 out of 70 features from the original dataset.

Please, **please** document(comment) your code and use standard notation for all variables. 

## Data Preprocessing (James)

- Min-max normalization of the selected 27 features.
- Verifying the integrity of the normalized dataset.

## Stratified 10-Fold Cross-Validation (Pending)

- Write a briefing on how the stratified 10-fold cross-validation work. 
- Implement this on the dataset. 

## Naive Bayes Classifier (Pending)

- Implement the Naive Bayes classifier. 
- Apply the classifier using the stratified 10-fold cross-validation scheme.
- Calculate the required metrics (ACC, PRE, REC, AUC)

## k-Nearest Neighbors Classifier (Nicole)

- Implement the classifier with Euclidean and Manhattan distance measures.
- Optimize k in the interval [1,15] considering only odd numbers.
- Calculate the required metrics (ACC, PRE, REC, AUC)
