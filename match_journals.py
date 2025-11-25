import csv
import re
from difflib import SequenceMatcher

def normalize_journal_name(name):
    """Normalize journal name for matching"""
    if not name or name == '':
        return ""
    # Convert to string and uppercase
    name = str(name).upper()
    # Remove common punctuation and special characters
    name = re.sub(r'[&\-\:\.\,\(\)\[\]]', ' ', name)
    # Remove extra spaces
    name = re.sub(r'\s+', ' ', name)
    return name.strip()

def similarity_score(str1, str2):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, str1, str2).ratio()

def find_best_match(journal_name, candidates, threshold=0.6):
    """Find best matching journal name from candidates
    candidates: list of (index, name) tuples
    """
    normalized_name = normalize_journal_name(journal_name)
    
    best_score = 0
    best_match_idx = None
    
    for idx, candidate in candidates:
        normalized_candidate = normalize_journal_name(candidate)
        
        # Skip empty candidates
        if not normalized_candidate:
            continue
        
        # Calculate similarity score
        score = similarity_score(normalized_name, normalized_candidate)
        
        # Boost score if one is contained in the other
        if normalized_name in normalized_candidate or normalized_candidate in normalized_name:
            score = max(score, 0.85)
        
        if score > best_score:
            best_score = score
            best_match_idx = idx
    
    if best_score >= threshold:
        return best_match_idx, best_score
    return None, 0

