MinViME - Minimum Viable Model Estimator 
-------------------------------------------

For many business problems it is worthwhile understanding how accurate a
machine learning model would need to be before you try and build it.

This information could be useful in prioritising projects or determining the
quantity and quality of data that will be needed. Extremely accurate models
for complicated problems typically require large amounts of data.

This application is a tool that allows you to estimate
what the minimum performance characteristics would need to be for a machine
learning problem. To make this estimate you will need to supply parameters
that describe the costs/benefits of the context in which it will be used.

### For Binary Classification Problems 

The application will make the estimate in terms of the ROC plot charcateristics 
that satisfy the requirements. The constraints need to be provided as:

* A cost/benefit payoff matrix
* The required ROI
* Information about the volume and frequency of the event you are predicting.

### For Regression/Time Series Problems

The application will make an estimate in terms of the minimum RMSE,MAE, and MAPE.
You will need to specify how the difference between actual and predicted values
will affect the business outcome. This can be as either proportional costs for 
errors that are too high ot too low, or as costs for predictions above a specified
margin of error.


# Usage




