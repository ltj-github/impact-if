import csv

# Quick check to see the column names
with open('d:/BaiduSyncdisk/R_packages_shiny/impact-if/2025中科院分区表.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    print("Columns in CAS file:")
    for col in reader.fieldnames:
        print(f"  '{col}' (repr: {repr(col)})")
    
with open('d:/BaiduSyncdisk/R_packages_shiny/impact-if/impact if.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    print("\nColumns in Impact Factor file:")
    for col in reader.fieldnames:
        print(f"  '{col}' (repr: {repr(col)})")
