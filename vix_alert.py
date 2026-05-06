# vix_alert.py
import yfinance as yf
import pandas as pd
from datetime import datetime
import requests
import json

# 获取VIX数据
def get_vix_data():
    vix = yf.Ticker("^VIX")
    df = vix.history(period="3mo")  # 最近3个月数据
    latest = df.iloc[-1]
    today_vix = round(latest['Close'], 2)
    
    # 计算20以上的最高点
    above_20 = df[df['Close'] >= 20]
    if not above_20.empty:
        recent_peak = round(above_20['Close'].max(), 2)
        # 判断是否从高点回落超过3%
        drop = round(recent_peak - today_vix, 2)
        is_dropping = drop >= 3  # 回落超过3%才算信号
    else:
        recent_peak = None
        is_dropping = False
        drop = 0
    
    return today_vix, recent_peak, is_dropping, drop

# 生成投资建议
def generate_suggestion(vix, peak, is_dropping, drop):
    if vix < 20:
        return f"🔵 观望\n当前VIX={vix}，低于20警戒线。\n建议：持有现金，等待机会。"
    elif vix >= 20 and not is_dropping:
        return f"⚠️ 警戒\n当前VIX={vix}，进入恐慌区。\n从高点{peak}仅回落{drop}点，未达3%触发条件。\n建议：等待进一步回落。"
    elif vix >= 20 and is_dropping:
        return f"🟢 低档买进信号！\n当前VIX={vix}，已从高点{peak}回落{drop}点（超过3%）。\n建议：可分批买入SPY/VOO。"
    else:
        return "数据异常，请检查"

# 发送到微信（通过Server酱）
def send_to_wechat(message):
    # 稍后填入你的key
    server_key = os.environ.get("WECHAT_SENDKEY")  # 需要替换
    url = f"https://sctapi.ftqq.com/{server_key}.send"
    data = {
        "title": "VIX投资建议",
        "desp": message
    }
    try:
        response = requests.post(url, data=data)
        return response.status_code == 200
    except:
        return False

# 主程序
def main():
    print(f"执行时间：{datetime.now()}")
    vix, peak, is_dropping, drop = get_vix_data()
    suggestion = generate_suggestion(vix, peak, is_dropping, drop)
    print(suggestion)
    
    # 发送到微信
    success = send_to_wechat(suggestion)
    if success:
        print("微信发送成功")
    else:
        print("微信发送失败，请检查SendKey")

if __name__ == "__main__":
    main()
