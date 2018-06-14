from django.shortcuts import render
from django.http import *
from django.shortcuts import render,HttpResponse
from yrt import models
from django.shortcuts import render,render_to_response
from django.shortcuts import render
import json
import datetime
import time

# Create your views here.





#用户登录
def api_login(request):
    if request.method=="POST":
        account = request.POST.get("account",None)  #从前端获取用户名
        password = request.POST.get("password",None)  #从前端获取密码
        status = request.POST.get("status",None)  #从前端获取密码
        print('登录账号'+ str(account))
        print('登录密码'+ str(password))
        print('登录类别'+ str(status))

        # 普通用户登录
        if models.customer.objects.filter(account=account) and status=="user":  #如果用户名存在
            login_data = list(models.customer.objects.filter(account=account).values())
            password_database = login_data[0]['password']   #获取数据库中用的密码
            print(password_database)
            name_database = login_data[0]['name']   #获取数据库中用的密码
            print(name_database)
            if password_database == password:   #如果用户的密码正确
                # re=render(request,'home.html')
                # re=HttpResponseRedirect('/')
                re=HttpResponse()
                re.set_cookie('account',account)  #设置cookie
                re.set_cookie('status',"1")  #设置status
                request.session['account'] = account  #session保存用户账号
                request.session['password'] = password_database  #session保存用户密码
                request.session['name'] = name_database  #session保存用户姓名
                request.session['status'] = "1"  #status 1 值普通用户

                return re
            else:
                re = json.dumps(
                    {
                        "status": "0",
                        "msg": ""
                    }
                )
                return HttpResponse(re, content_type="application/json")
        # 管理员登录
        elif models.user.objects.filter(account=account) and status=="manage":
            login_data = list(models.user.objects.filter(account=account).values())
            print(login_data)
            password_database = login_data[0]['password']   #获取数据库中用的密码
            print(password_database)
            name_database = login_data[0]['name']   #获取数据库中用的密码
            print(name_database)
            if password_database == password:   #如果用户的密码正确
                # re=render(request,'login.html')
                re=HttpResponse()
                re.set_cookie('account',account)  #设置cookie
                re.set_cookie('status',"-1")  #设置statua
                request.session['account'] = account  #session保存用户账号
                request.session['password'] = password_database  #session保存用户密码
                request.session['name'] = name_database  #session保存用户姓名
                request.session['status'] = "-1"  #status -1 指管理员

                return re
            else:
                re = json.dumps(
                    {
                        "status": "0",
                        "msg": ""
                    }
                )
                return HttpResponse(re, content_type="application/json")
        else:
            re = json.dumps(
                {
                    "status": "0",
                    "msg": ""
                }
            )
        return HttpResponse(re,content_type="application/json")
    else:
        re = json.dumps(
            {
                "status":"0",
                "msg":""
            }
        )
        return HttpResponse(re,content_type="application/json")


#用户注册
def api_addUser(request):
    if request.method=="POST":
        name = request.POST.get('name',None)
        account = request.POST.get('account',None)
        password = request.POST.get('password',None)
        print(name)
        if name != None and account != None and password != None:
            models.customer.objects.create(
                name=name,
                account=account,
                password=password
            )

            return render(request, 'addUserSucess.html')
        else:
            return render(request,'addUserError.html')
    else:
        return render(request,'addUserError.html')


#验证用户登录情况
def api_check(request):
    if request.method=="POST":
        account = request.session.get('account',None)
        status = request.session.get('status',None)
        name = request.session.get('name',None)
        # statusC = request.COOKIES.get("status",None)
        print(account)
        if account:
            if status=="1":
                re = json.dumps({
                    "status": "0",
                    "msg": "用户登录",
                    "name": name,
                    "account": account

                })
                return HttpResponse(re, content_type="application/json")
            elif status=="-1":
                re = json.dumps({
                    "status": "-1",
                    "msg": "管理员登录",
                    "name": name,
                    "account": account

                })
                return HttpResponse(re, content_type="application/json")
            else:
                re = json.dumps({
                    "status": "1",
                    "msg": "失败"

                })
                return HttpResponse(re, content_type="application/json")
        else:
            re = json.dumps({
            "status":"1",
            "msg":"失败"

            })
            return HttpResponse(re,content_type="application/json")

    else:
        re = json.dumps({
            "status": "1",
            "msg": "失败"

        })
        return HttpResponse(re, content_type="application/json")


#获取剧目信息；
def api_getOpera(request):
    if request.method=="POST":
        all_list = models.opera.objects.order_by('id').reverse()
        data=[]
        for i in range(len(all_list)):
            d={}
            # print(all_list[i].type)
            # print(all_list[i].name)
            # print(all_list[i].length)
            d['id']=all_list[i].id
            d['type']=all_list[i].type
            d['name']=all_list[i].name
            d['length']=all_list[i].length
            d['price']=all_list[i].price
            d['describe']=all_list[i].describe
            if all_list[i].status == 1 :
                d['status'] = "待上线"
            elif all_list[i].status == 2:
                d['status'] = "上线中"
            elif all_list[i].status == 3:
                d['status'] = "已下线"
            data.append(d)
        re = json.dumps({
            "status": "0",
            "msg": "获取成功",
            "data":data

        })
        return HttpResponse(re, content_type="application/json")


#添加剧目
def api_addOpera(request):
    if request.method=="POST":
        name = request.POST.get('name',None)
        type = request.POST.get('type',None)
        length = request.POST.get('length',None)
        describe = request.POST.get('describe',None)

        image = request.FILES.get('image')


        price = request.POST.get('price',None)
        print(image)
        print(image.size)
        if name:
            models.opera.objects.create(
                name = name,
                type = type,
                length = length,
                describe = describe,
                price = price,
                image = image
            )

            return render(request,'manage/addOpera.html')
        else:
            re = json.dumps({
                "status": "1",
                "msg": "请设置name",
                # "data": data

            })
            return HttpResponse(re, content_type="application/json")
    else:
        re = json.dumps({
            "status": "1",
            "msg": "请使用post",
            # "data": data

        })
        return HttpResponse(re, content_type="application/json")


#上线剧目
def api_onOpera(request):
    if request.method=="POST":
        id = request.POST.get('id',None) #获取到前端传入的id


        models.opera.objects.filter(id=id).update(
            status = 2
        )
        re = json.dumps(
            {
                "status":"0",
                "msg":""
            }
        )
        return HttpResponse(re,content_type="application/json")


#下线剧目
def api_downOpera(request):
    if request.method=="POST":
        id = request.POST.get('id',None) #获取到前端传入的id

        models.opera.objects.filter(id=id).update(
            status = 3
        )
        re = json.dumps(
            {
                "status":"0",
                "msg":""
            }
        )
        return HttpResponse(re,content_type="application/json")


#退出登录
def api_logout(request):
    request.session.clear()
    return HttpResponseRedirect('/')


#管理演出计划--->  给前端返回已经上线剧目的信息
def api_getOperaData(request):
    if request.method=="POST":
        all_list = models.opera.objects.filter(status=2).order_by("-pk")
        print("all_list"+str(all_list))

        if len(list(all_list))=="0":
            re = json.dumps({
                "status": "0",
                "msg": "获取成功",
                "data": []

            })
            return HttpResponse(re, content_type="application/json")
        else:
            data=[]
            for i in range(len(all_list)):
                d={}
                d['id']=all_list[i].id
                d['type']=all_list[i].type
                d['name']=all_list[i].name
                d['length']=all_list[i].length
                d['price']=all_list[i].price
                d['describe']=all_list[i].describe
                if all_list[i].status == 1 :
                    d['status'] = "待上线"
                elif all_list[i].status == 2:
                    d['status'] = "上线中"
                elif all_list[i].status == 3:
                    d['status'] = "已下线"
                data.append(d)
            re = json.dumps({
                "status": "0",
                "msg": "获取成功",
                "data":data

            })
            return HttpResponse(re, content_type="application/json")


