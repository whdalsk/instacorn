from django.shortcuts import render
from django.shortcuts import redirect
from django.db  import connection, DatabaseError
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpResponse
from django.db.models.query_utils import Q
from django.core.exceptions import ObjectDoesNotExist
# from .models import InstaMember

from django.core.mail import EmailMessage
import string
import random
import hashlib
import base64

from django.contrib.auth.hashers import pbkdf2


# Create your views here.
def hashing_password(password):
    count = random.randint(16, 21)
    string_pool = string.ascii_letters + string.digits + string.punctuation
    m_salt = "".join(random.choices(string_pool, k=count))
    hashedpw = hashlib.md5(str(password + m_salt).encode('utf-8')).hexdigest()

    return m_salt, hashedpw
#로그인

def inslogin(request):
    if request.method=='GET':
        return render(request, 'index.html')
    
    else:
        m_email = request.POST.get('m_email')
        password = request.POST.get('password')

        try:
            cursor = connection.cursor()
# m_salt 비밀번호 보안 강화
            msg = "select m_email, password, m_salt from insta_member where m_email = %s"
            cursor.execute(msg, [m_email])
            data = cursor.fetchone()
            
#아이디가 틀렸을 때
            if not data:
                messages.error(request, '아이디나 비밀번호가 일치하지 않습니다')
                return redirect('inslogin.do')

            m_email, regpw, m_salt = data

            # 디버깅을 위해 데이터 출력
            print(f"DB regpw: {regpw}")
            print(f"DB m_salt: {m_salt}")

            # MD5와 저장된 솔트를 사용하여 비밀번호를 검증
            hashedpw = hashlib.md5(str(password + m_salt).encode('utf-8')).hexdigest()

            # 해시된 비밀번호 출력
            print(f"Input hashedpw: {hashedpw}")
            
            if hashedpw != regpw:
                messages.error(request, '아이디나 비밀번호가 일치하지 않습니다')
                return redirect('inslogin.do')

            request.session['m_email'] = m_email
            return render(request, 'instacorn/main.html')
                
        except Exception as e:
            connection.rollback()
            print('failed login', e)
            messages.error(request, '에러 발생')
            
    return render(request, 'instacorn/main.html')

#def 로그아웃
def inslogout(request):
    if request.session.get('m_email'):
        del (request.session['m_email'])
    return redirect('inslogin.do')

#회원가입
def insjoin(request):
    if request.method=='GET':
        return render(request, 'instacorn/insjoin.html')
    
    else:
        m_email = request.POST.get('m_email')
        m_name = request.POST.get('m_name')
        m_id = request.POST.get('m_id')
        password = request.POST.get('password')
        

        try:
            with connection.cursor() as cursor:
                msg="select * from insta_member where m_id = (%s)"
                cursor.execute(msg, (m_id, ))
                data_id = cursor.fetchall()
                print('data_id', data_id)

                if len(data_id) != 0:
                    messages.error(request, '이미 존재하는 아이디입니다. 다른 아이디를 사용해주세요.')
                    return redirect('insjoin.do')
                
                msg="select * from insta_member where m_email = (%s)"
                cursor.execute(msg, (m_email, ))
                data_email = cursor.fetchall()
                print('data_email', data_email)

                if len(data_email) != 0:
                    messages.error(request, '이미 존재하는 이메일입니다. 다른 이메일를 사용해주세요.')
                    return redirect('insjoin.do')
            
                m_salt, hashedpw = hashing_password(password)
                msg="insert into insta_member(m_id, password, m_name, m_email, m_salt) values(%s, %s, %s, %s, %s)"
                cursor.execute(msg, (m_id, hashedpw, m_name, m_email, m_salt))
                
                if '@' not in m_email:
                    messages.error(request, '유효한 이메일 주소를 입력해주세요.')
                    return render(request, 'instacorn/insjoin.html')
                
            messages.success(request, '회원가입 완료, 로그인을 해주세요.')
            return redirect('inslogin.do')
            
            # 이메일 인증을 위한 토큰 생성 및 이메일 전송
           
        except DatabaseError as e:
            connection.rollback()
            print("Database error:", e)
            messages.error(request, '회원가입 중 오류가 발생했습니다.')
            return redirect('insjoin.do')
        

        
    

