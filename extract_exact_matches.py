import csv

# 列名映射
column_mapping = {
    'Rank': '排名',
    'Journal Name': '期刊名称',
    'JCR Year': 'JCR年份',
    'Abbreviated Journal': '期刊缩写',
    'Publisher': '出版商',
    'ISSN': 'ISSN',
    'eISSN': 'eISSN',
    'Total Cites': '总引用数',
    'Total Articles': '总文章数',
    'Citable Items': '可引用文章数',
    'Cited Half-Life': '被引半衰期',
    'Citing Half-Life': '引用半衰期',
    'JIF': '影响因子',
    '5-Year JIF': '5年影响因子',
    'JIF Without Self-Cites': '去除自引影响因子',
    'JCI': '引文影响力指标(JCI)',
    'JIF Quartile': 'JIF分区',
    'JIF Rank': 'JIF排名',
    '2025分区': '2025中科院分区',
    'Top': 'Top期刊',
    'Open Access': '开放获取'
}

# 读取模糊匹配报告，获取模糊匹配的期刊名称
fuzzy_matched_journals = set()
try:
    with open('d:/BaiduSyncdisk/R_packages_shiny/impact-if/match_report.csv', 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # match_report.csv 中记录的都是模糊匹配的期刊
            fuzzy_matched_journals.add(row['Impact Factor Journal'])
    print(f"Found {len(fuzzy_matched_journals)} fuzzy matched journals")
except Exception as e:
    print(f"Error reading match report: {e}")

# 读取完整匹配结果，筛选出精确匹配的
input_file = 'd:/BaiduSyncdisk/R_packages_shiny/impact-if/impact if_matched.csv'
output_file_en = 'd:/BaiduSyncdisk/R_packages_shiny/impact-if/impact if_matched_exact.csv'
output_file_zh = 'd:/BaiduSyncdisk/R_packages_shiny/impact-if/impact if_matched_exact_zh.csv'

print(f"Reading matched data from: {input_file}")

try:
    # 读取数据
    exact_matches = []
    with open(input_file, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        for row in reader:
            journal_name = row['Journal Name']
            # 只保留非模糊匹配的（即精确匹配的）
            # 如果有2025分区数据，但不在模糊匹配列表中，说明是精确匹配
            if row.get('2025分区') and journal_name not in fuzzy_matched_journals:
                exact_matches.append(row)
    
    print(f"Found {len(exact_matches)} exact matches")
    
    # 保存英文版本
    print(f"Saving English version to: {output_file_en}")
    with open(output_file_en, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(exact_matches)
    
    # 保存中文版本
    print(f"Saving Chinese version to: {output_file_zh}")
    new_fieldnames = [column_mapping.get(col, col) for col in fieldnames]
    
    with open(output_file_zh, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames)
        writer.writeheader()
        
        # 转换每行的键名
        for row in exact_matches:
            new_row = {}
            for key, value in row.items():
                new_key = column_mapping.get(key, key)
                new_row[new_key] = value
            writer.writerow(new_row)
    
    print("Done!")
    print(f"English version: {len(exact_matches)} rows")
    print(f"Chinese version: {len(exact_matches)} rows")
    
except Exception as e:
    print(f"Error: {e}")
