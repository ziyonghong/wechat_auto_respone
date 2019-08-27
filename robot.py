from wxpy import *

#微信自动回复聊天机器人
# 登录
bot = Bot()


# 初始化图灵机器人
tulingrobot = Tuling(api_key='008b981c33244ca8b2dcf214738ec0d3')
# 自动回复所有文字消息
@bot.register(msg_types=TEXT)
def auto_reply(msg):
    # 如果是群聊，但没有被 @，则不回复
    if isinstance(msg.chat, Group) and not msg.is_at:
        return
    else:
        # 回复消息内容和类型
        tulingrobot.do_reply(msg)
# 开始运行
bot.join()