# Read CAS classification table
print("Loading CAS classification table...")
cas_data = []
with open('d:/BaiduSyncdisk/R_packages_shiny/impact-if/2025中科院分区表.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cas_data.append(row)

print(f"CAS table loaded: {len(cas_data)} journals")

# Read impact factor table
print("Loading impact factor table...")
impact_data = []
with open('d:/BaiduSyncdisk/R_packages_shiny/impact-if/impact if.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        # Add new columns if not present
        if '2025分区' not in row:
            row['2025分区'] = ''
        if 'Top' not in row:
            row['Top'] = ''
        if 'Open Access' not in row:
            row['Open Access'] = ''
        impact_data.append(row)

print(f"Impact factor table loaded: {len(impact_data)} journals")

# Add new columns to fieldnames if needed
if '2025分区' not in fieldnames:
    fieldnames = list(fieldnames) + ['2025分区', 'Top', 'Open Access']

# Phase 1: Exact matching
print("\nPhase 1: Exact matching (case-insensitive)...")
exact_matches = 0

for cas_row in cas_data:
    cas_journal = cas_row['期刊名称']
    matched = False
    
    # Try exact match with Journal Name
    for impact_row in impact_data:
        if impact_row.get('Journal Name', '').upper() == cas_journal.upper():
            impact_row['2025分区'] = cas_row['2025分区']
            impact_row['Top'] = cas_row['Top']
            impact_row['Open Access'] = cas_row['Open Access']
            matched = True
    
    if matched:
        exact_matches += 1
        continue
    
    # Try exact match with Abbreviated Journal
    for impact_row in impact_data:
        if impact_row.get('Abbreviated Journal', '').upper() == cas_journal.upper():
            impact_row['2025分区'] = cas_row['2025分区']
            impact_row['Top'] = cas_row['Top']
            impact_row['Open Access'] = cas_row['Open Access']
            matched = True
    
    if matched:
        exact_matches += 1

print(f"Exact matches found: {exact_matches}")

# Phase 2: Fuzzy matching
print("\nPhase 2: Fuzzy matching for remaining journals...")
fuzzy_matches = 0
match_details = []

for i, cas_row in enumerate(cas_data):
    if i % 1000 == 0:
        print(f"Processing journal {i+1}/{len(cas_data)}...")
    
    cas_journal = cas_row['期刊名称']
    
    # Check if already matched
    already_matched = False
    for impact_row in impact_data:
        if (impact_row.get('Journal Name', '').upper() == cas_journal.upper() or
            impact_row.get('Abbreviated Journal', '').upper() == cas_journal.upper()):
            already_matched = True
            break
    
    if already_matched:
        continue
    
    # Prepare candidates for full journal names
    journal_candidates = [(idx, row.get('Journal Name', '')) 
                         for idx, row in enumerate(impact_data) 
                         if row.get('2025分区', '') == '']
    
    # Try matching with full names
    match_idx, score = find_best_match(cas_journal, journal_candidates, threshold=0.75)
    
    if match_idx is not None:
        impact_data[match_idx]['2025分区'] = cas_row['2025分区']
        impact_data[match_idx]['Top'] = cas_row['Top']
        impact_data[match_idx]['Open Access'] = cas_row['Open Access']
        fuzzy_matches += 1
        match_details.append({
            'CAS_Journal': cas_journal,
            'Matched_Journal': impact_data[match_idx]['Journal Name'],
            'Score': f"{score:.3f}",
            'Type': 'Full Name'
        })
        continue
    
    # Prepare candidates for abbreviated names
    abbrev_candidates = [(idx, row.get('Abbreviated Journal', '')) 
                        for idx, row in enumerate(impact_data)
                        if row.get('2025分区', '') == '']
    
    # Try matching with abbreviated names
    match_idx, score = find_best_match(cas_journal, abbrev_candidates, threshold=0.75)
    
    if match_idx is not None:
        impact_data[match_idx]['2025分区'] = cas_row['2025分区']
        impact_data[match_idx]['Top'] = cas_row['Top']
        impact_data[match_idx]['Open Access'] = cas_row['Open Access']
        fuzzy_matches += 1
        match_details.append({
            'CAS_Journal': cas_journal,
            'Matched_Journal': impact_data[match_idx]['Abbreviated Journal'],
            'Score': f"{score:.3f}",
            'Type': 'Abbreviated'
        })

print(f"Fuzzy matches found: {fuzzy_matches}")

# Save the updated impact factor file
output_file = 'd:/BaiduSyncdisk/R_packages_shiny/impact-if/impact if_matched.csv'
with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(impact_data)

print(f"\n✓ Updated file saved to: {output_file}")
print(f"\nTotal matches: {exact_matches + fuzzy_matches} out of {len(cas_data)} journals")
print(f"Match rate: {(exact_matches + fuzzy_matches) / len(cas_data) * 100:.2f}%")

# Save match details for review
if match_details:
    match_report_file = 'd:/BaiduSyncdisk/R_packages_shiny/impact-if/match_report.csv'
    with open(match_report_file, 'w', encoding='utf-8-sig', newline='') as f:
        match_fieldnames = ['CAS_Journal', 'Matched_Journal', 'Score', 'Type']
        writer = csv.DictWriter(f, fieldnames=match_fieldnames)
        writer.writeheader()
        writer.writerows(match_details)
    print(f"\nFuzzy match details saved to: {match_report_file}")

# Show statistics
matched_count = sum(1 for row in impact_data if row.get('2025分区', '') != '')
print(f"\nStatistics:")
print(f"- Journals with 2025分区 data: {matched_count}")
print(f"- Journals without match: {len(impact_data) - matched_count}")

# Count distribution
fenqu_count = {}
top_count = {}
oa_count = {}

for row in impact_data:
    fenqu = row.get('2025分区', '')
    if fenqu:
        fenqu_count[fenqu] = fenqu_count.get(fenqu, 0) + 1
    
    top = row.get('Top', '')
    if top:
        top_count[top] = top_count.get(top, 0) + 1
    
    oa = row.get('Open Access', '')
    if oa:
        oa_count[oa] = oa_count.get(oa, 0) + 1

if fenqu_count:
    print(f"\n2025分区 distribution:")
    for key in sorted(fenqu_count.keys()):
        print(f"  {key}: {fenqu_count[key]}")

if top_count:
    print(f"\nTop journal distribution:")
    for key, val in top_count.items():
        print(f"  {key}: {val}")

if oa_count:
    print(f"\nOpen Access distribution:")
    for key, val in oa_count.items():
        print(f"  {key}: {val}")

print("\n✓ Matching complete!")
