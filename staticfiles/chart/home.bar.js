Vue.component('home-bar', {
    data() {
        return {
            option: {
                color: ['#3398DB'],
                grid: {
                    left: '0%',
                    right: '6%',
                    bottom: '1%',
                    top: '10%',
                    containLabel: true
                },
                tooltip: {
                    trigger: 'item'
                },
                xAxis: [
                    {
                        axisLine: {
                            lineStyle: {
                                color: '#E5E5E5',
                                width: 1 //这里是为了突出显示加上的
                            }
                        },

                        axisLabel: {
                            show: true,
                            textStyle: {
                                color: '#999999'
                            }
                        },
                        data: ['重点人员', '重点车辆', '重点区域'],
                        axisTick: {
                            show: false
                        }
                    }
                ],
                yAxis: [
                    {
                        type: 'value',
                        axisLabel: {
                            show: true,
                            textStyle: {
                                color: '#999999'
                            }
                        },

                        axisLine: {
                            lineStyle: {
                                color: '#E5E5E5',
                                width: 1 //这里是为了突出显示加上的
                            }
                        },

                        splitLine: {
                            show: true,
                            lineStyle: {
                                type: 'solid', //设置网格线类型 dotted：虚线   solid:实线
                                color: '#F0F0F0',
                                width: '1'
                            }
                        }
                    }
                ],
                series: [
                    {
                        type: 'bar',
                        barWidth: '72px',
                        data: [100, 89, 25],
                        label: {
                            show: true,
                            position: 'top',
                            color: '#666666'
                        },
                        itemStyle: {
                            normal: {
                                color: function (params) {
                                    var colorList = ['#5C9AEE', '#F26F6F', '#8BD38A', '#EF954A'];
                                    return colorList[params.dataIndex];
                                }
                            }
                        }
                    }
                ]
            },
            total_dict: {
                monitor_discovery_total: '重点人员',
                vehicle_discovery_total: '重点车辆',
                area_discovery_total: '门禁通行'
            },
            options: [
                {
                    value: 0,
                    label: '最近一天'
                },
                {
                    value: 2,
                    label: '最近三天'
                },
                {
                    value: 6,
                    label: '最近七天'
                },
                {
                    value: 14,
                    label: '最近半个月'
                },
                {
                    value: 29,
                    label: '最近一个月'
                }
            ],
            value: 0,
            isActive: true,
        }
    },
    created() {
        this.get_count();
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
            self.get_count();
        }, 60000)
    },
    methods: {
        get_count: function () {
            let self = this;
            let start_time = new Date(new Date(new Date(new Date().setHours(0, 0, 0, 0)).setDate(new Date(new Date().setHours(0, 0, 0, 0)).getDate() - this.value))).format("YYYYMMDDhhmmss");
            let end_time = new Date(new Date().setHours(23, 59, 59, 0)).format("YYYYMMDDhhmmss");
            let params = {
                start_time: start_time,
                end_time: end_time
            }
            axios.get("/v1/monitor/monitor/count/?format=json", {params: params}, {
                'Content-Type': 'application/json;charset=UTF-8'
            }).then(res => {
                let bar_title = [];
                let bar_list = [];
                for (let key in res.data) {
                    bar_title.push(self.total_dict[key]);
                    bar_list.push(res.data[key]);
                }
                self.option.xAxis[0].data = bar_title;
                self.option.series[0].data = bar_list;
            });
        }
    },
    template:
        `
<div style="display: flex; position: relative">
    <echarts :option="option" style="width: 100%;height: 280px"></echarts>
    <el-select v-model="value" @change="get_count" size="mini" style="position: absolute; top: -20px; right: 20px; width: 120px;">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
    </el-select>
</div>
`
})