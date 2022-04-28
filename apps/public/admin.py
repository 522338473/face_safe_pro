import base64
import requests

from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings


class PublicModelAdmin:
    """
    公共Admin基类。用来覆盖默认规则。增加公共规则
    该类为第一继承类。否则根据新式类继承规则不会生效
    """

    readonly_fields = ['create_by', 'delete_at']
    list_per_page = 10
    list_default_per_page = 10
    change_list_template = 'admin/change_list.html'
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '120px',
            'align': 'center'
        }
    }

    def delete_model(self, request, obj):
        """删除数据的时候软删除"""
        if request.user.is_superuser:
            obj.delete()
        else:
            obj.set_delete()

    def delete_queryset(self, request, queryset):
        """query_set删除"""
        if request.user.is_superuser:
            queryset.delete()
        else:
            queryset.set_delete()

    def get_queryset(self, request):
        """
        all_objects: 表示已删除+未删除的所有数据
        objects: 表示未删除的所有数据
        TODO _ id: 如果传递参数，表示筛选
        """
        if request.user.is_superuser:
            # 超级管理员查看所有
            qs = self.model.all_objects.get_queryset()
        else:
            # 普通管理员查看未被删除的
            qs = self.model.objects.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def save_model(self, request, obj, form, change):
        """
        保存数据之前做点额外的操作哈
        """
        obj.create_by = request.user.username
        obj.save()
        return obj

    def get_query_params(self, request, name, default=None):
        """
        获取请求参数
        :param request:
        :param name: 参数值
        :param default: 默认值
        :return:
        """
        return request.POST.get(name, default) or request.GET.get(name, default)

    @staticmethod
    def get_head_url(request):
        """返回人脸完整路径"""
        return ''.join([settings.FAST_DFS_HOST, request.POST.get('photo')])

    def get_b64_image(self, request):
        """获取人脸b64"""
        return base64.b64encode(requests.get(url=self.get_head_url(request)).content).decode()

    def get_current_page(self, request):
        """获取当前页码"""
        return self.get_query_params(request, 'current_page', 1)

    def get_page_size(self, request):
        return self.get_query_params(request, 'page_size', None)

    """Action_for_account_start"""
    pass
    """Action_for_account_end"""

    """Action_for_archives_start"""

    def action_for_archives_group_test(self, request, queryset):
        """档案库Action"""
        self.message_user(request, '收到了请求、但是木有处理', messages.WARNING)

    action_for_archives_group_test.short_description = 'Action按钮测试'
    action_for_archives_group_test.enable = True
    action_for_archives_group_test.icon = 'fas fa-audio-description'
    action_for_archives_group_test.type = 'danger'
    action_for_archives_group_test.style = 'color:black;'
    action_for_archives_group_test.confirm = '你想干嘛?'

    def action_for_archives_group_another_test(self, request, queryset):
        """档案库Action"""
        messages.add_message(request, messages.SUCCESS, '哈哈哈')

    action_for_archives_group_another_test.short_description = '又一个Action测试按钮'
    action_for_archives_group_another_test.type = 'success'

    def action_for_archives_personnel_export(self, request, queryset):
        """档案人员Action"""
        self.message_user(request, '收到了请求、但是木有处理', messages.WARNING)

    action_for_archives_personnel_export.short_description = '自定义导出'
    action_for_archives_personnel_export.enable = True
    action_for_archives_personnel_export.icon = 'fas fa-download'
    action_for_archives_personnel_export.type = 'success'
    action_for_archives_personnel_export.confirm = '你想导出嘛?'

    def action_for_archives_personnel_import(self, request, queryset):
        """档案人员Action"""
        self.message_user(request, '收到了请求、但是木有处理', messages.WARNING)

    action_for_archives_personnel_import.short_description = '自定义导入'
    action_for_archives_personnel_import.enable = True
    action_for_archives_personnel_import.icon = 'fas fa-upload'
    action_for_archives_personnel_import.type = 'danger'
    action_for_archives_personnel_import.confirm = '你想导入嘛?'

    def action_for_archives_personnel_layer_input(self, request, queryset):
        post = request.POST
        if not post.get('_selected'):
            return JsonResponse(data={
                'status': 'error',
                'msg': '请先选中数据！'
            })
        else:
            return JsonResponse(data={
                'status': 'success',
                'msg': '处理成功！'
            })

    action_for_archives_personnel_layer_input.short_description = '弹出对话框输入'
    action_for_archives_personnel_layer_input.type = 'success'
    action_for_archives_personnel_layer_input.icon = 'el-icon-s-promotion'
    action_for_archives_personnel_layer_input.enable = True

    # 指定为弹出层，这个参数最关键
    action_for_archives_personnel_layer_input.layer = {
        # 弹出层中的输入框配置

        # 这里指定对话框的标题
        'title': '弹出层输入框',
        # 提示信息
        'tips': '这个弹出对话框是需要在admin中进行定义，数据新增编辑等功能，需要自己来实现。',
        # 确认按钮显示文本
        'confirm_button': '确认提交',
        # 取消按钮显示文本
        'cancel_button': '取消',

        # 弹出层对话框的宽度，默认50%
        'width': '40%',

        # 表单中 label的宽度，对应element-ui的 label-width，默认80px
        'labelWidth': "80px",
        'params': [{
            # 这里的type 对应el-input的原生input属性，默认为input
            'type': 'input',
            # key 对应post参数中的key
            'key': 'name',
            # 显示的文本
            'label': '名称',
            # 为空校验，默认为False
            'require': True
        }, {
            'type': 'select',
            'key': 'type',
            'label': '类型',
            'width': '200px',
            # size对应elementui的size，取值为：medium / small / mini
            'size': 'small',
            # value字段可以指定默认值
            'value': '0',
            'options': [{
                'key': '0',
                'label': '收入'
            }, {
                'key': '1',
                'label': '支出'
            }]
        }, {
            'type': 'number',
            'key': 'money',
            'label': '金额',
            # 设置默认值
            'value': 1000
        }, {
            'type': 'date',
            'key': 'date',
            'label': '日期',
        }, {
            'type': 'datetime',
            'key': 'datetime',
            'label': '时间',
        }, {
            'type': 'rate',
            'key': 'star',
            'label': '评价等级'
        }, {
            'type': 'color',
            'key': 'color',
            'label': '颜色'
        }, {
            'type': 'slider',
            'key': 'slider',
            'label': '滑块'
        }, {
            'type': 'switch',
            'key': 'switch',
            'label': 'switch开关'
        }, {
            'type': 'input_number',
            'key': 'input_number',
            'label': 'input number'
        }, {
            'type': 'checkbox',
            'key': 'checkbox',
            # 必须指定默认值
            'value': [],
            'label': '复选框',
            'options': [{
                'key': '0',
                'label': '收入'
            }, {
                'key': '1',
                'label': '支出'
            }, {
                'key': '2',
                'label': '收益'
            }]
        }, {
            'type': 'radio',
            'key': 'radio',
            'label': '单选框',
            'options': [{
                'key': '0',
                'label': '收入'
            }, {
                'key': '1',
                'label': '支出'
            }, {
                'key': '2',
                'label': '收益'
            }]
        }]
    }

    """Action_for_archives_end"""

    """Action_for_device_start"""
    pass
    """Action_for_device_end"""

    """Action_for_monitor_start"""
    pass
    """Action_for_monitor_end"""
