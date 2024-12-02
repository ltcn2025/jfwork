import re
import base64
import urllib.parse


def normalize_domain(domain):
    """
    标准化域名，去除 www、www1 等子域名，只保留主域名。
    """
    domain = domain.lower()  # 转小写
    # 去掉常见的子域名（如 www, www1）
    domain = re.sub(r"^(www\d*\.)", "", domain)
    return domain


def read_custom_file():
    """
    读取 custom.txt 文件并返回其中的规则内容。
    """
    try:
        with open('custom.txt', 'r') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print("custom.txt not found, skipping custom rules.")
        return []


def convert_gfw_to_switchyomega():
    # 使用集合来存储唯一的规则
    unique_domains = set()

    # 读取 custom.txt 文件
    custom_rules = read_custom_file()

    # 读取 gfw.txt 文件
    with open('gfw.txt', 'r') as file:
        gfw_rules = file.readlines()

    # 合并 custom.txt 和 gfw.txt 内容
    all_rules = custom_rules + gfw_rules

    # 处理合并后的所有规则
    for line in all_rules:
        # 跳过注释行
        if line.startswith('#') or line.strip() == '':
            continue

        # 去掉行尾的空格和换行符
        line = line.strip()

        # 处理以 || 开头的规则
        if line.startswith('||'):
            domain = line[2:]  # 去掉前缀 || 
            normalized_domain = normalize_domain(domain)  # 标准化域名
            unique_domains.add(f"||{normalized_domain}")
        else:
            # 对其他规则进行处理，去掉协议部分（http:// 或 https://）
            domain = re.sub(r"^https?://", "", line)
            normalized_domain = normalize_domain(domain)  # 标准化域名
            unique_domains.add(f"||{normalized_domain}")

    # 生成规则文件内容
    rules = "\n".join(unique_domains)

    # 写入 gfw-ok.txt 文件（规则原始格式）
    with open('gfw-ok.txt', 'w') as file:
        file.write(rules)

    base64_rules = urllib.parse.quote(rules)

    # 写入 base64 格式文件
    with open('gfw-ok-base64.txt', 'w') as file:
        file.write(base64_rules)


if __name__ == "__main__":
    convert_gfw_to_switchyomega()
