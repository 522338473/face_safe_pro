Vue.component('device-map', {
    props: ['style'],
    data() {
        return {
            //去高德开放平台申请的key
            key: '9e42abc80131110fad5b71d7d4a1d7e7',
            markers: [
                {
                    "address": "莲花山公园",
                    "geo": "114.058454,22.554387",
                    "create_at": "2022-04-14 00:03:05"
                },
                {
                    "address": "飞来石",
                    "geo": "114.035451,22.583554",
                    "create_at": "2022-04-14 00:03:05"
                },
                {
                    "address": "塘朗山公园",
                    "geo": "114.01056,22.572775",
                    "create_at": "2022-04-14 00:03:05"
                },
                {
                    "address": "欢乐谷-这个没有创建时间，不连他",
                    "geo": "113.980863,22.540911"
                },
                {
                    "address": "深圳湾",
                    "geo": "113.972108,22.518554",
                    "create_at": "2022-04-14 00:03:05"
                },
                {
                    "address": "红树林",
                    "geo": "114.011419,22.522677",
                    "create_at": "2022-04-14 00:03:05"
                }
            ],
        }
    },
    methods: {
        mapReady(map) {
            //地图初始化完成了，才能调用ajax接口请求数据，上面的markers 可以设置为空数组[]
            this.getData();
        },
        getData() {
            let self = this;
            axios.get('/v1/device/info/?format=json&paginate=off').then(res => {
                self.markers = res.data;
            })
        }
    },
    template: `
        <amap-lite :key="key" :markers="markers" :style="style" @map-ready="mapReady"></amap-lite>
        `
})