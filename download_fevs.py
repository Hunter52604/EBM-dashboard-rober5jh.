"""
FEVS 2024 Data Downloader
This script attempts to download the FEVS 2024 Public Data File from OPM
"""

import requests
import os
from pathlib import Path

def download_fevs_interactive():
    """
    Download FEVS data with proper form handling
    """
    print("="*80)
    print("FEVS 2024 Data Download Utility")
    print("="*80)

    # The OPM site requires form submission, so we'll try to simulate it
    base_url = "https://www.opm.gov"
    form_url = f"{base_url}/fevs/public-data-file/"

    print("\nAttempting to access OPM FEVS data portal...")

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })

    # Try direct download patterns for 2024
    possible_urls = [
        # Excel formats (sometimes available)
        "https://www.opm.gov/fevs/reports/Datasets/2024_FEVS_Prdf.xlsx",
        "https://www.opm.gov/fevs/public-data-file/2024_FEVS_Prdf.xlsx",

        # CSV formats
        "https://www.opm.gov/fevs/reports/Datasets/2024_FEVS_Prdf.csv",
        "https://www.opm.gov/fevs/public-data-file/2024_FEVS_Prdf.csv",

        # Alternative 2024 patterns
        "https://www.opm.gov/fevs/reports/data-files/2024-FEVS-Public-Data-File.csv",
        "https://www.opm.gov/fevs/reports/data-files/2024-FEVS-Public-Data-File.xlsx",

        # 2023 fallback (if 2024 not available yet)
        "https://www.opm.gov/fevs/reports/Datasets/2023_FEVS_Prdf.csv",
        "https://www.opm.gov/fevs/reports/Datasets/2023_FEVS_Prdf.xlsx",
    ]

    print(f"\nTrying {len(possible_urls)} possible download URLs...\n")

    for i, url in enumerate(possible_urls, 1):
        print(f"[{i}/{len(possible_urls)}] Testing: {url}")
        try:
            response = session.get(url, timeout=30, allow_redirects=True)

            if response.status_code == 200:
                # Check if we got actual data (not an error page)
                content_type = response.headers.get('content-type', '').lower()
                content_length = len(response.content)

                if content_length > 10000:  # At least 10KB
                    # Determine file extension
                    if 'excel' in content_type or url.endswith('.xlsx'):
                        filename = "2024_FEVS_Prdf.xlsx"
                    else:
                        filename = "2024_FEVS_Prdf.csv"

                    # Save the file
                    with open(filename, 'wb') as f:
                        f.write(response.content)

                    print(f"\n✓ SUCCESS!")
                    print(f"  Downloaded: {filename}")
                    print(f"  Size: {content_length:,} bytes ({content_length/1024/1024:.2f} MB)")
                    print(f"  Content-Type: {content_type}")
                    print(f"\n  File saved to: {os.path.abspath(filename)}")
                    return filename
                else:
                    print(f"  × Response too small ({content_length} bytes) - likely error page")
            else:
                print(f"  × HTTP {response.status_code}")

        except Exception as e:
            print(f"  × Error: {e}")

    print("\n" + "="*80)
    print("❌ Automatic download failed - Manual download required")
    print("="*80)
    print("\nThe OPM website requires interactive form submission.")
    print("\nPlease download manually:")
    print("\n  1. Open browser to: https://www.opm.gov/fevs/public-data-file/")
    print("  2. Select:")
    print("     - OPM FEVS Administration Year: 2024")
    print("     - File you are requesting: Public Data File")
    print("  3. Click 'Submit'")
    print("  4. Download the file when prompted")
    print("  5. Save it to this folder as: 2024_FEVS_Prdf.csv")
    print("\nAlternatively, check for the latest data at:")
    print("  https://www.opm.gov/fevs/reports/")
    print("="*80)

    return None

if __name__ == "__main__":
    result = download_fevs_interactive()

    if result:
        print("\n✓ Ready to analyze! Run: python fevs_analysis.py")
    else:
        print("\n⚠ Please download the file manually and save it as '2024_FEVS_Prdf.csv'")
        print("  Then run: python fevs_analysis.py")
