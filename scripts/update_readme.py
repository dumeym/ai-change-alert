"""
README 更新脚本
将新的分析结果插入到 README.md 中
"""
import json
import re
from datetime import datetime


def load_readme():
    """读取 README.md"""
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None


def save_readme(content):
    """保存 README.md"""
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)


def add_entry_to_month(current_month, new_entry):
    """向当月添加新条目"""
    # 查找表格行
    lines = current_month.split('\n')

    # 找到表格头部的位置
    table_start = -1
    separator_line = -1
    for i, line in enumerate(lines):
        if '| 日期 | 冲击类型 | 摘要 | 来源 |' in line:
            table_start = i
            separator_line = i + 1
            break

    if table_start == -1:
        # 没找到表格，创建新表格
        return current_month + f'''

| 日期 | 冲击类型 | 摘要 | 来源 |
|------|----------|------|------|
| {new_entry['date']} | {new_entry['impact_type']} | {new_entry['summary']} | [链接]({new_entry['url']}) |
'''

    # 插入新行到表格中
    new_row = f"| {new_entry['date']} | {new_entry['impact_type']} | {new_entry['summary']} | [链接]({new_entry['url']}) |"

    lines.insert(separator_line + 1, new_row)

    return '\n'.join(lines)


def update_readme(article_data):
    """更新 README.md"""
    # 解析输入的 JSON 数据
    try:
        data = json.loads(article_data)
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}")
        return

    # 读取现有 README
    readme = load_readme()

    if not readme:
        # 创建新的 README
        readme = f"""# AI 行业冲击监测

> 自动追踪 AI 技术对各行各业的冲击与变革

## 📊 最新动态

### {data['date'][:7]}

#### {data['industry']}

| 日期 | 冲击类型 | 摘要 | 来源 |
|------|----------|------|------|
| {data['date']} | {data['impact_type']} | {data['summary']} | [链接]({data['url']}) |

## 📁 按行业分类

### 💻 科技与互联网
...

### 🏥 医疗健康
...

### 🎓 教育培训
...

### 🏦 金融服务
...

### 🎨 内容创作
...

### 🏭 制造业
...

### 🛒 零售电商
...

### ⚖️ 法律服务
...

---

*本仓库由 AI 自动维护，最后更新时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
        save_readme(readme)
        print("README 已创建")
        return

    # 更新现有 README
    # 查找当前月份和行业部分
    current_month = data['date'][:7]  # 例如 "2026-02"
    industry = data['industry']

    month_pattern = rf"### {current_month}"
    industry_pattern = rf"#### {re.escape(industry)}"

    if month_pattern in readme:
        if industry_pattern in readme:
            # 找到对应的月份和行业部分
            lines = readme.split('\n')
            start_idx = -1
            end_idx = -1

            # 找到行业部分的起始位置
            for i, line in enumerate(lines):
                if line == f"#### {industry}":
                    start_idx = i
                elif start_idx != -1 and line.startswith('#### ') and i > start_idx:
                    end_idx = i
                    break
                elif start_idx != -1 and line.startswith('## ') and i > start_idx:
                    end_idx = i
                    break

            if start_idx != -1:
                if end_idx == -1:
                    end_idx = len(lines)

                current_section = '\n'.join(lines[start_idx:end_idx])
                updated_section = add_entry_to_month(current_section, data)
                lines[start_idx:end_idx] = updated_section.split('\n')
                readme = '\n'.join(lines)
        else:
            # 找到月份但没找到行业，添加新行业
            lines = readme.split('\n')
            insert_idx = -1

            # 找到月份的结束位置
            for i, line in enumerate(lines):
                if month_pattern in line:
                    # 找到下一个月份或章节
                    for j in range(i + 1, len(lines)):
                        if lines[j].startswith('### ') or lines[j].startswith('## '):
                            insert_idx = j
                            break
                    break

            if insert_idx == -1:
                insert_idx = len(lines)

            new_section = f"""

#### {industry}

| 日期 | 冲击类型 | 摘要 | 来源 |
|------|----------|------|------|
| {data['date']} | {data['impact_type']} | {data['summary']} | [链接]({data['url']}) |
"""
            lines.insert(insert_idx, new_section)
            readme = '\n'.join(lines)
    else:
        # 找不到月份，在最新动态部分添加新月份
        latest_dynamic_idx = readme.find("## 📊 最新动态")
        if latest_dynamic_idx != -1:
            lines = readme.split('\n')
            insert_idx = -1

            # 找到插入位置（在"最新动态"和下一个章节之间）
            for i, line in enumerate(lines):
                if line == "## 📊 最新动态":
                    for j in range(i + 1, len(lines)):
                        if lines[j].startswith('## ') and not lines[j].startswith('### '):
                            insert_idx = j
                            break
                    break

            if insert_idx == -1:
                insert_idx = len(lines)

            new_month = f"""

### {current_month}

#### {industry}

| 日期 | 冲击类型 | 摘要 | 来源 |
|------|----------|------|------|
| {data['date']} | {data['impact_type']} | {data['summary']} | [链接]({data['url']}) |
"""
            lines.insert(insert_idx, new_month)
            readme = '\n'.join(lines)

    # 更新最后更新时间
    readme = re.sub(
        r'\*本仓库由 AI 自动维护，最后更新时间:.*\*',
        f'*本仓库由 AI 自动维护，最后更新时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*',
        readme
    )

    save_readme(readme)
    print("README 已更新")


def main():
    if len(sys.argv) < 2:
        print("Usage: python update_readme.py <article_data_json>")
        sys.exit(1)

    article_data = sys.argv[1]
    update_readme(article_data)


if __name__ == "__main__":
    import sys
    main()
