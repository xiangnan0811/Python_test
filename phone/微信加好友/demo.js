click("通讯录");
sleep(1000);

// + 号
var v = id("fcu").findOne().bounds();
click(v.centerX(), v.centerY());
sleep(1000);
// 添加朋友
var r = id("ipm").text("添加朋友").findOne().bounds();
click(r.centerX(), r.centerY());
sleep(1000);
