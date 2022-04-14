Vue.component('webrtc', {
    props: {
        url: {
            type: String,
            default: "",
        },
        style: {
            type: String,
            default: ""
        }
    },
    data() {
        return {
            loading: false
        }
    },
    mounted() {
        let webrtc, webrtcSendChannel;
        this.startPlay();
    },
    methods: {
        startPlay() {
            let videoEl = document.querySelector('#webrtc-video');
            webrtc = new RTCPeerConnection({
                iceServers: [{
                    urls: [
                        "stun:stun01.sipphone.com",
                        "stun:stun.ekiga.net",
                        "stun:stun.fwdnet.net",
                        "stun:stun.ideasip.com",
                        "stun:stun.iptel.org",
                        "stun:stun.rixtelecom.se",
                        "stun:stun.schlund.de",
                        "stun:stunserver.org",
                        "stun:stun.softjoys.com",
                        "stun:stun.voiparound.com",
                        "stun:stun.voipbuster.com",
                        "stun:stun.voipstunt.com",
                        "stun:stun.voxgratia.org",
                        "stun:stun.xten.com",
                    ]
                }],
                sdpSemantics: "unified-plan"
            });
            webrtc.onnegotiationneeded = this.handleNegotiationNeeded;
            webrtc.ontrack = function (event) {
                console.log(event.streams.length + ' track is delivered');
                videoEl.srcObject = event.streams[0];
                videoEl.play();
            }
            webrtc.addTransceiver('video', {
                'direction': 'sendrecv'
            });
            webrtcSendChannel = webrtc.createDataChannel('foo');
            webrtcSendChannel.onclose = () => {
                // this.startPlay();
                console.log('sendChannel has closed');
            }
            webrtcSendChannel.onopen = () => {
                console.log('sendChannel has opened');
                webrtcSendChannel.send('ping');
                setInterval(() => {
                    webrtcSendChannel.send('ping');
                }, 1000)
            }
            webrtcSendChannel.onmessage = e => console.log(e.data);

        },
        async handleNegotiationNeeded() {
            let offer = await webrtc.createOffer();

            await webrtc.setLocalDescription(offer);

            fetch(this.url, {
                method: 'POST', body: new URLSearchParams({
                    data: btoa(webrtc.localDescription.sdp)
                })
            })
                .then(response => response.text())
                .then(data => {
                    try {
                        webrtc.setRemoteDescription(new RTCSessionDescription({
                            type: 'answer',
                            sdp: atob(data)
                        }))
                    } catch (e) {
                        console.warn(e);
                    }
                })
        }
    },
    beforeDestroy() {
        webrtc.close();
        webrtcSendChannel.close();
    },
    template:
        `
        <video v-loading="loading" id="webrtc-video" :style="style" autoplay controls muted playsinline></video>
`
})