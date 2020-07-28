<!-- Component for an individual parameter. Component determines what kind of inputs it
     should have based on the type of parameter. Tracks its own value changes and passes
     new values up to its parent on input -->
<template>
    <div>
      <!-- Render select box if categorical parameter -->
      <div class="cards" v-if="param_value.type === 'Categorical'">
        <div v-if="param_value.display_name"><b>{{param_value.display_name}}:</b></div>
        <div v-else><b>{{param_name}}:</b></div>
          <select v-model="emitSelection" multiple v-bind:class="{ inperror: errors.select}">
            <option v-for="option in param_value.sequence" :value="option">
              {{option}}
            </option>
          </select>

          <div v-if="errors.select" class="error-message"> {{ errors.select }} </div>
        <label>Type: {{param_value.type}}</label>
      </div>

      <!-- Otherwise, render lower, upper, and other fields for ints and float parameters -->
      <div class="cards" style="display: flex; flex-direction: column;" v-else>
          <div v-if="param_value.display_name"><b>{{param_value.display_name}}:</b></div>
          <div v-else><b>{{param_name}}:</b></div>
          <label>{{param_value.distribution === 'normal' ? "Mean" : "Lower"}}</label>
          <input
            type="number"
            :step="param_value.type === 'Int' ? 1 : 0.01"
            :value="lower"
            v-bind:class="{ inperror: errors.lower}"
            @input="updateLower(param_value, $event)">
          <span v-if="errors.lower" class="error-message"> {{ errors.lower }} </span>

          <label>{{param_value.distribution === 'normal' ? "Standard Deviation" : "Upper"}}</label>
          <input
            type="number"
            :step="param_value.type === 'Int' ? 1 : 0.01"
            :value="upper"
            v-bind:class="{ inperror: errors.upper}"
            @input="updateUpper(param_value, $event)">
          <span v-if="errors.upper" class="error-message"> {{ errors.upper }} </span>

          <!-- if quantization is null, we don't display edit boxes. -->
          <label v-if="quantization !== null">Quantization</label>
          <input
            v-if="quantization !== null"
            type="number"
            :value="quantization"
            v-bind:class="{ inperror: errors.quantization}"
            @input="updateQuantization(param_value, $event)">
          <span v-if="errors.quantization" class="error-message"> {{ errors.quantization }} </span>

        <label>Distribution: {{param_value.distribution}}  Log: {{param_value.log}}  Type: {{param_value.type}}</label>

      </div>
    </div>
</template>

<script>
  export default {
    name: "Parameter",
    props: ['param_name','param_value','upper','lower','quantization','selected','error_count'],
    data() {
      return {
        selection: [],
        errors: {
          lower: '',
          upper: '',
          quantization: '',
          select: ''
        }
      };
    },
    methods: {

      updateSelected: function(param_value, $event){
        this.validateSelected(param_value, [$event.target.value]);
        this.emitSelection('update:selected', [$event.target.value]);
      },

      updateLower: function(param_value, $event){
        this.validateLower(param_value, +$event.target.value);
        this.$emit('update:lower', +$event.target.value);
      },

      updateUpper: function(param_value, $event){
        this.validateUpper(param_value, +$event.target.value);
        this.$emit('update:upper', +$event.target.value);
      },

      updateQuantization: function(param_value, $event){
        this.validateQuantization(param_value, +$event.target.value);
        this.$emit('update:quantization', +$event.target.value);
        this.$emit('update:param_errors', this.error);
      },

      // Make sure at least one option is selected
      validateSelected: function(selected){
        if (!selected.length){
          this.errors.select = 'Select at least one option';
        } else {
          this.errors.select = '';
        }
        this.updateError();
      },

      // Validate lower field and update error object
      // changed_field is necessary for removing existing errors when validateUpper is called from another validator
      validateLower: function(param_value, low, changed_field='lower'){
        if (low > param_value['lower_max']){
            this.errors.lower = 'Lower must be less than ' + param_value['lower_max'];
        }
        else if (low < param_value['lower_min']){
            this.errors.lower = 'Lower must be greater than ' + param_value['lower_min'];
        }
        else if (changed_field === 'lower' && low > param_value.upper){
            this.errors.lower = 'Lower must be less than upper';
        }
        else {
          this.errors.lower = '';
        }
        // Check if this update changes errors on other fields
        if (changed_field === 'lower'){
          this.validateUpper(param_value, param_value.upper, 'lower');
          this.validateQuantization(param_value, param_value.quantization, param_value.upper - low);
          this.updateError();
        }
      },

      // Validate upper field and update error object
      // changed_field is necessary for removing existing errors when validateUpper is called from another validator
      validateUpper: function(param_value, up, changed_field='upper'){
        if (up > param_value['upper_max']){
          this.errors.upper = 'Upper must be less than ' + param_value['upper_max'];
        }
        else if (up < param_value['upper_min']){
          this.errors.upper = 'Upper must be greater than ' + param_value['upper_min'];
        }
        else if (changed_field === 'upper' && up < param_value.lower){
          this.errors.upper = 'Upper must be greater than lower';
        }
        else {
          this.errors.upper = '';
        }
        // Check if this update changes errors on other fields
        if (changed_field === 'upper'){
          this.validateLower(param_value, param_value.lower, 'upper');
          this.validateQuantization(param_value, param_value.quantization, up - param_value.lower);
          this.updateError();
        }
      },

      // Validate quantization field and update error object
      validateQuantization: function(param_value, q, interval=param_value.upper - param_value.lower){
        if (q > interval && interval > 0){
          this.errors.quantization = 'Quantization must be less than interval between upper and lower'
        }
        else if (q > param_value['quantization_max']){
          this.errors.quantization = 'Quantization must be less than ' + param_value['quantization_max']
        }
        else if (q < param_value['quantization_min']){
          this.errors.quantization = 'Quantization must be greater than ' + param_value['quantization_min']
        }
        else {
          this.errors.quantization = '';
        }
        this.updateError();
        // No other fields are currently affected by quantization. No need to call other validators
      },
      updateError: function() {
        let count = 0;
        for(let errorType in this.errors) {
          if(this.errors[errorType]){
            count++;
          }
        }
        this.$emit('update:error_count', count);
      }

    },
    computed: {
      // This is the computed function that saves and emits the changes.
      emitSelection: {
        get() {
          return this.selection;
        },
        set(val) {
          // Save the selection to the local variable. This is so the options
          // stay selected.
          this.validateSelected(val);
          this.selection = val;
          this.$emit('update:selected', val);
        }
      }
    },
    created() {
      this.selection = this.param_value.selected;
    }
  }
</script>
<style scoped>
.cards {
  width: 220px;
  background-color:#ffffffba; 
  box-shadow: 0 0 10px #0000002f;
  padding: 10px;
}
.inperror {
  border-color: #B22222;
}
div {
  margin: 5px;
}
div > * {
  margin-right: 5px;
}
</style>
