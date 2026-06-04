path = r"D:\sre-python\CheckProxyip\cm反代ip高优筛选订阅.py"
content = open(path, encoding="utf8").read()
content = content.replace("path=%2Fproxyip%3D47.76.218.163%3A443", "path=%2F")
open(path, "w", encoding="utf8").write(content)
print("Done")
