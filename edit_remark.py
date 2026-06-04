path = r"D:\sre-python\CheckProxyip\cm反代ip高优筛选订阅.py"
content = open(path, encoding="utf8").read()

# 1) Add country_cn and city extraction after asn line
content = content.replace(
    "        country = meta_data.get(\"country\")\n        asn = meta_data.get(\"asn\")",
    "        country = meta_data.get(\"country\")\n        asn = meta_data.get(\"asn\")\n        country_cn = meta_data.get(\"country_cn\") or country\n        city = meta_data.get(\"city\", \"\")"
)

# 2) Change full_url line to include dynamic fragment
content = content.replace(
    "            full_url = f\"{vless_prefix}{formatted_ip}:{port}{vless_suffix}\"",
    "            remark = f\"{country_cn}+{city}+{asn}\"\n            full_url = f\"{vless_prefix}{formatted_ip}:{port}{vless_suffix}#{remark}\""
)

open(path, "w", encoding="utf8").write(content)
print("Done")
