References
-----------

# \cite{Bradley97}

Bradley gives a discussion of methods for evaluating and comparing classifiers. He discusses a variety 
of common metrics and talks about ROI estimation in terms of misclassification costs. He dismisses this
with the observations that we usually do not know the associated costs of misclassification. He moves
on to describe a range of methods for estimating the area under the ROC curve and experiments designed to
evaluate this a single metric of classifier evaluation. He concludes with the observation that AUC is 
equivalent to the Wilcoxon test of ranks. 
Simulations are run on six medical data sets to establish that ranking classifiers

[https://doi.org/10.1016/S0031-3203(96)00142-2](https://doi.org/10.1016/S0031-3203(96)00142-2)

# \cite{Sanchez17} 

Sanchez argues that the application of a cost/yield matrix to the outcomes of a classifier decision
can be used to define a utility function that can be analysed in game theoretic terms. He confines his
analysis to situations in which the only yields are derived from true positives and true negatives,
and they are equal. The results in a demonstartion that the ideal classifier maximises predictive accuracy
by finding the threhsold of the ROC curve that intersects with the line TPR = 1 - FPR.


# \cite{Chen06}

Chen et al use numerical simulations to look at the impact of classification thresholds for a range of 
machine learning models applied to a selection of biomedical datasets. In their analysis they focus on
the minimising the costs of making mistakes (either false positives or false negatives). They derive an expression
for this cost function and then run simulations over different class balances generating sythetic data to
explore the sensitivity and specificty trade-off around the threshold interval around the point of maximum concordance. 



# \cite{LingLi98}

Ling and Li give an outline of many of the key considerations when applying machine learning examples.
They expand on the problems of imbalanced datasets and the poverty of accuracy as an evaluation metric.
They describe the cumulative lift chart and discuss how it can be used. They then describe techniques for
using the lift chart to generate an ROI plot to determine the optimal threshold.

[https://www.aaai.org/Papers/KDD/1998/KDD98-011.pdf](https://www.aaai.org/Papers/KDD/1998/KDD98-011.pdf)





