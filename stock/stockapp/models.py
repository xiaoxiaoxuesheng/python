#-*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
# Create your models here.

SEX_CHOICES = (
    ('0','男'),
    ('1','女'),
)

ORDER_CHOICES = (
    (0, 'Buy'),
    (1, 'Sell'),
)

ORDER_STATE = (
    (0, 'deity'),
    (1, 'deal'),
    (2, 'delete'),
    (3, 'cancel')
)


class User(AbstractUser):
    gender = models.CharField(choices = SEX_CHOICES,max_length = 1,verbose_name = '性别')
    age = models.IntegerField(blank=True, null=True,verbose_name='年龄')
    profession = models.CharField(max_length = 128,verbose_name='职业')
    #可以为空
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='QQ号码')
    #不能重复
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')
    money = models.FloatField(blank=True, null=True,  verbose_name='资金')
    frozen_money = models.FloatField(blank=True, null=True, unique=True, verbose_name='冻结资金')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username

class Deal(models.Model):
    genre = models.BooleanField(default = True ,verbose_name = '买卖类型')
    number = models.IntegerField(verbose_name = '股票编码')
    amount = models.IntegerField(default = 100,verbose_name = '买卖数量')
    figure = models.FloatField(verbose_name = '成交金额')
    time = models.DateTimeField(auto_now_add=True,verbose_name = '交易时间')
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = '交易记录'
        verbose_name_plural = verbose_name
        ordering = ['-time']

    def __str__(self):
        return str(self.time)

class Hold(models.Model):
    number = models.IntegerField(verbose_name = '股票编码')
    amount = models.IntegerField(default = 100,verbose_name = '持有数量')
    frozen_amount = models.IntegerField(default = 100,verbose_name = '冻结数量')
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = '持仓信息'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.number)

class Stock(models.Model):
    number = models.IntegerField(verbose_name= '股票编码')
    company_name = models.CharField(max_length = 64,verbose_name='公司名称')
    flow_in = models.FloatField(verbose_name = '总流入')
    flow_out = models.FloatField(verbose_name= '总流出')
    impressum = models.TextField(verbose_name='公司介绍')
    # amount = models.FloatField(verbose_name = '总股数')
    user = models.ManyToManyField(User)

    class Meta:
        verbose_name = '股票信息'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.company_name


class Link(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    callback_url = models.URLField(verbose_name='url地址')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.title


class BOSStock(models.Model):
    genre = models.IntegerField(verbose_name='买卖类型',choices=ORDER_CHOICES, default=0)
    number = models.IntegerField(verbose_name='股票编码')
    amount = models.IntegerField(default=100, verbose_name='买卖数量')
    totles = models.FloatField(verbose_name='挂单金额')
    ntotle = models.FloatField(verbose_name='当前金额')
    time = models.DateField(auto_now_add=True, verbose_name='挂单时间')
    state = models.IntegerField(verbose_name='状态',choices=ORDER_STATE, default=0)
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = '买卖挂单'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            data[f.name] = f.value_from_object(self)
        return data

    def toDict(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


class DealStock(models.Model):
    dealno = models.IntegerField(verbose_name='成交单号')
    number = models.IntegerField(verbose_name='股票编码')
    damount =  models.IntegerField(default=100, verbose_name='成交数量')
    totles = models.FloatField(verbose_name='成交金额')
    time = models.DateTimeField(auto_now_add=True, verbose_name='成交时间')
    suser = models.ForeignKey(User,related_name='suser')
    buser = models.ForeignKey(User,related_name='buser')

    class Meta:
        verbose_name = '成交单'
        verbose_name_plural = verbose_name
        ordering = ['id']