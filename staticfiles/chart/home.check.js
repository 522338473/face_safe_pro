Vue.component('home-check', {
    data() {
        return {
            loading: false,
            check: {},
        }
    },
    mounted() {
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
    template:
        `
        <div>
            <p>预警</p>
            <div style="width: 33%; float: left">
            <p style="color: #999999">重点人员</p>
            <p style="color: rgb(242, 111, 111); font-size: 32px; font-weight: 500; margin-top: 0; margin-bottom: 0; padding-left: 10px; cursor: pointer">{{ check.monitor_discovery_total }}</p>
</div>
            <div style="width: 33%; float: left">
            <p style="color: #999999">重点车辆</p>
            <p style="color: rgb(239, 149, 74); font-size: 32px; font-weight: 500; margin-top: 0; margin-bottom: 0; padding-left: 10px; cursor: pointer">{{ check.vehicle_discovery_total }}</p>
</div>
            <div style="width: 33%; float: left">
            <p style="color: #999999">重点区域</p>
            <p style="color: #3d7cd2; font-size: 32px; font-weight: 500; margin-top: 0; margin-bottom: 0; padding-left: 10px; cursor: pointer">{{ check.area_discovery_total }}</p>
</div>
        </div>
`
})