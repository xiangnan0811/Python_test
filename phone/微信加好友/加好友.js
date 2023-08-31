//作者：鲍继川   邮箱 baojichuan@qq.com
//var f=files.read("/sdcard/1/1.txt"));
//文件所在位置。打开并逐行读取。
//var f=files.read("/sdcard/1/1.txt"));

//主界面开始点击动作
while (!click("通讯录"));

sleep(1000);
//id("dmw").findOne().click();


//添加朋友
var v = id("fcu").findOne().bounds();
//log(v+"ggg");
click(v.centerX(), v.centerY());
sleep(1000);
var r = id("ipm").text("添加朋友").findOne().bounds();
//log(r);
click(r.centerX(), r.centerY());
sleep(1000);

//while (!click("添加朋友"));

//读取通讯录电话号码，遍历

var f = open("/sdcard/1/1.txt", "r");
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

    //while (!click("微信号/手机号"));

    sleep(2000);

    //className("ImageView").findOne().click();

    //var y=id("c8x").findOne();//.bounds();
    //log(y);

    // setClip(s[i]);

    if (s[i].trim() == "") {
        log("空字符串");
        back();
        sleep(1000);
        back();
        continue;
    }

    var et = className("EditText").findOne();
    et.setText(s[i]);

    //longClick(y.centerX(),y.centerY());

    sleep(1000);

    //var u=textContains("粘贴").findOne().bounds();
    //log("粘贴"+u);

    //click(70,330);
    //while(!click("粘贴"));

    log("做");
    while (!click("搜索"));

    /*

    sleep(1000);

    var p=id("ga1").findOne().bounds();
    log(p);
    click(p.centerX(),p.centerY());
    sleep(1000);
    */

    //className("android.widget.LinearLayout").click();

    //id("f43").findOne().click();

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
// 设置朋友圈权限 ，微信8.0 更新
var v = id("hzq").findOne().parent().parent().click();


    //id("f5h").findOne().setText(s[i]+"潜在");
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

//作者：鲍继川   邮箱 baojichuan@qq.com
toastLog("结束");
