# 인스타그램 프로젝트 | Django

![image](https://github.com/user-attachments/assets/cfaa67a7-a807-48cc-8e29-09a9e97bd7a3)

<br>

## 프로젝트 소개

공부를 위해 Django를 이용해 인스타그램을 만들어보았습니다.

<br>

## 개발 언어

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white)
![js](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=white)
![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySql](https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white)

<br>

## 개발 기간

2024.06.17 ~ 2024.06.26

<br>

## 멤버 및 역할

### 김종민
  - DB 설계 및 구축
  - 메인페이지, 마이페이지 기능 구현
  - 팔로우, 팔로워 기능 구현
  - 회원 및 게시물 신고 기능 구현

### 김동연
  - DB 설계 및 구축
  - 검색, 업로드 기능 구현

### 양정윤
  - 상세페이지 프론트엔드 및 기능 구현
  - 댓글 구현

### 오승빈
  - 업로드 기능 및 프론트엔드 구현

### 이채은(조장)
  - 관리자 페이지 구현
  - 전체 코드 병합

### 정은정
  - 회원가입 및 로그인 기능 구현
  - 회원정보 수정 기능 구현

### 한다솔
  - DB 서버 구축
  - 메시지 기능 구현

<br>

## 기능

### 회원가입
- 기본 정보를 적고 유효한 정보가 들어갔을 경우에 회원가입이 된다.

<br>

![image](https://github.com/user-attachments/assets/503ab624-4e28-472f-bd37-34373f8d73b2)

<br>

### 로그인
- 회원가입한 아이디, 비밀번호를 입력 시에 로그인이 된다.

<br>

![image](https://github.com/user-attachments/assets/eeec8ffd-112a-44f8-bf20-6a42e1956740)

<br>

### 비밀번호 재설정
- 비밀번호를 잊어버렸을 시에 이메일을 입력하면 해당 이메일로 비밀번호 재설정 메일이 가게 된다.

<br>

![image](https://github.com/user-attachments/assets/377a1863-2322-4f55-9bce-0f125f0089ee)

<br>

### 메인페이지
- 로그인 시에 메인페이지로 이동하게 된다.

<br>

![홈화면](https://github.com/user-attachments/assets/c335fc89-5244-4811-8342-b9c7abf6c364)

<br>

### 게시물 신고
- 게시물 오른쪽 상단의 버튼을 통해 게시물 신고 시 블러처리가 된다.

<br>

![신고버튼_중](https://github.com/user-attachments/assets/739a4b37-2b83-468e-aed3-45c7b5be2bbb)
![신고버튼_완_블러처리](https://github.com/user-attachments/assets/90671aae-f9a6-450e-9b71-20d9232ccb0d)

<br>

### 게시물 등록
- 만들기 버튼 클릭 후에 사진을 드래그 한 후, 글을 작성하면 게시물을 올릴 수 있다.

<br>

![image](https://github.com/user-attachments/assets/5221a8d1-093a-479e-99a3-8feab6e3a4d5)

<br>

### 검색
- 검색 버튼 클릭 시 검색 창이 뜬다.
- 사용자 이름이나 아이디를 입력 시에 해당하는 사용자 정보가 뜨게된다.

<br>

![검색_아이디](https://github.com/user-attachments/assets/addcd0c9-743d-40f8-a344-da6e0f2835de)

<br>

### 마이페이지
- 프로필 버튼이나 사용자 사진을 클릭 시에 마이페이지로 이동한다.
- 본인이 올린 게시물이나 팔로워, 팔로우 수를 확인할 수 있다.

<br>

![마이페이지](https://github.com/user-attachments/assets/905d5255-02ed-48dd-8940-de4cdaa86618)

<br>

### 팔로워/팔로잉
- 팔로우/팔로잉을 클릭시에 팔로워 팔로우 목록이 뜨게 된다.
- 해당 창에서 팔로워를 삭제할 수도, 팔로우를 취소할 수도 있다.

<br>

![image](https://github.com/user-attachments/assets/dd49550c-a0a7-48be-8c80-422a57ab8e46)

<br>

### 상세페이지
- 메인페이지나 마이페이지에서 게시물 클릭 시 상세페이지로 이동한다.
- 해당 창에서 게시물 수정/삭제, 댓글 등록/수정/삭제가 가능하다.

<br>

![상세페이지_댓글](https://github.com/user-attachments/assets/dc1304c8-1473-4deb-a8ce-3ab50c45af72)
![image](https://github.com/user-attachments/assets/d57e1b48-a254-4434-9d72-15ad52c94966)

<br>

### 메시지(DM)
- 메시지 버튼 클릭 시에 이동한다.
- 왼쪽에 대화를 나누는 사용자의 이름이 뜨고, 오른쪽에는 대화 내용이 뜬다.
- 오른쪽 창에서 대화를 나눌 수 있다.

<br>

![image](https://github.com/user-attachments/assets/6c9fba43-c242-47e7-a122-d74d16d0573f)

<br>

### 관리자페이지
- 관리자 아이디로 로그인 시 관리자페이지로 이동한다.
- 관리자페이지에서 신고된 사용자, 게시물들을 관리한다.

<br>

![관리자페이지](https://github.com/user-attachments/assets/257e21e0-5c10-4e54-9ca9-8cb1f4a90321)
![관리자_신고된게시물2](https://github.com/user-attachments/assets/95b4681a-0636-47a2-8f19-53824687e9b7)

<br>

## 소감
많은 인원이 참여한 프로젝트여서 처음에는 걱정이 많았다. 짧은 시간동안에 제대로된 성과를 낼 수 있을지가 의문이었기 때문이다.
하지만, 각자 맡은 역할들을 잘해주어서 결과물이 잘 나온 거 같다. 백엔드적인 부분도 많이 했었지만, 프론트엔드에서 시간을 많이
쓰게 되어 프론트엔드도 중요하다는 것을 깨닫게 되었다.
