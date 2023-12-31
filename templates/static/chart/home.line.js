Vue.component('home-line', {
    props: ['time_choice'],
    data() {
        return {
            option: {
                legend: {
                    show: true,
                    data: ['人员', '车辆']
                },
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
                        data: [
                            '2022-04-02',
                            '2022-04-03',
                            '2022-04-04',
                            '2022-04-05',
                            '2022-04-06',
                            '2022-04-07',
                            '2022-04-08',
                            '2022-04-09',
                            '2022-04-10',
                            '2022-04-11',
                            '2022-04-12',
                            '2022-04-13',
                            '2022-04-14',
                            '2022-04-15'
                        ],
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
                        name: '人员',
                        type: 'line',
                        data: [5, 14, 13, 15, 17, 18, 20, 10, 11, 34, 32, 87, 12, 10],
                        symbolSize: 8, //折线点的大小
                        itemStyle: {
                            normal: {
                                color: '#f04767',
                                lineStyle: {
                                    width: 2,
                                    type: 'solid', //'dotted'虚线 'solid'实线
                                    color: '#f04767'
                                }
                            }
                        }
                    },
                    {
                        name: '车辆',
                        type: 'line',
                        data: [1, 2, 3, 0, 0, 0, 0, 4, 9, 1, 0, 5, 6, 5],
                        symbolSize: 8, //折线点的大小
                        itemStyle: {
                            normal: {
                                color: '#3d7efc',
                                lineStyle: {
                                    width: 2,
                                    type: 'dotted', //'dotted'虚线 'solid'实线
                                    color: '#3d7efc'
                                }
                            }
                        }
                    }
                ]
            },
            type_dict: {
                people_count: '人员',
                vehicle_count: '车辆'
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
        this.time_change();
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
            self.time_change();
        }, 60000)
    },
    methods: {
        time_change: function () {
            //请求数据 伪代码
            let start_time = dayjs(new Date(new Date(new Date(new Date().setHours(0, 0, 0, 0)).setDate(new Date(new Date().setHours(0, 0, 0, 0)).getDate() - this.value)))).format("YYYYMMDDhhmmss");
            let end_time = dayjs(new Date(new Date().setHours(23, 59, 59, 0))).format("YYYYMMDDhhmmss");
            let self = this;
            let params = {
                start_time: start_time,
                end_time: end_time
            }
            axios.get("/v1/device/photo/snap_count/?format=json", {
                params: params
            }, {
                'Content-Type': 'application/json;charset=UTF-8'
            }).then(res => {
                // console.time('consume');
                let dates = res.data.dates;
                let people_list = res.data.people_count;
                let vehicle_list = res.data.vehicle_count;
                let start_date = new Date(Date.parse(dates['start_date']));  // 开始时间
                let vehicle_start_date = new Date(Date.parse(dates['start_date']));  // 开始时间
                let end_date = new Date(Date.parse(dates['end_date']));  // 结束时间
                let days = 24 * 60 * 60 * 1000;  // 一天的毫秒时间戳
                let dlt_day = (end_date - start_date) / days;  // 起止日期差
                let people_hour_list = [];  // 人脸数组元数据
                let vehicle_hour_list = [];  // 车辆数组数据
                let x_title = [];  // 横坐标轴
                let people_point_list = [];  // 人员
                let vehicle_point_list = [];  // 车辆

                let _start_date = start_date;
                if ((end_date - start_date) <= days) {
                    for (let item = 0; item < 24; item++) {
                        people_hour_list.push({
                            'date': String(item) + '点',
                            'count': 0
                        })
                    }
                    for (let item = 0; item < 24; item++) {
                        vehicle_hour_list.push({
                            'date': String(item) + '点',
                            'count': 0
                        })
                    }

                    for (let item in people_list) {
                        people_hour_list[parseInt(people_list[item].date.split(':')[1])].count = people_list[item].count
                    }

                    for (let item in vehicle_list) {
                        vehicle_hour_list[parseInt(vehicle_list[item].date.split(':')[1])].count = vehicle_list[item].count
                    }
                } else {
                    for (let item = 0; item < dlt_day; item++) {
                        if (item !== 0) {
                            people_hour_list.push({
                                'date': new Date(start_date.setDate(start_date.getDate() + 1)).format('YYYY-MM-DD'),
                                'count': 0
                            })
                        } else {
                            people_hour_list.push({
                                'date': new Date(start_date.setDate(start_date.getDate())).format('YYYY-MM-DD'),
                                'count': 0
                            })
                        }

                    }
                    for (let item = 0; item < dlt_day; item++) {
                        if (item !== 0) {
                            vehicle_hour_list.push({
                                'date': new Date(vehicle_start_date.setDate(vehicle_start_date.getDate() + 1)).format('YYYY-MM-DD'),
                                'count': 0
                            })
                        } else {
                            vehicle_hour_list.push({
                                'date': new Date(vehicle_start_date.setDate(vehicle_start_date.getDate())).format('YYYY-MM-DD'),
                                'count': 0
                            })
                        }

                    }

                    for (let i in people_hour_list) {
                        for (let j in people_list) {
                            if (people_hour_list[i].date === people_list[j].date) {
                                people_hour_list[i].count = people_list[j].count;
                                break
                            }
                        }

                    }

                    for (let i in vehicle_hour_list) {
                        for (let j in vehicle_list) {
                            if (vehicle_hour_list[i].date === vehicle_list[j].date) {
                                vehicle_hour_list[i].count = vehicle_list[j].count;
                            }
                        }
                    }

                }

                // X轴坐标轴
                for (let item in people_hour_list) {
                    x_title.push(people_hour_list[item].date)
                }
                // 人脸点坐标
                for (let item in people_hour_list) {
                    people_point_list.push(people_hour_list[item].count)
                }
                // 车辆点坐标
                for (let item in vehicle_hour_list) {
                    vehicle_point_list.push(vehicle_hour_list[item].count)
                }


                self.option.xAxis[0].data = x_title;
                self.option.series[0].data = people_point_list;
                self.option.series[1].data = vehicle_point_list;
                // console.timeEnd('consume');
            });
        }
    },
    template:
        `
<div style="display: flex; position: relative">
    <echarts :option="option" style="width: 100%;height: 280px"></echarts>
    <el-select v-model="value" @change="time_change" size="mini" style="position: absolute; top: -20px; right: 20px; width: 120px;">
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