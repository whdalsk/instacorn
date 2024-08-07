from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import InstaMemberSingo, InstaMember, InstaBoard, InstaBoardSingo



from django.contrib.admin.actions import delete_selected as default_delete_selected
# 기본 삭제 액션의 설명을 변경
default_delete_selected.short_description = '선택된 항목들을 삭제합니다.'


#계정 활성화 여부 필터
class MActiveBooleanFilter(admin.SimpleListFilter):
    title = _('계정 활성화 상태')
    parameter_name = 'm_active'

    def lookups(self, request, model_admin):
        return (
            (True, _('활성 계정')),
            (False, _('비활성 계정')),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(m_active=self.value())
        return queryset
    
#게시물 상태 필터
class BActiveBooleanFilter(admin.SimpleListFilter):
    title = _('게시물 상태')
    parameter_name = 'b_active'

    def lookups(self, request, model_admin):
        return (
            (True, _('정상')),
            (False, _('숨김')),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(b_active=self.value())
        return queryset    


#전체회원
@admin.register(InstaMember)
class InstaMemberAdmin(admin.ModelAdmin):
    list_display = ('m_no', 'm_id', 'm_name', 'm_email', 'm_active')
    list_editable = ('m_active',)
    search_fields = ('m_no', 'm_id', 'm_email','m_name',)
    readonly_fields = ('m_no', 'm_id', 'm_pwd', 'm_salt', 'm_name', 'm_email', 'm_img', 'm_date')
    list_filter = (MActiveBooleanFilter,)

    


#신고회원(비활성 처리 후 신고리스트에서 삭제)
@admin.register(InstaMemberSingo)
class InstaMemberSingoAdmin(admin.ModelAdmin):
    list_display = ('ms_no_display', 'reported_user', 'm_active_status')
    readonly_fields = ('ms_no',)
    actions = ['set_inactive']

    def ms_no_display(self, obj):
        return obj.ms_no.m_no

    def reported_user(self, obj):
        return obj.ms_no.m_id

    def m_active_status(self, obj):
        return obj.ms_no.m_active

    m_active_status.short_description = 'User Active Status'

    def set_inactive(self, request, queryset):
        updated_count = 0
        for singo in queryset:
            singo.ms_no.m_active = False 
            singo.ms_no.save()
            updated_count += 1

            singo.delete()
        
        self.message_user(request, f'{updated_count}건이 계정 비활성 처리 되었습니다.')

    set_inactive.short_description = '선택된 계정들을 비활성 처리 합니다.'
    


#전체 게시물
@admin.register(InstaBoard)
class InstaBoardAdmin(admin.ModelAdmin):
    list_display = ('b_code', 'b_content', 'b_photo', 'b_no', 'b_active')
    list_editable = ('b_active',)
    search_fields = ('b_content', 'b_code', 'b_date', 'b_no',)
    readonly_fields = ('b_code', 'b_content', 'b_photo', 'b_no', 'b_date')
    list_filter = (BActiveBooleanFilter,)

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
    
    
    

#신고된 게시물
@admin.register(InstaBoardSingo)
class InstaBoardSingoAdmin(admin.ModelAdmin):
    list_display = ('bs_code_display', 'reported_content', 'b_active_status')
    readonly_fields = ('bs_code',)
    actions = ['set_inactive']

    def bs_code_display(self, obj):
        return obj.bs_code.b_code
    
    def reported_content(self, obj):
        return obj.bs_code.b_content

    def b_active_status(self, obj):
        return obj.bs_code.b_active

    #b_active_status.short_description = '게시물 상태'

    def set_inactive(self, request, queryset):
        updated_count = 0
        for singo in queryset:
            singo.bs_code.b_active = False 
            singo.bs_code.save()
            updated_count += 1

            singo.delete()
        
        self.message_user(request, f'{updated_count}건이 게시물 숨김 처리 되었습니다.')

    set_inactive.short_description = '선택된 게시물들을 숨김 처리 합니다.'
    

    

admin.site.site_header = '관리자 페이지'
# admin.site.site_title = 'Custom Admin Title'

