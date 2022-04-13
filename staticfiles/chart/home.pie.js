Vue.component('home-pie', {
    data() {
        return {
            option: {
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b}: {c} ({d}%)'
                },
                color: ['#F26F6F', '#5C9AEE'],
                legend: {
                    orient: 'horizontal',
                    left: 70,
                    top: 230,

                },
                series: [
                    {
                        name: '摄像头状态',
                        type: 'pie',
                        radius: ["20%", "45%"],
                        center: ["50%", "40%"],
                        avoidLabelOverlap: false,
                        label: {
                            show: false,
                            position: 'center',
                            emphasis: {
                                show: true,
                                textStyle: {
                                    fontSize: "14",
                                    fontWeight: "bold",
                                },
                            }
                        },
                        emphasis: {
                            label: {
                                show: true,
                                fontSize: '14',
                                fontWeight: 'bold'
                            }
                        },
                        labelLine: {
                            normal: {
                                show: false,
                                length: 5,
                            },
                        },
                        itemStyle: {
                            normal: {
                                shadowBlur: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        },
                        data: [
                            {value: 2, name: '在线'},
                            {value: 1, name: '离线'}
                        ]
                    }
                ]
            }
        }
    },
    mounted() {

        //请求数据 伪代码
        let self = this;
        axios.get("/v1/device/info/device_status/?format=json").then(res => {
            let device_status = [];
            res.data.forEach(function (item) {
                if (item.status === 1) {
                    device_status.push({
                        name: '在线',
                        value: item.count
                    })
                } else {
                    device_status.push({
                        name: '离线',
                        value: item.count
                    })
                }
            })
            self.option.series[0].data = device_status;

        });
    },
    template:
        `<div style="display: flex">
    <echarts :option="option" style="width: 100%;height: 350px"></echarts>
</div>`
})