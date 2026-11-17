#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RAW_DIR="$ROOT/data/raw"
BASE="https://raw.githubusercontent.com/anshlambaoldgit/Adventure-Works-Data-Engineering-Project/main/Data"

FILES=(
  "AdventureWorks_Calendar.csv"
  "AdventureWorks_Customers.csv"
  "AdventureWorks_Product_Categories.csv"
  "AdventureWorks_Product_Subcategories.csv"
  "AdventureWorks_Products.csv"
  "AdventureWorks_Returns.csv"
  "AdventureWorks_Sales_2015.csv"
  "AdventureWorks_Sales_2016.csv"
  "AdventureWorks_Sales_2017.csv"
  "AdventureWorks_Territories.csv"
)

mkdir -p "$RAW_DIR"
for file in "${FILES[@]}"; do
  echo "Downloading $file"
  curl --fail --location --retry 3 "$BASE/$file" --output "$RAW_DIR/$file"
done

echo "Downloaded ${#FILES[@]} AdventureWorks CSV files to $RAW_DIR"
echo "Next: python -m unittest discover -s tests -p 'test_*.py' -v"
