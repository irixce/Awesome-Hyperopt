<!-- Individual flag component. Each flag in the list of flags in each section
     is a flag component. This component determines what type of flag it is
     and shows the appropriate options (radio, number box, etc.)
-->

<template>
  <div>

    <td v-if="display_name">{{display_name}}:</td>
    <td v-else>{{flag_name}}:</td>

    <td class="data" v-if="value_type === 'object'">
      <label>
        <!-- We're using v-bind (that's the :value="flag_value" shorthand)
         and @input -> $event -> $emit in place of v-model.
         v-model will bind the same variable, but will then try to update the
         variable, resulting in warning about mutating props.
         Using a custom @input, $event, $emit sequence allows us to let Main
         update the value of the flag, pushing the change back down to child
         instead of letting child mutate the value directly. -->
        <select
          :value="flag_value"
          :id="flag_name"
          v-bind:class="{inperror: error}"
          @input="updateSelect($event.target.value)"
        >
          <option v-for="option in options" :value="option">
            {{option}}
          </option>
        </select>
        <div v-if="error" class="error-message"> {{ error }} </div>
      </label>
    </td>

    <td v-else-if="value_type === 'number'">
      <label>
        <input
          type="number"
          v-bind:class="{inperror: error}"
          :value="flag_value"
          @input="updateNumber(+$event.target.value)"
        >
        <div v-if="error" class="error-message"> {{ error }} </div>
      </label>
    </td>

    <td v-else-if="value_type === 'boolean'">
      <input
        :value="flag_value"
        :checked="flag_value"
        v-bind:class="{inperror: error}"
        type="radio"
        id="true"
        @input="updateRadio(Boolean($event.target.checked))"
      >
      <label for="true">True</label>
      <!-- Notice the NOT (!) indicators on this button -->
      <input
        :value="flag_value"
        :checked="!flag_value"
        v-bind:class="{inperror: error}"
        type="radio"
        id="false"
        @input="updateRadio(!Boolean($event.target.checked))"
      >
      <label for="false">False</label>
    </td>

    <td v-else-if="value_type === 'string'">
      <label>
        <input
          :value="flag_value"
          v-bind:class="{inperror: error}"
          type="text"
          @input="updateText($event.target.value)"
        >
        <div v-if="error" class="error-message"> {{ error }} </div>
      </label>
    </td>

  </div>
</template>

<script>
  import Vue from 'vue'

  export default {
    options: '',
    name: "Flag",
    props: ['flag_name','flag_value','options','display_name', 'flag_min', 'flag_max'],
    data() {
      return {
        error: '',
        error_count: 0
      }
    },
    methods: {

      // Validate and then update parent with the new flag value
      updateSelect: function(e){
        // Don't need to validate. Always has a selected value
        this.emitToParent(e)
      },
      updateNumber: function(e){
        this.validateNumber(e)
        this.emitToParent(e)
      },
      updateRadio: function(e){
        // Don't need to validate. Always has a selected value
        this.emitToParent(e)
      },
      updateText: function(e){
        this.validateText(e)
        this.emitToParent(e)
      },

      // 'childToParent' is what main listens for to update flag values.
      emitToParent (new_flag_value) {
        this.$emit('childToParent', this.flag_name, new_flag_value, this.error_count)
      },

      // Validators
      validateText: function(new_flag_value){
        if (!new_flag_value.length){
          this.error = 'Required'
          this.error_count = 1
        }
        else {
          this.error = ''
          this.error_count = 0
        }
      },
      validateNumber: function(new_flag_value){
        if (new_flag_value < this.flag_min || new_flag_value > this.flag_max){
          this.error = 'Must be between ' + this.flag_min + ' and ' + this.flag_max
          this.error_count = 1
        }
        else {
          this.error = ''
          this.error_count = 0
        }
      }
    },

    computed: {
      value_type: function() {
        if(this.options !== "") {
          return 'object'
        } else {
          return typeof this.flag_value
        }
      },
    },
  }
</script>
<style scoped>
  .inperror {
    border-color: #B22222;
  }
</style>
