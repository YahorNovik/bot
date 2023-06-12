import sqlite3

def delete_all_data_from_table(table_name):
    # Connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Execute the DELETE FROM statement
    delete_query = f'DELETE FROM {table_name};'
    cursor.execute(delete_query)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Usage example
delete_all_data_from_table('users')
delete_all_data_from_table('gabinets')
delete_all_data_from_table('invoices')
delete_all_data_from_table('payments')