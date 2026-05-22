import sqlite3

conn=sqlite3.connect('company.db')

cursor=conn.cursor()

cursor.execute("""
    CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary INTEGER
)
""")

employees=[
    (1, 'Manikanta', 'Data Science', 80000),
    (2, 'Rahul', 'HR', 50000),
    (3, 'Sneha', 'Finance', 70000),
    (4, 'Kiran', 'Data Science', 90000),
    (5, 'Anjali', 'HR', 60000)  
]

cursor.executemany(
    'INSERT INTO employees VALUES (?, ?, ?, ?)',
    employees
)

conn.commit()
conn.close()

print('Database Created Successfully')