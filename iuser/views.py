from django.shortcuts import render
from django.shortcuts import redirect
from django.db  import connection, DatabaseError
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
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

from django.core.mail import EmailMessage
import string
import random
import hashlib
import base64

from django.contrib.auth.hashers import pbkdf2


# Create your views here.
def hashing_password(m_pwd):
    count = random.randint(16, 21)
    string_pool = string.ascii_letters + string.digits + string.punctuation
    m_salt = "".join(random.choices(string_pool, k=count))
    hashedpw = hashlib.md5(str(m_pwd + m_salt).encode('utf-8')).hexdigest()

    return m_salt, hashedpw

#로그인
def inslogin(request):
    if request.method == 'GET':
        return render(request, 'index.html', {'popup_message': ''})
    
    elif request.method == 'POST':
        m_email = request.POST.get('m_email')
        m_pwd = request.POST.get('m_pwd')

        try:
            # auth_user 테이블에서 사용자 인증
            user = authenticate(request, username=m_email, password=m_pwd)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('/admin/')

            # auth_user 테이블에 없는 경우 insta_member 테이블에서 확인
            cursor = connection.cursor()
            msg = "SELECT m_no, m_email, m_pwd, m_salt, m_active FROM insta_member WHERE m_email = %s"
            cursor.execute(msg, [m_email])
            data = cursor.fetchone()
            
            # 이메일이 틀렸을 때
            if not data:
                messages.error(request, '이메일이 존재하지 않습니다')
                return redirect('inslogin.do')

            m_no, m_email, regpw, m_salt, m_active = data           

            # MD5와 저장된 솔트를 사용하여 비밀번호를 검증
            hashedpw = hashlib.md5(str(m_pwd + m_salt).encode('utf-8')).hexdigest()
            
            if hashedpw != regpw:
                messages.error(request, '비밀번호가 일치하지 않습니다')
                return redirect('inslogin.do')
            
            if not m_active:
                # 팝업 메시지 전달
                context = {'popup_message': '회원님의 계정이 신고로 인하여 비활성화되었습니다. 계정 복구에 관한 문의사항은 아래 이메일로 문의해주세요.'}
                return render(request, 'index.html', context)
            
            request.session['m_no'] = m_no
            #return render(request, 'instacorn/main.html')
            return redirect('home.do')
                
        except Exception as e:
            connection.rollback()
            print('failed login', e)
            messages.error(request, '에러 발생')
            return redirect('inslogin.do')

#def 비밀번호찾기

#def 로그아웃
def inslogout(request):
    if request.session.get('m_no'):
        del (request.session['m_no'])
    return redirect('inslogin.do')

#회원가입
def insjoin(request):
    if request.method=='GET':
        return render(request, 'instacorn/insjoin.html')
    
    else:
        m_email = request.POST.get('m_email')
        m_name = request.POST.get('m_name')
        m_id = request.POST.get('m_id')
        m_pwd = request.POST.get('m_pwd')

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
            
                m_salt, hashedpw = hashing_password(m_pwd)
                m_img = "profile02.png"
                msg="insert into insta_member(m_id, m_pwd, m_name, m_email, m_salt, m_img) values(%s, %s, %s, %s, %s, %s)"
                cursor.execute(msg, (m_id, hashedpw, m_name, m_email, m_salt, m_img))

                if '@' not in m_email:
                    messages.error(request, '유효한 이메일 주소를 입력해주세요.')
                    return render(request, 'instacorn/insjoin.html')
                

            messages.success(request, '회원가입 완료, 로그인을 해주세요.')
            return redirect('inslogin.do')
                
        except:
            connection.rollback()
            print("회원가입실패")

            messages.error(request, '회원가입 에러 발생')
            return redirect('insjoin.do')
        
        finally:
            connection.close()

#회원정보수정
def insmember_modify(request):
    
    if request.method=="GET":
        try:
            m_no = request.session.get('m_no')
        except KeyError:
            messages.error(request, '로그인 정보가 없습니다.')
            return redirect('inslogin.do')       
        
        msg = "select * from insta_member where m_no = %s"


        try:
            with connection.cursor() as cursor:
                cursor.execute(msg, [m_no])
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


#회원정보 수정 저장
def insmember_modifysave(request):
    m_no = request.session.get('m_no')
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
        #return render(request, 'instacorn/home.html')
        request.session['m_no'] = m_no
        return redirect('home.do')
    
    except Exception as e:
            print('error')
            messages.error(request, '회원 정보 수정 중 오류가 발생했습니다.')
            return redirect('insmember_modify.do')

#비밀번호변경
def inspwd_modify(request):
    if request.method == 'POST':
        exist_m_pwd = request.POST.get('exist_m_pwd')
        new_m_pwd = request.POST.get('new_m_pwd')
        check_m_pwd = request.POST.get('check_m_pwd')     
        print(f"exist_m_pwd: {exist_m_pwd}, new_m_pwd: {new_m_pwd}, check_m_pwd: {check_m_pwd}")

    user = request.user

    if user.is_authenticated:
        if user.check_password(exist_m_pwd):
            if new_m_pwd == check_m_pwd:
                user.set_password(new_m_pwd)
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

    return render(request, 'instacorn/home.html')
    
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