#管理演出计划--->  给前端返回演出厅id
def api_getPlayData(request):
    if request.method=="POST":
        all_list = models.studio.objects.filter().all()
        print(all_list)
        data=[]
        for i in range(len(all_list)):
            d={}
            d['id'] = all_list[i].id
            d['col'] = all_list[i].col
            d['row'] = all_list[i].row
            data.append(d)
        re = json.dumps(
            {
                "status": "0",
                "msg": "获取成功",
                "data": data
            }
        )
        return HttpResponse(re,content_type="application/json")


#管理演出计划-->   根据前端提交的数据 添加演出时刻表 并生成票
def api_setPlay(request):
    if request.method=="POST":
        operaId = request.POST.get("operaId",None)
        playId = request.POST.get("playId",None)
        data = request.POST.get("data",None)
        time = request.POST.get("time",None)
        # 给演出厅1号安排演出计划
        if playId =="1":   #给演出厅1号安排演出计划
            all_list = list(models.schedule1.objects.filter(data=data).values())   #
            # 如果 在此日期下 没有安排任何演出
            if str(len(all_list)) == "0":
                if time == "1":  #根据时刻表存储剧目id
                    models.schedule1.objects.create(
                        data=data,
                        time8_11=operaId
                    )
                    try:
                        createTicket(operaId, playId, data, time)
                        print("创建票成功")
                    except:
                        print('创建票失败')
                elif time == "2":
                    models.schedule1.objects.create(
                        data=data,
                        time12_15=operaId
                    )
                    try:
                        createTicket(operaId, playId, data, time)
                        print("创建票成功")
                    except:
                        print('创建票失败')
                elif time == "3":
                    models.schedule1.objects.create(
                        data=data,
                        time16_19=operaId
                    )
                    try:
                        createTicket(operaId, playId, data, time)
                        print("创建票成功")
                    except:
                        print('创建票失败')
                elif time=="4":
                    models.schedule1.objects.create(
                        data=data,
                        time20_23=operaId
                    )
                    try:
                        createTicket(operaId, playId, data, time)
                        print("创建票成功")
                    except:
                        print('创建票失败')
                re = json.dumps({
                    "status":"0",
                    "msg":"演出安排成功"

                })
                return HttpResponse(re,content_type="application/json")
            else:
                # 根据场次不同进行添加
                if time =="1":
                    operatime = all_list[0].get('time8_11')
                    print(operatime)
                    if operatime==None or operatime==0:   #如果此时间段没有被安排
                        models.schedule1.objects.filter(data=data).update(
                            time8_11 = operaId
                        )
                        try:
                            createTicket(operaId, playId, data, time)
                            print("创建票成功")
                        except:
                            print('创建票失败')
                        re = json.dumps({
                            "status": "0",
                            "msg": "演出安排成功"

                        })
                        return HttpResponse(re, content_type="application/json")
                    else:  #如果此时间段被安排
                        re = json.dumps({
                            "ststua":"1",
                            "msg":"此时间段已经被安排"
                        })
                        return HttpResponse(re,content_type="application/json")
                elif time == "2":
                    print("lala")
                    operatime = all_list[0].get('time12_15')
                    print(operatime)
                    if operatime == None or operatime==0:  # 如果此时间段没有被安排
                        models.schedule1.objects.filter(data=data).update(
                            time12_15 = operaId
                        )
                        try:
                            createTicket(operaId, playId, data, time)
                            print("创建票成功")
                        except:
                            print('创建票失败')
                        re = json.dumps({
                            "status": "0",
                            "msg": "演出安排成功"

                        })
                        return HttpResponse(re, content_type="application/json")
                    else:  # 如果此时间段被安排
                        re = json.dumps({
                            "ststua": "1",
                            "msg": "此时间段已经被安排"
                        })
                        return HttpResponse(re, content_type="application/json")
                elif time == "3":
                    operatime = all_list[0].get('time16_19')
                    print(operatime)
                    if operatime == None or operatime==0:  # 如果此时间段没有被安排
                        models.schedule1.objects.filter(data=data).update(
                            time16_19 = operaId
                        )
                        try:
                            createTicket(operaId, playId, data, time)
                            print("创建票成功")
                        except:
                            print('创建票失败')
                        re = json.dumps({
                            "status": "0",
                            "msg": "演出安排成功"

                        })
                        return HttpResponse(re, content_type="application/json")
                    else:  # 如果此时间段被安排
                        re = json.dumps({
                            "ststua": "1",
                            "msg": "此时间段已经被安排"
                        })
                        return HttpResponse(re, content_type="application/json")
                elif time == "4":
                    operatime = all_list[0].get('time20_23')
                    print(operatime)
                    if operatime == None or operatime==0:  # 如果此时间段没有被安排
                        models.schedule1.objects.filter(data=data).update(
                            time20_23 = operaId
                        )
                        try:
                            createTicket(operaId, playId, data, time)
                            print("创建票成功")
                        except:
                            print('创建票失败')
                        re = json.dumps({
                            "status": "0",
                            "msg": "演出安排成功"

                        })
                        return HttpResponse(re, content_type="application/json")
                    else:  # 如果此时间段被安排
                        re = json.dumps({
                            "ststua": "1",
                            "msg": "此时间段已经被安排"
                        })
                        return HttpResponse(re, content_type="application/json")
        # 给演出厅2号安排演出计划
        elif playId =="2":
            all_list = list(models.schedule2.objects.filter(data=data).values())   #
            # 如果 在此日期下 没有安排任何演出
            if str(len(all_list)) == "0":
                if time == "1":  #根据时刻表存储剧目id
                    models.schedule2.objects.create(
                        data=data,
                        time8_11=operaId
                    )
                    try:
                        createTicket(operaId, playId, data, time)
                        print("创建票成功")
                    except:
                        print('创建票失败')
                elif time == "2":
                    models.schedule2.objects.create(
                        data=data,
                        time12_15=operaId
                    )
                    try:
                        createTicket(operaId, playId, data, time)
                        print("创建票成功")
                    except:
                        print('创建票失败')
                elif time == "3":
                    models.schedule2.objects.create(
                        data=data,
                        time16_19=operaId
                    )
                    try:
                        createTicket(operaId, playId, data, time)
                        print("创建票成功")
                    except:
                        print('创建票失败')
                elif time=="4":
                    models.schedule2.objects.create(
                        data=data,
                        time20_23=operaId
                    )
                    try:
                        createTicket(operaId, playId, data, time)
                        print("创建票成功")
                    except:
                        print('创建票失败')
                re = json.dumps({
                    "status":"0",
                    "msg":"演出安排成功"

                })
                return HttpResponse(re,content_type="application/json")
            else:
                # 根据场次不同进行添加
                if time =="1":
                    operatime = all_list[0].get('time8_11')
                    print(operatime)
                    if operatime==None or operatime==0:   #如果此时间段没有被安排
                        models.schedule2.objects.filter(data=data).update(
                            time8_11 = operaId
                        )
                        try:
                            createTicket(operaId, playId, data, time)
                            print("创建票成功")
                        except:
                            print('创建票失败')
                        re = json.dumps({
                            "status": "0",
                            "msg": "演出安排成功"

                        })
                        return HttpResponse(re, content_type="application/json")
                    else:  #如果此时间段被安排
                        re = json.dumps({
                            "ststua":"1",
                            "msg":"此时间段已经被安排"
                        })
                        return HttpResponse(re,content_type="application/json")
                elif time == "2":
                    print("lala")
                    operatime = all_list[0].get('time12_15')
                    print(operatime)
                    if operatime == None or operatime==0:  # 如果此时间段没有被安排
                        models.schedule2.objects.filter(data=data).update(
                            time12_15 = operaId
                        )
                        try:
                            createTicket(operaId, playId, data, time)
                            print("创建票成功")
                        except:
                            print('创建票失败')
                        re = json.dumps({
                            "status": "0",
                            "msg": "演出安排成功"

                        })
                        return HttpResponse(re, content_type="application/json")
                    else:  # 如果此时间段被安排
                        re = json.dumps({
                            "ststua": "1",
                            "msg": "此时间段已经被安排"
                        })
                        return HttpResponse(re, content_type="application/json")
                elif time == "3":
                    operatime = all_list[0].get('time16_19')
                    print(operatime)
                    if operatime == None or operatime==0:  # 如果此时间段没有被安排
                        models.schedule2.objects.filter(data=data).update(
                            time16_19 = operaId
                        )
                        try:
                            createTicket(operaId, playId, data, time)
                            print("创建票成功")
                        except:
                            print('创建票失败')
                        re = json.dumps({
                            "status": "0",
                            "msg": "演出安排成功"

                        })
                        return HttpResponse(re, content_type="application/json")
                    else:  # 如果此时间段被安排
                        re = json.dumps({
                            "ststua": "1",
                            "msg": "此时间段已经被安排"
                        })
                        return HttpResponse(re, content_type="application/json")
                elif time == "4":
                    operatime = all_list[0].get('time20_23')
                    print(operatime)
                    if operatime == None or operatime==0:  # 如果此时间段没有被安排
                        models.schedule2.objects.filter(data=data).update(
                            time20_23 = operaId
                        )
                        try:
                            createTicket(operaId, playId, data, time)
                            print("创建票成功")
                        except:
                            print('创建票失败')
                        re = json.dumps({
                            "status": "0",
                            "msg": "演出安排成功"

                        })
                        return HttpResponse(re, content_type="application/json")
                    else:  # 如果此时间段被安排
                        re = json.dumps({
                            "ststua": "1",
                            "msg": "此时间段已经被安排"
                        })
                        return HttpResponse(re, content_type="application/json")
        # 给演出厅3号安排演出计划
        elif playId =="3":
            all_list = list(models.schedule3.objects.filter(data=data).values())   #
            # 如果 在此日期下 没有安排任何演出
            if str(len(all_list)) == "0":
                if time == "1":  #根据时刻表存储剧目id
                    models.schedule3.objects.create(
                        data=data,
                        time8_11=operaId
                    )
                    try:
                        createTicket(operaId, playId, data, time)
                        print("创建票成功")
                    except:
                        print('创建票失败')
                elif time == "2":
                    models.schedule3.objects.create(
                        data=data,
                        time12_15=operaId
                    )
                    try:
                        createTicket(operaId, playId, data, time)
                        print("创建票成功")
                    except:
                        print('创建票失败')
                elif time == "3":
                    models.schedule3.objects.create(
                        data=data,
                        time16_19=operaId
                    )
                    try:
                        createTicket(operaId, playId, data, time)
                        print("创建票成功")
                    except:
                        print('创建票失败')
                elif time=="4":
                    models.schedule3.objects.create(
                        data=data,
                        time20_23=operaId
                    )
                    try:
                        createTicket(operaId, playId, data, time)
                        print("创建票成功")
                    except:
                        print('创建票失败')
                re = json.dumps({
                    "status":"0",
                    "msg":"演出安排成功"

                })
                return HttpResponse(re,content_type="application/json")
            else:
                # 根据场次不同进行添加
                if time =="1":
                    operatime = all_list[0].get('time8_11')
                    print(operatime)
                    if operatime==None or operatime==0:   #如果此时间段没有被安排
                        models.schedule3.objects.filter(data=data).update(
                            time8_11 = operaId
                        )
                        try:
                            createTicket(operaId, playId, data, time)
                            print("创建票成功")
                        except:
                            print('创建票失败')

                        re = json.dumps({
                            "status": "0",
                            "msg": "演出安排成功"

                        })
                        return HttpResponse(re, content_type="application/json")
                    else:  #如果此时间段被安排
                        re = json.dumps({
                            "ststua":"1",
                            "msg":"此时间段已经被安排"
                        })
                        return HttpResponse(re,content_type="application/json")
                elif time == "2":
                    print("lala")
                    operatime = all_list[0].get('time12_15')
                    print(operatime)
                    if operatime == None or operatime==0:  # 如果此时间段没有被安排
                        models.schedule3.objects.filter(data=data).update(
                            time12_15 = operaId
                        )
                        try:
                            createTicket(operaId, playId, data, time)
                            print("创建票成功")
                        except:
                            print('创建票失败')
                        re = json.dumps({
                            "status": "0",
                            "msg": "演出安排成功"

                        })
                        return HttpResponse(re, content_type="application/json")
                    else:  # 如果此时间段被安排
                        re = json.dumps({
                            "ststua": "1",
                            "msg": "此时间段已经被安排"
                        })
                        return HttpResponse(re, content_type="application/json")
                elif time == "3":
                    operatime = all_list[0].get('time16_19')
                    print(operatime)
                    if operatime == None or operatime==0:  # 如果此时间段没有被安排
                        models.schedule3.objects.filter(data=data).update(
                            time16_19 = operaId
                        )
                        try:
                            createTicket(operaId, playId, data, time)
                            print("创建票成功")
                        except:
                            print('创建票失败')
                        re = json.dumps({
                            "status": "0",
                            "msg": "演出安排成功"

                        })
                        return HttpResponse(re, content_type="application/json")
                    else:  # 如果此时间段被安排
                        re = json.dumps({
                            "ststua": "1",
                            "msg": "此时间段已经被安排"
                        })
                        return HttpResponse(re, content_type="application/json")
                elif time == "4":
                    operatime = all_list[0].get('time20_23')
                    print(operatime)
                    if operatime == None or operatime==0:  # 如果此时间段没有被安排
                        models.schedule3.objects.filter(data=data).update(
                            time20_23 = operaId
                        )
                        try:
                            createTicket(operaId, playId, data, time)
                            print("创建票成功")
                        except:
                            print('创建票失败')
                        re = json.dumps({
                            "status": "0",
                            "msg": "演出安排成功"

                        })
                        return HttpResponse(re, content_type="application/json")
                    else:  # 如果此时间段被安排
                        re = json.dumps({
                            "ststua": "1",
                            "msg": "此时间段已经被安排"
                        })
                        return HttpResponse(re, content_type="application/json")
        # 给演出厅3号安排演出计划
        elif playId =="4":
            all_list = list(models.schedule4.objects.filter(data=data).values())   #
            # 如果 在此日期下 没有安排任何演出
            if str(len(all_list)) == "0":
                if time == "1":  #根据时刻表存储剧目id
                    models.schedule4.objects.create(
                        data=data,
                        time8_11=operaId
                    )
                    try:
                        createTicket(operaId, playId, data, time)
                        print("创建票成功")
                    except:
                        print('创建票失败')
                elif time == "2":
                    models.schedule4.objects.create(
                        data=data,
                        time12_15=operaId
                    )
                    try:
                        createTicket(operaId, playId, data, time)
                        print("创建票成功")
                    except:
                        print('创建票失败')
                elif time == "3":
                    models.schedule4.objects.create(
                        data=data,
                        time16_19=operaId
                    )
                    try:
                        createTicket(operaId, playId, data, time)
                        print("创建票成功")
                    except:
                        print('创建票失败')
                elif time=="4":
                    models.schedule4.objects.create(
                        data=data,
                        time20_23=operaId
                    )
                    try:
                        createTicket(operaId, playId, data, time)
                        print("创建票成功")
                    except:
                        print('创建票失败')
                re = json.dumps({
                    "status":"0",
                    "msg":"演出安排成功"
                })
                return HttpResponse(re,content_type="application/json")
            else:
                # 根据场次不同进行添加
                if time =="1":
                    operatime = all_list[0].get('time8_11')
                    print(operatime)
                    if operatime==None or operatime==0:   #如果此时间段没有被安排
                        models.schedule4.objects.filter(data=data).update(
                            time8_11 = operaId
                        )
                        try:
                            createTicket(operaId, playId, data, time)
                            print("创建票成功")
                        except:
                            print('创建票失败')
                        re = json.dumps({
                            "status": "0",
                            "msg": "演出安排成功"

                        })
                        return HttpResponse(re, content_type="application/json")
                    else:  #如果此时间段被安排
                        re = json.dumps({
                            "ststua":"1",
                            "msg":"此时间段已经被安排"
                        })
                        return HttpResponse(re,content_type="application/json")
                elif time == "2":
                    print("lala")
                    operatime = all_list[0].get('time12_15')
                    print(operatime)
                    if operatime == None or operatime==0:  # 如果此时间段没有被安排
                        models.schedule4.objects.filter(data=data).update(
                            time12_15 = operaId
                        )
                        try:
                            createTicket(operaId, playId, data, time)
                            print("创建票成功")
                        except:
                            print('创建票失败')
                        re = json.dumps({
                            "status": "0",
                            "msg": "演出安排成功"

                        })
                        return HttpResponse(re, content_type="application/json")
                    else:  # 如果此时间段被安排
                        re = json.dumps({
                            "ststua": "1",
                            "msg": "此时间段已经被安排"
                        })
                        return HttpResponse(re, content_type="application/json")
                elif time == "3":
                    operatime = all_list[0].get('time16_19')
                    print(operatime)
                    if operatime == None or operatime==0:  # 如果此时间段没有被安排
                        models.schedule4.objects.filter(data=data).update(
                            time16_19 = operaId
                        )
                        try:
                            createTicket(operaId, playId, data, time)
                            print("创建票成功")
                        except:
                            print('创建票失败')
                        re = json.dumps({
                            "status": "0",
                            "msg": "演出安排成功"

                        })
                        return HttpResponse(re, content_type="application/json")
                    else:  # 如果此时间段被安排
                        re = json.dumps({
                            "ststua": "1",
                            "msg": "此时间段已经被安排"
                        })
                        return HttpResponse(re, content_type="application/json")
                elif time == "4":
                    operatime = all_list[0].get('time20_23')
                    print(operatime)
                    if operatime == None or operatime==0:  # 如果此时间段没有被安排
                        models.schedule4.objects.filter(data=data).update(
                            time20_23 = operaId
                        )

                        try:
                            createTicket(operaId, playId, data, time)
                            print("创建票成功")
                        except:
                            print('创建票失败')
                        re = json.dumps({
                            "status": "0",
                            "msg": "演出安排成功"

                        })
                        return HttpResponse(re, content_type="application/json")
                    else:  # 如果此时间段被安排
                        re = json.dumps({
                            "ststua": "1",
                            "msg": "此时间段已经被安排"
                        })
                        return HttpResponse(re, content_type="application/json")

        else:
            re = json.dumps(
                {
                    "status":"0",
                    "msg":"演出厅安排错误"
                }
            )
            return HttpResponse(re,content_type="application/json")


