import io
import json
import os
import tempfile
import unittest
from pathlib import Path

import app as tp1


class ChatAppTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.old_path = tp1.DB_PATH
        self.old_key = os.environ.pop("OPENAI_API_KEY", None)
        tp1.DB_PATH = Path(self.temp.name) / "chat.sqlite3"
        tp1.init_database()
        tp1.app.config["TESTING"] = True
        self.client = tp1.app.test_client()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        with tp1.database() as db:
            self.conversation_id = db.execute("SELECT id FROM conversations").fetchone()["id"]

    def tearDown(self):
        tp1.DB_PATH = self.old_path
        if self.old_key is not None:
            os.environ["OPENAI_API_KEY"] = self.old_key
        self.temp.cleanup()

    def test_discussions_specialty_and_export(self):
        response = self.client.post("/conversations", data={"specialty": "sql"})
        self.assertEqual(response.status_code, 302)
        new_id = int(response.headers["Location"].split("c=")[1])
        response = self.client.post(f"/conversations/{new_id}/specialty", data={"specialty": "python"})
        self.assertEqual(response.status_code, 302)
        with tp1.database() as db:
            row = db.execute("SELECT specialty FROM conversations WHERE id = ?", (new_id,)).fetchone()
        self.assertEqual(row["specialty"], "python")
        exported = json.loads(self.client.get("/conversations/export").data)
        self.assertEqual(len(exported), 2)

    def test_sql_import_question_rating_and_clear(self):
        sql = b"CREATE TABLE auteurs (id INTEGER);\nCREATE TABLE livres (id INTEGER);"
        response = self.client.post(
            f"/conversations/{self.conversation_id}/upload",
            data={"document": (io.BytesIO(sql), "bibliotheque.sql")},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.post(
            f"/conversations/{self.conversation_id}/messages",
            data={"message": "Quelles tables contient ce fichier ?"},
        )
        self.assertEqual(response.status_code, 302)
        with tp1.database() as db:
            messages = db.execute("SELECT * FROM messages ORDER BY id").fetchall()
            imported_table = db.execute(
                "SELECT name FROM sqlite_master WHERE name = 'auteurs'"
            ).fetchone()
        self.assertEqual(len(messages), 2)
        self.assertIn("auteurs", messages[1]["content"])
        self.assertIn("livres", messages[1]["content"])
        self.assertIsNone(imported_table)

        answer_id = messages[1]["id"]
        self.client.post(
            f"/conversations/{self.conversation_id}/messages/{answer_id}/rating",
            data={"rating": "1"},
        )
        page = self.client.get(f"/?c={self.conversation_id}")
        self.assertIn(b"bg-emerald-50", page.data)
        exported = json.loads(self.client.get(f"/conversations/{self.conversation_id}/export").data)
        self.assertEqual(exported["messages"][1]["rating"], 1)

        self.client.post(
            f"/conversations/{self.conversation_id}/messages/{answer_id}/rating",
            data={"rating": "-1"},
        )
        page = self.client.get(f"/?c={self.conversation_id}")
        self.assertIn(b"bg-rose-50", page.data)

        self.client.post(f"/conversations/{self.conversation_id}/clear")
        with tp1.database() as db:
            remaining = db.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
            document = db.execute("SELECT document_text FROM conversations").fetchone()[0]
        self.assertEqual(remaining, 0)
        self.assertIsNone(document)

    def test_rejects_non_text_file(self):
        response = self.client.post(
            f"/conversations/{self.conversation_id}/upload",
            data={"document": (io.BytesIO(b"print('bad')"), "script.py")},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
