"""Standard-library source contract tests for the AdventureWorks CSV files.

Download the ten CSV files into data/raw/ before running:
    python -m unittest discover -s tests -p "test_*.py" -v

These checks validate the source files and key columns without requiring Spark.
"""
import csv
import datetime as dt
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

EXPECTED_FILES = [
    "AdventureWorks_Calendar.csv",
    "AdventureWorks_Customers.csv",
    "AdventureWorks_Product_Categories.csv",
    "AdventureWorks_Product_Subcategories.csv",
    "AdventureWorks_Products.csv",
    "AdventureWorks_Returns.csv",
    "AdventureWorks_Sales_2015.csv",
    "AdventureWorks_Sales_2016.csv",
    "AdventureWorks_Sales_2017.csv",
    "AdventureWorks_Territories.csv",
]

REQUIRED_COLUMNS = {
    "AdventureWorks_Calendar.csv": {"Date"},
    "AdventureWorks_Customers.csv": {"CustomerKey"},
    "AdventureWorks_Product_Categories.csv": {"ProductCategoryKey", "CategoryName"},
    "AdventureWorks_Product_Subcategories.csv": {"ProductSubcategoryKey", "SubcategoryName", "ProductCategoryKey"},
    "AdventureWorks_Products.csv": {"ProductKey", "ProductSubcategoryKey", "ProductSKU", "ProductName", "ProductCost", "ProductPrice"},
    "AdventureWorks_Returns.csv": {"ReturnDate", "TerritoryKey", "ProductKey", "ReturnQuantity"},
    "AdventureWorks_Sales_2015.csv": {"OrderDate", "StockDate", "OrderNumber", "ProductKey", "CustomerKey", "TerritoryKey", "OrderLineItem", "OrderQuantity"},
    "AdventureWorks_Sales_2016.csv": {"OrderDate", "StockDate", "OrderNumber", "ProductKey", "CustomerKey", "TerritoryKey", "OrderLineItem", "OrderQuantity"},
    "AdventureWorks_Sales_2017.csv": {"OrderDate", "StockDate", "OrderNumber", "ProductKey", "CustomerKey", "TerritoryKey", "OrderLineItem", "OrderQuantity"},
    "AdventureWorks_Territories.csv": {"SalesTerritoryKey", "Region", "Country", "Continent"},
}

class AdventureWorksSourceContractTests(unittest.TestCase):
    def test_all_expected_files_exist(self):
        missing = [name for name in EXPECTED_FILES if not (RAW / name).is_file()]
        self.assertEqual([], missing, f"Missing source files under {RAW}: {missing}")

    def test_headers_contain_required_columns(self):
        for filename, required in REQUIRED_COLUMNS.items():
            with self.subTest(file=filename):
                with (RAW / filename).open("r", encoding="utf-8-sig", newline="") as handle:
                    reader = csv.reader(handle)
                    header = next(reader)
                self.assertTrue(all(h.strip() for h in header), "Blank header name")
                self.assertEqual(len(header), len(set(header)), "Duplicate header names")
                self.assertTrue(required.issubset(set(header)),
                                f"Missing columns: {required - set(header)}")

    def test_sales_dates_and_quantities(self):
        for year in (2015, 2016, 2017):
            filename = f"AdventureWorks_Sales_{year}.csv"
            with self.subTest(file=filename):
                with (RAW / filename).open("r", encoding="utf-8-sig", newline="") as handle:
                    reader = csv.DictReader(handle)
                    count = 0
                    for row in reader:
                        count += 1
                        dt.datetime.strptime(row["OrderDate"], "%m/%d/%Y")
                        dt.datetime.strptime(row["StockDate"], "%m/%d/%Y")
                        self.assertGreater(int(row["OrderQuantity"]), 0)
                        self.assertTrue(row["OrderNumber"].startswith("SO"))
                    self.assertGreater(count, 0, "Sales file has no data rows")

if __name__ == "__main__":
    unittest.main()
