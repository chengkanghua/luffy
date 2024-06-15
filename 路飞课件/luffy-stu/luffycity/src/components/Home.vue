<template>
  <div class="home">
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
        name: "Home",
        components:{
          Header,
          Banner,
          Footer,
        }
    }
</script>

<style scoped>

</style>
