from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Permission

from apps.account import models as account_models


# Register your models here.


class UserExtraInline(admin.StackedInline):
    model = account_models.UserExtra


admin.site.unregister(User)


@admin.register(User)
class UserExtraAdmin(UserAdmin):
    list_display = ['id', 'username', 'email', 'is_active', 'is_staff', 'last_login', 'mobile']
    list_filter = ['username', 'is_active']
    readonly_fields = ['is_superuser']
    inlines = [UserExtraInline]
    list_per_page = 10
    top_html = ' <el-alert title="请谨慎操作用户相关信息!" type="warning"></el-alert>'

    def get_queryset(self, request):
        """普通管理员登录不显示超级管理员账号信息"""
        qs = super(UserExtraAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.exclude(is_superuser=True)
        return qs

    def delete_model(self, request, obj):
        """账号信息直接删除"""
        super(UserExtraAdmin, self).delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        """账号信息直接删除"""
        super(UserExtraAdmin, self).delete_queryset(request, queryset)

    def mobile(self, obj):
        try:
            return obj.user.mobile
        except Exception as e:
            return e

    mobile.short_description = '手机号'


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content_type', 'message', 'action_time']
    list_filter = ['user__username', 'action_time']
    readonly_fields = ['action_time', 'user', 'content_type']
    exclude = ['change_message', 'action_flag', 'object_repr', 'object_id']
    list_per_page = 10

    def get_changelist_instance(self, request):
        return super(LogEntryAdmin, self).get_changelist_instance(request)

    @staticmethod
    def message(obj):
        return obj.get_change_message()

    message.short_description = '操作信息'


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'content_type', 'codename']
