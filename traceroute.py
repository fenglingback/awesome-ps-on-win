import subprocess
import requests
import json as _json


def get_route() -> list:

    host = input("\n请输入需要追踪的 ip/域名 ：")

    print("\n设置最大的追踪次数（跃点数），请注意：\n\n1. 区间为20 ~ 40，输入其他一律默认为30\n2. 如果最终结果的结尾出现\"→\"，可以把数字调大\n")
    num = input("请输入：")

    try:
        num = int(num)
        if num < 20 or num > 40:
            num = 30
    except ValueError:
        num = 30

    print(f"\n正在追踪 {host} 中，设置的最大跃点数为 {num} .........可能需要几分钟，请耐心等待.........")
    print("\n出现报错请检查：\n\n 1. ip/域名 的输入格式是否正确\n 2. 是否已经关闭代理\n")


    # 执行命令并获取输出结果
    result = subprocess.run(f"tracert -d -h {num} {host}", capture_output=True, text=True)


    # 打印输出结果
    data = result.stdout.splitlines("\n")

    data.pop(0)
    data.pop(0)
    data.pop(0)
    data.pop(0)
    data.pop(0)
    data.pop()
    data.pop()

    end_data = []

    for val in data:
        end_val = val.split(" \n")[0].split()[-1]
        if end_val != "请求超时。":
            end_data.append(end_val)

    return end_data


# end_data = ['202.97.93.49', '8.8.8.8']


def get_address(data: list) -> requests.Response:

    gz = _json.dumps(data)

    he = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }

    resp = requests.request(method="post", url="http://ip-api.com/batch?fields=57369&lang=zh-CN", data=gz, headers=he)

    return resp


def print_result(resp: requests.Response):

    # print(_json.dumps(resp.json(), indent=4, ensure_ascii=False))

    print("↓↓↓↓↓↓↓↓↓路由追踪结果为↓↓↓↓↓↓↓↓↓\n")

    result = ""

    for i, v in enumerate(resp.json(), start=1):
        if v["status"] == "fail":
            continue
        addr = v["country"] + v["regionName"] + v["city"]
        if i != len(resp.json()):
            result += (addr + " -> ")
        else:
            result += addr

    print(result)

    print("\n↑↑↑↑↑↑↑↑↑追踪完毕↑↑↑↑↑↑↑↑↑")


if __name__ == "__main__":

    is_continue = "y"
    while is_continue.lower() in ["yes", "y"]:
        data = get_route()
        resp = get_address(data)
        print_result(resp)
        is_continue = input("\n是否继续追踪？(y/n)：")
    else:
        print("\n--------------退出程序----------------")

    
