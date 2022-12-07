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

    # Get question with specific id from db
    def getSpecificQuestion(self, id):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(f'SELECT id, vraag FROM vragen WHERE id = ?', (id))
        data = cursor.fetchone()
        result = []

        for i in data:
            result.append(i)

        return result

    # Get all null values from db
    def getAllNullValues(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f'SELECT id, vraag, auteur, leerdoel FROM vragen WHERE vraag IS NULL OR auteur IS NULL OR leerdoel IS NULL;')
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        return table_content, table_headers