STOCK_TABLE = '('                               \
              'open_time   real PRIMARY KEY,'   \
              'close_time  real,'               \
              'open_price  float,'              \
              'close_price float,'              \
              'max_price   float,'              \
              'min_price   float,'               \
              'volume      integer'             \
              ')'

TABLE_TYPES = {
    "stock": STOCK_TABLE,
}


def create_table(table_name: str, table_type: str) -> str:
    """Returns sql command used to create table.
    Example use db.manager.execute(create_table('PER1-+IOD_M1', tables_factory.TABLE_TYPES["stock"]))"""
    command = f"CREATE TABLE {table_name} {table_type}"
    return command

