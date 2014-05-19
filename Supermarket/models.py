from django import forms
from django.conf import settings
from django.utils import timezone

from django.db import models
from django.db.models import Q
from django.db.models.fields.related import OneToOneField

import datetime
import operator
from collections import OrderedDict 

def getDateArr(start_date, end_date):
    res = {}
    d = start_date
    delta = datetime.timedelta(days = 1)
    while d <= end_date:
        res[d] = 0
        d += delta
    print OrderedDict(sorted(res.iteritems(), key = operator.itemgetter(0)))
    return OrderedDict(sorted(res.iteritems(), key = operator.itemgetter(0)))

class User(models.Model):
    user = OneToOneField(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return self.user.username


class SalesClerk(User):

    # bc is barcode
    def registerItem(self, bc):
        results = Item.objects.filter(Q(barcode = bc))
        return results

    # itemsis - [[item_id, quantity], ...]
    # TODO : if <= 0, do something
    def updateItems(self, itemsis):
        try:
            for itemi in itemsis:
                i = Item.objects.get(pk = itemi[0])
                i.quantity -= itemi[1]
            i.save()
            return True
        except Exception, e:
            return False
        

class Employee(User):

    def searchItem(self, term):
        results = SimilarItem.objects.filter(name__contains = term)
        return results

    # TODO : see if already exists
    def addItem(self, item):
        try:
            i = Item(similar_item = SimilarItem.objects.get(pk = item[0]),
                     barcode = item[1],
                     quantity = item[2],
                     max_price = item[3],
                     sale_price = item[4],
                     real_price = item[5],
                    )
            i.save()
            return True
        except Exception, e:
            print e
            return False

    def updateItem(self, item, quan):
        try:
            i = Item.objects.get(pk = item)
            i.quantity = quan
            i.save()
            return True
        except Exception, e:
            return False
        

class Manager(Employee):

    def getStats(self, item, start_date, end_date, flag):
        try:
            try:
                recs = Record.objects.filter(date__range = (start_date, end_date)).filter(item = item)
            except:
                recs = []
            arr = getDateArr(start_date, end_date)
            if flag == 1:
                for rec in recs:
                    print arr[rec.date]
                    arr[rec.date] += rec.quantity
            else:
                for rec in recs:
                    arr[rec.date] += rec.profit
            return arr
        except Exception, e:
            raise e

    def changePrice(self, item, price):
        i = Item.objects.get(pk = item)
        if(price < i.real_price):
            return "less"
        elif (datetime.date.today() - i.recent).days < 1:
            return "notagain"
        else:
            self.changePrice2(item, price)

    def changePrice2(self, item, price):
        i = Item.objects.get(pk = item)
        i.sale_price = float(price)
        i.recent = datetime.date.today()
        i.save()


class SimilarItem(models.Model):
    name = models.CharField(max_length = 64)

    def __unicode__(self):
        return self.name

class Item(models.Model):
    similar_item = models.ForeignKey(SimilarItem)
    barcode = models.CharField(max_length = 64)
    quantity = models.IntegerField(default = 0)
    max_price = models.FloatField()
    sale_price = models.FloatField()
    recent = models.DateField('Recently modified at', default = datetime.date.today)
    real_price = models.FloatField()

    def __unicode__(self):
        return "of " + self.similar_item.name

class Record(models.Model):
    item = models.ForeignKey(SimilarItem)
    quantity = models.IntegerField()
    profit = models.FloatField()
    date = models.DateField(auto_now_add = True, blank = True)

    def __unicode__(self):
        return "of " + self.item.name