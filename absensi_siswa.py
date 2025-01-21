from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="absensi_siswa"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/')
def index():
    connection = connect_to_database()
    if connection is None:
        return "Database connection failed."
    
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('index.html', tables=tables)

@app.route('/display/<table_name>')
def display_data(table_name):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    results = cursor.fetchall()
    
    # Mendapatkan nama kolom
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = [column[0] for column in cursor.fetchall()]
    
    # Ubah hasil menjadi list of dictionaries
    data = [dict(zip(columns, row)) for row in results]
    
    cursor.close()
    connection.close()
    
    return render_template('display.html', table_name=table_name, results=data, columns=columns)

@app.route('/insert', methods=['GET', 'POST'])
def insert_data():
    if request.method == 'POST':
        data = request.form.to_dict()
        connection = connect_to_database()
        cursor = connection.cursor()
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        query = f"INSERT INTO absensi ({columns}) VALUES ({placeholders})"
        
        try:
            cursor.execute(query, list(data.values()))
            connection.commit()
            flash('Data berhasil ditambahkan!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'error')
        finally:
            cursor.close()
            connection.close()
        
        return redirect(url_for('display_data', table_name='absensi'))
    
    return render_template('insert.html', table_name='absensi')

if __name__ == "__main__":
    app.run(debug=True)
    