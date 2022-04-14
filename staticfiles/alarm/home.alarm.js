Vue.component('home-alarm', {
    data() {
        return {
            loading: false,
            monitor_list: [],
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
                    <el-link href="javascript:alert('首页详情接口开发中.')">查看详情>></el-link>
                </el-col>
            </el-row>
        </div>
`
})