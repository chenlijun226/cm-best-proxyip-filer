path = r"D:\sre-python\CheckProxyip\cm反代ip高优筛选订阅.py"
content = open(path, encoding="utf8").read()

old = 'vless_suffix = "?encryption=none&security=tls&sni=.....&type=ws#edgetunnel"\n    #上一行格式为：?encryption=none&security=tls&sni=.......#edgetunnel 即除了host：端口之外的所有内容'

new = 'vless_suffix = "?encryption=none&security=tls&sni=cmbeta.910226.xyz&fp=chrome&insecure=0&allowInsecure=0&ech=cloudflare-ech.com%2Bhttps%3A%2F%2Fdns.alidns.com%2Fdns-query&type=ws&host=cmbeta.910226.xyz&path=%2Fproxyip%3D47.76.218.163%3A443"'

content = content.replace(old, new)
open(path, "w", encoding="utf8").write(content)
print("Done")
