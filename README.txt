CSI 3450 - Simplest Stock Market Database Demo

FILES
  stock_app.py - one-file Python console application

SETUP (Windows, VS Code)
1. Install Python (if necessary).
2. Install Microsoft ODBC Driver 18 for SQL Server (if necessary):
   https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
3. Open the folder containing stock_app.py in VS Code.
4. Terminal > New Terminal. Run:
   py -m pip install pyodbc
   py stock_app.py
5. Sign in with an account allowed to access the Azure SQL database.

DEMO
- Option 1 reads records from StockData.Assets.
- Option 2 reads records from StockData.MarketNews.
- Option 3 inserts a synthetic test news record for an existing symbol.
- Option 4 updates only records tagged 'Synthetic Test Data'.
- Invalid choices, unknown stock symbols, and SQL errors are handled.
- Verify changes in SSMS and refresh Power BI afterward.

The script uses parameterized SQL. It does not store a password.
Any inserts/updates affect the shared database.
