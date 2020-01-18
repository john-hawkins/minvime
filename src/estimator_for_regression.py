""" 
    Estimator for Regression
    Functions for estimating model performance requirements from business criteria
"""
import numpy as np
import pandas as pd

######################################################################
def extract_distribution_from_sample(filepath):
    """ Extract a sample of target values from a file on the given path """
    try:
        df = pd.read_csv(filepath)
        indecies = [ np.issubdtype(x, np.number) for x in df.dtypes]
        only_numeric = df.loc[:,indecies]
        if len(only_numeric.columns)==0:
            return [], " your sample file: Please provide a CSV with a column of numeric values."
        else:
            return list(only_numeric.iloc[:,0]), ""
    #try:
    #    df = pd.read_csv('evaluate.py')
    except pd.errors.ParserError:
        return [], "Problem Parsing your sample file: Please provide a CSV with a column of numeric values."
    except:
        return [], "There was an unanticipated problem with your file. Please provide a CSV with a column of numeric values."

######################################################################
def produce_distribution_sample(mean, max, min):
    """ Given a some simple parameters generate sample of target values """

    return [1,2,3], ""


######################################################################
def estimate_model_requirements_proportional( dist, cases, pred_value, under_pred, under_pred_unit, over_pred, over_pred_unit, minroi):
    """ Given a sample of target values and requirements -- estimate baseline performance characteristics """
    candidates = generate_candidate_predictions(dist)
    rez_rmse = 0
    rez_mape = 0
    rez_mae = 0
    rez_return = 0
    current_roi = -999
    for candidate in candidates: 
        roi = calculate_candidate_roi(dist, candidate, pred_value, under_pred, under_pred_unit, over_pred, over_pred_unit)
        if current_roi == -999 or ( roi >= minroi and current_roi > roi):
            rez_rmse, rez_mape, rez_mae = calculate_candidate_metrics(dist, candidate)
    return rez_rmse, rez_mape, rez_mae

########################################################################
def calculate_candidate_metrics(dist, candidate):
    errors = [ x-y for x,y in zip(dist, candidate) ]
    sqrerrors = [ (x-y)*(x-y) for x,y in zip(dist, candidate) ] 
    rmse = np.sqrt(np.mean(sqrerrors))
    mae = np.mean(np.abs(errors))
    mape = 0
    nominal_actuals = add_nominals(dist)
    return rmse, mape, mae

########################################################################
def add_nominals(dist):
    return list( map( lambda x: 0.0001 if x==0 else x, dist) ) 

########################################################################
def generate_candidate_predictions(dist):
    sigma = np.std(dist)
    factors = [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    candidates = []
    for index, factor in enumerate(factors):
        candidates.append( copy_with_noise(dist, factor*sigma) )
    return candidates

########################################################################
def copy_with_noise(dist, scale):
    rez = list(map(lambda x: x + scale*np.random.normal(), dist))
    return rez

########################################################################
def calculate_candidate_roi(dist, candidate, pred_value, under_pred, under_pred_unit, over_pred, over_pred_unit): 
    total = 0
    for pred, act in zip(candidate, dist):
        error = pred - act
        abs_error = np.abs(error)
        if act == 0:
            p_error = 100 * abs_error/0.0001
        else:
            p_error = 100 * abs_error/act
        if error<0:
            if under_pred_unit=='percent':
                total = total + pred_value - (under_pred * p_error)
            else:
                total = total + pred_value - (under_pred * abs_error)
        else:
            if over_pred_unit=='percent':
                total = total + pred_value - (over_pred * p_error)
            else:
                total = total + pred_value - (over_pred * abs_error)
    return total

