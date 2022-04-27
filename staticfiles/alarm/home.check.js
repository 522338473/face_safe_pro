Vue.component('home-check', {
    data() {
        return {
            loading: false,
            check: {},
        }
    },
    created() {
        this.get_un_check_count();
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
            if (!app || app.tabModel !== '0') {
                return;
            }
            self.get_un_check_count();
        }, 60000)
    },
    methods: {
        get_un_check_count: function () {
            let self = this;
            self.loading = true;
            axios.get('/v1/monitor/monitor/un_check_count/?format=json', {params: {}}, {
                'Content-Type': 'application/json;charset=UTF-8'
            }).then(res => {
                self.check = res.data;
            }).finally(() => {
                self.loading = false;
            })
        },
    },
    template:
        `
        <div>
            <p>预警</p>
            <div style="width: 33%; float: left">
            <p style="color: #999999; font-size: 20px;">重点人员</p>
            <p style="color: rgb(242, 111, 111); font-size: 32px; font-weight: 500; margin-top: 0; margin-bottom: 0; padding-left: 10px; cursor: pointer">{{ check.monitor_discovery_total || '0' }}</p>
</div>
            <div style="width: 33%; float: left">
            <p style="color: #999999; font-size: 20px;">重点车辆</p>
            <p style="color: rgb(239, 149, 74); font-size: 32px; font-weight: 500; margin-top: 0; margin-bottom: 0; padding-left: 10px; cursor: pointer">{{ check.vehicle_discovery_total || '0' }}</p>
</div>
            <div style="width: 33%; float: left">
            <p style="color: #999999; font-size: 20px;">重点区域</p>
            <p style="color: #3d7cd2; font-size: 32px; font-weight: 500; margin-top: 0; margin-bottom: 0; padding-left: 10px; cursor: pointer">{{ check.area_discovery_total || '0' }}</p>
</div>
        </div>
`
})