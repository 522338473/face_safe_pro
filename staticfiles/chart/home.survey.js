Vue.component('home-survey', {
    data() {
        return {
            loading: false,
            survey: {},
        }
    },
    mounted() {
        let self = this;
        self.loading = true;
        axios.get('/v1/device/photo/survey/?format=json', {params: {}}, {
            'Content-Type': 'application/json;charset=UTF-8'
        }).then(res => {
            self.survey = res.data;
        }).finally(() => {
            self.loading = false;
        })
    },
    template:
        `
        <div class="today-about">
        <p>概况</p>
        <div style="width: 100%; display: inline-block;  margin-bottom: 10px;">
            <div style="width: 25%; display: block; float: left;border-right: 1px solid #e5e5e5;">
                <p style="font-size: 20px; color: #999999; letter-spacing: 0; line-height: 24px; margin: 0;">今日抓拍</p>
                <p style="height: 62px; font-size: 46px; font-weight: 500; color: #3d7cd2; border-bottom: 1px solid rgb(229, 229, 229); margin: 0 17px 0 0; cursor: pointer">{{ survey.now_days_snap_total || 10000 }}</p>
            </div>
            <div style="width: 25%; display: block; float: left; margin-left: 17px;">
                <p style="font-size: 20px; color: #999999; letter-spacing: 0; line-height: 24px; margin: 0">总抓拍</p>
                <p style="height: 62px; font-size: 46px; font-weight: 500; color: #3d7cd2; border-bottom: 1px solid rgb(229, 229, 229); margin: 0; cursor: pointer">{{ survey.all_days_snap_total || 1000000000 }}</p>
            </div>
        </div>
        <div style="width: 100%;display: inline-block">
            <div style="width: 25%; display: block; float: left;border-right: 1px solid #e5e5e5;">
                <p style="font-size: 20px; color: #999999; letter-spacing: 0; line-height: 24px; margin: 0;">重点人员</p>
                <p style="height: 62px; font-size: 46px; font-weight: 500; color: rgb(241, 111, 111); margin: 0; cursor: pointer">{{ survey.monitor_total || 999 }}</p>
            </div>
            <div style="width: 25%; display: block; float: left;border-right: 1px solid #e5e5e5; margin-left: 17px">
                <p style="font-size: 20px; color: #999999; letter-spacing: 0; line-height: 24px; margin: 0;">关注人员</p>
                <p style="height: 62px; font-size: 46px; font-weight: 500; color: rgb(239, 149, 74); margin: 0; cursor: pointer">{{ survey.personnel_total || 999 }}</p>
            </div>
            <div style="width: 25%; display: block; float: left; margin-left: 17px">
                <p style="font-size: 20px; color: #999999; letter-spacing: 0; line-height: 24px; margin: 0;">人员档案</p>
                <p style="height: 62px; font-size: 46px; font-weight: 500; color: rgb(139, 211, 138); margin: 0; cursor: pointer">{{ survey.archives_total || 500 }}</p>
            </div>
        </div>
    </div>
`
})