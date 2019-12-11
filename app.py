from flask import Flask, flash, request, render_template
import estimator as esti # The file estimator.py 
import os

app = Flask(__name__)


# ###################################################################################
# Index Page
@app.route('/', methods = ['POST', 'GET'])
def index():
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

    return render_template("index.html",
       tp=tp, fp=fp, tn=tn, fn=fn, cases=cases, baserate=baserate, minroi=minroi)

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

    auc, prec, recall = esti.estimate_model_requirements(
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
        return render_template("intervention.html")

# ###################################################################################
# 
@app.route('/proportional', methods = ['POST', 'GET'])
def proportional():
        return render_template("proportional.html")

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


