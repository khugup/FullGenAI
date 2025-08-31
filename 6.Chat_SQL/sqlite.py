import sqlite3

# Connect to sqlite
connection=sqlite3.connect("student.db")

# create a cursor object to insert record,create table
cursor=connection.cursor()

# Create the table
table_info="""
create table STUDENT2(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT)
"""
cursor.execute(table_info)

# Insert some more records
cursor.execute('''Insert Into STUDENT2 values('Krish','DataScience','A',90)''')
cursor.execute('''Insert Into STUDENT2 values('John','DataScience','A',100)''')
cursor.execute('''Insert Into STUDENT2 values('Mukesh','DataScience','A',86)''')
cursor.execute('''Insert Into STUDENT2 values('Jacob','Devops','A',50)''')
cursor.execute('''Insert Into STUDENT2 values('Dipesh','Devops','A',35)''')

# Display all the records
print("The inserted records are")
data=cursor.execute('''Select * from STUDENT2''')
for row in data:
    print(row)


# Commit your changes in the database
connection.commit()
connection.close()