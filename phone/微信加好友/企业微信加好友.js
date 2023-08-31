
function init() {
    auto.waitFor();
    var height = device.height;
    var width = device.width;
    setScreenMetrics(width, height);
    console.show();
    console.setSize(device.width * 6 / 7, device.height / 3);
    console.setPosition(device.width / 14, device.height * 1 / 4);
    randomSleep(1000, 2000);
}

function enterWechat() {
    toast("进入企业微信");
    launchApp("企业微信");
    randomSleep(1500, 2000);
}

function initializeToAdd() {
    toast("初始化");
    randomSleep(1500, 2000);
    // 先点击消息
    toast("点击消息");
    click("消息");
    randomSleep(1700, 2000);
    // 再点击通讯录
    toast("点击通讯录");
    click("通讯录");
    randomSleep(1800, 2000);
    // 点击客户
    toast("点击我的客户");
    var v = id("fz2").findOne().bounds();
    click(v.centerX(), v.centerY());
    randomSleep(1800, 2000);
    // 点击添加
    toast("点击添加")
    var v = id("kb5").findOne().bounds();
    click(v.centerX(), v.centerY());
    randomSleep(1800, 2000);
    // 点击搜索手机号添加
    toast("点击搜索手机号添加");
    var v = id("kzh").text("搜索手机号添加").findOne().bounds();
    click(v.centerX(), v.centerY());
    randomSleep(1800, 2000);
    // 初始化完成
    toast("初始化完成");
    randomSleep(1800, 2000);
}

function sendAdd(phone) {
    var v = id("jo").text("添加为联系人").findOne().bounds();
    click(v.centerX(), v.centerY());
    randomSleep(1800, 2000);
    // 设置添加理由
    // 1. 点击输入框
    var awa = id("awa").findOne().bounds();
    click(awa.centerX(), awa.centerY());
    randomSleep(1800, 2000);
    // 2. 清空输入框
    // var awb = id("awb").findOne().bounds();
    // click(awb.centerX(), awb.centerY());
    // randomSleep(1800, 2000);
    // 3. 填入添加理由
    var ed = className("EditText").findOne();
    content = phone.send_content;
    if (content == "" || content == undefined || content == null) {
        content = "嗨，你好";
    }
    ed.setText(content);
    randomSleep(1800, 2000);
    // 4. 关闭输入法
    var awn = id("e03").findOne().bounds();
    click(awn.centerX(), awn.centerY());
    randomSleep(1800, 2000);
    // 5. 点击确定
    var e0j = id("e0j").text("发送添加邀请").findOne().bounds();
    click(e0j.centerX(), e0j.centerY());
    randomSleep(4200, 5200);
    // 6. 发送更新请求
    phone.content = content;
    phone.nickname = nickname;
    phone.send_time = getNow();
    phone.send_times = phone.send_times + 1;
    var wechat = assambleWechat(phone);
    updateWechat(wechat);
    // 7. 返回
    backAndRandomSleep(2000, 3000);
}

function getNow() {
    var now = new Date();
    year = now.getFullYear();
    month = now.getMonth() + 1;
    if (month < 10) {
        month = "0" + month;
    }
    day = now.getDate();
    hour = now.getHours();
    minute = now.getMinutes();
    second = now.getSeconds();
    formatNow = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second;
    return formatNow;
}

function getUserNickname() {
    // 获取用户昵称
    var jox = id("jox").findOne();
    nickname = jox.text();
    return nickname;
}

