from django.db import models

# Create your models here.


enum_user=(
    (1,'manager'),
    (2,'employee')
)


# 用户表
class user(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=100,null=False)   #工号
    name = models.CharField(max_length=100,null=False)   #姓名
    account = models.CharField(max_length=160,null=False)    #账号
    password = models.CharField(max_length=160,null=False)    #密码
    department = models.IntegerField(choices=enum_user,null=False)   #分类
    def __str__(self):
        return self.name

#演出厅表
class studio(models.Model):
    id = models.AutoField(primary_key=True)
    col = models.IntegerField(null=False)   #行
    row = models.IntegerField(null=False)  #列
    play_id = models.IntegerField(null=True)   #当前上线的剧目id
    # def __str__(self):
    #     return self.id

#座位表
class seat1(models.Model):
    id = models.AutoField(primary_key=True)
    col = models.IntegerField(null=False)   #行
    row = models.IntegerField(null=False)  #列
    # def __str__(self):
    #     return self.id

# 座位表
class seat2(models.Model):
    id = models.AutoField(primary_key=True)
    col = models.IntegerField(null=False)   #行
    row = models.IntegerField(null=False)  #列
    #
    # def __str__(self):
    #     return self.id

# 座位表
class seat3(models.Model):
    id = models.AutoField(primary_key=True)
    col = models.IntegerField(null=False)   #行
    row = models.IntegerField(null=False)  #列

    # def __str__(self):
    #     return self.id

# 座位表
class seat4(models.Model):
    id = models.AutoField(primary_key=True)
    col = models.IntegerField(null=False)   #行
    row = models.IntegerField(null=False)  #列
    #
    # def __str__(self):
    #     return self.id

# 座位表

# class seat5(models.Model):
#     id = models.AutoField(primary_key=True)
#     col = models.IntegerField  # 行
#     row = models.IntegerField  # 列
#
#     def __str__(self):
#         return self.id



#消费者表
class customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,null=False)  #消费者姓名
    account = models.CharField(max_length=160,null=False)  #账号
    password = models.CharField(max_length=160,null=False)  #密码

    def __str__(self):
        return self.name


enum_opera=(
    (1,'wait'),
    (2,'on'),
    (3,'down')
)
#剧目表
class opera(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=160,default='未分类')  #剧目分类
    name = models.CharField(max_length=160,null=False)    #剧目名称
    describe = models.CharField(max_length=2000,null=True)   #剧目的描述
    image = models.ImageField(upload_to='img',null=True,default="None")    #剧目的图片二进制
    length = models.CharField(max_length=160,null=False)     #剧目时长
    price = models.CharField(max_length=160,null=False)    #剧目票价
    status = models.IntegerField(choices=enum_opera,default='1')  #剧目状态

    def __str__(self):
        return self.name

#时刻表
class schedule1(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.CharField(max_length=200,null=False)   #日期 1 2 3 4 5 6 7 8
    time8_11 = models.IntegerField(null=True)
    time12_15 = models.IntegerField(null=True)
    time16_19 = models.IntegerField(null=True)
    time20_23 = models.IntegerField(null=True)

    def __str__(self):
        return self.data

#时刻表
class schedule2(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.CharField(max_length=200,null=False)   #日期
    time8_11 = models.IntegerField(null=True)
    time12_15 = models.IntegerField(null=True)
    time16_19 = models.IntegerField(null=True)
    time20_23 = models.IntegerField(null=True)

    def __str__(self):
        return self.data

#时刻表
class schedule3(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.CharField(max_length=200,null=False)   #日期
    time8_11 = models.IntegerField(null=True)
    time12_15 = models.IntegerField(null=True)
    time16_19 = models.IntegerField(null=True)
    time20_23 = models.IntegerField(null=True)

    def __str__(self):
        return self.data

#时刻表
class schedule4(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.CharField(max_length=200,null=False)   #日期
    time8_11 = models.IntegerField(null=True)
    time12_15 = models.IntegerField(null=True)
    time16_19 = models.IntegerField(null=True)
    time20_23 = models.IntegerField(null=True)

    def __str__(self):
        return self.data




enum_ticket=(
    (1,'sold'),
    (2,'not'),
    (3,'wait')
)
#票表
class ticket(models.Model):
    id = models.AutoField(primary_key=True)    #票id
    operaId = models.CharField(max_length=10,default="None")   #剧目id
    studio = models.CharField(max_length=10,default="None")   #演出厅

    date = models.CharField(max_length=20,default="None")    #日期
    time = models.CharField(max_length=20,default="None")    #场次
    name = models.CharField(max_length=20,default="None")     #名称
    price = models.CharField(max_length=10,default="None")    #价格
    length = models.CharField(max_length=10,default="None")

    row = models.IntegerField(null=False,default=0)     #行
    col = models.IntegerField(null=False,default=0)     #列
    status = models.IntegerField(choices=enum_ticket,default='2')  #状态

    # def __str__(self):
    #     return self.status


enum_order = (
    (1, 'buy'),
    (2, 'unbuy')
)
#订单表
class order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.CharField(max_length=160,null=True)   #购买者
    money = models.IntegerField(null=False)   #总金额
    data = models.CharField(max_length=160,null=False)  #订单时间
    orderlist = models.CharField(max_length=200,null=False)  #订单内容
    status = models.IntegerField(choices=enum_order,default='1')  #订单分类

    def __str__(self):
        return self.data


