import unittest

from app.services.authService import authenticate_user, register_user


class FakeCollection:
    def __init__(self):
        self.docs = []

    def find_one(self, query):
        for doc in self.docs:
            if all(doc.get(k) == v for k, v in query.items()):
                return doc
        return None

    def insert_one(self, doc):
        self.docs.append(doc)
        return type("Result", (), {"inserted_id": len(self.docs)})()


class FakeDatabase:
    def __init__(self):
        self.users = FakeCollection()


class AuthServiceTests(unittest.TestCase):
    def test_register_and_login_work_with_hashed_password(self):
        db = FakeDatabase()
        user = register_user(db, "Asha", "asha@example.com", "StrongPass123")

        self.assertEqual(user["email"], "asha@example.com")
        self.assertNotEqual(user["password_hash"], "StrongPass123")

        authenticated = authenticate_user(db, "asha@example.com", "StrongPass123")
        self.assertIsNotNone(authenticated)
        self.assertEqual(authenticated["email"], "asha@example.com")

        wrong_password = authenticate_user(db, "asha@example.com", "WrongPass")
        self.assertIsNone(wrong_password)


if __name__ == "__main__":
    unittest.main()
