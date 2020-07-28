from upload_errors import InvalidFlag


class FlagUpload:
    # constructor for the FlagUpload object
    def __init__(self, file, top_flags, platform_flags, resource_flags, problem_space_flags):

        # input file
        self.file = file

        # flags to be updated
        self.top = top_flags
        self.platform = platform_flags
        self.resource = resource_flags
        self.problem_space = problem_space_flags

        # status messages
        self.status = ""
        self.message = ""
        self.error_message = ""

    def check_valid_key(self):

        # using 'list(set(list(...' is a method of removing duplicated while
        # constructing a list.
        # The last three parts added handle edge cases related to the
        # split_type key.
        all_keys = list(set(list(self.top.keys())
                            + list(self.platform.keys())
                            + list(self.resource.keys())
                            + list(self.problem_space.keys())
                            + list(['split_file'])
                            + list(['split_test_size'])
                            + list(['split_k'])))

        invalid_keys = [key for key in self.file.keys() if key not in all_keys]

        if len(invalid_keys) != 0:
            self.error_message = "The following are not valid flags: " + str(invalid_keys)
            raise InvalidFlag

    # The bulk of this update method is designed to handle the split_type edge
    # cases. This is due to the way Main.vue updates the flag data when the user
    # changes the split type. The uploaded flag file must check the uploaded
    # split_type against the associated split type value (split_k, split_file,
    # or split_test_size)
    def update_top_flags(self):
        # a mini-dictionary to be used below. Matches split values with types
        val_to_type = {
            'split_file': 'user',
            'split_k': 'k-fold',
            'split_test_size': 'train-test'
        }
        # and another mini-dictionary going the other way
        type_to_val = {
            'user': 'split_file',
            'k-fold':'split_k',
            'train-test':'split_test_size'
        }
        # list comprehension checks top flag keys and all split values
        new_flags = [key for key in self.file.keys()
                     if key in self.top.keys()
                     or key in val_to_type.keys()]
        for flag in new_flags:
            # If the current flag is one of the three split value types
            if flag in val_to_type.keys():
                # we're going to construct a new flag object
                new_flag = {}
                # first check to see if the split type matches the split value
                if self.file.get('split_type') != val_to_type.get(flag):
                    self.error_message = "Split type and value mismatch"
                    raise InvalidFlag
                else:
                    # remove any existing split values from the top flags.
                    self.top.pop('split_file',
                                 self.top.pop('split_k',
                                              self.top.pop('split_test_size')))
                    # then populate the flag object appropriately
                    if flag == 'split_file':
                        new_flag['display_name'] = "Path to Split File"
                    else:
                        if flag == 'split_k':
                            new_flag['display_name'] = "k"
                        elif flag == 'split_test_size':
                            new_flag['display_name'] = "Test Size"
                        new_flag['min'] = 0
                        new_flag['max'] = 1000
                    new_flag['options'] = ""
                    new_flag['error_count'] = 0
                    new_flag['value'] = self.file.get(flag)
                    self.top[flag] = new_flag
            # else we just update the flag value.
            else:
                self.top[flag]['value'] = self.file.get(flag)
        # finally we need to do a check to see if the user uploaded a new
        # split_type and forgot to upload the associated split type value.
        splittype = self.top['split_type']['value']
        if not self.top.get(type_to_val.get(splittype)):
            self.error_message = "Split type changed and split value not compatible"
            raise InvalidFlag

    def update_platform_flags(self):
        new_flags = [key for key in self.file.keys() if key in self.platform.keys()]
        for i in range(len(new_flags)):
            self.platform[new_flags[i]]['value'] = self.file.get(new_flags[i])

    def update_resource_flags(self):
        new_flags = [key for key in self.file.keys() if key in self.resource.keys()]
        for i in range(len(new_flags)):
            self.resource[new_flags[i]]['value'] = self.file.get(new_flags[i])

    def update_problem_space_flags(self):
        new_flags = [key for key in self.file.keys() if key in self.problem_space.keys()]
        for i in range(len(new_flags)):
            self.problem_space[new_flags[i]]['value'] = self.file.get(new_flags[i])

    def update(self):
        try:
            self.check_valid_key()
            self.update_top_flags()
            self.update_platform_flags()
            self.update_resource_flags()
            self.update_problem_space_flags()
        except InvalidFlag:
            self.status = "failed"
            self.message = self.error_message
        else:
            self.status = "success"
            self.message = "Flags file successfully uploaded!"
