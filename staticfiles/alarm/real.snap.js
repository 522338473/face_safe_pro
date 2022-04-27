Vue.component('real-snap', {
    props: {
        id: {
            type: String,
            default: "",
        }
    },
    data() {
        return {
            loading: false,
            device_photo_list: [],
            paginator: {
                count: 0,
                page_size: 30,
                page_count: 0,
                paginate: 'on',
            },
        }
    },
    created() {
        this.get_real_snap()
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
            console.log('....');
            self.get_real_snap();
        }, 3000)
    },
    methods: {
        get_real_snap: function () {
            let self = this;
            self.loading = true;
            axios.get('/v1/device/photo/', {
                params: {
                    'paginate': self.paginator.paginate,
                    'device': self.id,
                }
            }, {
                'Content-Type': 'application/json;charset=UTF-8'
            }).then(res => {
                self.device_photo_list = res.data.results;
            }).finally(() => {
                self.loading = false
            })
        }
    },
    template:
        `
        <div class="face-img box-group">
            <div class="img-list" v-for="(item, index) of device_photo_list" :key="index">
                <el-image
                        style="width: 140px; height: 120px"
                        :src="item.head_path">
                </el-image>
                <p style="line-height: 40px">{{item.take_photo_time}}</p>
            </div>
        </div>
`
})