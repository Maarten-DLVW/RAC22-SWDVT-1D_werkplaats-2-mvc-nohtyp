import os
import sqlite3

class QuestionModel: 
    def __init__(self, database_file):
        self.database_file = database_file
        if not os.path.exists(self.database_file):
            raise FileNotFoundError(f"Could not find database file: {database_file}")

    # Select all questions with questions with special characters from db
    def getAllSpecialCharacters(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f'SELECT * FROM vragen WHERE vraag LIKE "%<br>%" OR vraag LIKE "%&nbsp;%";')
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        return table_content, table_headers

    # Edit special characters
    def editSpecialCharacters(self, id, question):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(f'UPDATE vragen SET vraag = ? WHERE id = ?', (question, id))
        conn.commit()