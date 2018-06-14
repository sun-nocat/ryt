"""ttms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from yrt import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index),
    url(r'^home$',views.home),
    url(r'^index',views.index),
    url(r'^dh',views.dh),
    url(r'^login$',views.login),
    url(r'^loginError$',views.loginError),
    url(r'^ticket',views.ticket),
    url(r'^addUser',views.addUser),
    url(r'^manageIndex',views.manageIndex),  #跳转到管理员登录之后的主页面
    url(r'^manageDh',views.manageDh),  #跳转到管理员登录之后的导航页面
    url(r'^manageHome',views.manageHome),  #跳转到管理员登录之后的主页面
    url(r'^addOpera',views.addOpera),  #跳转到管理员登录之后的添加剧目页面
    url(r'^statusOpera',views.statusOpera),  #跳转到管理员登录之后的添加剧目页面
    url(r'^managePlay',views.managePlay),  #跳转到管理员登录之后的添加剧目页面
    url(r'^findPlay$',views.findPlay),  #跳转到管理员登录之后的查询演出计划页面
    url(r'^findPlay2$',views.findPlay2),  #跳转到管理员登录之后的查询演出计划页面
    url(r'^findPlay3$',views.findPlay3),  #跳转到管理员登录之后的查询演出计划页面
    url(r'^findPlay4$',views.findPlay4),  #跳转到管理员登录之后的查询演出计划页面
    url(r'^opera$',views.opera),  #跳转到管理员登录之后的查询演出计划页面
    url(r'^showOpera$',views.showOpera),  #跳转到管理员登录之后的查询演出计划页面
    url(r'^showOperaR$',views.showOpera),  #跳转到管理员登录之后的查询演出计划页面
    url(r'^checkSeat$',views.checkSeat),  #用户选择座位的页面
    url(r'^showOrder',views.showOrder),  #管理员查看订单
#--------------------    ----------------------    ---------
    url(r'^api/login$',views.api_login),
    url(r'^api/addUser$',views.api_addUser),
    url(r'^api/check$',views.api_check),
    url(r'^api/logout$',views.api_logout),
    url(r'^api/getOpera$',views.api_getOpera),
    url(r'^api/addOpera$',views.api_addOpera),
    url(r'^api/onOpera$',views.api_onOpera),
    url(r'^api/downOpera$',views.api_downOpera),
    url(r'^api/getOperaData$',views.api_getOperaData),
    url(r'^api/getPlayData$',views.api_getPlayData),
    url(r'^api/setPlay$',views.api_setPlay),
    url(r'^api/getPlay$',views.api_getPlay),
    url(r'^api/delPlay$',views.api_delPlay),
    url(r'^api/getOperaById$',views.api_getOperaById),
    url(r'^api/getTicket$',views.api_getTicket),
    url(r'^api/setTicket$',views.api_setTicket),
    url(r'^api/getOperaList$',views.api_getOperaList),
    url(r'^api/getOrder$',views.api_getOrder),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
