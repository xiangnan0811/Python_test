// 进入微信
launchApp("微信");
sleep(1000);

// + 号
var v = id("fcu").findOne().bounds();
click(v.centerX(), v.centerY());
sleep(1000);
// 添加朋友
var r = id("ipm").text("添加朋友").findOne().bounds();
click(r.centerX(), r.centerY());
sleep(1000);

// 读取手机号，遍历添加
var f = open("./手机号.txt", "r");
var s = f.readlines();
log(s.length);
var l = s.length;
for (var i = 0; i < l; i++) {
    log(s[i] + "xxx");

    sleep(3000);
    log("222");

    var t = id("hej").findOne().bounds();
    log(t);
    click(t.centerX(), t.centerY());
    sleep(1000);

    var et = className("EditText").findOne();
    et.setText(s[i]);

    sleep(1000);

    log("做");
    while (!click("搜索"));

    sleep(3000);

    log("搜索后");
	//异常处理
    if (textContains("该用户不存在").exists()) {
        back();
        sleep(1000);
        continue;
    }

    if (textContains("发消息").exists()) {
        log("发消息存在")
        back();
        sleep(1500);
        back();
        continue;
    }

    if (textContains("状态异常").exists()) {
        log("状态异常")

        sleep(1500);
        back();
        continue;
    }

    while (!click("添加到通讯录"));

    sleep(3000);

    if (textContains("发消息").exists()) {
        log("无验证通过")
        back();
        sleep(1500);
        back();
        continue;
    }

	sleep(1000);

    // id("f5e").findOne().setText("嗨，你好");
    while (!click("发送"));
    sleep(2000);
    if (textContains("操作过于频繁").findOnce() != null) {
        log("操作过于频繁，终止");
        break;
    }
    log("已添加好友" + s[i]);

    sleep(2000);

    back();

    sleep(2000);
    back();
}

toastLog("结束");
alert("结束");

toastLog("结束");
