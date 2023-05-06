from sqlalchemy import Integer


def build_query_filter(query, filters, table):
    for field, value in filters.items():
        if value is not None and field in table.FILTERS_TO_COLUMNS:
            column = table.FILTERS_TO_COLUMNS[field]
            # Convert string values to integers
            if isinstance(column.type, Integer) and isinstance(value, str):
                value = int(value)
            query = query.filter(column == value)
    return query
