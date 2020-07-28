<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
:root {
  /*Global Variables*/
  --spacing: 20px;
}
#app {
  /*Main Container of Application*/
  margin-top: var(--spacing);
}
html {
  box-sizing: border-box;
  overflow-y: scroll;
}
*,
*:before,
*:after {
  box-sizing: inherit;
}
body {
  /*Main Text content styling*/
  margin: 0px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    Oxygen-Sans, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif,
    'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
  font-size: 1rem; /*1rem == 16px*/
  font-weight: 500;
  line-height: 2rem;
  outline: none;
  color: #212529;
  text-align: center;
  background-color: #fff;
}
button:focus {
  border-color: #73afea;
  box-shadow: 0 0 4px rgba(115, 175, 234, 0.4);
}
select {
  -moz-appearance: none;
  -webkit-appearance: none;
  appearance: none;
  background: url('./assets/DropdownArrow.svg') no-repeat right 8px center
    #ffffff;
  padding-left: 10px;
  height: 2rem;
  width: 100%;
  outline: none;
  border-radius: 0px;
  border: 1px solid #e5e5e5;
  border-color: rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
  font-size: 1rem;
}
select[multiple]{
  height: 100%;
  border-radius: 4px;
  padding: 0px;
  background: #ffffff;
}
select[multiple]:hover {
  color: 0;
  background: 0;
}
option {
  padding: 5px;
  border-bottom: 1px solid #216bb3;
}
option:checked {
    color: white;
    -webkit-text-fill-color: white;
    background: #267ace linear-gradient(0deg, #267ace 0%, #267ace 100%);
}
select[multiple]:focus option:checked {
  background: #267ace linear-gradient(0deg, #267ace 0%, #267ace 100%);
}
button {
  /*How we style Buttons*/
  display: block;
  background-color: #ffffff; /* Green */
  border: 1px solid #e5e5e5;
  border-color: rgba(0, 0, 0, 0.15);
  color: #2e2e2e;
  padding: 5px 5px;
  font-weight: 500;
  outline: none;
  border-radius: 3px; /* Changes corner curves*/
  text-align: center;
  text-decoration: none;
  margin: 5px 0px 5px 0px;
  font-size: 1rem;
}

.upload-wrapper {
  height: 2.5rem;
  overflow: hidden;
  position: relative;
  display: flex; 
  align-items: center;
}

.upload-wrapper input[type=file] {
  font-size: 2rem;
  position: absolute;
  top: 0;
  left: 0;
  opacity: 0;
}

input[type=file]:focus + button{
  box-shadow: 0 0 0 3px rgba(38, 122, 206, 0.486);
}

table {
  background-color: #aaaaaa10;
  width: 100%;
}

td.data {
  width: 250px;
}
input[type]:focus,
select:focus {
  border-color: #73afea;
  box-shadow: 0 0 4px rgba(115, 175, 234, 0.4);
}
input[type='text'], /*Styling of our textboxes*/
[type='number']{
  padding-left: 10px;
  height: 2rem;
  width: 100%;
  position: relative;
  outline: none;
  border-radius: 0px;
  border: 1px solid #e5e5e5;
  border-color: rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
  font-size: 1rem;
}
#check {
    margin:4px;
    background-color:#FFFFFF;
    border-radius:4px;
    border:1px solid #D0D0D0;
    overflow:none;
}

#check:hover {
    box-shadow: 0 0 3px rgba(38, 122, 206, 0.486);
}

#check label {
    width: 15px;
    height: 15px;
}

#check label img {
    width: 15px;
    height: 15px;
    text-align:center;
    padding:3px 0px;
    display: block;
    opacity: 0;
}
#check input {
  opacity: 0;
}
#check label input {
    position: absolute;
}

#check input:checked + img {
    opacity: 100;
}
</style>
