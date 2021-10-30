import os
from typing import Dict, List, Any

import sqlite3

conn = sqlite3.connect(os.path.join("data", "veles.db"), isolation_level=None)


def insert(table: str, column_values: Dict):
    cursor = conn.cursor()
    columns = ', '.join(column_values.keys())
    values = tuple(column_values.values())
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.execute(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    lastrowid = cursor.lastrowid
    cursor.close()
    return lastrowid


def fetchall(table: str, columns: List[str]) -> List[Dict[str, Any]]:
    cursor = conn.cursor()
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    cursor.close()
    return result


def fetchall_with_filter(table: str, columns: List[str], f: List[str]):
    cursor = conn.cursor()
    columns_joined = ", ".join(columns)
    query = f"SELECT {columns_joined} FROM {table} "
    if f:
        condition = " AND ".join(f)
        query += f"WHERE {condition}"
    cursor.execute(query)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    cursor.close()
    return result


def delete(table: str, row_id: int) -> None:
    cursor = conn.cursor()
    row_id = int(row_id)
    cursor.execute(f"delete from {table} where id={row_id}")
    cursor.close()


def get_cursor():
    cursor = conn.cursor()
    return cursor


def _init_db(cursor):
    """Инициализирует БД"""
    with open(os.path.join("scripts", "createdb.sql"), "r") as f:
        sql = f.read()
    cursor.executescript(sql)


def check_db_exists():
    cursor = conn.cursor()
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='adepts'")
    table_exists = cursor.fetchall()
    if table_exists:
        cursor.close()
        return
    _init_db(cursor)
    cursor.close()


check_db_exists()
