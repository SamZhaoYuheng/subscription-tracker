def get_cancel_guide(platform):
    guide_dict = {
        "Netflix": "前往Netflix官网账号设置，选择取消订阅，按指引完成。",
        "Spotify": "打开Spotify网页版，进入账号计划，取消高级订阅。",
        "YouTube": "YouTube账号-购买和会员，找到会员并取消。",
        "ChatGPT Plus": "OpenAI官网账户页面，管理订阅取消。"
    }
    return guide_dict.get(platform, "请自行前往对应平台账号页面查找取消入口。")
