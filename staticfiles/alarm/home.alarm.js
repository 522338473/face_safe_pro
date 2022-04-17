Vue.component('home-alarm', {
    data() {
        return {
            loading: false,
            monitor_list: [],
            dialogVisible: false,
            detail_id: '',
        }
    },
    mounted() {
        let self = this;
        self.loading = true;
        axios.get('/v1/monitor/monitor_discover/?format=json', {
            params: {
                limit: 10,
                offset: 0
            }
        }, {
            'Content-Type': 'application/json;charset=UTF-8'
        }).then(res => {
            self.monitor_list = res.data.results;
        }).finally(() => {
            self.loading = false;
        })
    },
    methods: {
        handleClose(done) {
            this.$confirm('确认关闭？')
                .then(_ => {
                    done();
                })
                .catch(_ => {
                });
        },
        detail_dialog: function (id) {
            this.detail_id = id;
            this.dialogVisible = true;
        },
    },
    template:
        `
        <div style="margin-top: 10px; height: 800px; width: 100%; overflow: auto">
            <el-row
                    style="margin-top: 5px"
                    class="row"
                    v-for="(item, index) in monitor_list"
                    :key="index"
            >
                <el-col :span="5" style="width: 100px">
                    <img :src="item.target.photo" alt="" width="100px" height="100px">
                </el-col>
                <el-col :span="7" style="width: 100px">
                    <img :src="item.record.head_path" alt="" width="100px" height="100px">
                </el-col>
                <el-col :span="8" style="margin-left: 10px; min-width: 120px; overflow: auto">
                    <p style="font-size: 28px; font-weight: 500; color: #606266; margin: 0;">{{ item.target.name }}</p>
                    <p style="font-size: 14px; color: #909399; overflow: hidden; height: 30px;line-height: 30px; margin: 0">{{ item.record.take_photo_time }}</p>
                    <el-link @click="detail_dialog(item.id)" size="mini">详情</el-link>
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
                <iframe :src='"/v1/device/photo_detail/?id=" + detail_id' frameborder="0" height="100%" width="100%"></iframe>
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