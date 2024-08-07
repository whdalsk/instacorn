from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.http import JsonResponse
# Create your views here.
def main(request):
    select = int(request.GET.get('select'))
    if select == 1: # chatList 가져오기
        curId = int(request.GET.get('curId'))
        chats_list = setChats(curId)
        return JsonResponse(chats_list, safe=False)
    elif select == 2: # send
        dm = str(request.GET.get('dm'))
        me = int(request.GET.get('me'))
        you = int(request.GET.get('you'))
        # return HttpResponse("Saved!")
        return JsonResponse(sendDM(dm, me, you), safe=False)
    elif select == 3: # receive
        dm = str(request.GET.get('dm'))
        me = int(request.GET.get('me'))
        you = int(request.GET.get('you'))
        # return HttpResponse("Saved!")
        return JsonResponse(receiveDM(dm, me, you), safe=False)
    else:
        return HttpResponse("xx?")

def sendDM(dm, me, you):
    cursor = connection.cursor()
     
    dm_room = f"""
            SELECT dr_host, dr_guest
            FROM dm_room
            WHERE dr_host = {me}
        """
    cursor.execute(dm_room)
    rows = cursor.fetchall()
    tu = (me, you)
    # 방이 없으면 방 생성 양쪽 다
    if tu not in rows:
        create_dmroom = """
            INSERT INTO dm_room (dr_host, dr_guest)
            VALUES (%s, %s), (%s, %s)
        """
        cursor.execute(create_dmroom, [me, you, you, me])
        connection.commit()  # 변경 사항 저장
        
    
    insert_query = """
            INSERT INTO Messages (sender_id, receiver_id, message_text)
            VALUES (%s, %s, %s)
            """
           
    cursor.execute(insert_query, [me, you, dm])
    connection.commit()  # 변경 사항 저장
    update_time = """
        UPDATE dm_room
        SET created_at = CURRENT_TIMESTAMP
        WHERE (dr_host =%s AND dr_guest =%s) OR (dr_host =%s AND dr_guest =%s)
    """
    cursor.execute(update_time, [me, you, you, me])
    connection.commit()  # 변경 사항 저장
    print("데이터가 성공적으로 저장되었습니다.ssss")        
    # pass
    return setChats(me)

def receiveDM(dm, me, you):
    cursor = connection.cursor()
     
    dm_room = f"""
            SELECT dr_host, dr_guest
            FROM dm_room
            WHERE dr_guest = {me}
        """
    cursor.execute(dm_room)
    rows = cursor.fetchall()
    tu = (you, me)
    # 방이 없으면 방 생성 양쪽 다
    if tu not in rows:
        create_dmroom = """
            INSERT INTO dm_room (dr_host, dr_guest)
            VALUES (%s, %s), (%s, %s)
        """
        cursor.execute(create_dmroom, [me, you, you, me])
        connection.commit()  # 변경 사항 저장
        
    insert_query = """
            INSERT INTO Messages (sender_id, receiver_id, message_text)
            VALUES (%s, %s, %s)
            """
           
    cursor.execute(insert_query, [you, me, dm])
    connection.commit()  # 변경 사항 저장
    
    update_time = """
        UPDATE dm_room
        SET created_at = CURRENT_TIMESTAMP
        WHERE (dr_host =%s AND dr_guest =%s) OR (dr_host =%s AND dr_guest =%s)
    """
    cursor.execute(update_time, [me, you, you, me])
    connection.commit()  # 변경 사항 저장
    print("데이터가 성공적으로 저장되었습니다.ssss")        
    # pass
    return setChats(me)

def setChats(id):
    cursor = connection.cursor()
    # dm romm 생성
    dm_room = f"""
            SELECT i.m_name, i.m_no, d.created_at
            FROM dm_room d inner join insta_member i on d.dr_guest = i.m_no  
            WHERE d.dr_host = {id}
            ORDER BY created_at ASC
    """
    # messages
    messages = f"""
            SELECT sender_id, receiver_id, message_text, sent_at
            FROM Messages
            WHERE sender_id = {id} or receiver_id = {id}
            ORDER BY sent_at ASC
    """
    cursor.execute(dm_room)
    rows = cursor.fetchall()
    name = None
    chats = {}  # 채팅 데이터를 저장할 딕셔너리
    # 방 만들기
    for row in rows:
        createdat = row[2]
        name = row[0]
        i_id = row[1]
        chats[i_id] = {
            "id": i_id,
            "name": name,
            "messages":[],
            "createdat":createdat.strftime("%Y/%m/%d %H:%M:%S"),
            } # print(charts) = {i_id: "name"}
        # 내가 보냈냐 안 보냈냐 확인 
        # chats[partner_id]['messages'].append({
        #     'text': message_text,
        #     'sent_at': sent_at,
        # })
    # receive가 i_id
    cursor.execute(messages)
    rows = cursor.fetchall()
    # 메세지 내용 추가하기
    for row in rows:
        sent_at = row[3]
        message_text = row[2]
        receiver_id = row[1]
        sender_id = row[0]
        a = lambda x: x if x != id else sender_id
        if sender_id == id:
            chats[a(receiver_id)]['messages'].append({
            'text': message_text,
            'sent_at': sent_at,
            'send': True,
            'name':name,
        })
        else:
            chats[a(receiver_id)]['messages'].append({
            'text': message_text,
            'sent_at': sent_at,
            'send': False,
            'name':name,
        })
    chats_list = list(chats.values())
    return chats_list
