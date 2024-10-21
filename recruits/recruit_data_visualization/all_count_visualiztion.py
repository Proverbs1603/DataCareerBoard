import sqlite3

def get_data_count(db_path, table_name):
    # SQLite3 데이터베이스에 연결
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 데이터 개수 쿼리 실행
        query = "SELECT COUNT(*) FROM {}".format(table_name)
        cursor.execute(query)
        
        # 결과 가져오기
        all_position_count = cursor.fetchone()[0]
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        all_position_count = None
    finally:
        # 연결 종료
        cursor.close()
        conn.close()
    
    return all_position_count