import io
path = r"D:\sre-python\CheckProxyip\cm反代ip高优筛选订阅.py"
with io.open(path, "r", encoding="utf8") as f:
    content = f.read()

# 1) Add os import before json
content = content.replace(
    u"import json\nimport urllib.request\nimport urllib.error",
    u"import os\nimport json\nimport urllib.request\nimport urllib.error"
)

# 2) Before the try block, insert proxy detection
old_try = u'''    print(f"\u5EFA\u7ACB\u7F51\u7EDC\u8FDE\u63A5: \u5F00\u59CB\u6293\u53D6\u76EE\u6807\u63A5\u53E3\u6570\u636E {API_URL}")
    
    try:
        request_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        req = urllib.request.Request(API_URL, headers=request_headers)
        with urllib.request.urlopen(req, timeout=20) as response:
            json_response = response.read().decode('utf8')
            raw_data = json.loads(json_response)
    except urllib.error.URLError as e:'''

new_try = u'''    print(f"\u5EFA\u7ACB\u7F51\u7EDC\u8FDE\u63A5: \u5F00\u59CB\u6293\u53D6\u76EE\u6807\u63A5\u53E3\u6570\u636E {API_URL}")

    def get_system_proxy():
        """\u4ECE Windows \u6CE8\u518C\u8868\u8BFB\u53D6\u7CFB\u7EDF\u4EE3\u7406\u8BBE\u7F6E"""
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                               r"Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings") as key:
                proxy_enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
                if proxy_enable:
                    proxy_server, _ = winreg.QueryValueEx(key, "ProxyServer")
                    if proxy_server and not proxy_server.startswith(('http://', 'https://', 'socks')):
                        proxy_server = 'http://' + proxy_server
                    return proxy_server
        except Exception:
            pass
        return None

    proxy = (os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy') or
             os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy') or
             get_system_proxy())

    try:
        request_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        req = urllib.request.Request(API_URL, headers=request_headers)

        if proxy:
            proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
            opener = urllib.request.build_opener(proxy_handler)
            with opener.open(req, timeout=20) as response:
                json_response = response.read().decode('utf8')
                raw_data = json.loads(json_response)
        else:
            with urllib.request.urlopen(req, timeout=20) as response:
                json_response = response.read().decode('utf8')
                raw_data = json.loads(json_response)
    except urllib.error.URLError as e:'''

content = content.replace(old_try, new_try)

with io.open(path, "w", encoding="utf8") as f:
    f.write(content)

print("Modified successfully")
