# AdventureWorks source data

The supplied Azure project document identifies the open-source **Adventure Works** dataset and lists these ten CSVs:

1. `AdventureWorks_Calendar.csv`
2. `AdventureWorks_Customers.csv`
3. `AdventureWorks_Product_Categories.csv`
4. `AdventureWorks_Product_Subcategories.csv`
5. `AdventureWorks_Products.csv`
6. `AdventureWorks_Returns.csv`
7. `AdventureWorks_Sales_2015.csv`
8. `AdventureWorks_Sales_2016.csv`
9. `AdventureWorks_Sales_2017.csv`
10. `AdventureWorks_Territories.csv`

Dataset repository: https://github.com/anshlambaoldgit/Adventure-Works-Data-Engineering-Project/tree/main/Data

Download the files into `data/raw/` while preserving the filenames. The original document's screenshot shows a GitHub URL with an older account name; the link above is the currently discoverable repository location. Confirm file availability and column names before running the notebooks.

Raw data is excluded from Git. Do not commit licensed, personal, or confidential data unless redistribution is permitted.
## Download
Run `bash scripts/download_adventureworks.sh` from the repository root. The script downloads only the ten filenames in the source manifest from the linked public GitHub dataset repository. Then run the source contract tests.
