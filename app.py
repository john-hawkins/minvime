from flask import Flask, flash, request, render_template
import src.estimator as esti # The file src/estimator.py 
import src.estimator_for_regression as r_esti # The src/estimator_for_regression.py
from werkzeug.utils import secure_filename
from pathlib import Path
import os

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'

ALLOWED_EXTENSIONS = set(['csv'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ###################################################################################
# Index Page
@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template("index.html")

# ###################################################################################
# Cost Benefit Page
@app.route('/payoff_matrix', methods = ['POST', 'GET'])
def payoff_matrix():
    tp = 5000
    fp = -50
    tn = 0
    fn = 0
    minroi = 10000
    cases = 10000
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
        tp = 5000
        fp = -50
        tn = 0
        fn = 0
        minroi = 10000 
        cases = 10000 
        baserate = 0.001

    auc, prec, recall = esti.estimate_binary_model_requirements(
        tp=tp, fp=fp, tn=tn, fn=fn, cases=cases, baserate=baserate, minroi=minroi)

    auc = round(auc, 3)
    prec = round(prec, 3)
    recall = round(recall, 3)

    return render_template("analyse.html", auc=auc, precision=prec, recall=recall,  
        tp=tp, fp=fp, tn=tn, fn=fn, cases=cases, baserate=baserate, minroi=minroi)

# ###################################################################################
# Intervention Page
@app.route('/intervention')
def intervention():
    minroi = 10000
    cases = 10000
    cost  = 10
    baserate = 0.01
    succrate = 0.1
    backfire = 0.03
    payoff = 1000
    payback = -400


    return render_template("intervention.html", 
        minroi=minroi, cases=cases, baserate=baserate,
        cost=cost, payoff=payoff, payback=payback,
        succrate=succrate, backfire=backfire
    )

# ###################################################################################
# Intervention Page 
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
       cases = 10000
       cost  = 10
       baserate = 0.01
       succrate = 0.1
       backfire = 0.03
       payoff = 1000
       payback = -400

    tp, fp, tn, fn = esti.estimate_intervention_requirements(cases=cases, baserate=baserate,
                                                cost=cost, payoff=payoff, payback=payback,
                                                succrate=succrate, backfire=backfire)

    auc, prec, recall = esti.estimate_binary_model_requirements(
        tp=tp, fp=fp, tn=tn, fn=fn, cases=cases, baserate=baserate, minroi=minroi)

    auc = round(auc, 3)
    prec = round(prec, 3)
    recall = round(recall, 3)

    return render_template("analyse_intervention.html", 
        auc=auc, precision=prec, recall=recall,
        minroi=minroi, cases=cases, baserate=baserate,
        cost=cost, payoff=payoff, payback=payback,
        succrate=succrate, backfire=backfire
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
# Intervention Page
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
        dist, message = r_esti.extract_distribution_from_sample(filepath)
    else:
        dist, message = r_esti.produce_distribution_sample(mean=mean, max=max, min=min)

    if len(dist) == 0: 
        return render_template("error.html", message=message, link="proportional.html")

    rmse, mape, mae = r_esti.estimate_model_requirements_proportional(
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
        return render_template("thresholded.html")

# ###################################################################################
# About Page
@app.route('/about')
def about():
        return render_template("about.html")


# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
	app.run(port=5000, debug=True)


