import upload_errors


class ConfigUpload:

    # constructor for ConfigUpload object
    def __init__(self, file, configs):
        self.file = file
        self.configs = configs
        self.status = ""
        self.message = ""
        self.bad_model_type = ""
        self.bad_problem = ""
        self.bad_model = ""
        self.bad_params = ""

    # each of the check_xxx methods compares the uploaded file against what
    # currently exists in the system. This is a shallow check to make sure the
    # user isn't trying to upload something completely new.

    # checks model type (classical / neural_networks)
    def check_model_type(self):
        # using 'list(set(list(...' is a method of removing duplicated while
        # constructing a list.
        config_keys = list(set(list(self.configs.keys())))
        invalid_keys = [key for key in self.file.keys() if key not in config_keys]
        if len(invalid_keys) != 0:
            self.bad_model_type = "The following are not valid model types: " + str(invalid_keys)
            raise upload_errors.InvalidModelTypes

    # checks problem type (classification / regression)
    def check_problem_type(self, model_type):
        problem_keys = list(set(list(self.configs[model_type].keys())))
        invalid_keys = [key for key in self.file[model_type].keys() if key not in problem_keys]
        if len(invalid_keys) != 0:
            self.bad_problem = "The following are not valid problem types: " + str(invalid_keys)
            raise upload_errors.InvalidProblemTypes

    # checks the models (knn, svc, etc...)
    def check_model(self, model_type, problem_type):
        model_keys = list(set(list(self.configs[model_type][problem_type].keys())))
        invalid_keys = [key for key in self.file[model_type][problem_type].keys() if key not in model_keys]
        if len(invalid_keys) != 0:
            self.bad_model = "The following are not valid algorithm types: " + str(invalid_keys)
            raise upload_errors.InvalidAlgTypes

    # checks the parameters (upper, lower, quantization, etc...)
    def check_params(self, model_type, problem_type, model):
        param_keys = list(set(list(self.configs[model_type][problem_type][model]['parameters'].keys())))
        invalid_keys = [key for key in self.file[model_type][problem_type][model].keys() if key not in param_keys]
        if len(invalid_keys) != 0:
            self.bad_params = "The following are not valid parameter types: " + str(invalid_keys)
            raise upload_errors.InvalidParamsTypes

    # deeply nested for loops iterate over the file, calling appropriate check
    # methods as it goes.
    # Consider making this all recursive or daisy-chaining the checks to 
    # improve readability.
    def update_configs(self):
        self.check_model_type()
        model_types = self.file.keys()
        for model_type in model_types:
            self.check_problem_type(model_type)
            problem_types = self.file[model_type].keys()
            for problem_type in problem_types:
                self.check_model(model_type, problem_type)
                models = self.file[model_type][problem_type].keys()
                for model in models:
                    self.check_params(model_type, problem_type, model)
                    params = self.file[model_type][problem_type][model].keys()
                    for param in params:
                        # now we dig into the parameter attributes
                        param_attributes = self.file[model_type][problem_type][model][param].keys()
                        for attribute in param_attributes:
                            # get the new value from the uploaded file
                            new_val = self.file[model_type][problem_type][model][param][attribute]
                            if attribute == "sequence":
                                # if it's select box, append new to old
                                default_vals = self.configs[model_type][problem_type][model]['parameters'][param][attribute]
                                self.configs[model_type][problem_type][model]['parameters'][param][attribute] = list(set(default_vals + new_val))
                            else:
                                # else just give it a new value
                                self.configs[model_type][problem_type][model]['parameters'][param][attribute] = new_val

    def update(self):
        try:
            self.check_model_type()
            self.update_configs()
        except upload_errors.InvalidModelTypes:
            self.status = "failed"
            self.message = self.bad_model_type
        except upload_errors.InvalidProblemTypes:
            self.status = "failed"
            self.message = self.bad_problem
        except upload_errors.InvalidAlgTypes:
            self.status = "failed"
            self.message = self.bad_model
        except upload_errors.InvalidParamsTypes:
            self.status = "failed"
            self.message = self.bad_params
        else:
            self.status = "success"
            self.message = "Configs file successfully uploaded!"
