<template>
  <div id="app">
    <img src="./assets/logo.png">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
body{
    margin: 0;
    padding: 0;
  }
  ul{
    list-style: none;
    padding: 0;
    margin: 0;
  }
  li{
    list-style: none;
  }
  /*.el-header{*/
  /*  width: 1200px;*/
  /*}*/
  input,select,textarea{
    border: none;
    outline: none;
  }
  a{
    text-decoration: none;
    color: #4a4a4a;
  }

</style>
