""""
Requires: pip install pyodbc, Microsoft ODBC Driver 18 for SQL Server.
Uses Microsoft Entra interactive sign-in; no password stored in the file.
"""

import pyodbc

SERVER = "grantsazureserver.database.windows.net"
DATABASE = "Database-Design-Implementation-Project"


def connect():
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER=tcp:{SERVER},1433;"
        f"DATABASE={DATABASE};"
        "Authentication=ActiveDirectoryInteractive;"
        "UID=ajkubs@oakland.edu;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=60;"
    )

    return pyodbc.connect(connection_string)


def view_stocks(conn):
    rows = conn.cursor().execute(
        "SELECT TOP (20) AssetID, Symbol, AssetName "
        "FROM StockData.Assets ORDER BY Symbol"
    ).fetchall()
    print("\nFIRST 20 ASSETS")
    for row in rows:
        print(f"{row.AssetID:>4}  {row.Symbol:<12} {row.AssetName}")
    if not rows:
        print("No assets found.")


def view_test_news(conn):
    rows = conn.cursor().execute(
        "SELECT N.NewsID, A.Symbol, N.ArticleTitle "
        "FROM StockData.MarketNews AS N "
        "JOIN StockData.Assets AS A ON A.AssetID = N.AssetID "
        "WHERE N.DataSource = ? ORDER BY N.NewsID DESC",
        "Synthetic Test Data",
    ).fetchall()
    print("\nSYNTHETIC TEST NEWS")
    for row in rows:
        print(f"ID {row.NewsID}: {row.Symbol} - {row.ArticleTitle}")
    if not rows:
        print("No synthetic news records found.")


def add_test_news(conn):
    symbol = input("Stock symbol (e.g. AAPL): ").strip().upper()
    title = input("Test news title: ").strip()
    if not symbol or not title or len(title) > 500:
        print("Enter a symbol and a title of 1–500 characters.")
        return
    if not title.startswith("TEST: "):
        title = "TEST: " + title
    if len(title) > 500:
        print("The title is too long (maximum 500 characters).")
        return

    cursor = conn.cursor()
    asset = cursor.execute(
        "SELECT AssetID FROM StockData.Assets WHERE Symbol = ?", symbol
    ).fetchone()
    if asset is None:
        print("Stock symbol not found. No record was inserted.")
        return
    cursor.execute(
        "INSERT INTO StockData.MarketNews "
        "(AssetID, ArticleTitle, ArticleSummary, NewsSource, DataSource, RetrievedAtUtc) "
        "VALUES (?, ?, ?, ?, ?, SYSUTCDATETIME())",
        asset.AssetID, title, "Synthetic test record for CSI 3450 application demo.",
        "Project Demo", "Synthetic Test Data",
    )
    conn.commit()
    print("Test news inserted into the shared Azure SQL database.")


def update_test_news(conn):
    view_test_news(conn)
    value = input("News ID to update: ").strip()
    if not value.isdigit():
        print("Enter a numeric News ID.")
        return
    title = input("New test news title: ").strip()
    if not title:
        print("The title cannot be empty.")
        return
    if not title.startswith("TEST: "):
        title = "TEST: " + title
    if len(title) > 500:
        print("Title must be 500 characters or fewer.")
        return
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE StockData.MarketNews SET ArticleTitle = ? "
        "WHERE NewsID = ? AND DataSource = ?",
        title, int(value), "Synthetic Test Data",
    )
    if cursor.rowcount == 0:
        print("No matching synthetic test record. Nothing changed.")
        return
    conn.commit()
    print("Test news updated in the shared Azure SQL database.")


def main():
    print("CSI 3450 - STOCK MARKET DATABASE DEMO")
    try:
        with connect() as conn:
            print("Connected to Azure SQL!\n")
            while True:
                print("\n1. View stocks")
                print("2. View test news")
                print("3. Add test news")
                print("4. Update test news")
                print("5. Exit")
                choice = input("Choose 1-5: ").strip()
                if choice == "5":
                    print("Goodbye!")
                    break
                try:
                    if choice == "1":
                        view_stocks(conn)
                    elif choice == "2":
                        view_test_news(conn)
                    elif choice == "3":
                        add_test_news(conn)
                    elif choice == "4":
                        update_test_news(conn)
                    else:
                        print("Please choose a number from 1 to 5.")
                except pyodbc.Error as error:
                    conn.rollback()
                    print(f"Database operation failed: {error}")
    except pyodbc.Error as error:
        print(f"Could not connect to Azure SQL: {error}")
        print("Check your Microsoft sign-in, SQL permissions, firewall, and ODBC Driver 18.")
    except (EOFError, KeyboardInterrupt):
        print("\nExited.")


if __name__ == "__main__":
    main()
