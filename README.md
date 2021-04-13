MinViME - Minimum Viable Model Estimator 
=====================================================

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![build](https://github.com/john-hawkins/minvime/workflows/build/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/minvime.svg)](https://pypi.org/project/minvime)
[![Documentation Status](https://readthedocs.org/projects/minvime/badge/?version=latest)](https://minvime.readthedocs.io/en/latest/?badge=latest)
  
:copyright: 2020 John Hawkins

```
STATUS: Functional
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

If you use MinViME in academic work please reference the following paper:
```
Hawkins, John.,(2020), Minimum Viable Model Estimates for Machine Learning Projects,
Proceedings of the 6th International Conference on Computer Science, 
Engineering And Applications (CSEA 2020), pages 37-46, Issue 18, Volume 10,
DOI: 10.5121/csit.2020.101803
```

### For Binary Classification Problems 

The application will make the estimate in terms of the ROC plot characteristics 
that satisfy the requirements. The constraints need to be provided as:

* A cost/benefit payoff matrix
* The required ROI
* Information about the volume and frequency of the event you are predicting.


See examples in the [scripts directory](https://github.com/john-hawkins/minvime/tree/master/scripts)

### For Regression/Time Series Problems
```
In Progress
```
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


## Usage

You can use this application in multiple ways. The core application will launch a Flask
web application through which you can enter the parameters of the business problem you
require an estimate for.

### Web Application

This web application can be launched via the runner:

```
./minvime-runner.py 
```

Or you caniInvoke the directory as a package:

```
python -m minvime
```

Or simply install the package and use the command line application directly

#### Installation

Installation from the source tree:

```
git clone https://github.com/john-hawkins/minvime
cd minvime
python setup.py install
```

(or via pip from PyPI):

```
pip install minvime 
```

Now, the ``minvime`` command will launch the application 

```
minvime
```

### Library

Alternatively you can use minvime as a library of functions to use inside your own
applications or Jupyter Notebooks

```
import minvime as mvime

```


# Acknowledgements

Python package built using the
[bootstrap cmdline template](https://github.com/jgehrcke/python-cmdline-bootstrap)
 by [jgehrcke](https://github.com/jgehrcke)


