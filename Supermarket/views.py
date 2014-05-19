from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login as djLogin, logout as djLogout
from django.contrib.auth.models import User as djUser
from django.views.decorators.csrf import csrf_exempt

from Supermarket.models import *
import json
import datetime
import string
import operator
from collections import OrderedDict

def gettop(start_date, end_date, flag = 1):
    sits = SimilarItem.objects.all()
    recs = {}
    for sit in sits:
        try:
            recs[sit] = Record.objects.filter(item = sit).filter(date__range = (start_date, end_date))
        except:
            recs[sit] = []
    if flag == 1:
        for rec in recs:
            qq = 0
            for i in recs[rec]:
                qq += i.quantity
            recs[rec] = qq
    else:
        for rec in recs:
            count = 0
            for i in recs[rec]:
                count += i.profit
            recs[rec] = count
    xx = sorted(recs.iteritems(), key = operator.itemgetter(1))[::-1][:10]
    return OrderedDict(xx)

def login(request):
    if(request.user.is_authenticated()):
        try:
            user = SalesClerk.objects.get(user__username = str(request.user.username))
        except:
            try:
                user = Manager.objects.get(user__username = str(request.user.username))
            except:
                try:
                    user = Employee.objects.get(user__username = str(request.user.username))
                except:
                    return HttpResponseRedirect('invalidLogin')
        if type(user) is SalesClerk:
            return HttpResponseRedirect('salesClerk')
        elif type(user) is Employee:
            return HttpResponseRedirect('employee')
        elif type(user) is Manager:
            return HttpResponseRedirect('manager')
    return render(request,'login.html', {'message':''})

def invalidLogin(request):
    return render(request,'login.html', {'message':'Invalid User ID or Password'})

def logged_out(request):
    return render(request,'login.html', {'message':'Successfully Logged Out'})

def logout(request):
    djLogout(request)
    return HttpResponseRedirect('logged_out')

def checkCreds(request):
    user = authenticate(username = request.GET['login_userid'], password = request.GET['login_passwd'])
    if user is not None:
        djLogin(request, user)
        return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('invalidLogin')

def salesClerk(request):
    if(request.user.is_authenticated()):
        try:
            user = SalesClerk.objects.get(user__username = str(request.user.username))
        except:
            return HttpResponseRedirect('login')
        # get all items and top 10's
        return render(request,'salesClerk.html', {'user':user})
    else:
        return HttpResponseRedirect('invalidLogin')

def employee(request):
    if(request.user.is_authenticated()):
        try:
            user = Employee.objects.get(user__username = str(request.user.username))
        except:
            return HttpResponseRedirect('login')
        sits = SimilarItem.objects.all()
        return render(request,'employee.html', {'sits': sits, 'user': user})
    else:
        return HttpResponseRedirect('invalidLogin')

def manager(request):
    if(request.user.is_authenticated()):
        try:
            user = Manager.objects.get(user__username = str(request.user.username))
        except:
            return HttpResponseRedirect('login')
        sits = SimilarItem.objects.all()
        # TODO : sort accordingly
        top = gettop(datetime.date.today(), datetime.date.today())
        top10 = gettop(datetime.date.today() - datetime.timedelta(days = 10), datetime.date.today())
        return render(request,'manager.html', {'sits': sits, 'top': top, 'top10': top10, 'user': user})
    else:
        return HttpResponseRedirect('invalidLogin')

def searchItem(request):
    if(request.user.is_authenticated()):
        try:
            user = Manager.objects.get(user__username = str(request.user.username))
        except:
            try:
                user = Employee.objects.get(user__username = str(request.user.username))
            except:
                return HttpResponseRedirect('login')
        flag = type(user) is Employee
        sits = user.searchItem(request.GET['term'])
        return render(request, 'search.html', {"sits": sits, 'flag': flag})
    else:
        return HttpResponseRedirect('invalidLogin')

def itemInfo(request, item_id):
    if(request.user.is_authenticated()):
        try:
            user = Manager.objects.get(user__username = str(request.user.username))
        except:
            try:
                user = Employee.objects.get(user__username = str(request.user.username))
            except:
                return HttpResponseRedirect('login')
        manager = type(user) is Manager
        sit = SimilarItem.objects.get(pk = item_id)
        return render(request, 'itemInfo.html', {"sit": sit, "manager": manager})
    else:
        return HttpResponseRedirect('invalidLogin')

def changePrice(request):
    if(request.user.is_authenticated()):
        try:
            user = Manager.objects.get(user__username = str(request.user.username))
        except:
            return HttpResponseRedirect('login')
        return HttpResponse(user.changePrice(int(request.GET['id']), request.GET['price']))
    else:
        return HttpResponseRedirect('invalidLogin')

