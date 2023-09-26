# Proyecto 4 : Feature Selection
## Simulated Annealing (SA) + Symmetrical Uncertainty

### The work has been divided in sections to be considered as follows:

1. Data Preprocessing (James)

**Objective**

To normalize the dataset so that the features are scaled within a specific range.

**Steps to Implement**
- Load the dataset using pandas.read_csv().
- Apply Min-Max scaling to normalize the features.

**Need to know for the defense!**
- Understanding Min-Max scaling and its effect on the dataset.

2. _**Feature Selection Method: Simulated Annealing + Symmetrical Uncertainty**_ (Nico & Daniel, this will be a real challenge, so le the faith of the gods be with you)

**Objective**

To implement a feature selection algorithm using Simulated Annealing combined with Symmetrical Uncertainty as the objective function.

**Steps to Implement**
- Implement the Simulated Annealing algorithm.
- Define Symmetrical Uncertainty as the objective function.
- Use Simulated Annealing to select feature subsets based on Symmetrical Uncertainty.

**Need to know for the defense!**
- Understand the Simulated Annealing algorithm, its parameters, and how it works for optimization problems.
- Familiarize yourself with the Symmetrical Uncertainty metric and how it measures the relevance of features.

3. Top Five Feature Subsets (Nicky, on this depends the rest of the semester so beware)

**Objective**

To identify the top five feature subsets based on their per capita importance.

**Steps to Implement**

- Use the Simulated Annealing algorithm to generate a list of promising feature subsets.
- Calculate the per capita importance for each feature subset.

**Need to know for the defense!**
- Understand the concept of per capita importance and how to calculate it.

4. AUC Score-based Ranking (Sebas, this one should be pretty easy actually, so you owe us one)

**Objective**

To rank the top five feature subsets based on their AUC (Area Under the Curve) scores.

**Steps to Implement**
- Use a classification model (e.g., logistic regression, SVM, etc.) to evaluate the AUC score for each of the top five feature subsets.
- Rank the subsets based on their AUC scores.

**Need to know for the defense!**
- Understanding the AUC metric and how it is used to evaluate classification models.
- Familiarize yourself with ROC (Receiver Operating Characteristic) curves.

5. Interpretation and Conclusion (James)

**Objective**

To interpret the results and conclude the study.

**Steps to Implement**
- Discuss the per capita importance and its implications.
- Interpret the AUC scores for the feature subsets.
- Conclude the study, noting any limitations and suggesting avenues for future work.

**Need to know for the defense!**
- Methods for interpreting AUC scores and per capita importance.
- Limitations of using Simulated Annealing and Symmetrical Uncertainty for feature selection.

