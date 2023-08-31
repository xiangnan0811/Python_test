console.show();
var r = http.get("http://192.168.3.166:8899/phone", {
    headers: {
        'imei': device.getIMEI(),
        'fingerprint': device.fingerprint
    }
});
log("code = " + r.statusCode);
log("html = " + r.body.string());
