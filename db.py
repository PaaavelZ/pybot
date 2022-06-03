import os
import sqlite3

from datetime import date


class Database:
    DB_NAME = "hws.db"

    def __enter__(self):
        self.__connection = sqlite3.connect(self._get_path())
        self.__init_table()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__connection.commit()
        self.__connection.close()

    def _get_path(self) -> str:
        path = os.path.realpath(__file__)
        path = path.removesuffix(os.path.basename(__file__))
        path = os.path.join(path, self.DB_NAME)
        path = r"{}".format(path)
        return path

    def __init_table(self) -> None:
        self.__connection.executescript("""
            CREATE TABLE IF NOT EXISTS users(
                id INT PRIMARY KEY,
                is_admin BOOLEAN,
                name VARCHAR(15),
                UNIQUE(id)
            );
            
            CREATE TABLE IF NOT EXISTS subjects(
                id INTEGER PRIMARY KEY,
                name VARCHAR(15)
            );
            
            CREATE TABLE IF NOT EXISTS hws(
                id INT PRIMARY KEY,
                deadline DATE,
                description VARCHAR(100),
                subj_id INT,
                FOREIGN KEY(subj_id) REFERENCES subjects(id),
                UNIQUE(id)
            );
        """)

        self.__connection.commit()

    # users
    def is_admin(self, user_id: int) -> bool:
        admin = self.__connection.execute(f"""SELECT is_admin FROM users WHERE id = ?;""", (user_id,)).fetchone()
        return admin[0] if admin is not None else False

    def is_user(self, user_id: int) -> bool:
        user = self.__connection.execute(f"""SELECT is_admin FROM users WHERE id = ?;""", (user_id,)).fetchone()
        return user is not None

    def add_user(self, user_id: int, is_admin: bool, name: str) -> None:
        self.__connection.execute(f"""
            INSERT OR REPLACE INTO users (id, is_admin, name)
                VALUES (?, ?, ?);
        """, (user_id, is_admin, name))
        self.__connection.commit()

    def get_user(self, id: int) -> tuple:
        return self.__connection.execute(f"""
                    SELECT id, is_admin, name
                    FROM users
                    WHERE id = ?""", (id,)).fetchone()

    def get_users(self) -> list:
        return self.__connection.execute("""SELECT id, is_admin, name FROM users""").fetchall()

    def delete_user(self, id: int) -> None:
        self.__connection.execute(f"""
            DELETE FROM users
            WHERE id = ?
            """, (id,))
        self.__connection.commit()

    # subjects
    def add_subject(self, name: str) -> None:
        self.__connection.execute(f"""
            INSERT INTO subjects (name)
            VALUES (?);
            """, (name,))
        self.__connection.commit()

    def get_subject_id(self, name: str) -> int:
        subj_id = self.__connection.execute("""
            SELECT id
            FROM subjects
            WHERE name = ?
            """, (name,)).fetchone()
        if subj_id is None:
            raise ValueError("Некорректное название предмета")
        return subj_id[0]

    def get_subjects(self) -> list:
        return self.__connection.execute("""
            SELECT id, name
            FROM subjects
            """).fetchall()

    def delete_subject(self, subj_id: int) -> None:
        self.__connection.execute(f"""
            DELETE FROM subjects
            WHERE id = ?
            """, (subj_id,))
        self.__connection.commit()

    # hws
    def add_hw(self, deadline: date, description: str, subj_id: int) -> None:
        self.__connection.execute(f"""
            INSERT INTO hws (deadline, description, subj_id)
                VALUES (?, ?, ?);
        """, (deadline, description, subj_id))
        self.__connection.commit()

    def get_hw(self, id: int) -> tuple:
        return self.__connection.execute(f"""
                    SELECT id, deadline, description
                    FROM hws
                    WHERE id = ?""", (id,)).fetchone()

    def get_hw_id(self, deadline: date) -> int:
        hw_id = self.__connection.execute(f"""
            SELECT id
            FROM hws
            WHERE deadline = ?""", (deadline,)).fetchone()
        return hw_id[0] if hw_id is not None else None

    def get_hws_by_subj_name(self, subj_name: str) -> list:
        return self.__connection.execute(f"""
            SELECT hws.id AS id, hws.deadline AS deadline, hws.description AS description
            FROM hws
            INNER JOIN subjects
            ON hws.subj_id = subjects.id
            WHERE subjects.name = ?
        """, (subj_name,)).fetchall()

    def get_hws(self) -> dict[str, list]:
        res = {}
        subjects = self.get_subjects()

        for subj in subjects:
            subj_name = subj[1]
            res[subj_name] = self.get_hws_by_subj_name(subj_name)

        return res

    def update_hw(self, hw_id: int, deadline: date, description: str) -> None:
        self.__connection.execute(f"""
                    UPDATE hws
                    SET deadline = ?,
                        description = ?
                    WHERE id = ?;
                """, (deadline, description, hw_id))
        self.__connection.commit()

    def delete_hw(self, hw_id: int) -> None:
        self.__connection.execute(f"""
            DELETE FROM hws
            WHERE id = ?
            """, (hw_id,))
        self.__connection.commit()

    def cmd(self) -> None:
        self.__connection.execute("""DROP TABLE users""")
        self.__connection.commit()
