import os
path = r"D:\sre-python\CheckProxyip\cm反代ip高优筛选订阅.py"
content = open(path, encoding="utf8").read()

old = '        v4_ip = item.get("ip")\n        v6_ip = meta_data.get("clientIp")\n        \n        node_ips = []\n        if v4_ip:\n            node_ips.append(v4_ip)\n        if v6_ip:\n            node_ips.append(v6_ip)'

new = '        v4_ip = item.get("ip")\n\n        node_ips = []\n        if v4_ip:\n            node_ips.append(v4_ip)'

if old in content:
    content = content.replace(old, new)
    open(path, "w", encoding="utf8").write(content)
    print("Done - removed IPv6")
else:
    print("Pattern not found, checking actual content...")
    idx = content.find('v4_ip')
    if idx >= 0:
        print(content[idx:idx+200])
