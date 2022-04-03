from django.urls import reverse
from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from simpleui.admin import AjaxAdmin
from simplepro.dialog import ModalDialog, MultipleCellDialog

from apps.archives import models as archives_models
from apps.public.admin import PublicModelAdmin
from apps.public.resources import PersonnelResources


# Register your models here.


@admin.register(archives_models.ArchivesGroup)
class ArchivesGroupAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'detail']
    search_fields = ['name']
    top_html = ' <el-alert title="这是顶部的" type="success"></el-alert>'
    actions = ['action_for_archives_group_test', 'action_for_archives_group_another_test']

    def dialog_url(self, model):
        modal = ModalDialog()
        modal.cell = '<el-link type="primary">点击查看</el-link>'
        modal.title = "详情对话框"
        # 这里的url可以写死，也可以用django的方向获取url，可以根据model的数据，传到url中
        modal.url = reverse('public:test1') + "?id=%s" % model.id
        modal.show_cancel = True
        return modal

    dialog_url.short_description = '弹出对话框'

    # 这个自定义的对话框，可以在admin也可以在model中声明
    def async_load(self, model):
        modal = ModalDialog()
        modal.title = 'Dialog 异步加载'
        modal.height = '500px'
        modal.width = '800px'
        modal.cell = f"{model.id}-异步加载"
        modal.show_cancel = False
        modal.url = reverse('public:test2') + "?id=%s" % model.id
        return modal

    async_load.short_description = '异步加载'

    def save_model(self, request, obj, form, change):
        """保存数据之前做点额外的操作"""
        if change:
            print('表示修改', change)
        else:
            print('表示新增', change)
        obj.create_by = request.user.username
        super(ArchivesGroupAdmin, self).save_model(request, obj, form, change)


@admin.register(archives_models.Personnel)
class PersonnelAdmin(PublicModelAdmin, ImportExportModelAdmin, AjaxAdmin):
    list_display = ['id', 'archives_group', 'name', 'phone', 'id_card', 'image', 'operation']
    list_filter = ['archives_group', 'create_at']
    exclude = ['is_access', 'device_list']  # TODO: 该字段为扩展字段，后期决定存留
    search_fields = ['name', 'phone', 'id_card']
    resource_class = PersonnelResources
    actions = ['action_for_archives_personnel_export', 'action_for_archives_personnel_import', 'action_for_archives_personnel_layer_input']
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'archives_group': {
            'label': '库名称',
            'width': '130px'
        },
        'name': {
            'width': '80px'
        },
        'phone': {
            'width': '120px'
        },
        'id_card': {
            'width': '180px'
        },
        'image': {
            'width': '120px'
        },
    }
    top_html = ' <el-alert title="这是顶部的" type="success"></el-alert>'
    bottom_html = ' <el-alert title="这是底部的" type="warning"></el-alert>'

    def image(self, obj):
        return mark_safe('<img src="%s" width=30px;>' % obj.photo)

    image.short_description = 'Admin头像'

    def operation(self, model):
        trail = ModalDialog(
            cell='<el-link type="primary">轨迹搜索</el-link>',
            title='人员档案轨迹搜索',
            url='/v1/device/search_image/',
            height='450px',
            width='1200px',
            show_cancel=True
        )
        return MultipleCellDialog([trail])

    operation.short_description = '操作'


@admin.register(archives_models.AccessDiscover)
class AccessDiscoverAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'target', 'record', 'checked', 'similarity', 'operation']
    list_filter = ['target']
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'target': {
            'width': '140px'
        },
        'checked': {
            'width': '120px'
        },
        'similarity': {
            'width': '100px'
        }
    }

    def operation(self, model):
        detail = ModalDialog(
            cell='<el-link type="primary">通行详情</el-link>',
            title='门禁人员通行详情',
            url=reverse('archives:access_pass_detail') + '?id=%s' % model.id,
            height='450px',
            width='1200px',
            show_cancel=True
        )
        back = ModalDialog(
            cell='<el-link type="primary">回放视频</el-link>',
            title='回放视频',
            url=reverse('device:video_playback') + '?id=%s' % model.id,  # 暂时写死。后期写活
            height='435px',
            width='800px',
            show_cancel=True
        )
        return MultipleCellDialog([detail, back])

    operation.short_description = '操作'
