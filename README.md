MinViME - Minimum Viable Model Estimator 
----------------------------------------
```
STATUS: INCOMPLETE -- THIS PROJECT IS A WORK IN PROGRESS
```

For many business problems it is worthwhile understanding how accurate a
machine learning model would need to be before you try and build it.

This information could be useful in prioritising projects or determining the
quantity and quality of data that will be needed. Extremely accurate models
for complicated problems typically require large amounts of data.

This application is a tool that allows you to estimate
what the minimum performance characteristics would need to be for a machine
learning problem. To make this estimate you will need to supply parameters
that describe the costs and benefits of the context in which it will be used.

### For Binary Classification Problems 

The application will make the estimate in terms of the ROC plot characteristics 
that satisfy the requirements. The constraints need to be provided as:

* A cost/benefit payoff matrix
* The required ROI
* Information about the volume and frequency of the event you are predicting.

### For Regression/Time Series Problems

The application will make an estimate in terms of the minimum RMSE, MAE, and MAPE.
You will need to specify how the difference between actual and predicted values
will affect the business outcome. This can be as either proportional costs for 
errors that are too high ot too low, or as costs for predictions above a specified
margin of error.


#### Caveats

In order to produce a MAPE score regardless of the distribution we add a nominal 
value of 0.0001 to calculate the percentage error when actuals are zero. 
There are many situations in which this would not be acceptable, for example,
when the quantities being prediced are in fact very low value real numbers. 
If your target distribution has many zero values and 
is confined to values that very close to zero then please ignore the MAPE estimates. 


# Usage




