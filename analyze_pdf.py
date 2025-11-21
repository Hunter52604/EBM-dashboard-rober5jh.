"""
PDF Analysis Script
Extracts and analyzes content from the PDF file
"""

import pdfplumber
import pandas as pd
import re

pdf_path = "robertsonjoshua_LATE_5890806_link (1).pdf"

print("="*80)
print("PDF Analysis")
print("="*80)
print(f"\nAnalyzing: {pdf_path}\n")

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    print("\n" + "="*80)

    # Extract all text
    full_text = ""
    for i, page in enumerate(pdf.pages, 1):
        text = page.extract_text()
        full_text += text + "\n\n"
        print(f"\n--- PAGE {i} ---\n")
        print(text)
        print("\n")

    # Try to extract tables
    print("\n" + "="*80)
    print("EXTRACTING TABLES")
    print("="*80)

    all_tables = []
    for i, page in enumerate(pdf.pages, 1):
        tables = page.extract_tables()
        if tables:
            print(f"\nFound {len(tables)} table(s) on page {i}")
            for j, table in enumerate(tables, 1):
                print(f"\nTable {j} on page {i}:")
                df = pd.DataFrame(table[1:], columns=table[0] if table else None)
                print(df)
                all_tables.append(df)

    # Save extracted content
    with open("pdf_extracted_text.txt", "w", encoding="utf-8") as f:
        f.write(full_text)

    print("\n" + "="*80)
    print("✓ Text saved to: pdf_extracted_text.txt")

    if all_tables:
        for i, df in enumerate(all_tables):
            filename = f"pdf_table_{i+1}.csv"
            df.to_csv(filename, index=False)
            print(f"✓ Table {i+1} saved to: {filename}")

    print("="*80)
