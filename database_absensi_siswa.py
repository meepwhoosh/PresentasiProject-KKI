import mysql.connector

def connect_to_database(host, user, password, database):
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

def display_data(connection, table_name):
    cursor = connection.cursor()
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    results = cursor.fetchall()
    
    print(f"Data dari tabel {table_name}:")
    for row in results:
        print(row)
    
    cursor.close()

def insert_data(connection, table_name, data):
    cursor = connection.cursor()
    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    
    cursor.execute(query, list(data.values()))
    connection.commit()
    print(f"Data berhasil ditambahkan ke tabel {table_name}.")
    
    cursor.close()

def main():
    # Input informasi koneksi
    host = input("Masukkan host (default: localhost): ") or "localhost"
    user = input("Masukkan username: ")
    password = input("Masukkan password: ")
    database = input("Masukkan nama database: ")

    connection = connect_to_database(host, user, password, database)
    if connection is None:
        return

    while True:
        print("\nMenu:")
        print("1. Tampilkan data dari tabel")
        print("2. Tambah data ke tabel")
        print("3. Keluar")
        choice = input("Pilih opsi: ")

        if choice == '1':
            table_name = input("Masukkan nama tabel: ")
            display_data(connection, table_name)
        elif choice == '2':
            table_name = input("Masukkan nama tabel: ")
            data = {}
            while True:
                column = input("Masukkan nama kolom (atau ketik 'selesai' untuk selesai): ")
                if column.lower() == 'selesai':
                    break
                value = input(f"Masukkan nilai untuk kolom {column}: ")
                data[column] = value
            insert_data(connection, table_name, data)
        elif choice == '3':
            break
        else:
            print("Opsi tidak valid. Silakan coba lagi.")

    connection.close()

if __name__ == "__main__":
    main()