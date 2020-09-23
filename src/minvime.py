# -*- coding: utf-8 -*-

"""minvime: provides entry point main() which loads the Flask app."""

__version__ = "0.1.0"

from flask import Flask, flash, request, redirect, render_template, url_for, make_response
from werkzeug.utils import secure_filename
from pathlib import Path
import os

from .estimator_classification import estimate_intervention_requirements
from .estimator_classification import estimate_binary_model_requirements

from .estimator_regression import extract_distribution_from_sample
from .estimator_regression import produce_distribution_sample
from .estimator_regression import estimate_model_requirements_proportional
from .estimator_regression import estimate_model_requirements_thresholded

#import .estimator as esti # The file minvime/estimator.py

#import .estimator_for_regression as r_esti # The minvime/estimator_for_regression.py

UPLOAD_FOLDER = './uploads'

ALLOWED_EXTENSIONS = set(['csv'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)

# ###################################################################################
#    MAIN APPLICATION ENTRY POINT
#      With debug=True, Flask server will auto-reload
#      when there are code changes
def main():
    app.run(port=5000, debug=True)


# ###################################################################################
# Index Page
@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template("index.html")

# ###################################################################################
# Cost Benefit Page
@app.route('/payoff_matrix', methods = ['POST', 'GET'])
def payoff_matrix():
    tp = 2000
    fp = -150
    tn = 0
    fn = 0
    minroi = 10000
    cases = 1000000
    baserate = 0.001
    if request.method == 'POST':
       if 'tp' in request.values:
          tp = float(request.form["tp"])
          fp = float(request.form["fp"])
          tn = float(request.form["tn"])
          fn = float(request.form["fn"])
          cases = float(request.form["cases"])
          baserate = float(request.form["baserate"])

    return render_template("payoff_matrix.html",
       tp=tp, fp=fp, tn=tn, fn=fn, cases=cases, baserate=baserate, minroi=minroi)

# ###################################################################################
@app.route('/analyse', methods = ['POST', 'GET'])
def analyse():
    if 'tp' in request.values:
        tp = float(request.form["tp"])
        fp = float(request.form["fp"])
        tn = float(request.form["tn"])
        fn = float(request.form["fn"])
        minroi = float(request.form["minroi"])
        cases = float(request.form["cases"])
        baserate = float(request.form["baserate"])
    else:
        tp = 2000
        fp = -150
        tn = 0
        fn = 0
        minroi = 10000
        cases = 1000000
        baserate = 0.001

    auc, prec, recall, fprs, tprs = estimate_binary_model_requirements(
        tp=tp, fp=fp, tn=tn, fn=fn, cases=cases, baserate=baserate, minroi=minroi)

    auc = round(auc, 3)
    prec = round(prec, 3)
    recall = round(recall, 3)

    return render_template("analyse.html", auc=auc, precision=prec, recall=recall,
        tp=tp, fp=fp, tn=tn, fn=fn, cases=cases, baserate=baserate, minroi=minroi, fprs=fprs, tprs=tprs)

# ###################################################################################
# Intervention Page
@app.route('/intervention')
def intervention():
    minroi = 10000
    cases = 1000000
    cost  = -10
    baserate = 0.001
    succrate = 0.1
    backfire = 0.03
    payoff = 2000
    payback = -100

    return render_template("intervention.html",
        minroi=minroi, cases=cases, baserate=baserate,
        cost=cost, payoff=payoff, payback=payback,
        succrate=succrate, backfire=backfire
    )

# ###################################################################################
# analyse Intervention Page
@app.route('/analyse_intervention', methods = ['POST', 'GET'])
def analyse_intervention():
    if 'payoff' in request.values:
       cases = float(request.form["cases"])
       cost = float(request.form["cost"])
       baserate = float(request.form["baserate"])
       succrate = float(request.form["succrate"])
       backfire = float(request.form["backfire"])
       payoff = float(request.form["payoff"])
       payback = float(request.form["payback"])
       minroi = float(request.form["minroi"])
    else:
       minroi = 10000
       cases = 1000000
       cost  = -10
       baserate = 0.001
       succrate = 0.1
       backfire = 0.03
       payoff = 2000
       payback = -100

    tp, fp, tn, fn = estimate_intervention_requirements(cases=cases, baserate=baserate,
                                                cost=cost, payoff=payoff, payback=payback,
                                                succrate=succrate, backfire=backfire)

    auc, prec, recall, fprs, tprs = estimate_binary_model_requirements(
        tp=tp, fp=fp, tn=tn, fn=fn, cases=cases, baserate=baserate, minroi=minroi)

    auc = round(auc, 3)
    prec = round(prec, 3)
    recall = round(recall, 3)

    return render_template("analyse_intervention.html",
        auc=auc, precision=prec, recall=recall,
        minroi=minroi, cases=cases, baserate=baserate,
        cost=cost, payoff=payoff, payback=payback,
        succrate=succrate, backfire=backfire, fprs=fprs, tprs=tprs
    )

# ###################################################################################
#
@app.route('/proportional', methods = ['POST', 'GET'])
def proportional():
    minroi = 10000
    cases = 10000
    pred_value = 100
    over_pred = -10
    under_pred = -10
    mean = 100
    min = 0
    max = 500

    return render_template("proportional.html",
        minroi=minroi, cases=cases, mean=mean, max=max, min=min,
        pred_value=pred_value, under_pred=under_pred, over_pred=over_pred
    )

# ###################################################################################
# Analyse Proportional Costs for a Regression Problem
@app.route('/analyse_proportional', methods = ['POST', 'GET'])
def analyse_proportional():
    minroi = float(request.form["minroi"])
    cases = float(request.form["cases"])
    pred_value = float(request.form["pred_value"])
    over_pred = float(request.form["over_pred"])
    over_pred_unit = request.form["over_pred_unit"]
    under_pred = float(request.form["under_pred"])
    under_pred_unit = request.form["under_pred_unit"]
    mean = float(request.form["mean"])
    min = float(request.form["min"])
    max = float(request.form["max"])

    # CHECK FOR THE SAMPLE FILE
    sample_file = False
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            sample_file = True

    if sample_file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        dist, message = extract_distribution_from_sample(filepath)
    else:
        dist, message = produce_distribution_sample(mean=mean, max=max, min=min)

    if len(dist) == 0:
        return render_template("error.html", message=message, link="proportional.html")

    rmse, mape, mae = estimate_model_requirements_proportional(
        dist=dist, cases=cases,
        pred_value=pred_value, under_pred=under_pred, under_pred_unit=under_pred_unit,
        over_pred=over_pred, over_pred_unit=over_pred_unit, minroi=minroi
    )
    rmse = round(rmse, 3)
    mape = round(mape, 3)
    mae = round(mae, 3)

    return render_template("analyse_proportional.html",
        rmse=rmse, mae=mae, mape=mape, minroi=minroi, cases=cases,
        mean=mean, max=max, min=min,
        pred_value=pred_value, under_pred=under_pred, over_pred=over_pred
    )


# ###################################################################################
#
@app.route('/thresholded')
def thresholded():
    minroi = 10000
    cases = 10000
    pred_value = 100
    over_pred = -10
    over_pred_threshold = 10
    under_pred = -10
    under_pred_threshold = 10
    mean = 100
    min = 0
    max = 500

    return render_template("thresholded.html",
        minroi=minroi, cases=cases, mean=mean, max=max, min=min,
        pred_value=pred_value, under_pred=under_pred, under_pred_threshold=under_pred_threshold,
        over_pred=over_pred, over_pred_threshold=over_pred_threshold
    )

# ###################################################################################
# Analyse thresholded Costs for a Regression Problem
@app.route('/analyse_thresholded', methods = ['POST', 'GET'])
def analyse_thresholded():
    minroi = float(request.form["minroi"])
    cases = float(request.form["cases"])
    pred_value = float(request.form["pred_value"])
    over_pred = float(request.form["over_pred"])
    over_pred_unit = request.form["over_pred_unit"]
    over_pred_threshold = request.form["over_pred_threshold"]
    under_pred = float(request.form["under_pred"])
    under_pred_unit = request.form["under_pred_unit"]
    under_pred_threshold = request.form["under_pred_threshold"]
    mean = float(request.form["mean"])
    min = float(request.form["min"])
    max = float(request.form["max"])

    # CHECK FOR THE SAMPLE FILE
    sample_file = False
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            sample_file = True

    if sample_file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        dist, message = extract_distribution_from_sample(filepath)
    else:
        dist, message = produce_distribution_sample(mean=mean, max=max, min=min)

    if len(dist) == 0:
        return render_template("error.html", message=message, link="thresholded.html")

    rmse, mape, mae = estimate_model_requirements_thresholded(
        dist=dist, cases=cases, pred_value=pred_value,
        under_pred=under_pred, under_pred_unit=under_pred_unit, under_pred_threshold=under_pred_threshold,
        over_pred=over_pred, over_pred_unit=over_pred_unit, over_pred_threshold=over_pred_threshold, minroi=minroi
    )

    rmse = round(rmse, 3)
    mape = round(mape, 3)
    mae = round(mae, 3)

    return render_template("analyse_thresholded.html",
        rmse=rmse, mae=mae, mape=mape, minroi=minroi, cases=cases,
        mean=mean, max=max, min=min,
        pred_value=pred_value, under_pred=under_pred, under_pred_threshold=under_pred_threshold,
        over_pred=over_pred, over_pred_threshold=over_pred_threshold
    )



# ###################################################################################
# About Page
@app.route("/showplot")
def showplot():

    fprs = request.args.get('fprs')
    tprs = request.args.get('tprs')
    print("FPRS:", fprs)
    print("TPRS:", tprs)
    fpr = fprs[1:-1].replace("e 00","").split()
    tpr = tprs[1:-1].replace("e 00","").split()
    print("FPR:", fpr)
    print("TPR:", tpr)
    x = [ float(x) for x in fpr]
    y = [ float(x) for x in tpr]

    from io import BytesIO
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure

    fig=Figure()
    ax=fig.add_subplot(111)
    ax.plot(x, y, '-')
    ax.set_title("Estimated Minimum Viable ROC")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

# ###################################################################################
# About Page
@app.route('/about')
def about():
        return render_template("about.html")



# ###################################################################################
if __name__ == '__main__':
    main()
