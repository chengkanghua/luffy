from . import views
from rest_framework.routers import DefaultRouter

# 路由列表
urlpatterns = []

router = DefaultRouter()  # 可以处理视图的路由器，自动通过视图来生成增删改查的url路径
router.register('students', views.StudentViewSet)  #students是生成的url前缀，名称随便写， 向路由器中注册视图集

urlpatterns += router.urls  # 将路由器中的所以路由信息追到到django的路由列表中