def newUser(request):
    if(request.user.is_authenticated()):
        try:
            user = Manager.objects.get(user__username = str(request.user.username))
        except:
            return HttpResponseRedirect('login')
        return render(request, 'newUser.html', {})
    else:
        return HttpResponseRedirect('invalidLogin')

def newUserReg(request):

    if(request.user.is_authenticated()):
        try:
            u = Manager.objects.get(user__username = str(request.user.username))
        except:
            return HttpResponseRedirect('login')
        if(int(request.POST['type']) == 1):
            s = SalesClerk(user = djUser.objects.create_user(request.POST['userid'], password = request.POST['passwd']))
        else:
            s = Employee(user = djUser.objects.create_user(request.POST['userid'], password = request.POST['passwd']))
        s.save()
        return HttpResponse("success")
    else:
        return HttpResponseRedirect('invalidLogin')

def toptop(request):
    if(request.user.is_authenticated()):
        try:
            u = Manager.objects.get(user__username = str(request.user.username))
        except:
            return HttpResponseRedirect('login')
        if request.GET['flag'] == "1":
            recs = gettop(datetime.date.today() - datetime.timedelta(days = int(request.GET['duration'])), datetime.date.today())
        else:
            recs = gettop(datetime.date.today() - datetime.timedelta(days = int(request.GET['duration'])), datetime.date.today(), "2")
        return render(request, 'toptop.html', {"recs": recs})
    else:
        return HttpResponseRedirect('invalidLogin')

def newItem(request):
    if(request.user.is_authenticated()):
        try:
            user = Employee.objects.get(user__username = str(request.user.username))
        except:
            return HttpResponseRedirect('login')
        if len(Item.objects.filter(barcode = request.POST.get('barcode', '000000'))) > 0:
            return HttpResponse('already')
        aaa = [ int(request.POST.get('itemid', 1)),
                request.POST.get('barcode', '000000'),
                int(request.POST.get('quantity', 0)),
                float(request.POST.get('mprice', 0)),
                float(request.POST.get('sprice', 0)),
                float(request.POST.get('rprice', 0))]
        p = user.addItem(aaa)
        return HttpResponse(p)
    else:
        return HttpResponseRedirect('invalidLogin')

def newSItem(request):
    if(request.user.is_authenticated()):
        try:
            u = Employee.objects.get(user__username = str(request.user.username))
        except:
            return HttpResponseRedirect('login')
        p = SimilarItem(name = request.POST['name'])
        p.save()
        return HttpResponse('success')
    else:
        return HttpResponseRedirect('invalidLogin')

def regItem(request):
    if(request.user.is_authenticated()):
        try:
            u = SalesClerk.objects.get(user__username = str(request.user.username))
        except:
            return HttpResponseRedirect('login')
        it = Item.objects.filter(barcode = request.GET['bc']).values()[0]
        it['name'] = Item.objects.filter(barcode = request.GET['bc'])[0].similar_item.name
        it.pop('recent')
        return HttpResponse(json.dumps(it), content_type = "application/json")
    else:
        return HttpResponseRedirect('invalidLogin')

def updateRecords(request):
    if(request.user.is_authenticated()):
        try:
            u = SalesClerk.objects.get(user__username = str(request.user.username))
        except:
            return HttpResponseRedirect('login')
        for r in request.POST:
            quan = int(request.POST[r])
            try:
                it = Item.objects.get(pk = r[5:-1])

                it.quantity -= quan
                it.save()
                r = Record(item = it.similar_item,
                            quantity = quan,
                            profit = quan * ((it.sale_price) - (it.real_price)))
                r.save()
            except:
                return HttpResponse('wrong')
        return HttpResponse('peace')
    else:
        return HttpResponseRedirect('invalidLogin')

def getStats(request):
    if(request.user.is_authenticated()):
        try:
            u = Manager.objects.get(user__username = str(request.user.username))
        except:
            return HttpResponseRedirect('login')
        try:
            start = request.GET['start_date'].split('-')
            end = request.GET['end_date'].split('-')
            s = datetime.date(int(start[0]), int(start[1]), int(start[2]))
            e = datetime.date(int(end[0]), int(end[1]), int(end[2]))
            if not((s <= e) and (e <= datetime.date.today())):
                return HttpResponse('invalid')
            arr = u.getStats(int(request.GET['itemid']), s, e, int(request.GET['flag']))
            arr2 = {}
            for a in arr:
                arr2[a.strftime("%Y-%m-%d")] = arr[a]
            return HttpResponse(json.dumps(arr2), content_type = "application/json")
        except Exception, ex:
            print "ex = " + str(ex)
            return HttpResponse('invalid')
        return HttpResponse('peace')
    else:
        return HttpResponseRedirect('invalidLogin')