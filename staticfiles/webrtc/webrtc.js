Vue.component('webrtc', {
    props: ['style', 'url'],
    data() {
        return {
            loading: false
        }
    },
    mounted() {
        let self = this;

    },
    template:
        `
        <div :style="style">
        {{ url || '木有获取到数据' }}
</div>
`
})