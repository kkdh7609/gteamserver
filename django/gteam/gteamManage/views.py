from django.shortcuts import render
from django.http import HttpResponse
from gteamManage import firebase_util
from django.shortcuts import redirect
# Create your views here.
tt = "123"
tempId = ""


class Data:
    def __init__(self, num, name, email, role, status):
        self.num = num
        self.name = name
        self.email = email
        self.role = role
        self.status = status


class StadiumData:
    def __init__(self, num, name, location, phone):
        self.num = num
        self.name = name
        self.location= location
        self.phone = phone


class RegData:
    def __init__(self, collectId, num, name, email, role, regNum, keyId, btn, val):
        self.collectId = collectId
        self.num = num
        self.name = name
        self.email = email
        self.role = role
        self.regNum = regNum
        self.keyId = keyId
        self.btn = btn
        self.val = val


def users(request):
    db = firebase_util.setFireStore()
    doc_ref = db.collection(u'user').stream()
    arr = []
    cnt = 1
    for doc in doc_ref:
        temp_doc = doc.to_dict()
        name = temp_doc["name"]
        email = temp_doc["email"]
        if temp_doc["isUser"]:
            role = "user"
        else:
            role = "manager"
        status = "Active"
        arr.append(Data(cnt, name, email, role, status))
        cnt += 1

    context = {'arr': arr, 'arrLen': len(arr)}

    return render(request, 'gteamManage/user.html', context)


def stadium(request):
    db = firebase_util.setFireStore()
    doc_ref = db.collection(u'stadium').stream()
    arr = []
    cnt = 1
    for doc in doc_ref:
        temp_doc = doc.to_dict()
        name = temp_doc["stadiumName"]
        phone = temp_doc["telephone"]
        location = temp_doc["location"]
        arr.append(StadiumData(cnt, name, location, phone))
        cnt += 1

    context = {'arr': arr, 'arrLen': len(arr)}

    return render(request, 'gteamManage/stadium.html', context)


def manager(request):
    global tt, tempId
    db = firebase_util.setFireStore()
    doc_ref = db.collection(u'managerReg').stream()
    arr = []
    cnt = 1
    for doc in doc_ref:
        temp_doc = doc.to_dict()
        collectId = doc.id
        name = temp_doc["name"]
        email = temp_doc["email"]
        keyId = temp_doc["key"]
        regNum = temp_doc["businessNum"]
        role = "manager"
        btn = f"Accept{cnt}"
        val = keyId
        arr.append(RegData(collectId, cnt, name, email, role, regNum, keyId, btn, val))
        cnt += 1
    tt = request.POST.get(f"Accept")
    if tt:
        tempId = tt.split(" ")[0]
        for tempNum in range(0, len(arr)):
            if arr[tempNum].keyId == tempId:
                db.collection(u'user').document(arr[tempNum].keyId).update({"permission": True})
                db.collection(u'managerReg').document(arr[tempNum].collectId).delete()
        return redirect('/manager')

    context = {'arr': arr, 'arrLen': len(arr)}
    return render(request, 'gteamManage/manager.html', context)


def home(request):
    return render(request, 'gteamManage/home.html')


def post_call(request):
    typeId = int(request.POST.get("type"))
    target = request.POST.get("target")
    try:
        token = firebase_util.push_notification(typeId, target)
        return HttpResponse(token)
    except Exception:
        HttpResponse(Exception)
