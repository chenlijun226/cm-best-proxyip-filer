path = r"D:\sre-python\CheckProxyip\cm反代ip高优筛选订阅.py"
content = open(path, encoding="utf8").read()
content = content.replace('remark = f"{country_cn}+{city}+{asn}"', 'remark = f"{country_cn}-{city}-AS{asn}"')
open(path, "w", encoding="utf8").write(content)
print("Done")
