import sqlite3

DB_NAME = "database.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            item_type TEXT NOT NULL,
            color TEXT NOT NULL,
            description TEXT NOT NULL,
            gate TEXT NOT NULL,
            image TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_report(category, item_type, color, description, gate, image):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reports (category, item_type, color, description, gate, image)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (category, item_type, color, description, gate, image))

    conn.commit()
    conn.close()


def get_all_reports():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reports ORDER BY id DESC")
    reports = cursor.fetchall()

    conn.close()
    return reports


def search_reports(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    like_keyword = "%" + keyword + "%"

    cursor.execute("""
        SELECT * FROM reports
        WHERE category LIKE ?
        OR item_type LIKE ?
        OR color LIKE ?
        OR description LIKE ?
        OR gate LIKE ?
        ORDER BY id DESC
    """, (like_keyword, like_keyword, like_keyword, like_keyword, like_keyword))

    results = cursor.fetchall()
    conn.close()
    return results


def count_all_reports():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM reports")
    total = cursor.fetchone()[0]

    conn.close()
    return total


def count_by_category(category):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM reports WHERE category = ?", (category,))
    count = cursor.fetchone()[0]

    conn.close()
    return count


def delete_report(report_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM reports WHERE id = ?", (report_id,))

    conn.commit()
    conn.close()