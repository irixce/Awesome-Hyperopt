import json
import xxhash
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from flask_cors import CORS
from sqlalchemy import exc
from upload_flag import FlagUpload
from upload_config import ConfigUpload

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
with open('dbLogin.txt') as creds:
    app.config['SQLALCHEMY_DATABASE_URI'] = creds.readline()

db = SQLAlchemy(app)


# This is the table construction for the configurations table
class Configurations(db.Model):
    __tablename__ = 'configurations'
    conf_id = db.Column(db.String(16), primary_key=True)
    conf_json = db.Column(JSON, nullable=False)
    experiments = db.relationship('Experiments', backref='author')
    results = db.relationship('Results', backref='author')

    def __repr__(self):
        return f"Configurations('{self.conf_id}, {self.conf_json}')"


# This is the table construction for the experiments table.
class Experiments(db.Model):
    __tablename__ = 'experiments'
    index = db.Column(db.Integer, primary_key=True)
    flag_id = db.Column(db.String(16), nullable=False)

    exp_name = db.Column(db.String(30), nullable=False)
    data_df = db.Column(db.String(30), nullable=False)
    worker_class = db.Column(db.String(30), nullable=False)
    answer_column = db.Column(db.String(30), nullable=False)
    split_type = db.Column(db.String(30), nullable=False)
    problem_type = db.Column(db.String(30), nullable=False)
    model_type = db.Column(db.String(30), nullable=False)
    split_file = db.Column(db.String(30))
    split_test_size = db.Column(db.String(30))
    split_k = db.Column(db.String(30))

    exp_flags = db.Column(JSON, nullable=False)
    conf_id = db.Column(db.String(16), db.ForeignKey('configurations.conf_id'),
                        nullable=False)
    exp_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(10), nullable=False)

    # experiments = db.relationship('Experiments')

    def __repr__(self):
        return f"Results('{self.exp_id}, {self.exp_flags}, {self.exp_data}, {self.status}')"


# This is the table construction for the results table. This table is
# a relationship between Configurations and Experiments.
class Results(db.Model):
    # conf_id is pulled from the configurations table
    index = db.Column(db.Integer, primary_key=True)
    conf_id = db.Column(db.String(16), db.ForeignKey('configurations.conf_id'),
                        nullable=False)
    # exp_id is pulled from the experiments table
    exp_id = db.Column(db.Integer, db.ForeignKey('experiments.index'),
                       nullable=False)
    # results should be a table, or some other kind of data structure, I think.
    results = db.Column(JSON, nullable=False)

    def __repr__(self):
        return f"Experiments('{self.conf_id}, {self.exp_id}, {self.results}')"


# create_all() is run once to create AutoHopts.db. Changes to the schema
# of the database or tables can be tricky. James needed to remove the old .db
# file, then execute this command to re-create it using the new schema.
# Migration tools exist, but until we have real data, re-creating may be easier

# db.create_all()

# enable CORS
CORS(app)


# ping can be used to test if the server is running.
# for local use, enter http://localhost:8080/#/ping
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


# This is for sending default model configuration to frontend
@app.route('/defaultModels', methods=['GET'])
def default_models():
    # read the configurations file and load into set
    with open('default_configurations.json') as json_file:
        return jsonify(json.load(json_file))


# This is for sending default AWS flags to frontend
@app.route('/defaultPlatformFlags', methods=['GET'])
def default_aws_flags():
    # read the flag file and load into set
    with open('default_aws.json') as json_file:
        return jsonify(json.load(json_file))


# This is for sending default flags to frontend
@app.route('/defaultFlags', methods=['GET'])
def default_flags():
    # read the flag file and load into set
    with open('default_flags.json') as json_file:
        return jsonify(json.load(json_file))


# Check that a filepath is valid
@app.route('/validatePath', methods=['POST'])
def validate_path():
    response_object = {}
    valid = True  # placeholder. Later, replace this with an actual check
    if valid:
        response_object['status'] = 'success'
    else:
        response_object['status'] = 'failed'
    return jsonify(response_object)


# Upload and process flag file
@app.route('/uploadFlags', methods=['POST'])
def upload_flags():
    response_object = {}

    # Access file
    file = json.loads(request.form.get('file'))

    # Convert posted flag objects to modifiable dicts
    top_flags = json.loads(request.form.get('topFlags'))
    platform_flags = json.loads(request.form.get('platformFlags'))
    resource_flags = json.loads(request.form.get('resourceFlags'))
    problem_space_flags = json.loads(request.form.get('problemSpaceFlags'))

    # Create FlagUpload object to do all flag updating and error handling
    # Call FlagUpload's update function; updates all flags & checks for errors
    flag_upload = FlagUpload(file, top_flags, platform_flags, resource_flags, problem_space_flags)
    flag_upload.update()

    # Add updated flags to response object
    response_object['topFlags'] = flag_upload.top
    response_object['platformFlags'] = flag_upload.platform
    response_object['resourceFlags'] = flag_upload.resource
    response_object['problemSpaceFlags'] = flag_upload.problem_space

    # Get fail/success status and message from FlagUpload after processing
    response_object['status'] = flag_upload.status
    response_object['message'] = flag_upload.message

    return jsonify(response_object)


# Upload and process model configurations file
@app.route('/uploadConfigs', methods=['POST'])
def upload_configs():
    response_object = {}

    # Access file
    file = json.loads(request.form.get('file'))

    # Convert posted config object to modifiable dicts
    configs = json.loads(request.form.get('configs'))

    # Create ConfigUpload object to do all config updating and error handling
    # Call ConfigUpload's update function; updates all configs & checks for errors
    config_upload = ConfigUpload(file, configs)
    config_upload.update()

    # Add updated configs to response object
    response_object['configs'] = config_upload.configs

    # Get fail/success status and message from ConfigUpload after processing
    response_object['status'] = config_upload.status
    response_object['message'] = config_upload.message

    return jsonify(response_object)