#회원정보수정
# @login_required
def insmember_modify(request):
    if request.method=="GET":
        try:
            idx = request.session['m_email']
        except KeyError:
            messages.error(request, '로그인 정보가 없습니다.')
            return redirect('inslogin.do')
        idx2 = str(idx)
        print(idx2)
        msg = "select * from insta_member where m_email = %s"
        print(msg, [idx2])

        try:
            with connection.cursor() as cursor:
                cursor.execute(msg, [idx2])
                data = cursor.fetchone()

            if data:
                m_email = data[5]
                m_id = data[1]
                m_name = data[4]
                return render(request, 'instacorn/insmember_modify.html', {
                    'm_email': m_email, 'm_id': m_id, 'm_name': m_name, 
                    })
            else:
                messages.error(request, '회원 정보를 찾을 수 없습니다.')
                return redirect('inslogin.do')
            
        except DatabaseError as e:
            print(f'Database error: {e}')
            messages.error(request, '데이터베이스 오류가 발생했습니다.')
            return redirect('inslogin.do')

    elif request.method == "POST":
        if 'update_info' in request.POST:
            return insmember_modifysave(request)
        elif 'change_password' in request.POST:
            return inspwd_modify(request)
        
    return render(request, 'instacorn/insmember_modify.html')


def insmember_modifysave(request):
    m_email = request.POST.get('m_email')
    m_id = request.POST.get('m_id')
    m_name = request.POST.get('m_name')
    print(f'넘어온 값들: {m_email}, {m_id}, {m_name}')

    try:
        with connection.cursor() as cursor:
                msg="select * from insta_member where m_id = (%s)"
                cursor.execute(msg, (m_id, ))
                data_id = cursor.fetchall()
                if len(data_id) != 0:
                    messages.error(request, '이미 존재하는 아이디입니다. 다른 아이디를 사용해주세요.')
                    return redirect('insmember_modify.do')
                msg = "update insta_member set m_id = %s, m_name = %s where m_email = %s"
                cursor.execute(msg,  [m_id, m_name, m_email])
                connection.commit()
                print('수정완료')
        
        messages.success(request, '회원정보가 수정되었습니다.')
        return render(request, 'instacorn/main.html')
    
    except Exception as e:
            print('error')
            messages.error(request, '회원 정보 수정 중 오류가 발생했습니다.')
            return redirect('insmember_modify.do')

#비밀번호변경
# @login_required
def inspwd_modify(request):
    # context={}
    # if request.method == 'POST':
    #     exist_password = request.POST.get('exist_password')
    #     user = request.user
    #     if check_password(exist_password,user.password):
    #         new_password = request.POST.get('new_password')
    #         check_password = request.POST.get('check_password')
    #         if new_password == check_password:
    #             user.set_password(new_password)
    #             user.save()
    #             auth.login(request,user)
    #             messages.success(request, '비밀번호가 변경되었습니다.')
    #         else:
    #             context.update({'error:''새 비밀번호가 일치하지 않습니다.'})
    #     else:
    #         context.update({'error':"현재 비밀번호가 일치하지 않습니다."})
    # return render(request, 'instacorn/main.html')
        
    if request.method == 'POST':
        exist_password = request.POST.get('exist_password')
        new_password = request.POST.get('new_password')
        check_password = request.POST.get('check_password')     
        print(f"exist_password: {exist_password}, new_password: {new_password}, check_password: {check_password}")

    user = request.user
    # user = request.session.get('m_no')
    m_email = request.session.get('m_email')
    if m_email.is_authenticated:
        if user.check_password(exist_password):
            if new_password == check_password:
                user.set_password(new_password)
                user.save()
                print('aaaaaaaa')
                update_session_auth_hash(request, user)
                messages.success(request, '비밀번호가 변경되었습니다.')
            else:
                messages.error(request, '새 비밀번호가 일치하지 않습니다.')
        else:
            messages.error(request, '현재 비밀번호가 일치하지 않습니다.')
    else:
            messages.error(request, '로그인된 사용자가 아닙니다.')

    return render(request, 'instacorn/main.html')
    

#비밀번호 재설정(찾기)
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        print(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = get_user_model().objects.filter(Q(email=data))
            print( associated_users, data)
            print("찾은 사용자 수:", associated_users.count())
            if associated_users.exists():    
                for user in associated_users:
                    subject = '비밀번호 재설정'
                    email_template_name = "instacorn/pwd_reset_email.txt"
                    
                    c = {
                        "email": user.email,
                        'domain': settings.HOSTNAME,
                        'site_name': 'instacorn',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': settings.PROTOCOL,
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'eunjeong474@gmail.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/inspwdreset/done/")
                
    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name='instacorn/inspwdreset.html',
        context={'password_reset_form': password_reset_form})

