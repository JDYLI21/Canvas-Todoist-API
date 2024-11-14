import sqlite3

class DB:
    def __init__(self):
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        self.cur.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="assignments"')
        self.check = self.cur.fetchall()

    def init_db(self):
        self.cur.execute('CREATE TABLE assignments (course_id INT NOT NULL, assignment_id INT NOT NULL, updated_at TEXT, completed BOOLEAN)')
        self.con.commit()

    def fetch_assignments(self, course_id):
        self.cur.execute(f'SELECT * FROM assignments WHERE course_id={course_id}')
        data = self.cur.fetchall()
        return data
    
    def add_assignment(self, course_id, assignment_id, updated_at, completed):
        self.cur.execute('INSERT INTO assignments VALUES (?, ?, ?, ?)', (course_id, assignment_id, updated_at, completed))
        self.con.commit()

    def update_assignment(self, course_id, assignment_id, updated_at, completed):
        self.cur.execute('UPDATE assignments SET updated_at=?, completed=? WHERE course_id=? AND assignment_id=?', (updated_at, completed, course_id, assignment_id))
        self.con.commit()