#管理演出计划-->   获取详细的演出计划数据
def api_getPlay(request):
    if request.method == "POST":
        status = request.POST.get("status",None)  #获取需要·查询·的影院的id、
        if status =="1":  #·1号·剧院
            playlist = models.schedule1.objects.all().order_by("-pk")  #获取·1·号剧院的演出计划
            print("playlist= "+ str(playlist))
            datas=[]
            for i in range(len(playlist)):
                playTimeList1 = getOD(playlist[i].time8_11)  #获取第一场演出剧目的详细数据
                if len(playTimeList1)!=0:
                    # print(str(playTimeList1) + str(playlist[i].data))
                    data = playlist[i].data
                    time = "8:00-11:00"
                    schedule = "一号演出厅"
                    dict2 = {"date":data,"schedule":schedule,"time":time}
                    dict1 = dict(playTimeList1[0], **dict2)
                    datas.append(dict1)
                    # print(dict1)

                playTimeList2 = getOD(playlist[i].time12_15)  #获取第二场演出剧目的详细数据
                if len(playTimeList2)!=0:
                    # print(str(playTimeList2) + str(playlist[i].data))
                    data = playlist[i].data
                    time = "12:00-15:00"
                    schedule = "一号演出厅"
                    dict2 = {"date":data,"schedule":schedule,"time":time}
                    dict1 = dict(playTimeList2[0], **dict2)
                    # print(dict1)
                    datas.append(dict1)

                playTimeList3 = getOD(playlist[i].time16_19)
                if len(playTimeList3) != 0:
                    # print(str(playTimeList3) + str(playlist[i].data))
                    data = playlist[i].data
                    time = "16:00-19:00"
                    schedule = "一号演出厅"
                    dict2 = {"date":data,"schedule":schedule,"time":time}
                    dict1 = dict(playTimeList3[0], **dict2)
                    # print(dict1)
                    datas.append(dict1)

                playTimeList4 = getOD(playlist[i].time20_23)
                if len(playTimeList4) != 0:
                    # print(str(playTimeList3) + str(playlist[i].data))
                    data = playlist[i].data
                    time = "20:00-23:00"
                    schedule = "一号演出厅"
                    dict2 = {"date":data,"schedule":schedule,"time":time}
                    dict1 = dict(playTimeList4[0], **dict2)
                    # print(dict1)
                    datas.append(dict1)

            re = json.dumps(
                {
                    "status":"0",
                    "msg":"获取一号演出厅演出计划成功",
                    "data":datas
                }
            )
            return HttpResponse(re,content_type="application/json")

        elif status =="2":  #·2号·剧院
            playlist = models.schedule2.objects.all().order_by("-pk")  #获取·1·号剧院的演出计划
            print("playlist= "+ str(playlist))
            datas=[]
            for i in range(len(playlist)):
                playTimeList1 = getOD(playlist[i].time8_11)  #获取第一场演出剧目的详细数据
                if len(playTimeList1)!=0:
                    # print(str(playTimeList1) + str(playlist[i].data))
                    data = playlist[i].data
                    time = "8:00-11:00"
                    schedule = "二号演出厅"
                    dict2 = {"date":data,"schedule":schedule,"time":time}
                    dict1 = dict(playTimeList1[0], **dict2)
                    datas.append(dict1)
                    # print(dict1)

                playTimeList2 = getOD(playlist[i].time12_15)  #获取第二场演出剧目的详细数据
                if len(playTimeList2)!=0:
                    # print(str(playTimeList2) + str(playlist[i].data))
                    data = playlist[i].data
                    time = "12:00-15:00"
                    schedule = "二号演出厅"
                    dict2 = {"date":data,"schedule":schedule,"time":time}
                    dict1 = dict(playTimeList2[0], **dict2)
                    # print(dict1)
                    datas.append(dict1)

                playTimeList3 = getOD(playlist[i].time16_19)
                if len(playTimeList3) != 0:
                    # print(str(playTimeList3) + str(playlist[i].data))
                    data = playlist[i].data
                    time = "16:00-19:00"
                    schedule = "二号演出厅"
                    dict2 = {"date":data,"schedule":schedule,"time":time}
                    dict1 = dict(playTimeList3[0], **dict2)
                    # print(dict1)
                    datas.append(dict1)

                playTimeList4 = getOD(playlist[i].time20_23)
                if len(playTimeList4) != 0:
                    # print(str(playTimeList3) + str(playlist[i].data))
                    data = playlist[i].data
                    time = "20:00-23:00"
                    schedule = "二号演出厅"
                    dict2 = {"date":data,"schedule":schedule,"time":time}
                    dict1 = dict(playTimeList4[0], **dict2)
                    # print(dict1)
                    datas.append(dict1)

            re = json.dumps(
                {
                    "status":"0",
                    "msg":"获取二号演出厅演出计划成功",
                    "data":datas
                }
            )
            return HttpResponse(re,content_type="application/json")

        elif status =="3":  #·3号·剧院
            playlist = models.schedule3.objects.all().order_by("-pk")  #获取·1·号剧院的演出计划
            print("playlist= "+ str(playlist))
            datas=[]
            for i in range(len(playlist)):
                playTimeList1 = getOD(playlist[i].time8_11)  #获取第一场演出剧目的详细数据
                if len(playTimeList1)!=0:
                    # print(str(playTimeList1) + str(playlist[i].data))
                    data = playlist[i].data
                    time = "8:00-11:00"
                    schedule = "三号演出厅"
                    dict2 = {"date":data,"schedule":schedule,"time":time}
                    dict1 = dict(playTimeList1[0], **dict2)
                    datas.append(dict1)
                    # print(dict1)

                playTimeList2 = getOD(playlist[i].time12_15)  #获取第二场演出剧目的详细数据
                if len(playTimeList2)!=0:
                    # print(str(playTimeList2) + str(playlist[i].data))
                    data = playlist[i].data
                    time = "12:00-15:00"
                    schedule = "三号演出厅"
                    dict2 = {"date":data,"schedule":schedule,"time":time}
                    dict1 = dict(playTimeList2[0], **dict2)
                    # print(dict1)
                    datas.append(dict1)

                playTimeList3 = getOD(playlist[i].time16_19)
                if len(playTimeList3) != 0:
                    # print(str(playTimeList3) + str(playlist[i].data))
                    data = playlist[i].data
                    time = "16:00-19:00"
                    schedule = "三号演出厅"
                    dict2 = {"date":data,"schedule":schedule,"time":time}
                    dict1 = dict(playTimeList3[0], **dict2)
                    # print(dict1)
                    datas.append(dict1)

                playTimeList4 = getOD(playlist[i].time20_23)
                if len(playTimeList4) != 0:
                    # print(str(playTimeList3) + str(playlist[i].data))
                    data = playlist[i].data
                    time = "20:00-23:00"
                    schedule = "三号演出厅"
                    dict2 = {"date":data,"schedule":schedule,"time":time}
                    dict1 = dict(playTimeList4[0], **dict2)
                    # print(dict1)
                    datas.append(dict1)

            re = json.dumps(
                {
                    "status":"0",
                    "msg":"获取三号演出厅演出计划成功",
                    "data":datas
                }
            )
            return HttpResponse(re,content_type="application/json")

        elif status =="4":  #·4号·剧院
            playlist = models.schedule4.objects.all().order_by("-pk")  #获取·1·号剧院的演出计划
            print("playlist= "+ str(playlist))
            datas=[]
            for i in range(len(playlist)):
                playTimeList1 = getOD(playlist[i].time8_11)  #获取第一场演出剧目的详细数据
                if len(playTimeList1)!=0:
                    # print(str(playTimeList1) + str(playlist[i].data))
                    data = playlist[i].data
                    time = "8:00-11:00"
                    schedule = "四号演出厅"
                    dict2 = {"date":data,"schedule":schedule,"time":time}
                    dict1 = dict(playTimeList1[0], **dict2)
                    datas.append(dict1)
                    # print(dict1)

                playTimeList2 = getOD(playlist[i].time12_15)  #获取第二场演出剧目的详细数据
                if len(playTimeList2)!=0:
                    # print(str(playTimeList2) + str(playlist[i].data))
                    data = playlist[i].data
                    time = "12:00-15:00"
                    schedule = "四号演出厅"
                    dict2 = {"date":data,"schedule":schedule,"time":time}
                    dict1 = dict(playTimeList2[0], **dict2)
                    # print(dict1)
                    datas.append(dict1)

                playTimeList3 = getOD(playlist[i].time16_19)
                if len(playTimeList3) != 0:
                    # print(str(playTimeList3) + str(playlist[i].data))
                    data = playlist[i].data
                    time = "16:00-19:00"
                    schedule = "四号演出厅"
                    dict2 = {"date":data,"schedule":schedule,"time":time}
                    dict1 = dict(playTimeList3[0], **dict2)
                    # print(dict1)
                    datas.append(dict1)

                playTimeList4 = getOD(playlist[i].time20_23)
                if len(playTimeList4) != 0:
                    # print(str(playTimeList3) + str(playlist[i].data))
                    data = playlist[i].data
                    time = "20:00-23:00"
                    schedule = "四号演出厅"
                    dict2 = {"date":data,"schedule":schedule,"time":time}
                    dict1 = dict(playTimeList4[0], **dict2)
                    # print(dict1)
                    datas.append(dict1)

            re = json.dumps(
                {
                    "status":"0",
                    "msg":"获取四号演出厅演出计划成功",
                    "data":datas
                }
            )
            return HttpResponse(re,content_type="application/json")


