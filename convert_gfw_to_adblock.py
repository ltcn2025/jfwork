import re
import base64
import hashlib
import textwrap


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


def calculate_checksum(content):
    """
    计算校验和，返回 '! Checksum: [checksum]'
    """
    checksum = hashlib.md5(content.encode('utf-8')).hexdigest()
    return f"! Checksum: {checksum}"


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

    # 计算校验和并添加到规则末尾
    checksum = calculate_checksum(rules)
    rules_with_checksum = f"{rules}\n{checksum}\n"

    # 添加额外注释到规则文件开头和结尾
    annotated_rules = (
        "[AutoProxy 0.2.9]\n"
        "! Checksum: Placeholder\n"
        "! Title: GFWList4LL\n"
        "! Last Modified: Placeholder Date\n"
        "! HomePage: https://github.com/gfwlist/gfwlist\n"
        "! License: https://www.gnu.org/licenses/gpl-2.0.txt\n"
        f"{rules_with_checksum}"
        "!------------EOF------------\n"
    )

    # 写入 gfw-ok.txt 文件（规则原始格式，带注释）
    with open('gfw-ok.txt', 'w') as file:
        file.write(annotated_rules)

    # 使用 Base64 编码规则内容
    base64_rules = base64.b64encode(annotated_rules.encode('utf-8')).decode('utf-8')

    # 按 64 个字符一行分割 Base64 编码的内容
    formatted_base64_rules = "\n".join(textwrap.wrap(base64_rules, 64))

    # 写入 base64 格式文件
    with open('gfw-ok-base64.txt', 'w') as file:
        file.write(formatted_base64_rules)


if __name__ == "__main__":
    convert_gfw_to_switchyomega()
