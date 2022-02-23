from time import strftime

import flask
import logging
from logging.handlers import RotatingFileHandler
import os

import pandas as pd
import dill
dill._dill._reverse_typemap['ClassType'] = type

start_dt = strftime("[%Y-%b-%d %H:%M:%S]")

log_path = './log'
model_path = './model' # для работы из контейнера


handler = RotatingFileHandler(filename=log_path + './log.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

model_name = 'LogisticRegression'
model_file = model_path + '/' + model_name + '.dill'
model = None

def load_model():
	global model
	try:
		with open(model_file, 'rb') as f:
			model = dill.load(f)
	except IOError as e:
		logger.error(f"{start_dt} Error loading '{model_file}': {str(e)}")
		exit(1)
	logger.info(f"{start_dt} Loaded model: " + str(model))



app = flask.Flask(__name__)
model = None
host = "0.0.0.0"
port = 8180


@app.route("/", methods=["GET"])
def general():
	return f"""Welcome! 'http://{host}:{port}/predict' to POST"""


@app.route("/predict", methods=["POST"])
def predict():
	data = {"success": False}
	dt = strftime("[%Y-%b-%d %H:%M:%S]")
	if flask.request.method == "POST":
		request_json = flask.request.get_json()
		Incident_Date = request_json.get('Incident_Date', '')
		fatalities_total = request_json.get('fatalities_total', '')
		occupants_tottal = request_json.get('occupants_tottal', '')
		survived_total = request_json.get('survived_total', '')
		try:
			logger.info(f"{dt} Data: text='{text}', location='{location}', keyword='{keyword}'")
			preds = pipeline_lr.predict_proba(pd.DataFrame({"Incident_Date": [Incident_Date], "fatalities_total": [fatalities_total], "occupants_tottal": [occupants_tottal], "survived_total":[survived_total]}))
		except AttributeError as e:
			logger.warning(f'{dt} Exception: {str(e)}')
			data['predictions'] = str(e) + ' model = ' + str(model)
			data['success'] = False
			return flask.jsonify(data)
		data["predictions"] = preds[:, 1][0]
		logger.info(f"{dt} Data: Incident_Date='{Incident_Date}', fatalities_total='{fatalities_total}', occupants_tottal='{occupants_tottal}', survived_total='{survived_total}' - predicted {data['predictions']}")
		data["success"] = True
	return flask.jsonify(data)


if __name__ == "__main__":
	logger.info(f"{strftime('[%Y-%b-%d %H:%M:%S]')} Loading model and starting server ...")
	load_model()
	port = int(os.environ.get('PORT', port))
	app.run(host=host, port=port, debug=False)