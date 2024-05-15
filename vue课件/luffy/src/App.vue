<template>
  <div id="app">

    <router-view/>
  </div>
</template>

<script>

export default {
  name: 'App',

}
</script>

<style>
  body{
    padding: 0;
    margin:0;
  }
  a{
    text-decoration: none;
    color: #4a4a4a;
  }
  a:hover{
    color: #000;
  }
  .header .el-menu li .el-submenu__title{
    height: 26px!important;
    line-height: 26px!important;
  }
  .el-menu--popup{
    min-width: 140px;
  }
  ul{
      list-style: none;
      padding:0;
      margin:0;
    }
</style>
