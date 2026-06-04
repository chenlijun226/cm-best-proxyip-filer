#正常执行后会在当前目录下生成一行一个的分析链接文件。50行一个文件。ipv4和v6都会包含在内

import os
import json
import urllib.request
import urllib.error

def generate_vless_from_api():
    TARGET_COUNTRY = None
    
    TARGET_ASNS = {
        906,     
        25820,   
        32097,   
        63888,   
        396982,  
        137929,  
        40065,   
        135064,  
        4809,    
        9929,    
        58453    
    }
    
    TARGET_PORT = None

    API_URL = "https://zip.cm.edu.kg/all.json"
    vless_prefix = "vless://b49b465d-657e-4dc0-8b09-215477e9519b@"
    #上一行格式为：vless_prefix = "vless://7f5a9f60-e2fb-46d0-b771-cdbe1db22046@" 更换自己的uuid+@
    vless_suffix = "?encryption=none&security=tls&sni=cmbeta.910226.xyz&fp=chrome&insecure=0&allowInsecure=0&ech=cloudflare-ech.com%2Bhttps%3A%2F%2Fdns.alidns.com%2Fdns-query&type=ws&host=cmbeta.910226.xyz&path=%2F"
    
    print(f"建立网络连接: 开始抓取目标接口数据 {API_URL}")

    def get_system_proxy():
        """从 Windows 注册表读取系统代理设置"""
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                               r"Software\Microsoft\Windows\CurrentVersion\Internet Settings") as key:
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
    except urllib.error.URLError as e:
        print(f"致命阻断: 网络通信故障 详情: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"致命阻断: 数据结构损坏 详情: {e}")
        return
    except Exception as e:
        print(f"致命阻断: 发生未预期错误 详情: {e}")
        return

    print("数据拉取完毕: 启动数据结构动态重构机制")
    
    node_data_list = []
    
    if isinstance(raw_data, list):
        node_data_list = raw_data
    elif isinstance(raw_data, dict):
        for key, value in raw_data.items():
            if isinstance(value, list):
                node_data_list.extend(value)
            elif isinstance(value, dict):
                node_data_list.append(value)

    if not node_data_list:
        print("致命阻断: 原始 JSON 结构解析失败或数据源为空。")
        return
        
    seen_ips = set()
    final_links = []
    best_filter_lines = []

    for item in node_data_list:
        if not isinstance(item, dict):
            continue
            
        meta_data = item.get("meta", {})
        
        port = item.get("_port") or meta_data.get("_port")
        if port is None:
            port_list = item.get("port")
            if isinstance(port_list, list) and len(port_list) > 0:
                port = port_list[0]
                
        country = meta_data.get("country")
        asn = meta_data.get("asn")
        country_cn = meta_data.get("country_cn") or country
        city = meta_data.get("city", "")
        as_org = meta_data.get("asOrganization", "")

        if port is None:
            continue

        if TARGET_COUNTRY and country != TARGET_COUNTRY:
            continue
            
        if TARGET_ASNS and asn not in TARGET_ASNS:
            continue
            
        if TARGET_PORT and int(port) != TARGET_PORT:
            continue
        
        v4_ip = item.get("ip")

        node_ips = []
        if v4_ip:
            node_ips.append(v4_ip)
            
        if not node_ips:
            continue
            
        for current_ip in node_ips:
            if current_ip in seen_ips:
                continue

            seen_ips.add(current_ip)

            best_filter_line = f"{current_ip}:{port}#{country_cn}-{as_org}-AS{asn}"
            best_filter_lines.append(best_filter_line)
            
            if ":" in current_ip:
                formatted_ip = f"[{current_ip}]"
            else:
                formatted_ip = current_ip
                
            remark = f"{country_cn}-{city}-{as_org}-AS{asn}"
            full_url = f"{vless_prefix}{formatted_ip}:{port}{vless_suffix}#{remark}"
            final_links.append(full_url)

    total_links = len(final_links)
    print(f"多维匹配完成: 精确筛出并去重 {total_links} 个独立合规节点。")

    if total_links == 0:
        return

    chunk_size = 100
    for i in range(0, total_links, chunk_size):
        chunk = final_links[i : i + chunk_size]
        file_index = (i // chunk_size) + 1
        output_filename = f"vless_api_part{file_index}.txt"

        with open(output_filename, 'w', encoding='utf8') as out_f:
            for link in chunk:
                out_f.write(link + "\n")

        print(f"数据固化: {output_filename} 封装完毕包含 {len(chunk)} 条记录")

    # 写入 cm-proxyip-best-filter.txt：每行格式 ip#country_cn+city+asn
    best_filter_filename = "cm-proxyip-best-filter.txt"
    with open(best_filter_filename, 'w', encoding='utf8') as f:
        for line in best_filter_lines:
            f.write(line + "\n")
    print(f"数据固化: {best_filter_filename} 封装完毕包含 {len(best_filter_lines)} 条记录")

if __name__ == "__main__":
    generate_vless_from_api()
