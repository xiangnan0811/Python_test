// const Http = XmlHttpRequest();
// const Url = "http://192.168.3.166:8899/phone";
// Http.open("GET", Url);
// Http.send();

// Http.onreadystatechange = (e) => {
//     toast(Http.responseText);
// }

console.show();
http.get("http://192.168.3.166:8899/phone", {}, function(res, err){
    if(err){
        console.error(err);
        return;
    }
    log("code = " + res.statusCode);
    log("html = " + res.body.string());
});
