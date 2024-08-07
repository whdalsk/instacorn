from django.db import models

class InstaMember(models.Model):
    m_no = models.AutoField(primary_key=True)
    m_id = models.CharField(max_length=300)
    m_pwd = models.CharField(max_length=300)
    m_salt = models.CharField(max_length=300)
    m_name = models.CharField(max_length=100)
    m_email = models.CharField(max_length=300)
    m_img = models.CharField(max_length=300, null=True, blank=True)
    m_active = models.BooleanField(default=True)
    m_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.m_name

    class Meta:
        managed = False  # 이 설정을 통해 Django가 이 테이블을 관리하지 않도록 합니다.
        db_table = 'insta_member'
        verbose_name = '전체 회원'  
        verbose_name_plural = '전체 회원' 
     

class InstaMemberSingo(models.Model):
    ms_no = models.OneToOneField(InstaMember, on_delete=models.CASCADE, db_column='ms_no', primary_key=True)

    def __str__(self):
        #return f"Report for {self.ms_no.m_name}"
        return str(self.ms_no.m_no)

    class Meta:
        managed = False
        db_table = 'insta_member_singo'
        verbose_name = '신고된 회원'  
        verbose_name_plural = '신고된 회원' 


class InstaBoard(models.Model):
    b_code = models.AutoField(primary_key=True)
    b_content = models.CharField(max_length=500)
    b_photo = models.CharField(max_length=500)
    b_no = models.IntegerField()
    b_date = models.DateTimeField(auto_now_add=True)
    b_active = models.BooleanField(default=True)

    def __str__(self):
        return self.b_content

    class Meta:
        managed = False  # Django가 이 테이블을 관리하지 않도록 설정합니다.
        db_table = 'insta_board'
        verbose_name = '전체 게시물'  # 단수형 이름 설정
        verbose_name_plural = '전체 게시물'  # 복수형 이름 설정


class InstaBoardSingo(models.Model):
    bs_code = models.OneToOneField(InstaBoard, on_delete=models.CASCADE, db_column='bs_code', primary_key=True)

    def __str__(self):
        #return f"Report for {self.bs_code.b_content}"
        return str(self.bs_code.b_code)

    class Meta:
        managed = False  # Django가 이 테이블을 관리하지 않도록 설정합니다.
        db_table = 'insta_board_singo'
        verbose_name = '신고된 게시물'
        verbose_name_plural = '신고된 게시물'

