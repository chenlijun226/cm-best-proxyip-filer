path = r"D:\sre-python\CheckProxyip\cm反代ip高优筛选订阅.py"
content = open(path, encoding="utf8").read()
idx = content.find("country = meta_data.get")
print(content[idx:idx+300])
print("---")
idx2 = content.find("full_url = ")
print(content[idx2-30:idx2+200])
