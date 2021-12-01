from typing import Dict, List, Any

from utils.db_api.postgres_db import QuickConnection


def insert(table: str, column_values: Dict):
    with QuickConnection() as cursor:
        columns = ', '.join(column_values.keys())
        values = tuple(map(str, column_values.values()))
        placeholders = ", ".join(["%s"] * len(column_values.keys()))
        cursor.execute(
            f"INSERT INTO {table} "
            f"({columns}) "
            f"VALUES ({placeholders}) RETURNING id",
            values)
        lastrowid = cursor.fetchone()[0]
    return lastrowid


def fetchall(table: str, columns: List[str]) -> List[Dict[str, Any]]:
    with QuickConnection() as cursor:
        columns_joined = ", ".join(columns)
        cursor.execute(f"SELECT {columns_joined} FROM {table}")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            dict_row = {}
            for index, column in enumerate(columns):
                dict_row[column] = row[index]
            result.append(dict_row)
    return result


def fetchall_with_filter(table: str, columns: List[str], f: List[str]):
    with QuickConnection() as cursor:
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
    return result


def delete(table: str, row_id: int) -> None:
    with QuickConnection() as cursor:
        row_id = int(row_id)
        cursor.execute(f"delete from {table} where id={row_id}")