#根据指定的剧目id获取剧目的详细信息
def getOD(operaId):
    all_list = list(models.opera.objects.filter(id=operaId).order_by("-pk"))
    # print(all_list)
    if len(all_list)=="0":
        data=[]
        return data
    else:
        data=[]
        for i in range(len(all_list)):
            d={}
            d['id']=all_list[i].id
            d['type']=all_list[i].type
            d['name']=all_list[i].name
            d['length']=all_list[i].length
            d['image']=all_list[i].image.name
            print(all_list[i].image.name)
            d['price']=all_list[i].price
            d['describe']=all_list[i].describe
            if all_list[i].status == 1 :
                d['status'] = "待上线"
            elif all_list[i].status == 2:
                d['status'] = "上线中"
            elif all_list[i].status == 3:
                d['status'] = "已下线"
            data.append(d)
        # print("data="+str(data))
    return data

# 根据剧目id和演出厅id　生成票　
# 参数 operaId剧目id  studioId 演出厅id  date 演出时间  time  演出的场次
def createTicket(operaId,studioId,date,time):
    operalist = list(models.opera.objects.filter(id=operaId).values()) #根据剧目id获取信息
    name = operalist[0].get("name",None)
    length = operalist[0].get("length",None)
    price = operalist[0].get("price",None)
    print(name)

    for i in range(1,11):
        for j in range(1,11):
            models.ticket.objects.create(
                operaId=operaId,
                name=name,
                price=price,
                length=length,
                studio=int(studioId),
                date=date,
                time=time,
                row=i,
                col=j,
            )
    status="0"
    return status


