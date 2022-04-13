//注册一个Vue的组件
Vue.component("amap-lite", {
    props: {
        key: {
            type: String,
            default: "9e42abc80131110fad5b71d7d4a1d7e7",
            required: false
        },
        //地图上的点
        markers: {
            type: Array,
            default: () => [],
            required: false
        }
    },
    watch: {
        markers: {
            handler: function (newVal, oldVal) {
                this.addMarkers();
            },
            deep: true
        }
    },
    data() {
        return {
            loading: false,
            map: null
        }
    },
    mounted() {
        let self = this;
        self.loading = true;
        AMapLoader.load({
            "key": this.key,              // 申请好的Web端开发者Key，首次调用 load 时必填
            "version": "2.0",   // 指定要加载的 JSAPI 的版本，缺省时默认为 1.4.15
            "plugins": [],           // 需要使用的的插件列表，如比例尺'AMap.Scale'等
            "AMapUI": {             // 是否加载 AMapUI，缺省不加载
                "version": '1.1',   // AMapUI 版本
                "plugins": ['overlay/SimpleMarker'],       // 需要加载的 AMapUI ui插件
            },
            "Loca": {                // 是否加载 Loca， 缺省不加载
                "version": '2.0'  // Loca 版本
            },
        }).then((AMap) => {
            self.initMap(AMap);
        }).catch((e) => {
            console.error(e);  //加载错误提示
        });
    },
    methods: {
        initMap(AMap) {
            let self = this;
            let map = new AMap.Map(self.$refs.container);
            // map.addControl(new AMap.Scale());

            self.map = map;
            self.AMap = AMap;
            self.addMarkers(AMap);
            map.on('complete', () => {
                self.loading = false;
                self.$emit('map-ready', map);
            });
            window.map = map;

        },
        getPosition(geo) {
            let AMap = this.AMap;
            let gs = geo.split(",");
            return new AMap.LngLat(gs[0], gs[1]);
        },
        addPath() {
            let self = this;
            let map = self.map;
            let AMap = self.AMap;

            //计算路径数据
            let path = [];
            let markers = self.markers;
            for (let i = 0; i < markers.length; i++) {
                let marker = markers[i];
                if (marker.create_at) {
                    let position = self.getPosition(marker.geo);
                    path.push([position.lng, position.lat]);
                }
            }
            if(path.length === 0){
                return;
            }
            let polyline1 = new AMap.Polyline({
                path: path,            // 设置线覆盖物路径
                showDir: true,
                strokeColor: '#3366bb',   // 线颜色
                strokeWeight: 10           // 线宽
            });
            map.add(polyline1);
            // console.log(path)

        },
        addMarkers() {
            let self = this;
            let map = self.map;
            let AMap = self.AMap;
            //清空覆盖物
            map.clearMap();
            //如果数据不为空点时候，设置地图点中心为第一个点
            if (self.markers.length > 0) {
                map.setCenter(self.getPosition(self.markers[0].geo));
            }
            //设置点
            self.markers.forEach(item => {
                // console.log(item)
                let marker = new AMap.Marker({
                    icon: "https://webapi.amap.com/theme/v1.3/markers/n/mark_r.png",
                    position: self.getPosition(item.geo),
                    anchor: 'bottom-center'
                });
                marker.setTitle(item.address);
                map.add(marker);
                // self.map.addMarker(marker);
            });

            //添加路径
            self.addPath();

            map.setFitView();

        }

    },
    template: `<div ref="container" v-loading="loading">这是一个地图的组件</div>`
})