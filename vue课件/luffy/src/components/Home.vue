<template>
  <div id="home">
    <Header></Header>
    <Banner></Banner>

    <Footer></Footer>
  </div>
</template>

<script>
import Header from './common/Header'
import Banner from './common/Banner'
import Footer from './common/Footer'
export default {
  name:"Home",
  data(){
    return {

    }
  },
  components:{
    Header,
    Banner,
    Footer,
  }
}
</script>

<style scoped>
.home{
  padding-top: 80px;
}
</style>
