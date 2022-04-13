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
            }
        }
    },
    mounted() {

        //请求数据 伪代码
        let self = this;
        axios.get("/v1/monitor/monitor/count/?format=json", {params: {}}, {
            'Content-Type': 'application/json;charset=UTF-8'
        }).then(res => {
            // console.log(res.data)
        });
    },
    template:
        `<div style="display: flex">
    <echarts :option="option" style="width: 100%;height: 280px"></echarts>
</div>`
})