# 删除演出计划
def api_delPlay(request):
    if request.method=="POST":
        studio = request.POST.get("studio",None)   #获取演出厅的信息   --->
        data = request.POST.get("data",None)    #获取时间 data-->
        time = request.POST.get("time",None)   # 获得场次 time-->根据场次的不同进行更改
        if studio == "1":  #如果是一号演出厅
               # 找到id为
            if time == "1":
                models.schedule1.objects.filter(data=data,).update(   #找到对应的演出时刻，将演出时刻质控
                    time8_11=0
                )
                if models.ticket.objects.filter(studio=studio,date=data,time=time):
                    models.ticket.objects.filter(studio=studio,date=data,time=time).delete()  #根据演出厅 演出时间 演出场次 找到对应的票
                    print("删除票成功")
            if time == "2":
                models.schedule1.objects.filter(data=data,).update(   #找到对应的演出时刻，将演出时刻质控
                    time12_15=0
                )
                if models.ticket.objects.filter(studio=studio,date=data,time=time):
                    models.ticket.objects.filter(studio=studio,date=data,time=time).delete()  #根据演出厅 演出时间 演出场次 找到对应的票
                    print("删除票成功")
            if time == "3":
                models.schedule1.objects.filter(data=data,).update(   #找到对应的演出时刻，将演出时刻质控
                    time16_19=0
                )
                if models.ticket.objects.filter(studio=studio,date=data,time=time):
                    models.ticket.objects.filter(studio=studio,date=data,time=time).delete()  #根据演出厅 演出时间 演出场次 找到对应的票
                    print("删除票成功")
            if time == "4":
                models.schedule1.objects.filter(data=data,).update(   #找到对应的演出时刻，将演出时刻质控
                    time20_23=0
                )
                if models.ticket.objects.filter(studio=studio,date=data,time=time):
                    models.ticket.objects.filter(studio=studio,date=data,time=time).delete()  #根据演出厅 演出时间 演出场次 找到对应的票
                    print("删除票成功")
            re = json.dumps({
                "status":"0",
                "msg":"删除一号演出厅的演出计划成功",

            })
            return HttpResponse(re,content_type="application/json")
        if studio == "2":  #如果是一号演出厅
               # 找到id为
            if time == "1":
                models.schedule2.objects.filter(data=data,).update(   #找到对应的演出时刻，将演出时刻质控
                    time8_11=0
                )
                if models.ticket.objects.filter(studio=studio,date=data,time=time):
                    models.ticket.objects.filter(studio=studio,date=data,time=time).delete()  #根据演出厅 演出时间 演出场次 找到对应的票
                    print("删除票成功")
            if time == "2":
                models.schedule2.objects.filter(data=data,).update(   #找到对应的演出时刻，将演出时刻质控
                    time12_15=0
                )
                if models.ticket.objects.filter(studio=studio,date=data,time=time):
                    models.ticket.objects.filter(studio=studio,date=data,time=time).delete()  #根据演出厅 演出时间 演出场次 找到对应的票
                    print("删除票成功")
            if time == "3":
                models.schedule2.objects.filter(data=data,).update(   #找到对应的演出时刻，将演出时刻质控
                    time16_19=0
                )
                if models.ticket.objects.filter(studio=studio,date=data,time=time):
                    models.ticket.objects.filter(studio=studio,date=data,time=time).delete()  #根据演出厅 演出时间 演出场次 找到对应的票
                    print("删除票成功")
            if time == "4":
                models.schedule2.objects.filter(data=data,).update(   #找到对应的演出时刻，将演出时刻质控
                    time20_23=0
                )
                if models.ticket.objects.filter(studio=studio,date=data,time=time):
                    models.ticket.objects.filter(studio=studio,date=data,time=time).delete()  #根据演出厅 演出时间 演出场次 找到对应的票
                    print("删除票成功")
            re = json.dumps({
                "status":"0",
                "msg":"删除一号演出厅的演出计划成功",

            })
            return HttpResponse(re,content_type="application/json")
        if studio == "3":  #如果是一号演出厅
               # 找到id为
            if time == "1":
                models.schedule3.objects.filter(data=data,).update(   #找到对应的演出时刻，将演出时刻质控
                    time8_11=0
                )
                if models.ticket.objects.filter(studio=studio,date=data,time=time):
                    models.ticket.objects.filter(studio=studio,date=data,time=time).delete()  #根据演出厅 演出时间 演出场次 找到对应的票
                    print("删除票成功")
            if time == "2":
                models.schedule3.objects.filter(data=data,).update(   #找到对应的演出时刻，将演出时刻质控
                    time12_15=0
                )
                if models.ticket.objects.filter(studio=studio,date=data,time=time):
                    models.ticket.objects.filter(studio=studio,date=data,time=time).delete()  #根据演出厅 演出时间 演出场次 找到对应的票
                    print("删除票成功")
            if time == "3":
                models.schedule3.objects.filter(data=data,).update(   #找到对应的演出时刻，将演出时刻质控
                    time16_19=0
                )
                if models.ticket.objects.filter(studio=studio,date=data,time=time):
                    models.ticket.objects.filter(studio=studio,date=data,time=time).delete()  #根据演出厅 演出时间 演出场次 找到对应的票
                    print("删除票成功")
                else:
                    print("没有找到票")
            if time == "4":
                models.schedule3.objects.filter(data=data,).update(   #找到对应的演出时刻，将演出时刻质控
                    time20_23=0
                )
                if models.ticket.objects.filter(studio=studio,date=data,time=time):
                    models.ticket.objects.filter(studio=studio,date=data,time=time).delete()  #根据演出厅 演出时间 演出场次 找到对应的票
                    print("删除票成功")
            re = json.dumps({
                "status":"0",
                "msg":"删除一号演出厅的演出计划成功",

            })
            return HttpResponse(re,content_type="application/json")
        if studio == "4":  #如果是一号演出厅
               # 找到id为
            if time == "1":
                models.schedule4.objects.filter(data=data,).update(   #找到对应的演出时刻，将演出时刻质控
                    time8_11=0
                )
                if models.ticket.objects.filter(studio=studio,date=data,time=time):
                    models.ticket.objects.filter(studio=studio,date=data,time=time).delete()  #根据演出厅 演出时间 演出场次 找到对应的票
                    print("删除票成功")
            if time == "2":
                models.schedule4.objects.filter(data=data,).update(   #找到对应的演出时刻，将演出时刻质控
                    time12_15=0
                )
                if models.ticket.objects.filter(studio=studio,date=data,time=time):
                    models.ticket.objects.filter(studio=studio,date=data,time=time).delete()  #根据演出厅 演出时间 演出场次 找到对应的票
                    print("删除票成功")
            if time == "3":
                models.schedule4.objects.filter(data=data,).update(   #找到对应的演出时刻，将演出时刻质控
                    time16_19=0
                )
                if models.ticket.objects.filter(studio=studio,date=data,time=time):
                    models.ticket.objects.filter(studio=studio,date=data,time=time).delete()  #根据演出厅 演出时间 演出场次 找到对应的票
                    print("删除票成功")
            if time == "4":
                models.schedule4.objects.filter(data=data,).update(   #找到对应的演出时刻，将演出时刻质控
                    time20_23=0
                )
                if models.ticket.objects.filter(studio=studio,date=data,time=time):
                    models.ticket.objects.filter(studio=studio,date=data,time=time).delete()  #根据演出厅 演出时间 演出场次 找到对应的票
                    print("删除票成功")
            re = json.dumps({
                "status":"0",
                "msg":"删除一号演出厅的演出计划成功",

            })
            return HttpResponse(re,content_type="application/json")
        else:
            re = json.dumps({
                "status": "0",
                "msg": "删除演出计划失败",

            })
            return HttpResponse(re, content_type="application/json")

