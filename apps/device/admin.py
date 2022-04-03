from django.urls import reverse
from django.contrib import admin
from simplepro.dialog import ModalDialog, MultipleCellDialog

from apps.device import models as device_models
from apps.public.admin import PublicModelAdmin


# Register your models here.


@admin.register(device_models.DeviceInfo)
class DeviceInfoAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'ip', 'address', 'status', 'channel', 'operation']
    list_filter = ['name', 'device_type', 'create_at']
    exclude = ['last_login', 'last_logout', 'snap_count', 'monitor_count']
    list_per_page = 3
    change_list_template = 'admin/device/deviceinfo/change_list.html'
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'name': {
            'label': '设备名称',
            'width': '160px'
        },
        'ip': {
            'width': '120px'
        },
        'address': {
            'width': 'auto',
        },
        'status': {
            'label': '状态',
            'width': '100px'
        },
        'channel': {
            'label': '通道',
            'width': '80px'
        },
        'operation': {
            'width': '160px'
        }
    }

    def operation(self, model):
        login = ModalDialog(
            cell='<el-link type="primary" {status}>登录</el-link>'.format(status='disabled' if model.status == 0 else ''),
            title='摄像头登录',
            url='http://192.168.2.164/',
            height='80%',
            width='90%',
            show_cancel=True
        )
        real = ModalDialog(
            cell='<el-link type="primary" {status}>实况</el-link>'.format(status='disabled' if model.status == 0 else ''),
            title='摄像头实况',
            url='/admin/device/deviceinfo/real_time/',
            height='40%',
            width='50%',
            show_cancel=True
        )
        return MultipleCellDialog([login, real])

    operation.short_description = '操作'

    # 这个自定义的对话框，可以在admin也可以在model中声明
    def async_load(self, model):
        modal = ModalDialog()
        modal.height = '500px'
        modal.width = '800px'
        modal.cell = f"{model.id}-异步加载"
        modal.show_cancel = False
        modal.url = reverse('public:test2') + "?id=%s" % model.id
        return modal

    async_load.short_description = '异步加载'


@admin.register(device_models.DevicePhoto)
class DevicePhotoAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'address', 'take_photo_time', 'head_path', 'operation']
    list_filter = ['device', 'take_photo_time']
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '60px'
        },
        'head_path': {
            'label': '人脸照'
        },
        'take_photo_time': {
            'width': '170px'
        },
        'operation': {
            'width': '200px'
        }
    }

    def operation(self, model):
        query = ModalDialog(
            cell='<el-link type="primary">查询</el-link>',
            title='抓拍记录',
            url=reverse('device:photo_search') + '?id=%s' % model.id,
            height='450px',
            width='1200px',
            show_cancel=True
        )
        detail = ModalDialog(
            cell='<el-link type="primary">详情</el-link>',
            title='数据详情',
            url=reverse('device:photo_detail') + '?id=%s' % model.id,
            height='450px',
            width='1200px',
            show_cancel=False
        )
        back = ModalDialog(
            cell='<el-link type="primary">回放视频</el-link>',
            title='回放视频',
            url=reverse('device:video_playback') + '?id=%s' % model.id,  # 暂时写死。后期写活
            height='435px',
            width='800px',
            show_cancel=True
        )
        return MultipleCellDialog([query, detail, back])

    operation.short_description = '操作'


@admin.register(device_models.DeviceOffLine)
class DeviceOffLineAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'device', 'checked', 'alarm_type', 'photo_path']
    list_filter = ['device', 'create_at']
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'checked': {
            'width': '120px'
        }
    }


@admin.register(device_models.Motor)
class MotorAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'device', 'address', 'take_photo_time', 'motor_path']
    list_filter = ['device', 'create_at']
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'device': {
            'width': '160px'
        },

    }


@admin.register(device_models.Vehicle)
class VehicleAdmin(PublicModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'device', 'address', 'take_photo_time', 'plate', 'plate_path', 'operation']
    list_filter = ['device', 'create_at']
    search_fields = ['plate', 'color', 'types']
    fields_options = {
        'id': {
            'fixed': 'left',
            'width': '80px'
        },
        'device': {
            'width': '160px'
        },
        'take_photo_time': {
            'width': '170px'
        },
        'plate': {
            'width': '100px'
        },
        'operation': {
            'width': '180px'
        }
    }

    def operation(self, model):
        query = ModalDialog(
            cell='<el-link type="primary">查询</el-link>',
            title='机动车搜索',
            url=reverse('device:vehicle_search') + '?id=%s' % model.id,
            height='450px',
            width='1200px',
            show_cancel=True
        )
        detail = ModalDialog(
            cell='<el-link type="primary">详情</el-link>',
            title='机动车详情',
            url=reverse('device:vehicle_detail') + '?id=%s' % model.id,
            height='450px',
            width='1200px',
            show_cancel=True
        )
        back = ModalDialog(
            cell='<el-link type="primary">回放视频</el-link>',
            title='回放视频',
            url=reverse('device:video_playback') + '?id=%s' % model.id,
            height='435px',
            width='800px',
            show_cancel=True
        )
        return MultipleCellDialog([query, detail, back])

    operation.short_description = '操作'
