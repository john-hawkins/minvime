import sys
import pytest
import src.estimator as esti # The file ../src/estimator.py

"""
This file (test_estimator.py) contains the unit tests for the src/estimator.py file.
"""


def test_estimate_model_requirements():
    """
       Test the ROI estimator for binary classification models.
    """

    auc, prec, recall = esti.estimate_binary_model_requirements(
        tp=2000, fp=-100, tn=0, fn=0, cases=100000,
        baserate=0.001, minroi=10000
    )

    assert round(auc,3) == 0.892
    assert round(prec,4) == 0.0596
    assert round(recall,4) == 0.3164

def test_estimate_intervention_requirements():
    tp, fp, tn, fn = esti.estimate_intervention_requirements(1000, 0.1, 10, 100, -100, 0.5, 0.01)
    assert round(tp,1) == 40.0
    assert round(fp,1) == -11.0

