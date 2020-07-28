<template>
  <div>
    <!-- if showConfirm is true, show the confirmation page instead of main page -->
    <confirm v-if="showConfirm"/>
    <div class="main-container" v-show="showMain">
      <div class="header">
        <img class="logo" src='../assets/Deepcurelogo.svg'>
        <h1>Begin New Experiment</h1>
      </div>
      <div class="top-submit">
        <button class="submit" type="button" v-on:click="onSubmit">
          Submit
        </button></div>

      <!-- Start of left column in top flags section on main page.
           v-if is used to delay rendering this box until the values were
           computed. This prevents a browser console vale undefined error. -->
      <div class="left" v-if="topFlags.name">
        <div v-bind:class="{ inperror: blank(topFlags['name']) && submitted }">
          <b>{{topFlags['name'].display_name}}:</b>
          <span v-if="blank(topFlags['name']) && submitted" class="error-message"> Required </span><br />
          <input
            class = "path"
            type="text"
            v-model="topFlags['name'].value"
            placeholder="3rd cephalosporins"
          />
        </div>
        <div v-bind:class="{ inperror: blank(topFlags['data_df']) && submitted || !validDataPath && submitted}">
          {{topFlags['data_df'].display_name}}:
          <span v-if="blank(topFlags['data_df']) && submitted" class="error-message"> Required </span>
          <span v-else-if="!validDataPath && submitted" class="error-message"> Invalid Path </span><br />
          <input
            class="path"
            type="text"
            v-model="topFlags['data_df'].value"
            placeholder="C:/MoleculeSet"
          />
        </div>
        <div v-bind:class="{ inperror: blank(topFlags['answer_column']) && submitted}">
          {{topFlags['answer_column'].display_name}}:
          <span v-if="blank(topFlags['answer_column']) && submitted" class="error-message"> Required </span><br />
          <input
            class="path"
            type="text"
            v-model="topFlags['answer_column'].value"
            placeholder="delta_g"
          />
        </div>
      </div>

      <!-- Start of middle columns in top flags section on main page -->
      <div class="middle" v-if="topFlags['worker_class']">
        {{topFlags['worker_class'].display_name}}:<br />
        <select v-model="topFlags['worker_class'].value">
          <option v-for="option in topFlags['worker_class'].options">
            {{ option }}
          </option>
        </select>
        {{topFlags['split_type'].display_name}}:<br />
        <select v-model="update_split">
          <option v-for="option in topFlags['split_type'].options">
            {{ option }}
          </option>
        </select>
        <br />
        <!-- This next input is split_file, split_k, or split_test_size -->
        {{topFlags[split_var].display_name}}:
        <span v-if="blank(topFlags[split_var]) && submitted" class="error-message"> Required </span>
        <!-- validSplitFilePath is always true when split type is not user -->
        <span v-else-if="!validSplitFilePath && submitted" class="error-message"> Invalid Path </span>
        <br />
        <!-- v-model.number preserves number values when appropriate.
             ***HOWEVER***, if 'user' is selected as the Split Type, this turns into
             a text box. If the user enters a number into this, it'll stick as a number
             until the user deletes everything and re-enters characters. -->
        <div v-bind:class="{ inperror: blank(topFlags[split_var]) && submitted || !validSplitFilePath && submitted}">
          <input
            :type="split_var_type"
            v-model.number="topFlags[split_var].value"
            placeholder="C:/Path/Split"
          />
        </div>
      </div>

      <!-- Start of right column in top flags section on main page -->
      <div class="right" v-if="topFlags['problem_type']">
        {{topFlags['problem_type'].display_name}}:
        <select v-model="topFlags['problem_type'].value">
          <option v-for="option in topFlags['problem_type'].options">
            {{ option }}
          </option>
        </select>
        {{topFlags['model_type'].display_name}}:
        <select v-model="topFlags['model_type'].value">
          <option v-for="option in topFlags['model_type'].options">
            {{ option }}
          </option>
        </select>

        <!-- Upload buttons -->
        <span class="up">
        <span>Flag File:<span style="margin-left: 3px; font-size:.7rem; color: #757575;">optional</span></span>
        <div class="upload-wrapper">
          <input type="file" @change="handleFlagFileSelect" accept=".json">
          <button tabindex="-10" class="button blue-btn" type="button">Upload</button>
        </div>
      </span>
        <span class="up">
        <span>Model Configurations:<span style="margin-left: 3px; font-size:.7rem; color: #757575;">optional</span></span>
         <div class="upload-wrapper">
           <input type="file" @change="handleConfigFileSelect" accept=".json">
          <button tabindex="-10" class="button blue-btn" type="button">Upload</button>
        </div>
      </span>
      </div>

      <div class="bottom" v-if="modelOptions">
        <!-- Model configurations section -->
        <div>
          <dropdown @click="toggleModels"> Models
            <!-- If section is collapsed and no models are selected, show error message -->
            <span v-if="!checked_model_count" class="error-message">
            Select at least one model
          </span>
            <!-- If section is collapsed and there are errors, show error count -->
            <span v-else-if="models_error_count && !showModels" class="error-message">
            Errors: {{ models_error_count }}
          </span>
          </dropdown>
          <transition name="slide-fade">
            <table v-show="showModels">
              <tr v-for="(model_value, model_name) in all_models">
                <!-- .sync works in place of (and sometimes with. See Parameter.vue)
                 v-model and is designed for parent/child updates.

                 Add .sync after the variable being passed as a prop. The child
                 emits directly, so, for selected, the child has a 'selected' prop
                 and <input
                        :value="selected"
                        @input="$emit('update:selected', $event.target.checked)">-->
                <Model
                  v-show="current_models.hasOwnProperty(model_name)"
                  :model_params.sync="model_value.parameters"
                  :display_name="model_value.display_name"
                  :model_name="model_name"
                  :selected.sync="model_value.selected"
                  :error_count.sync="model_value.error_count"
                  class="content"
                ></Model>
              </tr>
            </table>
          </transition>
        </div>


        <!-- Platform flags section-->
        <div>
          <dropdown @click="togglePlatformFlags"> Platform Flags
            <!-- If section is collapsed and there are errors, show error count -->
            <span v-if="platform_flags_error_count && !showPlatformFlags" class="error-message">
            Errors: {{ platform_flags_error_count }}
          </span>
          </dropdown>
          <transition name="slide-fade">
            <table v-show="showPlatformFlags">
              <!-- This whole loop creates the cloud_service flag. The browser
              console was throwing an error if the flag was created directly using
              platformFlags['cloud_service']. -->
              <tr v-for="(flag_value, flag_name) in platformFlags" v-if="flag_name === 'cloud_service'">
                <!-- the v-on listens for an event from Flag.vue.
                  The flag_value/name are passed in as through props. -->
                <Flag
                  v-on:childToParent="updatePlatformFlag"
                  :flag_value="flag_value.value"
                  :display_name="flag_value.display_name"
                  :flag_min="flag_value.min"
                  :flag_max="flag_value.max"
                  :flag_name="flag_name"
                  :options="flag_value.options"
                  class="content"
                >
                </Flag>
              </tr>
              <!-- We don't create a flag object if the flag_name is cloud_service.
                   That flag is created right above this. -->
              <tr v-for="(flag_value, flag_name) in platformFlags" v-if="flag_name !== 'cloud_service'">
                <!-- the v-on listens for an event from Flag.vue.
                  The flag_value/name are passed in as through props. -->
                <Flag
                  v-on:childToParent="updatePlatformFlag"
                  :flag_value="flag_value.value"
                  :display_name="flag_value.display_name"
                  :flag_name="flag_name"
                  :flag_min="flag_value.min"
                  :flag_max="flag_value.max"
                  :options="flag_value.options"
                  class="content"
                >
                </Flag>
              </tr>
            </table>
          </transition>
          <notifications position="bottom left" group="notif" :max="1" />
        </div>


        <!-- Section for Search Space Size and Resources Flags -->
        <div>
          <dropdown @click="toggleResourceFlags"> Search Space Resources
            <!-- If section is collapsed and there are errors, show error count -->
            <span v-if="resource_flags_error_count && !showResourceFlags" class="error-message">
            Errors: {{ resource_flags_error_count }}
          </span>
          </dropdown>
          <transition name="slide-fade">
            <table v-show="showResourceFlags">
              <tr v-for="(flag_value, flag_name) in resourceFlags">
                <!-- the v-on listens for an event from Flag.vue.
                  The flag_value/name are passed in as through props. -->
                <Flag
                  v-on:childToParent="updateResourceFlag"
                  :flag_value="flag_value.value"
                  :display_name="flag_value.display_name"
                  :flag_name="flag_name"
                  :flag_min="flag_value.min"
                  :flag_max="flag_value.max"
                  :options="flag_value.options"
                  class="content"
                >
                </Flag>
              </tr>
            </table>
          </transition>
        </div>


        <!-- Section for Problem Space Parameter Flags -->
        <div>
          <dropdown @click="toggleProblemSpaceFlags"> Problem Space Parameters
            <!-- If section is collapsed and there are errors, show error count -->
            <span v-if="problem_space_flags_error_count && !showProblemSpaceFlags" class="error-message">
            Errors: {{ problem_space_flags_error_count }}
          </span>
          </dropdown>
          <transition name="slide-fade">
            <table               v-show="showProblemSpaceFlags">
              <tr v-for="(flag_value, flag_name) in problemSpaceFlags">
                <!-- the v-on listens for an event from Flag.vue.
                  The flag_value/name are passed in as through props. -->
                <Flag
                  v-on:childToParent="updateProblemSpaceFlag"
                  :flag_value="flag_value.value"
                  :display_name="flag_value.display_name"
                  :flag_name="flag_name"
                  :flag_min="flag_value.min"
                  :flag_max="flag_value.max"
                  :options="flag_value.options"
                  class="content"
                >
                </Flag>
              </tr>
            </table></transition></div>
        <transition name="slide-fade">
          <button  v-show="showModels || showPlatformFlags || showProblemSpaceFlags || showResourceFlags" class="submit bottom-submit" type="button" v-on:click="onSubmit">
            Submit
          </button>
        </transition>
        <div style="content:''; margin-bottom:100px;" v-show="showModels || showPlatformFlags || showProblemSpaceFlags || showResourceFlags"></div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import Model from './Model.vue';
  import router from '../router';
  import { EventBus } from '../event-bus.js';
  import dropdown from './dropdown.vue';
  import Flag from './Flag';
  import Confirm from './Confirm.vue';

  export default {
    data() {
      return {
        showMain: true,
        showConfirm: false,
        showModels: false,
        showPlatformFlags: false,
        showProblemSpaceFlags: false,
        showResourceFlags: false,
        topFlags: {},
        platformFlags: {},
        problemSpaceFlags: {},
        resourceFlags: {},
        modelOptions: {},
        submitted: false,
        validDataPath: true,
        validSplitFilePath: true,
        uploadJsonObj: {},
        FAIL: "failed",
        SUCCESS: "success",
      };
    },
    watch: {
      // As soon as user starts changing the file path, make sure path is set to valid
      // This clears the "Invalid path" error message after user has submitted an invalid path
      'topFlags.data_df.value': function() {
        this.validDataPath = true;
      },
      'topFlags.split_file.value': function() {
        this.validSplitFilePath = true;
      },
    },
    methods: {

      // Handles flag file as input json and emits an object
      // containing the parsed json, if it was able to be parsed,
      // along with an error, if one was caught
      handleFlagFileSelect(event) {
        // get the user selected files object.
        let files = event.target.files;

        // then get the single file object, located at index 0
        let file = files[0];

        let reader = new FileReader();

        // this onload function is an Immediately-invoked Function Expression.
        // event2 is generated by the call to reader.readAsText(file) below
        reader.onload = (function() {
          return function(event2) {
            try {

              this.uploadJsonObj = JSON.parse(event2.target.result);
              // package the parsed json and error into an object to be emitted.
              // error is null because no error was caught
              let return_obj = [this.uploadJsonObj, null];
              //pass the packaged object
              EventBus.$emit('pass-flags-package-to-mounted', return_obj);

            } catch(error) {

              console.log(error);
              // the json object is null because we did not successfully
              // parse the json
              let return_obj = [null, error];
              //pass the packaged object
              EventBus.$emit('pass-flags-package-to-mounted', return_obj);
            }
          };
        })();

        // from docs: The readAsText() method is used to read the contents of
        // the specified file. When the read operation is complete, the
        // readyState is changed to DONE, the loadend event is triggered, and
        // the 'result' attribute contains the contents of the file as a text
        // string.
        // This is required to trigger the onload function above.
        reader.readAsText(file);
      },

      // Handles config file as input json and emits an object containing the
      // parsed json, if it was able to be parsed, along with an error, if one
      // was caught.
      // **** See handleFlagFileSelect for detailed code comments. ****
      handleConfigFileSelect(event) {
        let files = event.target.files;
        let file = files[0]; //file contents at index 0
        let reader = new FileReader();
        reader.onload = (function() {
          return function(event2) {
            try {
              this.uploadJsonObj = JSON.parse(event2.target.result);
              let return_obj = [this.uploadJsonObj, null];
              EventBus.$emit('pass-configs-package-to-mounted', return_obj);
            } catch(error) {
              console.log(error);
              let return_obj = [null, error];
              EventBus.$emit('pass-configs-package-to-mounted', return_obj);
            }
          };
        })();
        reader.readAsText(file);
      },

      handleFlagFileUpload(flagFileContents) {
        // Append file and objects that will be updated if file is valid
        let formData = new FormData();
        formData.append('file', JSON.stringify(flagFileContents));
        formData.append('topFlags', JSON.stringify(this.topFlags));
        formData.append('platformFlags', JSON.stringify(this.platformFlags));
        formData.append('resourceFlags', JSON.stringify(this.resourceFlags));
        formData.append('problemSpaceFlags', JSON.stringify(this.problemSpaceFlags));

        // Send file and objects to backend. Get back updated objects or error
        const path = 'http://localhost:5000/uploadFlags';
        axios.post(
          path,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        ).then((response) => {
          if (response.data.status === this.SUCCESS){
            // if backend status was successful, get the updated flags options
            // and activate a success notification with whatever message came
            // from the backend
            this.topFlags = response.data.topFlags;
            this.platformFlags = response.data.platformFlags;
            this.resourceFlags = response.data.resourceFlags;
            this.problemSpaceFlags = response.data.problemSpaceFlags;
            this.activate_notification(this.SUCCESS, response.data.message);
          } else {
            // if backend status was not successful, activate a failed
            // notification with whatever message came from the backend
            this.activate_notification(this.FAIL, response.data.message);
          }
        })
          .catch((error) => {
            console.log(error);
            this.activate_notification(this.FAIL, error);
          });
      },

      handleConfigFileUpload(configFileContents) {
        // Append file and objects that will be updated if file is valid
        let formData = new FormData();
        formData.append('file', JSON.stringify(configFileContents));
        formData.append('configs', JSON.stringify(this.modelOptions));

        // Send file and objects to backend. Get back updated objects or error
        const path = 'http://localhost:5000/uploadConfigs';
        axios.post(
          path,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        ).then((response) => {
          if (response.data.status === this.SUCCESS){
            // if backend status was successful, get the updated model options
            // and activate a success notification with whatever message came
            // from the backend
            this.modelOptions = response.data.configs;
            this.activate_notification(this.SUCCESS, response.data.message);
          } else {
            // if backend status was not successful, activate a failed
            // notification with whatever message came from the backend
            this.activate_notification(this.FAIL, response.data.message);
          }

        })
          .catch((error) => {
            console.log(error);
            this.activate_notification(this.FAIL, error);
          });
      },

      updatePlatformFlag: function(key, value, err) {
        // Method uses $set so that the flag value is reactive to changes.
        // format: $set(property, sub property, new value)
        this.$set(this.platformFlags[key], "value", value);
        this.$set(this.platformFlags[key], "error_count", err);
      },

      updateResourceFlag: function(key, value, err) {
        this.$set(this.resourceFlags[key], "value", value);
        this.$set(this.resourceFlags[key], "error_count", err);
      },

      updateProblemSpaceFlag: function(key, value, err) {
        this.$set(this.problemSpaceFlags[key], "value", value);
        this.$set(this.problemSpaceFlags[key], "error_count", err);
      },

      toggleModels: function() {
        this.showModels = !this.showModels;
      },

      togglePlatformFlags: function() {
        this.showPlatformFlags = !this.showPlatformFlags;
      },

      toggleResourceFlags: function() {
        this.showResourceFlags = !this.showResourceFlags;
      },

      toggleProblemSpaceFlags: function() {
        this.showProblemSpaceFlags = !this.showProblemSpaceFlags;
      },

      // Create output flagfile to display on confirmation page. This does not
      // save to database.
      // Called when user presses button to view confirmation page
      createFlagfile: function() {
        // Combine all flags into a single object
        let obj = {
          setup: this.topFlags,
          flags: Object.assign({}, this.platformFlags, this.resourceFlags, this.problemSpaceFlags)
        }
        const path = 'http://localhost:5000/saveFlags';
        return axios.post(path, obj)
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error);
            this.activate_notification(this.FAIL, error);
          });
      },

      // Create output config file to display on confirmation page. This does
      // not save to database.
      // Called when user presses button to view confirmation page
      createConfigFile: function() {
        const path = 'http://localhost:5000/saveConfigs';
        return axios.post(path, this.checked_models)
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error);
            this.activate_notification(this.FAIL, error);
          });
      },

      // Called when user presses submit button
      async onSubmit () {
        this.submitted = true;
        if (await this.validForm()) {
          // Write flags to json and write model configurations to json
          await Promise.all([this.createFlagfile(), this.createConfigFile()])
          // Switch to confirmation page
          this.showMain = false;
          this.showConfirm = true;
          // Set submitted to false so top flag error message don't display immediately if user clears a value
          this.submitted = false;
        }
      },

      // Show pop-up notification
      activate_notification: function(status, message) {
        let status_display =  "STATUS: " + status;
        let message_display = "MESSAGE: " + message;

        if (status === this.FAIL) {
          this.notification(status_display, message_display, 'error');
        } else if (status === this.SUCCESS) {
          this.notification(status_display, message_display, 'success');
        } else {
          this.notification(status_display, message_display, null)
        }
      },

      notification: function(status, message, notif_type) {
        setTimeout( () =>
          this.$notify({
            group: 'notif',
            title: status,
            text: message,
            type: notif_type,
            duration: 2000,
            speed: 700,
          }), 500);
      },

      // Get platform flags from backend
      // In the future, update this method to iterate over list of flag names
      // and populate with values from AWS Object
      getDefaultPlatformFlags() {
        const path = 'http://localhost:5000/defaultPlatformFlags';
        axios.get(path)
          .then((response) => {
            this.platformFlags = response.data;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
            this.activate_notification(this.FAIL, error);
          });
      },

      // Get all other flags besides platform flags
      getDefaultFlags() {
        const path = 'http://localhost:5000/defaultFlags';
        axios.get(path)
          .then((response) => {

            // Get all flags
            let flags = response.data;

            // Filter for top flags
            this.topFlags = flags['top'];

            // Filter for search space size and resource flags
            this.resourceFlags = flags['resources'];

            // Filter for problem space parameter flags
            this.problemSpaceFlags = flags['problem_space'];
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },

      // Get model options from backend
      getDefaultModelOptions() {
        const path = 'http://localhost:5000/defaultModels';
        axios.get(path)
          .then((response) => {
            this.modelOptions = response.data;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },

      // Check if field is invalid (only checks if empty right now)
      // Update error count as needed
      blank: function(flag){
        if (!flag['value']){
          flag['error_count'] = 1;
          return true;
        }
        else {
          flag['error_count'] = 0;
          return false;
        }
      },

      // Check if file path is valid
      validatePath: function(filepath){
        const path = 'http://localhost:5000/validatePath';
        return axios.post(path, filepath)
          .then((response) => {
            return response.data.status === this.SUCCESS;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error);
            this.activate_notification(this.FAIL, error);
          });
      },

      // Check if there are any errors (does not include filepath errors)
      // Returns true if error count is 0 and there is at least one selected model
      noErrors: function(){
        return !this.top_flags_error_count
          && !this.platform_flags_error_count
          && !this.problem_space_flags_error_count
          && !this.resource_flags_error_count
          && !this.models_error_count
          && this.checked_model_count;
      },

      // Check if form is valid by making sure file paths are valid and there
      // are 0 other errors
      async validForm (){
        try {
          this.validDataPath = await this.validatePath(this.topFlags['data_df']['value']);
          if (this.topFlags['split_type']['value'] === "user") {
            this.validSplitFilePath = await this.validatePath(this.topFlags['split_file']['value']);
          } else {
            // Split type is not user. Set to true so this value has no impact on validation
            this.validSplitFilePath = true;
          }
          return this.validDataPath && this.validSplitFilePath && this.noErrors();
        } catch (err) {
          // eslint-disable-next-line
          console.log(error);
          this.activate_notification(this.FAIL, error);
        }
      },
    },
    computed: {
      // Models that the user has selected by checking them
      checked_models() {
        let onlyCheckedModels = {};
        // Check if create() hook has populated modelOptions and topFlags
        if(this.modelOptions['classical'] && this.topFlags['problem_type']) {
          // turn current_models into an array, then forEach over the array.
          // each element of the array is a key value pair. Example;
          // ['knn_reg', {'display_name': ... }]
          // so model[0] is the model name. model[1] is the object representing
          // that model.
          Object.entries(this.current_models).forEach(function (model) {
            // If the model is checked
            if (model[1].selected) {
              // add it to what will be returned, using the object property
              // assignment notation.
              onlyCheckedModels[model[0]] = model[1];
            }
          });
          return onlyCheckedModels;
        }
      },
      checked_model_count(){
        if(this.modelOptions['classical'] && this.topFlags['problem_type']){
          return Object.keys(this.checked_models).length;
        }
        // Error message will display if at least one model isn't selected
        // Return 1 to avoid displaying error message before created() has finished populating values
        return 1;
      },
      all_models() {
        if(this.modelOptions['classical'] && this.topFlags['problem_type']) {
          return Object.assign({},
            this.modelOptions['classical']['classification'],
            this.modelOptions['classical']['regression'],
            this.modelOptions['neural_networks']['classification'],
            this.modelOptions['neural_networks']['regression']);
        }
      },
      // This computed value returns the models relating to the current
      // problem type and model type selections.
      current_models() {
        // This if checks to see that the modelOptions and topFlags objects
        // have been set up by the created() hook. Without this, there is a
        // browser console error when the return statement tries to grab the
        // value. As soon as the created() hook fills in the
        // modelOptions and topFlags objects, it triggers this computed value
        // to be recalculated. Putting the if there just causes
        // the calculation to skip until the required objects are set up
        if(this.modelOptions['classical'] && this.topFlags['problem_type']){
          // console.log(this.modelOptions[this.topFlags['model_type'].value][this.topFlags['problem_type'].value]);
          return this.modelOptions[this.topFlags['model_type'].value][this.topFlags['problem_type'].value];
        }
      },
      // Count the number of errors in each section
      top_flags_error_count(){
        let count = 0;
        let flags = this.topFlags;
        Object.keys(flags).forEach(function (flag) {
          count += flags[flag].error_count;
        });
        return count;
      },
      platform_flags_error_count(){
        let count = 0;
        let flags = this.platformFlags;
        Object.keys(flags).forEach(function (flag) {
          count += flags[flag].error_count;
        });
        return count;
      },
      resource_flags_error_count(){
        let count = 0;
        let flags = this.resourceFlags;
        Object.keys(flags).forEach(function (flag) {
          count += flags[flag].error_count;
        });
        return count;
      },
      problem_space_flags_error_count(){
        let count = 0;
        let flags = this.problemSpaceFlags;
        Object.keys(flags).forEach(function (flag) {
          count += flags[flag].error_count;
        });
        return count;
      },
      models_error_count(){
        let count = 0;
        if(this.modelOptions['classical'] && this.topFlags['problem_type']) {
          let models = this.checked_models;
          Object.keys(models).forEach(function (model) {
            count += models[model].error_count;
          });
        }
        return count;
      },
      // This computed value holds a string that corresponds to the flag key
      // that depends on the split_type. It's used up in lines 25-47 when
      // creating the <input ...> for the flag it represents.
      split_var() {
        if(this.topFlags['split_type']) {
          let split = this.topFlags['split_type'].value;
          if(split === 'user'){
            return 'split_file';
          } else if(split === 'k-fold'){
            return 'split_k';
          } else if(split === 'train-test'){
            return 'split_test_size';
          } else {
            return 'bad_split_type';
          }
        }
      },
      // similar to split_var, this holds a string representing the data type
      // of the flag represented by split_var.
      split_var_type() {
        if(this.topFlags['split_type']) {
          let split = this.topFlags['split_type'].value;
          if(split === 'user'){
            return 'text';
          } else if(split === 'k-fold'){
            return 'number';
          } else if(split === 'train-test'){
            return 'number';
          } else {
            return 'bad_split_type';
          }
        }
      },
      // this computed function is triggered when the user changes split_type
      update_split: {
        get() {
          return this.topFlags['split_type'].value;
        },
        set(val) {
          this.$set(this.topFlags['split_type'], 'value', val);
          let newFlag = {};
          this.$delete(this.topFlags, 'split_file');
          this.$delete(this.topFlags, 'split_k');
          this.$delete(this.topFlags, 'split_test_size');
          if(val === 'user'){
            newFlag.display_name = "Path to Split File";
            newFlag.value = "";
          } else if(val === 'k-fold'){
            newFlag.display_name = "k";
          } else if(val === 'train-test'){
            newFlag.display_name = "Test Size";
          } else {
            newFlag.display_name = "bad_split_type";
            newFlag.value = "bad_split_type";
          }
          newFlag.options = "";
          if(val === 'k-fold' || val === 'train-test') {
            newFlag.value = 1;
            newFlag.min = 0;
            newFlag.max = 1000;
          }
          newFlag.error_count = 0;
          this.$set(this.topFlags, this.split_var, newFlag);
        }
      }
    },
    components: {  Model, Flag, dropdown, Confirm },
    created() {
      this.getDefaultFlags();
      this.getDefaultPlatformFlags();
      this.getDefaultModelOptions();
    },
    mounted() {

      // If go-back is clicked then toggle correct data
      EventBus.$on('go-back', value => {
        this.showMain = true;
        this.showConfirm = false;
        this.submitted = false;
      });

      // waits for submission click on the confirm page and
      // extracts status and message from /submitRun
      EventBus.$on('submit-got-clicked', update  => {
        let status = update[0]; // first arg is status
        let message = update[1]; // second arg is message
        this.showMain = true;
        this.showConfirm = false;
        // activate notification using status and message
        this.activate_notification(status, message);
      });

      // waits for user selected flag file to be read. This is the step
      // between the file being read in and the file being processed in backend
      EventBus.$on('pass-flags-package-to-mounted', value => {

        let json_obj = value[0]; // the actual file content
        let err = value[1];      // the front end error, if one exists

        // if an error came from front end, activate a notification as failed
        // and show the front end error. else, do the handling in the backend,
        // where other errors can be generated as the file contents are analyzed
        if (err != null) {
          this.activate_notification(this.FAIL, err);
        } else {
          this.handleFlagFileUpload(json_obj);
        }
      });

      // waits for user selected config file to be read.
      EventBus.$on('pass-configs-package-to-mounted', value => {

        let json_obj = value[0]; //the actual file content
        let err = value[1];      //the front end error, if one exists

        if (err != null) {
          this.activate_notification(this.FAIL, err);
        } else {
          this.handleConfigFileUpload(json_obj);
        }
      });
    },
  };
</script>

<style>
  h1 {
    /*Main Header*/
    align-self: center;
    color: #000;
    font-size: 1.5rem;
  }
  .main-container {
    /*Container that holds main UI*/
    margin-left: 8%;
    margin-right: 8%;
    display: grid;
    grid-template-columns: repeat(3, 2fr);
    grid-template-rows: repeat(auto-fill, minmax(100px, 1fr));
    grid-gap: 1em;
  }
  .logo{
    margin-right:5px;
    width: 20px;
    height:20px;
  }
  .header {
    /*GRID styling for Main header*/
    width: 100%;
    margin-bottom: 15px;
    grid-column: 1 / span 2;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    white-space: nowrap;
  }
  .left > *,
  .middle > *,
  .right > * {
    /*Adds spacing for everything in the top three columns*/
    margin-bottom: var(--spacing);
    white-space: nowrap;
  }
  /*CSS GRID LOCATIONS*/
  .left {
    grid-column: 1 / span 3;
    text-align: left;
  }
  .bottom-submit{
    height: 2.5rem;
  }
  .middle {
    grid-column: 1 / span 3;
    text-align: left;
  }
  .right {
    text-align: left;
    grid-column: 1 / span 3;
  }
  .bottom {
    margin-top: 10px;
    grid-column: 1 / span 3;
    display: flex;
    flex-direction: column;
  }
  /*END OF CSS GRID LOCATIONS*/
  .content{
    /*Inside of the acordian dropdowns*/
    padding: 3px;
  }
  .bottom > * {
    /*Adds 10px to the bottom of each dropdown*/
    margin-bottom: 20px;
  }
  .top-submit {
    grid-column: 3;
    align-self: center;
    display: flex;
    justify-content: flex-end;
  }
  .submit{
    outline: none;
    background: #26a958;
    border: 1px solid #168f48;
    color: #fff;
  }
  .submit:focus {
    /*When you tab or right click the submit button*/
    box-shadow: 0 0 0 3px rgba(38, 169, 88, 0.562);
  }
  .up {
    /*syling for the Upload section*/
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .blue-btn {
    /*Styles buttons into the blue design*/
    background-color: #267ace;
    border: 1px solid #216bb3;
    color: #ffff;
  }
  .blue-btn:focus {
    /*When you tab or right click the submit button*/
    box-shadow: 0 0 0 3px rgba(38, 122, 206, 0.486);
  }
  .error-message {
    color: #B22222;
    font-size: .7rem;
  }
  .inperror > input{
    border: 1px solid #B22222;
  }
  /* Each breakpoint means add/change this style when we hit the one pass the
   * min-width given
   */
  @media only screen and (min-width: 720px) {
    h1 {font-size: 3rem;}
    .left {
      grid-column: 1;
      padding: 0 3px 0 3px;
      text-align: left;
      background-color: #00000001;
    }
    .middle {
      border-left: 3px solid #e6e5e5;
      border-right: 3px solid #e5e5e5;
      padding: 0 20px 0 20px;
      text-align: left;
      grid-column: 2;
    }
    .right {
      grid-column: 3;
      padding: 0 3px 0 3px;
      text-align: left;
    }
    .up {
      flex-direction: row;
      justify-content: space-between;
    }
    .bottom {
      grid-column: 1 / span 3;
    }
    .logo{
      margin-right:5px;
      width: 50px;
      height:50px;
    }
  }
  @media only screen and (min-width: 920px) {
    td {
      display: table-cell;
    }
    .main-container{
      grid-template-rows: repeat(auto-fill, minmax(100px, 1fr));}
    .slide-fade-enter-active {
      /* Anything this size and above will have the animation */
      transition: all 0.1s ease;
    }
    .slide-fade-leave-active {
      transition: all 0.05s cubic-bezier(1, 0.5, 0.8, 1);
    }
    .slide-fade-enter,
    .slide-fade-leave-to {
      transform: translateY(10px);
      opacity: 0;
    }
  }
  @media only screen and (min-width: 960px) {
    button {
      width: 80px;
    }
  }

  @media only screen and (min-width: 1280px) {
    button {
      width: 90px;
    }
    h1 {
      font-size: 4rem;
    }
  }
</style>