#根据剧目id获取剧目信息
def api_getOperaById(request):
    if request.method=="POST":
        operaId = request.POST.get("operaId",None)
        all_list = list(models.opera.objects.filter(id=operaId))
        # print(all_list)
        if len(all_list) == "0":
            data = []
            return data
        else:
            data = []
            for i in range(len(all_list)):
                d = {}
                d['id'] = all_list[i].id
                d['type'] = all_list[i].type
                d['name'] = all_list[i].name
                d['length'] = all_list[i].length
                d['price'] = all_list[i].price
                d['image'] = all_list[i].image.name
                d['describe'] = all_list[i].describe
                if all_list[i].status == 1:
                    d['status'] = "待上线"
                elif all_list[i].status == 2:
                    d['status'] = "上线中"
                elif all_list[i].status == 3:
                    d['status'] = "已下线"
                data.append(d)
            re=json.dumps({
                "status":"0",
                "msg":"",
                "data":data
            })
            return HttpResponse(re,content_type="application/json")


# 时间  场次  演出厅studio
def api_getTicket(request):
    if request.method=="POST":
        date = request.POST.get("date",None)
        studio = request.POST.get("studio",None)
        time = request.POST.get("time",None)

        ticketList = models.ticket.objects.filter(studio=studio,date=date,time=time)
        print(ticketList[0].status)
        data=[]
        for i in range(len(ticketList)):
            data.append(ticketList[i].status)

        re = json.dumps({
            "status":"0",
            "msg":"success",
            "data":data
        })
        return HttpResponse(re,content_type="application/json")


