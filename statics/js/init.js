var Init = (function () {
    let library = (function () {
        return {
            GetDeviceID: function () {
                let id = localStorage.getItem("device_id")
                if (id == null) {
                    var s = [];
                    var hexDigits = "0123456789abcdef";
                    for (var i = 0; i < 36; i++) {
                        s[i] = hexDigits.substr(Math.floor(Math.random() * 0x10), 1);
                    }
                    s[14] = "4";
                    s[19] = hexDigits.substr((s[19] & 0x3) | 0x8, 1);
                    s[8] = s[13] = s[18] = s[23] = "-";
                    id = s.join("");
                    localStorage.setItem("device_id", id)
                }
                return id;
            },
            IsAppleStore: function () {
                let u = navigator.userAgent,
                    app = navigator.appVersion;
                let ios = !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/);
                let iPad = u.indexOf('iPad') > -1;
                let iPhone = u.indexOf('iPhone') > -1 || u.indexOf('Mac') > -1;
                return ios || iPad || iPhone;
            },
            IsAndroidList: function () {
                let u = navigator.userAgent;
                return u.indexOf('Android') > -1 || u.indexOf('Adr') > -1;
            },
            IsPC: function () {
                let userAgentInfo = navigator.userAgent;
                let Agents = ["Android", "iPhone",
                    "SymbianOS", "Windows Phone",
                    "iPad", "iPod"];
                let flag = true;
                for (var v = 0; v < Agents.length; v++) {
                    if (userAgentInfo.indexOf(Agents[v]) > 0) {
                        flag = false;
                        break;
                    }
                }
                return flag;
            },
            GetDeviceType: function () {
                if (library.IsAppleStore()) {
                    return "mobile"
                }
                if (library.IsAndroidList()) {
                    return "mobile"
                }
                if (library.IsPC()) {
                    return "pc"
                }
            }
        }
    })()
    return {
        getDevice_id:function (){
            return library.GetDeviceID()
        },
        getDevice_type:function (){
            return library.GetDeviceType()
        },
        getDevice_brand:function (){
            return "unknown"
        },
        getProtocol_type:function (){
            return "websocket"
        }
    }
})()