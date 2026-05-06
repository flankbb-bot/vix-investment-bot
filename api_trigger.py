mport os
import json
import urllib.request

def main():
    # 抓VIX
    url = 'https://query1.finance.yahoo.com/v8/finance/chart/%5EVIX'
    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read())
        vix = data['chart']['result'][0]['meta']['regularMarketPrice']
    
    # 规则
    if vix < 20:
        msg = f'观望 {vix}'
    elif vix < 25:
        msg = f'警戒 {vix}'
    else:
        msg = f'买进信号 {vix}'
    
    # 发微信
    sendkey = os.environ.get('WECHAT_SENDKEY')
    urllib.request.urlopen(f'https://sctapi.ftqq.com/{sendkey}.send?title=VIX&desp={msg}')
    print('ok')

if __name__ == '__main__':
    main()