#购票接口
#参数 行 列 日期 场次  演出厅
def api_setTicket(request):
    if request.method=="POST":
        row = request.POST.get("row",None)            #    5
        col = request.POST.get("col",None)              #  3
        date = request.POST.get("date",None)        #日期  2018-05-05
        time = request.POST.get("time",None)       #场次   1 2 3 4
        studio = request.POST.get("studio",None)       #演出厅  1 2 3 4
        operaname = request.POST.get("operaname",None)        #剧目名
        count = request.POST.get("count",None)          #总金额   50
        account = request.COOKIES.get("account",None)       #用户账号     ios
        # countticket = request.POST.get("countticket",None)  #票数    1
        print(operaname)
        print(account)
        print(count)
        # print(countticket)
        #时间 场次 演出厅 票数 总计消费额 剧目名  用户
        models.ticket.objects.filter(studio=studio,time=time,date=date,row=row,col=col).update(
            status=1
        )
        date1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        setOrder(date1,time,studio,count,operaname,account)

    #调用订单表，将购票数据保存在order表中

        print('购买成功')
        re=json.dumps({
            "status":"0",
            "msg":"购买票成功",
            "data":""
        })
        return HttpResponse(re,content_type="application/json")


#获取已经已经被安排的演出的剧目信息
def api_getOperaList(request):
    if request.method == "POST":

        datas=[]  #保存返回的数据
        playlist = models.schedule1.objects.all()  #获取·1·号剧院的演出计划
        print("playlist= "+ str(playlist))
        for i in range(len(playlist)):
            playTimeList1 = getOD(playlist[i].time8_11)  #获取第一场演出剧目的详细数据
            if len(playTimeList1)!=0:
                # print(str(playTimeList1) + str(playlist[i].data))
                data = playlist[i].data
                time = "8:00-11:00"
                schedule = "一号演出厅"
                dict2 = {"date":data,"schedule":schedule,"time":time}
                dict1 = dict(playTimeList1[0], **dict2)
                datas.append(dict1)
                # print(dict1)

            playTimeList2 = getOD(playlist[i].time12_15)  #获取第二场演出剧目的详细数据
            if len(playTimeList2)!=0:
                # print(str(playTimeList2) + str(playlist[i].data))
                data = playlist[i].data
                time = "12:00-15:00"
                schedule = "一号演出厅"
                dict2 = {"date":data,"schedule":schedule,"time":time}
                dict1 = dict(playTimeList2[0], **dict2)
                # print(dict1)
                datas.append(dict1)

            playTimeList3 = getOD(playlist[i].time16_19)
            if len(playTimeList3) != 0:
                # print(str(playTimeList3) + str(playlist[i].data))
                data = playlist[i].data
                time = "16:00-19:00"
                schedule = "一号演出厅"
                dict2 = {"date":data,"schedule":schedule,"time":time}
                dict1 = dict(playTimeList3[0], **dict2)
                # print(dict1)
                datas.append(dict1)

            playTimeList4 = getOD(playlist[i].time20_23)
            if len(playTimeList4) != 0:
                # print(str(playTimeList3) + str(playlist[i].data))
                data = playlist[i].data
                time = "20:00-23:00"
                schedule = "一号演出厅"
                dict2 = {"date":data,"schedule":schedule,"time":time}
                dict1 = dict(playTimeList4[0], **dict2)
                # print(dict1)
                datas.append(dict1)

        playlist = models.schedule2.objects.all()  #获取·1·号剧院的演出计划
        print("playlist= "+ str(playlist))
        for i in range(len(playlist)):
            playTimeList1 = getOD(playlist[i].time8_11)  #获取第一场演出剧目的详细数据
            if len(playTimeList1)!=0:
                # print(str(playTimeList1) + str(playlist[i].data))
                data = playlist[i].data
                time = "8:00-11:00"
                schedule = "二号演出厅"
                dict2 = {"date":data,"schedule":schedule,"time":time}
                dict1 = dict(playTimeList1[0], **dict2)
                datas.append(dict1)
                # print(dict1)

            playTimeList2 = getOD(playlist[i].time12_15)  #获取第二场演出剧目的详细数据
            if len(playTimeList2)!=0:
                # print(str(playTimeList2) + str(playlist[i].data))
                data = playlist[i].data
                time = "12:00-15:00"
                schedule = "二号演出厅"
                dict2 = {"date":data,"schedule":schedule,"time":time}
                dict1 = dict(playTimeList2[0], **dict2)
                # print(dict1)
                datas.append(dict1)

            playTimeList3 = getOD(playlist[i].time16_19)
            if len(playTimeList3) != 0:
                # print(str(playTimeList3) + str(playlist[i].data))
                data = playlist[i].data
                time = "16:00-19:00"
                schedule = "二号演出厅"
                dict2 = {"date":data,"schedule":schedule,"time":time}
                dict1 = dict(playTimeList3[0], **dict2)
                # print(dict1)
                datas.append(dict1)

            playTimeList4 = getOD(playlist[i].time20_23)
            if len(playTimeList4) != 0:
                # print(str(playTimeList3) + str(playlist[i].data))
                data = playlist[i].data
                time = "20:00-23:00"
                schedule = "二号演出厅"
                dict2 = {"date":data,"schedule":schedule,"time":time}
                dict1 = dict(playTimeList4[0], **dict2)
                # print(dict1)
                datas.append(dict1)

        playlist = models.schedule3.objects.all()  #获取·1·号剧院的演出计划
        print("playlist= "+ str(playlist))
        for i in range(len(playlist)):
            playTimeList1 = getOD(playlist[i].time8_11)  #获取第一场演出剧目的详细数据
            if len(playTimeList1)!=0:
                # print(str(playTimeList1) + str(playlist[i].data))
                data = playlist[i].data
                time = "8:00-11:00"
                schedule = "三号演出厅"
                dict2 = {"date":data,"schedule":schedule,"time":time}
                dict1 = dict(playTimeList1[0], **dict2)
                datas.append(dict1)
                # print(dict1)

            playTimeList2 = getOD(playlist[i].time12_15)  #获取第二场演出剧目的详细数据
            if len(playTimeList2)!=0:
                # print(str(playTimeList2) + str(playlist[i].data))
                data = playlist[i].data
                time = "12:00-15:00"
                schedule = "三号演出厅"
                dict2 = {"date":data,"schedule":schedule,"time":time}
                dict1 = dict(playTimeList2[0], **dict2)
                # print(dict1)
                datas.append(dict1)

            playTimeList3 = getOD(playlist[i].time16_19)
            if len(playTimeList3) != 0:
                # print(str(playTimeList3) + str(playlist[i].data))
                data = playlist[i].data
                time = "16:00-19:00"
                schedule = "三号演出厅"
                dict2 = {"date":data,"schedule":schedule,"time":time}
                dict1 = dict(playTimeList3[0], **dict2)
                # print(dict1)
                datas.append(dict1)

            playTimeList4 = getOD(playlist[i].time20_23)
            if len(playTimeList4) != 0:
                # print(str(playTimeList3) + str(playlist[i].data))
                data = playlist[i].data
                time = "20:00-23:00"
                schedule = "三号演出厅"
                dict2 = {"date":data,"schedule":schedule,"time":time}
                dict1 = dict(playTimeList4[0], **dict2)
                # print(dict1)
                datas.append(dict1)

        playlist = models.schedule4.objects.all()  #获取·1·号剧院的演出计划
        print("playlist= "+ str(playlist))
        for i in range(len(playlist)):
            playTimeList1 = getOD(playlist[i].time8_11)  #获取第一场演出剧目的详细数据
            if len(playTimeList1)!=0:
                # print(str(playTimeList1) + str(playlist[i].data))
                data = playlist[i].data
                time = "8:00-11:00"
                schedule = "四号演出厅"
                dict2 = {"date":data,"schedule":schedule,"time":time}
                dict1 = dict(playTimeList1[0], **dict2)
                datas.append(dict1)
                # print(dict1)

            playTimeList2 = getOD(playlist[i].time12_15)  #获取第二场演出剧目的详细数据
            if len(playTimeList2)!=0:
                # print(str(playTimeList2) + str(playlist[i].data))
                data = playlist[i].data
                time = "12:00-15:00"
                schedule = "四号演出厅"
                dict2 = {"date":data,"schedule":schedule,"time":time}
                dict1 = dict(playTimeList2[0], **dict2)
                # print(dict1)
                datas.append(dict1)

            playTimeList3 = getOD(playlist[i].time16_19)
            if len(playTimeList3) != 0:
                # print(str(playTimeList3) + str(playlist[i].data))
                data = playlist[i].data
                time = "16:00-19:00"
                schedule = "四号演出厅"
                dict2 = {"date":data,"schedule":schedule,"time":time}
                dict1 = dict(playTimeList3[0], **dict2)
                # print(dict1)
                datas.append(dict1)

            playTimeList4 = getOD(playlist[i].time20_23)
            if len(playTimeList4) != 0:
                # print(str(playTimeList3) + str(playlist[i].data))
                data = playlist[i].data
                time = "20:00-23:00"
                schedule = "四号演出厅"
                dict2 = {"date":data,"schedule":schedule,"time":time}
                dict1 = dict(playTimeList4[0], **dict2)
                # print(dict1)
                datas.append(dict1)

        print(datas)
        idlist1=[]
        for i in range(len(datas)):
            print(datas[i].get("id"))
            idlist1.append(datas[i].get("id"))
        idlist=list(set(idlist1))   #idlist保存经过筛选的剧院的id
        returndata=[]
        for i in range(len(datas)):
            for j in range(len(idlist)):
                if datas[i].get("id")==idlist[j]:
                    d={}
                    d["name"]=datas[i].get("name")     #
                    d["length"]=datas[i].get("length")  #
                    d["price"]=datas[i].get("price")   #
                    d["id"]=datas[i].get("id")   #
                    d["describe"]=datas[i].get("describe")  #
                    d["date"]=datas[i].get("date")
                    d["schedule"]=datas[i].get("schedule")
                    d["schedule"]=datas[i].get("schedule")


        print(idlist)

        re = json.dumps(
            {
                "status":"0",
                "msg":"获取演出厅演出计划成功",
                "data":datas
            }
        )
        return HttpResponse(re,content_type="application/json")



