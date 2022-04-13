Vue.component('index-chart', {
    data() {
        return {
            option1: {
                xAxis: {
                    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                },
                yAxis: {},
                series: [
                    {
                        type: 'bar',
                        data: [23, 24, 18, 25, 27, 28, 25]
                    }
                ]
            },
            option2: {
                xAxis: {
                    type: 'category',
                    data: ['A', 'B', 'C']
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        data: [120, 200, 150],
                        type: 'line'
                    }
                ]
            }
        }
    },
    mounted() {
        //动态更新数据
        //在这里 利用axios一类的工具请求接口，然后返回数据，
        // 设置到对应到图表上面就会自动更新数据，
        // 图表到option内容可以参考echarts的文档 https://echarts.apache.org/handbook/zh/how-to/chart-types/line/basic-line

        //请求数据 伪代码
        let self = this;
        axios.get("https://sdc.72wo.com/echarts/line.json").then(res => {
            // console.log(res)
            //可以返回整个option，也可以返回option的数据
            //这里的例子，是返回了全部option的数据
            let data = res.data;
            self.option2 = data;

        });
    },
    template:
        `<div style="display: flex">
    <div> 图表插件</div>
    <echarts :option="option1" style="width: 300px;height: 300px"></echarts>
    <echarts :option="option2" style="width: 300px;height: 300px"></echarts>
</div>`
})