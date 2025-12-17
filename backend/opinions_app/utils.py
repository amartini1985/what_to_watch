import sqlite3

def get_rating_from_db(opinion_id):
    con = sqlite3.connect('instance/db.sqlite3')

    cur = con.cursor()

    cur.execute(f'''
    SELECT AVG(R.rating)
    FROM opinions AS O JOIN reviews AS R ON O.id = R.opinion 
    WHERE O.id = {opinion_id}
    ''')
    result = cur.fetchone()
    con.close()
    return result

# для подключения к mysql использовать драйвер MySQL Connector/Python
# pip install mysql-connector-python
#     conn = mysql.connector.connect(
    #     host="localhost",
    #     user="your_username",
    #     password="your_password",
    #     database="your_database"
    # )