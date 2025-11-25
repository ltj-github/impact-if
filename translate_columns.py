import csv
import codecs

# Define the column mapping
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

input_file = 'd:/BaiduSyncdisk/R_packages_shiny/impact-if/impact if_matched.csv'
output_file = 'd:/BaiduSyncdisk/R_packages_shiny/impact-if/impact if_matched_zh.csv'

print(f"Reading file: {input_file}")

try:
    # Read the input file
    with open(input_file, 'r', encoding='utf-8-sig', newline='') as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames
        
        # Create new fieldnames based on mapping
        new_fieldnames = [column_mapping.get(col, col) for col in fieldnames]
        
        # Write to output file
        print(f"Saving to: {output_file}")
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=new_fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write rows
            row_count = 0
            for row in reader:
                # Create a new row with translated keys
                new_row = {}
                for key, value in row.items():
                    new_key = column_mapping.get(key, key)
                    new_row[new_key] = value
                writer.writerow(new_row)
                row_count += 1
                
    print(f"Done! Processed {row_count} rows.")
    print("New columns:", new_fieldnames)

except Exception as e:
    print(f"Error: {e}")
