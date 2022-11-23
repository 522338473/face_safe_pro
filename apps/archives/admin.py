from django.urls import reverse
from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from simpleui.admin import AjaxAdmin
from simplepro.dialog import ModalDialog, MultipleCellDialog

from archives import models as archives_models
from public.admin import PublicModelAdmin
from archives import resources as archives_resources
from utils.constant import VIDEO_PLAY_TYPE, DETAIL_TYPE
from utils.face_discern import face_discern


# Register your models here.


@admin.register(archives_models.ArchivesGroup)
class ArchivesGroupAdmin(PublicModelAdmin, AjaxAdmin):
    list_display = ["id", "name", "personnel_count", "detail"]
    search_fields = ["name"]
    top_html = ' <el-alert title="档案库分类" type="success"></el-alert>'

    def personnel_count(self, obj):
        """统计档案库下人员总数"""
        return obj.personnel_set.count()

    personnel_count.short_description = "人员总数"

    def dialog_url(self, model):
        modal = ModalDialog()
        modal.cell = '<el-button type="text">点击查看</el-button>'
        modal.title = "详情对话框"
        # 这里的url可以写死，也可以用django的方向获取url，可以根据model的数据，传到url中
        modal.url = reverse("public:test1") + "?id={id}".format(id=model.hash)
        modal.show_cancel = True
        return modal

    dialog_url.short_description = "弹出对话框"

    # 这个自定义的对话框，可以在admin也可以在model中声明
    def async_load(self, model):
        modal = ModalDialog()
        modal.title = "Dialog 异步加载"
        modal.height = "500px"
        modal.width = "800px"
        modal.cell = f"{model.id}-异步加载"
        modal.show_cancel = False
        modal.url = reverse("public:test2") + "?id={id}".format(id=model.hash)
        return modal

    async_load.short_description = "异步加载"

    def save_model(self, request, obj, form, change):
        """保存数据之前做点额外的操作"""
        if change:
            print("表示修改", change)
        else:
            print("表示新增", change)
        obj.create_by = request.user.username
        super(ArchivesGroupAdmin, self).save_model(request, obj, form, change)


@admin.register(archives_models.Personnel)
class PersonnelAdmin(PublicModelAdmin, ImportExportModelAdmin, AjaxAdmin):
    list_display = [
        "id",
        "archives_group",
        "name",
        "phone",
        "id_card",
        "date_of_birth",
        "household_register",
        "image",
        "operation",
    ]
    list_filter = ["archives_group", "create_at"]
    search_fields = ["name", "phone", "id_card"]
    resource_class = archives_resources.PersonnelResources
    # actions = ['action_for_archives_personnel_export', 'action_for_archives_personnel_import', 'action_for_archives_personnel_layer_input']
    fields_options = {
        "id": {"fixed": "left", "width": "320px"},
        "archives_group": {"label": "库名称", "width": "130px"},
        "name": {"width": "80px"},
        "phone": {"width": "120px"},
        "id_card": {"width": "180px"},
        "date_of_birth": {"width": "180px"},
        "image": {"width": "120px"},
    }
    top_html = ' <el-alert title="这是顶部的" type="success"></el-alert>'
    bottom_html = ' <el-alert title="这是底部的" type="warning"></el-alert>'

    def image(self, obj):
        return mark_safe(
            """
            <el-popover placement="left" title="" trigger="hover">
             <el-image style="width: 150px; height: 150px" src={url} fit="fit"></el-image> 
             <el-image slot="reference" style="width: 30px; height: 30px" src={url} fit="fit"></el-image> 
            </el-popover> 
            """.format(
                url=obj.photo
            )
        )

    image.short_description = "照片"

    def operation(self, model):
        trail = ModalDialog(
            cell='<el-button type="text">轨迹搜索</el-button>',
            title="人员档案轨迹搜索",
            url=reverse("device:search_image")
            + "?id={id}".format(id=model.hash),  # 暂时写死。后期写活
            height="450px",
            width="1200px",
            show_cancel=True,
        )
        return MultipleCellDialog([trail])

    operation.short_description = "操作"

    def save_model(self, request, obj, form, change):
        """人员档案新增"""
        obj.create_by = request.user.username
        instance = super(PersonnelAdmin, self).save_model(request, obj, form, change)
        if not change:
            try:
                image = self.get_b64_image(request)
                result = face_discern.face_add(image=image, user_id=instance.hash)
                if result.get("error") == -1:
                    instance.set_delete()
                    self.message_user(request, "人脸注册失败")
            except Exception as e:
                instance.set_delete()
                self.message_user(request, "人脸注册失败")

    def delete_model(self, request, obj):
        """人员档案表单删除: 无论算法删除与否。页面必须删除"""
        try:
            result = face_discern.face_del(user_id=obj.hash)
            if result.get("error") == -1:
                pass
        except Exception as e:
            pass
        finally:
            if request.user.is_superuser:
                obj.delete()
            else:
                obj.set_delete()

    def delete_queryset(self, request, queryset):
        """人员档案列表删除: 无论算法删除与否。页面必须删除"""
        for query in queryset:
            try:
                result = face_discern.face_del(user_id=query.hash)
                if result.get("error") == -1:
                    pass
            except Exception as e:
                pass
            finally:
                if request.user.is_superuser:
                    query.delete()
                else:
                    query.set_delete()


@admin.register(archives_models.AccessDiscover)
class AccessDiscoverAdmin(PublicModelAdmin, AjaxAdmin):
    list_display = [
        "id",
        "target",
        "pass_time",
        "pass_address",
        "similarity",
        "image",
        "operation",
    ]
    list_filter = ["target", "create_at"]
    fields_options = {
        "id": {"fixed": "left", "width": "320px"},
        "target": {"label": "门禁人员"},
        "image": {"label": "通行抓拍", "width": "120px"},
    }

    def pass_time(self, obj):
        return obj.record.take_photo_time

    pass_time.short_description = "通行时间"

    def pass_address(self, obj):
        return obj.record.address

    pass_address.short_description = "通行地点"

    def image(self, obj):
        return mark_safe(
            """
            <el-popover placement="left" title="" trigger="hover">
             <el-image style="width: 150px; height: 150px" src={url} fit="fit"></el-image> 
             <el-image slot="reference" style="width: 30px; height: 30px" src={url} fit="fit"></el-image> 
            </el-popover> 
            """.format(
                url=obj.record.head_path
            )
        )

    image.short_description = "通行抓拍"

    def operation(self, model):
        detail = ModalDialog(
            cell='<el-button type="text">通行详情</el-button>',
            title="门禁人员通行详情",
            url=reverse("archives:access_pass_detail")
            + "?id={id}&detail_type={detail_type}".format(
                id=model.hash, detail_type=DETAIL_TYPE["ACCESS_DISCOVER_DETAIL"]
            ),
            height="450px",
            width="1200px",
            show_cancel=True,
        )
        back = ModalDialog(
            cell='<el-button type="text">回放视频</el-button>',
            title="回放视频",
            url=reverse("device:video_playback")
            + "?id={id}&video_play_type={video_play_type}".format(
                id=model.record.hash,
                video_play_type=VIDEO_PLAY_TYPE["ACCESS_DISCOVER_VIDEO_PLAY"],
            ),  # 暂时写死。后期写活
            height="435px",
            width="800px",
            show_cancel=True,
        )
        return MultipleCellDialog([detail, back])

    operation.short_description = "操作"