function add(phone) {
    // 填充手机号
    toast("填充手机号");
    randomSleep(1800, 2000);
    // 再输入手机号
    var et = className("EditText").findOne();
    toast("输入手机号");
    et.setText(phone.id);
    randomSleep(1800, 2000);
    // 点击搜索
    var search = id("i55").findOne().bounds();
    click(search.centerX(), search.centerY());
    toast("点击搜索");
    randomSleep(2800, 3500);
    // 判断是否搜索到
    // 对方仅使用企业微信
    if (textContains("企业信息暂时不可见").exists()) {
        randomSleep(1800, 2000);
        toast("对方仅使用企业微信");
        randomSleep(1800, 2000);
        var onlyWork = assambleOnlyWechatWork(phone);
        updateWechat(onlyWork);
        randomSleep(1000, 2000);
        backAndRandomSleep(2000, 3000);
    }
    if(textContains("对方同时使用微信和企业微信").exists()){
        toast("对方同时使用微信和企业微信");
        randomSleep(1800, 2000);
        var cpe = id("cpe").findOne().bounds();
        toast("选择个人微信");
        click(cpe.centerX(), cpe.centerY());
        randomSleep(3900, 4200);
        phone.nickname = getUserNickname();
        sendAdd(phone);
        backAndRandomSleep(2000, 3000);
    }
    // 用户不存在
    if (textContains("该用户不存在").exists()) {
        randomSleep(2000, 3000);
        toast("该用户不存在");
        var ceo = id("ceo").text("确定").findOne().bounds();
        click(ceo.centerX(), ceo.centerY());
        randomSleep(3900, 4200);
        var wechat = assambleNotExistPhone(phone);
        updateWechat(wechat);
        randomSleep(1000, 2000);
    }
    // 已经是好友
    if (textContains("发消息").exists()) {
        randomSleep(1800, 2000);
        toast("已经是好友");
        backAndRandomSleep(2000, 3000);
        phone.nickname = getUserNickname();
        phone.send_time = getNow();
        var friend = assambelFriend(phone);
        updateWechat(friend);
    }
    // 存在但不是好友
    if (textContains("添加为联系人").exists()) {
        randomSleep(1800, 2000);
        toast("存在但不是好友");
        randomSleep(1800, 2000);
        // 获取用户昵称
        phone.nickname = getUserNickname();
        sendAdd(phone);
    }
}

function assambleNotExistPhone(phone) {
    var result = {};
    result.phone = phone.id;
    result.is_add = 4;
    result.nickname = phone.wechat_nickname;
    result.send_content = phone.content;
    result.send_time = phone.send_time;
    result.send_times = phone.send_times;
    return result;
}

function assambleOnlyWechatWork(phone) {
    var result = {};
    result.phone = phone.id;
    result.is_add = 5;
    result.nickname = phone.wechat_nickname;
    result.send_content = phone.content;
    result.send_time = phone.send_time;
    result.send_times = phone.send_times;
    return result;
}

function assambleWechat(phone) {
    var wechat = {};
    wechat.phone = phone.id;
    wechat.is_add = 1;
    wechat.send_content = phone.content;
    wechat.nickname = phone.nickname;
    wechat.send_time = phone.send_time;
    wechat.send_times = phone.send_times;
    return wechat;
}

function assambleFriend(phone) {
    var friend = {};
    friend.phone = phone.id;
    friend.is_add = 2;
    friend.send_content = phone.content;
    friend.nickname = phone.nickname;
    friend.send_time = phone.send_time;
    friend.send_times = phone.send_times;
    return friend;
}

function getPhone() {
    var r = http.get("http://47.108.151.116:6802/phone", {
        headers: {
            'token': "g^@8clGZ99^lYAt3*TZPFW9JUyNyfJ",
            'finger': device.fingerprint
        }
    });
    if (r.statusCode === 200) {
        toast("从云端获取手机号成功");
        var phone = r.body.json();
        return phone;
    } else {
        toast("从云端获取手机号失败");
        return [];
    }
}

function updateWechat(wechat) {
    var url = "http://47.108.151.116:6802/update";
    var r = http.postJson(url, {
        "phone": wechat.phone,
        "is_add": wechat.is_add,
        "send_content": wechat.send_content,
        "wechat_nickname": wechat.nickname,
        "send_time": wechat.send_time,
        "send_times": wechat.send_times
    }, {
        headers: {
            "token": "g^@8clGZ99^lYAt3*TZPFW9JUyNyfJ",
            "finger": device.fingerprint
        }
    });
    if (r.statusCode == 200) {
        toast("更新微信成功");
    } else {
        toast("更新微信失败");
    };
}

function randomSleep(m, n) {
    var random = parseInt(Math.random() * (n - m + 1) + m, 10);
    sleep(random);
}

function backAndRandomSleep(m, n) {
    back();
    randomSleep(m, n);
}

function exit() {
    // 返回
    backAndRandomSleep(1000, 2000);
    // 返回
    backAndRandomSleep(1000, 2000);
    // 返回
    backAndRandomSleep(1000, 2000);
    toast("添加好友任务完成完成");
}

function main() {
    // 初始化
    // init();
    // 进入企业微信
    enterWechat();
    // 准备工作
    initializeToAdd();
    // 从云端获取手机号信息
    phone = getPhone();
    for (var i = 0; i < phone.length; i++) {
        // 循环添加好友
        add(phone[i]);
    }
    // 结束退出
    exit();
}

main();
