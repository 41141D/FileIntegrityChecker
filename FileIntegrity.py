import hashlib
import sqlite3
class FileIntegrity:
    def __init__(self):
        self.db = sqlite3.connect("jungle.db")
        self.cursor = self.db.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS file_hashing (file_name TEXT,original_file TEXT)''')
        self.db.commit()
    def save_hash(self,file_path:str,file_name:str):
        hashing =self._calculate_hash(file_path)
        self.cursor.execute('''INSERT INTO file_hashing VALUES (?,?)''',(file_name,hashing))
        self.db.commit()
    def compare_hash(self,file_name:str,changed_file:str):
        updated_file_hash = self._calculate_hash(changed_file)
        self.cursor.execute('''
        SELECT original_file FROM file_hashing WHERE file_name=?
        ''',(file_name,))
        result = self.cursor.fetchone()
        original_file = result[0] if result else None
        if original_file:
            if original_file == updated_file_hash:
                print(f"same hash = same file   {original_file} | {updated_file_hash}")
            else:
                print(f"different hash = different file or file has been modified {original_file} | {updated_file_hash}")
    def _calculate_hash(self, file_hash: str):
        hasher = hashlib.sha256()
        with open(file_hash, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
