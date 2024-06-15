<template>
    <div class="footer">
      <div class="footer-item">
        <div class="foot-left">
        <div class="foot-content">
          <p>
            <span>关于我们</span>
            &nbsp;&nbsp;|&nbsp;&nbsp;
            <span>贝里小卖铺</span>
          </p>
          <p>
            地址：北京市昌平区顺沙路八号院汇德商厦402  邮箱：customer@luffycity.com
          </p>
          <p>
             © 2017-2020 北京路飞学城教育科技有限公司版权所有
            <a class="copyright" href="http://beian.miit.gov.cn" target="_blank" >京ICP备17072161号-1</a>
          </p>
          <p>
            <a class="report-link" target="_blank" href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=11010102002019&amp;token=1ee3034d-ba3a-4cc3-89d4-89875e2dd0b1">
              <img class="report-img" src="//img.alicdn.com/tfs/TB1..50QpXXXXX7XpXXXXXXXXXX-40-40.png" style="float:left" >
              京公网安备 11010102002019号
            </a>
          </p>
        </div>

      </div>
        <img src="@/assets/code.png" alt="" class="code">
      </div>
    </div>
</template>

<script>
    export default {
        name: "Footer"
    }
</script>

<style scoped>

  .footer{
    display: flex;
    align-items: center;
    width: 100%;
    height: 140px;
    flex-direction: column;
    overflow: hidden;
    background: #191c25;
  }
  .footer .foot-left{
    display: flex;
    align-items: center;
  }
  .footer .foot-left .foot-content p{
    margin-bottom: 10px;
    font-size: 13px;
    font-family: PingFangSC-Regular;
    font-weight: 400;
    color: #d0d0d0;
  }
  .footer-item{
    width: 960px;
    height: 100%;
    justify-content: space-between;
  }
  .foot-left{
    display: flex;
    align-items: center;
    float: left;
  }
  .foot-content a{
    color: #d0d0d0;
  }
  .footer .foot-left .foot-content p:first-child span{
    font-size: 16px;
    font-weight: 400;
    display: inline-block;
    font-family: PingFangSC-Regular;
    cursor: pointer;
  }
  .foot-content .report-img{
    display: inline-block;
    height: 20px;
    margin-right: 12px;
  }
  .footer-item .code{
    width: 74px;
    height: auto;
    margin-right: 100px;
    float: right;
    padding-top: 30px;
  }

</style>
