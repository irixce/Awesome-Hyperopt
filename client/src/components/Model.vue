<!-- Component for representing an individual model. Each model contains several parameters -->
<template>
  <div class="model">
    <div class="label">
      <div id="check">
        <label>
          <input
            :value="selected"
            :checked="selected"
            type="checkbox"
            id="modelChecked"
            @input="$emit('update:selected', $event.target.checked)"
          ><img style="color: #E0E0E0" src="@/assets/checkmark.svg"/>
        </label>
      </div>
      <label v-if="display_name">{{display_name}}</label>
      <label v-else>{{model_name}}</label>
      <button id="edit" @click="toggleModelParams" > <img src="@/assets/pencil.svg"/> </button>
      <span v-if="showModelErrorCount" class="error-message"> Errors: {{ this.countedErrors }} </span>
    </div>
    <transition name="slide-fade">
      <div class="parameter" v-show="showModelParams">
        <div v-for="(param_value, param_name) in model_params">

          <Parameter :param_name="param_name"
                     :param_value="param_value"
                     :lower.sync="param_value.lower"
                     :upper.sync="param_value.upper"
                     :quantization.sync="param_value.quantization"
                     :selected.sync="param_value.selected"
                     :error_count.sync="param_value.error_count"
                     class="content"
          ></Parameter>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
  import dropdown from './dropdown.vue';
  import Parameter from './Parameter';

  export default {
    name: "Model",
    props: ['model_params','model_name', 'selected','display_name','error_count'],
    data() {
      return {
        showModelParams: false,
      };
    },
    methods: {
      toggleModelParams: function(e) {
        this.showModelParams = !this.showModelParams;
      },
    },
    computed: {
      countedErrors() {
        let count = 0;
        for(let param in this.model_params) {
          if(this.model_params[param].error_count){
            count += this.model_params[param].error_count;
          }
        }
        this.$emit('update:error_count', count);
        return count;
      },
      showModelErrorCount(){
        return this.countedErrors > 0 && !(this.showModelParams) && this.selected;
      }
    },
    components: { Parameter, dropdown },
  }
</script>
<style scoped>
  .model {
    display: flex;
    flex-direction: column;
    justify-content: left;
    text-align: left;
    align-items: flex-start;
  }
  .label{
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
  }
  .label > * {
    margin-right: 5px;
  }
  .parameter {
    text-align: left;
    margin: 5px;
    display: flex;
    justify-content: flex-start;
    flex-direction:column;
    flex-wrap: wrap;
    align-self: center;
  }
  #edit {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    width: 40px;
    height: 30px;
    border-radius: 3px;
    font-size: 14px;
    font-weight: 400;
    padding: 6px 10px;
    background-color: #fff;
    border-color: #e5e5e5;
    color: #2e2e2e;
  }
  #edit:hover {
    background-color: #73afea3d;
  }
  @media only screen and (min-width: 920px) {
    .parameter {
      flex-direction: row;
    }
  }
</style>
