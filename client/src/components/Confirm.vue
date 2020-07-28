<!-- Confirmation page -->
<template>
  <div>
    <h1>Confirm Experiment Setup</h1>
      <h3>Preview Files:</h3>
      <div class="frames">
      <div class="inside">
      <iframe
        width="500"
        height="200"
        src="http://localhost:5000/saveConfigs"
      >
      </iframe>
      Model Configurations
      </div>
      <div class="inside">
      <iframe
        width="500"
        height="200"
        src="http://localhost:5000/saveFlags"
      >
      </iframe>
      Flags & Setup
      </div>
      </div>
    <span
      style="display: flex; justify-content: center"
    >
      <button class="green" style="background-color: #fff; color: #168f48;" type="button" v-on:click="editConfig">Go Back</button>
      <button class="green" type="button" v-on:click="confirm">Confirm</button>
    </span>

  </div>
</template>

<script>
import axios from 'axios';
import { EventBus } from '../event-bus.js';

export default {
  name: 'Confirm',

  data() {
    return {
      show: false,
      configs: {},
      flags_setup: {},
    };
  },
  methods: {
    // Go back to main page without submitting experiment
    editConfig: function() {
      EventBus.$emit('go-back', 1);
    },

    // Communicates to Main that the submit button got clicked
    // Passes it a list called update which contains two elements:
    // the submitRun response status and message
    emitSubmissionToMain: function(exp_update) {
      EventBus.$emit('submit-got-clicked', exp_update);
    },

    // Submit experiment and go back to main page
    confirm: function() {
      this.submitExperiment();
    },

    // Send experiment to backend so it can be written to database and sent to scheduler
    submitExperiment: function() {
        const path = "http://localhost:5000/submitRun";

        // Combine all configurations and flags into a single object
        let experiment = Object.assign({}, {'configurations': this.configs}, this.flags_setup);

        // Send experiment to backend
        axios.post(path, experiment)
          .then((response) => {
            let status = response.data.status;
            let message = response.data.message;

            // Create list containing status and message
            // to be passed to Main
            let exp_update = [status, message];

            // Notify main that experiment was submitted
            this.emitSubmissionToMain(exp_update);
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error);
          });
      },
  },

  created() {
      // Get configs file
      let path = "http://localhost:5000/saveConfigs";
      axios.get(path)
          .then((response) => {
            this.configs = response.data;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });

      // Get flag file
      path = "http://localhost:5000/saveFlags"
      axios.get(path)
          .then((response) => {
            this.flags_setup = response.data;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
    },
};
</script>

<style scoped>
.frames{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.inside{
  margin: 20px;
  display: flex;
  justify-content: center;
  flex-direction: column;
}
iframe{
  height: 600px;
  width: 500px;
  border-radius: 3px;
  border: 1px solid #0000000f;
  box-shadow: 0 0 10px #0000002f;
}

h3 {
  color: rgb(77, 77, 77);
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}
button {
  width: 7rem;
  height: 3rem;
  font-size: 1.5rem;
}
.green {
  outline: none;
  margin: 20px;
  background: #26a958;
  border: 1px solid #168f48;
  color: #fff;
}
.green:focus {
  box-shadow: 0 0 0 3px rgba(38, 169, 88, 0.562);
}
a {
  color: #42b983;
}
@media only screen and (max-width: 500px) {
  iframe {
    width: 100%;
  }
}
@media only screen and (min-width: 961px) {
  .frames {
  flex-direction: row; 
  }
}
</style>
