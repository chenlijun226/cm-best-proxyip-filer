path = r"D:\sre-python\CheckProxyip\cm反代ip高优筛选订阅.py"
content = open(path, encoding="utf8").read()

# 1) Add asOrganization extraction after city line
content = content.replace(
    "        city = meta_data.get(\"city\", \"\")",
    "        city = meta_data.get(\"city\", \"\")\n        as_org = meta_data.get(\"asOrganization\", \"\")"
)

# 2) Update remark to include asOrganization
content = content.replace(
    "remark = f\"{country_cn}-{city}-AS{asn}\"",
    "remark = f\"{country_cn}-{city}-{as_org}-AS{asn}\""
)

open(path, "w", encoding="utf8").write(content)
print("Done")
