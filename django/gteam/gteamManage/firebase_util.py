import firebase_admin
from firebase_admin import credentials, firestore, datetime, messaging
from multiprocessing import Process

def setFireStore():
    if not len(firebase_admin._apps):
        cred = credentials.Certificate("service_key.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

def push_notification(typeId, target):   # type1은 예약접수 시작, 2는 주인에게 알림, 3는 예약완료 알 림
    db = setFireStore()
    if typeId == 1:
        gameId = target
        doc_ref = db.collection(u'game3').document(gameId)
        userList = doc_ref.get().get(u'userList')
        user_ref = db.collection(u'user').stream()

        arr = []
        th_arr = []
        for doc in user_ref:
            if(doc.to_dict()['email'] in userList):
                new_user_ref = db.collection(u'token').document(doc.id)
                token = new_user_ref.get().get(u'token')
                arr.append(token)

        for token in arr:
            th_arr.append(Process(target=push_message, args=(token, "예약접수", f"{doc_ref.get().get(u'gameName')} 게임의 예약접수가 시작되었습니다.")))
        for th in th_arr:
            th.start()
        for th in th_arr:
            th.join()
        return "Success"

    elif typeId == 2:
        stadiumId = target
        doc_ref = db.collection(u'stadium').document(stadiumId)
        ownerId = doc_ref.get().get('ownerId')
        owner_ref = db.collection(u'token').document(ownerId)
        token = owner_ref.get().get('token')
        title = "예약접수"
        body = "예약접수가 들어왔습니다."
        push_message(token, title, body)
        return token

    else:
        gameId = target
        doc_ref = db.collection(u'game3').document(gameId)
        userList = doc_ref.get().get(u'userList')
        user_ref = db.collection(u'user').stream()

        arr = []
        th_arr = []
        for doc in user_ref:
            if (doc.to_dict()['email'] in userList):
                new_user_ref = db.collection(u'token').document(doc.id)
                token = new_user_ref.get().get(u'token')
                arr.append(token)

        for token in arr:
            th_arr.append(Process(target=push_message, args=(token, "예약완료", f"{doc_ref.get().get(u'gameName')} 게임의 예약접수가 완료되었습니다.")))
        for th in th_arr:
            th.start()
        for th in th_arr:
            th.join()
        return "Success"


def push_message(token, title, body):
    token = token
    message = messaging.Message(
        android=messaging.AndroidConfig(
            ttl=datetime.timedelta(seconds=3600),
            priority='normal',
            notification=messaging.AndroidNotification(
                title = title,
                body = body,
                icon='',
                color='#f45342',
                sound='default'
            )
        ),
        token = token
    )

    try:
        response = messaging.send(message)
        print("Successfully sent message:", response)
    except Exception:
        print(Exception)

    return
