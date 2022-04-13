Vue.component('home-line', {
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
            }
        }
    },
    mounted() {

        //请求数据 伪代码
        let self = this;
        axios.get("/v1/device/photo/snap_count/?format=json", {
            params: {
                start_time: '20220402000000',
                end_time: '20220422000000'
            }
        }, {
            'Content-Type': 'application/json;charset=UTF-8'
        }).then(res => {
            // console.log(res.data);
        });
    },
    template:
        `<div style="display: flex">
    <echarts :option="option" style="width: 100%;height: 280px"></echarts>
</div>`
})