<!-- Custom dropdown used when expanding model configurations and flags sections -->
<template>
  <div id='dropcontainer'>
    <button v-on:click="show = !show" @click="callback($event)" type='button' id='dropdown'>
      <slot>Button</slot>
      <img v-if="this.show === false" id='dropdownarrow' src='../assets/DropdownArrow.svg'/>
      <img v-else id='dropdownarrow' src='../assets/DropupArrow.svg'/>
    </button >
  </div>
</template>

<style scoped>
  #dropdown {
    margin: 0;
    display: flex;
    border-radius: 0;
    align-items: baseline;
    align-self: center;
    justify-content: space-between;
    width: 100%;
    padding: 8px;
  }
  #dropdownarrow {
    padding-bottom: 2px;
  }
  #dropdown > span {
    position:absolute;
    align-self: center;
    right: 0;
    left: 0;
  }
</style>

<script>
  export default {
    name: "dropdown",
    data() {
      return {
        show: false,
      };
    },
    methods: {
      callback: function(e) {
        this.$emit('click', e);
      },
    },
  }
</script>