# Write flags to file when user presses submit on main page
# Get is for displaying file on confirmation page
@app.route('/saveFlags', methods=['POST', 'GET'])
def save_flags():
    response_object = {'status': 'success'}

    if request.method == 'POST':
        # Get flags and setup info (setup corresponds to all fields above models in the app)
        obj = request.get_json()

        # Get rid of all key-value pairs in dictionary except for key_name: value
        for key, val in obj['setup'].items():
            obj['setup'][key] = val['value']
        for key, val in obj['flags'].items():
            obj['flags'][key] = val['value']

        # Depending on which split type was chosen, only one related split key will exist
        # For non-chosen ones, insert and set to null. Needed for submitting to database
        if 'split_k' not in obj['setup']:
            obj['setup']['split_k'] = None
        if 'split_test_size' not in obj['setup']:
            obj['setup']['split_test_size'] = None
        if 'split_file' not in obj['setup']:
            obj['setup']['split_file'] = None

        # Write to file
        try:
            with open('experiment_flags.json', 'w') as json_file:
                json.dump(obj, json_file, indent=4)
                response_object['message'] = 'flagfile created'
        except IOError:
            response_object['message'] = 'flagfile not created'

    else:
        # Give the current flag file to frontend
        try:
            with open('experiment_flags.json', 'r') as json_file:
                return jsonify(json.load(json_file))
        except IOError:
            response_object['message'] = 'flagfile not found'
            response_object['status'] = 'failed'

    return jsonify(response_object)


# Write model configurations to file when user presses submit on main page
# Get is for displaying file on confirmation page
@app.route('/saveConfigs', methods=['POST', 'GET'])
def save_configs():
    response_object = {'status': 'success'}

    if request.method == 'POST':
        configs = request.get_json()

        # Get rid of unnecessary key-value pairs in dictionary
        for model_name, model_values in configs.items():
            configs[model_name] = model_values['parameters']
            for param_val in configs[model_name].values():
                param_val.pop('display_name', 'error')
                param_val.pop('sequence', 'error')
                param_val.pop('lower_min', 'error')
                param_val.pop('lower_max', 'error')
                param_val.pop('upper_min', 'error')
                param_val.pop('upper_max', 'error')
                param_val.pop('quantization_min', 'error')
                param_val.pop('quantization_max', 'error')
                param_val.pop('error_count', 'error')

        # Write to file
        try:
            with open('experiment_configs.json', 'w') as json_file:
                json.dump(configs, json_file, indent=4)
                response_object['message'] = 'config file created'
        except IOError:
            response_object['message'] = 'config file not created'

    else:
        # Give the current flag file to frontend
        try:
            with open('experiment_configs.json', 'r') as json_file:
                return jsonify(json.load(json_file))
        except IOError:
            response_object['message'] = 'config file not found'
            response_object['status'] = 'failed'

    return jsonify(response_object)


@app.route('/submitRun', methods=['POST'])
def submit_run():
    response_object = {'status': 'success'}

    # We get the entire json which consists of model configurations,
    # flag information, and setup (setup corresponds to everything above models in the app)
    post_data = request.get_json()

    # separate them, generate hash, and add them
    # into database
    config = post_data['configurations']
    expr = post_data['flags']
    setup = post_data['setup']

    # Hash for configuration table
    hashed_id_conf = xxhash.xxh64(str(config)).hexdigest()

    # Hash for Experiment table (Concatenating with time so Hash is always unique)
    hashed_id_exp = xxhash.xxh64(str(expr)).hexdigest()

    # Default status for experiment (FOR NOW)
    status = 'Submitted'

    # Getting the configuration with same hash from the configuration table if exist.
    tmp_config = Configurations.query.filter_by(conf_id=hashed_id_conf).all()

    try:
        if len(tmp_config) == 0:
            con = Configurations(conf_id=hashed_id_conf,
                                 conf_json=config
                                 )

            db.session.add(con)
            db.session.commit()
            exp = Experiments(flag_id=hashed_id_exp,
                              exp_flags=expr,
                              conf_id=con.conf_id,
                              exp_name=setup['name'],
                              data_df=setup['data_df'],
                              answer_column=setup['answer_column'],
                              worker_class=setup['worker_class'],
                              split_type=setup['split_type'],
                              problem_type=setup['problem_type'],
                              model_type=setup['model_type'],
                              split_file=setup['split_file'],
                              split_test_size=setup['split_test_size'],
                              split_k=setup['split_k'],
                              status=status
                              )
            db.session.add(exp)
            db.session.commit()

            response_object['message'] = 'Submitted. Experiment id: ' + hashed_id_conf

        else:
            exp = Experiments(flag_id=hashed_id_exp,
                              exp_flags=expr,
                              conf_id=tmp_config[0].conf_id,
                              exp_name=setup['name'],
                              data_df=setup['data_df'],
                              answer_column=setup['answer_column'],
                              worker_class=setup['worker_class'],
                              split_type=setup['split_type'],
                              problem_type=setup['problem_type'],
                              model_type=setup['model_type'],
                              split_file=setup['split_file'],
                              split_test_size=setup['split_test_size'],
                              split_k=setup['split_k'],
                              status=status
                              )
            db.session.add(exp)
            db.session.commit()
            response_object['message'] = 'Experiment id: ' + hashed_id_conf

    except exc.SQLAlchemyError:
        response_object['status'] = 'failed'
        response_object['message'] = 'Experiment not added. Submit again.'
        logging.exception("Error writing to tables")

    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
