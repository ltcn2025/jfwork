import re

def normalize_domain(domain):
    """
    标准化域名，去除 www、www1 等子域名，只保留主域名。
    """
    domain = domain.lower()  # 转小写
    # 去掉常见的子域名（如 www, www1）
    domain = re.sub(r"^(www\d*\.)", "", domain)
    return domain

def convert_gfw_to_adblock():
    # 使用集合来存储唯一的规则
    unique_domains = set()

    # 下载的 gfwlist.txt 文件路径
    with open('gfw.txt', 'r') as file:
        lines = file.readlines()

    for line in lines:
        # 跳过注释行
        if line.startswith('#') or line.strip() == '':
            continue

        # 去掉行尾的空格和换行符
        line = line.strip()

        # 处理以 || 开头的规则
        if line.startswith('||'):
            domain = line[2:]  # 去掉前缀 || 
            normalized_domain = normalize_domain(domain)  # 标准化域名
            unique_domains.add(f"||{normalized_domain}$")
        else:
            # 对其他规则进行处理，去掉协议部分（http:// 或 https://）
            domain = re.sub(r"^https?://", "", line)
            normalized_domain = normalize_domain(domain)  # 标准化域名
            unique_domains.add(f"||{normalized_domain}$")

    # 将去重后的规则一次性写入 gfw-ok.txt 文件
    with open('gfw-ok.txt', 'w') as file:
        for domain in unique_domains:
            file.write(f"{domain}\n")

if __name__ == "__main__":
    convert_gfw_to_adblock()