def setOrder(date,time,studio,count,operaname,account):

    orderlist=[]
    orderlist.append(time)
    orderlist.append(operaname)
    orderlist.append(studio)
    models.order.objects.create(
        customer=account,
        money=count,
        data=date,
        status=1,
        orderlist=orderlist,

    )
    print('生成流水成功')
    status='0'
    return status


#获取订单信息
def api_getOrder(request):
    if request.method=="POST":
        orderlist = list(models.order.objects.all())
        orderlist = orderlist[::-1]
        data=[]
        for i in range(len(orderlist)):
            d={}
            d['name'] = orderlist[i].customer

            d['date'] = orderlist[i].data
            d['money'] = orderlist[i].money

            orderlist1=orderlist[i].orderlist.strip("'").split("'")
            d['time'] = orderlist1[1]
            d['operaname'] = orderlist1[3]
            d['studio'] = orderlist1[5]

            d['status'] = orderlist[i].status
            data.append(d)
        print(data)

        re = json.dumps({
            "dtatus":"0",
            "msg":"",
            "data":data
        })
        return HttpResponse(re,content_type="application/json")













def manageIndex(request):
    return render(request,'manage/manageIndex.html')

def addOpera(request):
    return render(request,'manage/addOpera.html')

def home(request):
    return render(request,'home.html')

def index(request):
    return render(request,'index.html')

def dh(request):
    return render(request,'dh.html')

def login(request):
    return render(request,'login.html')

def loginError(request):
    return render(request,'loginError.html')

def addUser(request):
    return render(request,'addUser.html')

def manageDh(request):
    return render(request,'manage/manageDh.html')

def manageHome(request):
    return render(request,'manage/manageHome.html')

def statusOpera(request):
    return render(request,'manage/statusOpera.html')

def managePlay(request):
    return render(request,'manage/managePlay.html')

def findPlay(request):
    return render(request,'manage/findPlay.html')

def findPlay2(request):
    return render(request,'manage/findPlay2.html')

def findPlay3(request):
    return render(request,'manage/findPlay3.html')

def findPlay4(request):
    return render(request,'manage/findPlay4.html')

def opera(request):
    return render(request,'opera/opera.html')

def showOpera(request):
    return render(request,'opera/showOpera.html')

def checkSeat(reauest):
    return render(reauest,'opera/checkSeat.html')

def ticket(reauest):
    return render(reauest,'ticket.html')

def showOrder(request):
    return render(request,'manage/showOrder.html')

def showOrderR(request):

    return HttpResponseRedirect("/showOpera")
