Vue.component('real-alarm', {
    data() {
        return {
            loading: false,
            isActive: true,
            dialogVisible: false,
            monitor_discover_list: [],
            dialog_detail: {
                target_path: '',
                target_name: '',
                head_path: '',
                body_path: '',
                back_path: '',
                similarity: '',
                device_name: '',
                device_address: '',
                take_photo_time: '',
                face_data: '',
                human_data: ''
            }
        }
    },
    created() {
        this.get_real_alarm();
    },
    mounted() {
        let self = this;
        // 浏览器失去焦点停止查询、节省开销
        window.addEventListener('focus', e => {
            self.isActive = true;
        });
        window.addEventListener('blur', e => {
            self.isActive = false;
        });
        setInterval(() => {
            if (!self.isActive) {
                return;
            }
            self.get_real_alarm();
        }, 3000)
    },
    methods: {
        get_real_alarm: function () {
            let self = this;
            self.loading = true;
            axios.get('/v1/monitor/monitor_discover/', {
                params: {
                    'limit': 10,
                    'offset': 0
                }
            }, {
                'Content-Type': 'application/json;charset=UTF-8'
            }).then(res => {
                self.monitor_discover_list = res.data.results
            }).finally(() => {
                self.loading = false
            })
        },
        detail_dialog: function (params) {
            let self = this;
            self.dialog_detail.target_name = params.target.name;
            self.dialog_detail.target_path = params.target.photo;
            self.dialog_detail.head_path = params.record.head_path;
            self.dialog_detail.body_path = params.record.body_path;
            self.dialog_detail.back_path = params.record.back_path;
            self.dialog_detail.similarity = params.similarity;
            self.dialog_detail.device_name = params.record.device.name;
            self.dialog_detail.device_address = params.record.address;
            self.dialog_detail.take_photo_time = params.record.take_photo_time;
            self.dialog_detail.face_data = params.record.face_data;
            self.dialog_detail.human_data = params.record.human_data;
            this.dialogVisible = true;
        },
    },
    template:
        `
        <div style="padding-top: 20px">
            <el-row
                    style="max-width: 200px; margin-left: 20px; margin-top: 15px"
                    class="row"
                    v-for="(item, index) in monitor_discover_list"
                    :key="index"
            >
                <el-col :span="12">
                    <el-image
                            style="width: 100px; height: 100px;"
                            fit="cover"
                            :src="item.target.photo"
                    >
                    </el-image>
                </el-col>
                <el-col :span="12">
                    <el-image
                            style="width: 100px; height: 100px"
                            fit="contain"
                            :src="item.record.head_path"
                    >
                    </el-image>
                </el-col>
                <el-col :span="12">
                    {{item.target.name}}
                </el-col>
                <el-col :span="12" style="text-align: right">
                    <el-link @click="detail_dialog(item)">详情</el-link>
                </el-col>
                <el-col :span="6" class="notice_col">
                    {{item.similarity}}%
                </el-col>
            </el-row>
            <el-row>
            <el-dialog
                    title="报警详情"
                    :visible.sync="dialogVisible"
                    :append-to-body="true"
                    :destroy-on-close="true"
                    :show-close="true"
                    width="1200px">
                <div style="width: 100%; height: 450px; overflow: hidden">
                    <el-col :span="4">
                        <div style="width: 190px; height: 110px; text-align: center;">
                            <div style="width: 95px; height: 110px; float: left; overflow: hidden">
                                <h5>原图像</h5>
                                <el-image :src="dialog_detail.target_path" style="width: 100%;"></el-image>
                            </div>
                            <div style="width: 95px; height: 110px; float: left; overflow: hidden">
                                <h5>抓拍图像</h5>
                                <el-image :src="dialog_detail.head_path" style="width: 100%"></el-image>
                            </div>
                        </div>
                        <h5 style="margin-top: 10px; margin-bottom: 10px">相似度: {{dialog_detail.similarity}}%</h5>
                        <div style="background-color: gray; width: 190px; height: 300px; overflow: hidden">
                            <el-image :src="dialog_detail.body_path" style="width: 100%"></el-image>
                        </div>
                    </el-col>
                    <el-col :span="15">
                        <div style="width: 713px; height: 430px; margin-left: 20px">
                            <el-image :src="dialog_detail.back_path" style="padding-top: 19px; width: 100%; height: 100%"></el-image>
                        </div>
                    </el-col>
                    <el-col :span="3">
                        <div style="width: 100%; height: 430px; margin-left: 20px">
                            <div style="padding-top: 19px">
                                <el-tooltip class="item" effect="dark" :content="dialog_detail.target_name" placement="left">
                                    <el-button>人员姓名</el-button>
                                </el-tooltip>
                            </div>
                            <div style="padding-top: 19px">
                                <el-tooltip class="item" effect="dark" :content="dialog_detail.face_data" placement="left">
                                    <el-button>人脸特征</el-button>
                                </el-tooltip>
                            </div>
                            <div style="padding-top: 19px">
                                <el-tooltip class="item" effect="dark" :content="dialog_detail.human_data" placement="left">
                                    <el-button>人体特征</el-button>
                                </el-tooltip>
                            </div>
                            <div style="padding-top: 19px">
                                <el-tooltip class="item" effect="dark" :content="dialog_detail.device_name" placement="left">
                                    <el-button>抓拍设备</el-button>
                                </el-tooltip>
                            </div>
                            <div style="padding-top: 19px">
                                <el-tooltip class="item" effect="dark" :content="dialog_detail.device_address" placement="left">
                                    <el-button>抓拍地址</el-button>
                                </el-tooltip>
                            </div>
                            <div style="padding-top: 19px">
                                <el-tooltip class="item" effect="dark" :content="dialog_detail.take_photo_time" placement="left">
                                    <el-button>抓拍时间</el-button>
                                </el-tooltip>
                            </div>
                        </div>
                    </el-col>
                </div>
                <span slot="footer" class="dialog-footer">
                    <el-button @click="dialogVisible = false">取 消</el-button>
                    <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
                </span>
            </el-dialog>
        </el-row>
        </div>
`
})