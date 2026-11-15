import unittest
from app import create_app
from models import db, User, Product


class ShopTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({'TESTING': True, 'SECRET_KEY': 'test-only', 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def post(self, path, **data):
        self.client.get('/login')
        with self.client.session_transaction() as session:
            data['csrf_token'] = session['csrf_token']
        return self.client.post(path, data=data)

    def register(self):
        return self.post('/register', email=' Demo@Example.test ', password='test-password-123')

    def test_registration_and_hash(self):
        self.assertEqual(self.register().status_code, 303)
        user = db.session.execute(db.select(User)).scalar_one()
        self.assertEqual(user.email, 'demo@example.test')
        self.assertNotEqual(user.password, 'test-password-123')
        self.assertEqual(self.register().status_code, 409)

    def test_login_dashboard_logout(self):
        self.assertEqual(self.client.get('/dashboard').status_code, 302)
        self.register()
        self.assertEqual(self.post('/login', email='demo@example.test', password='test-password-123').status_code, 303)
        self.assertIn(b'demo@example.test', self.client.get('/dashboard').data)
        self.assertEqual(self.client.get('/logout').status_code, 405)
        self.assertEqual(self.post('/logout').status_code, 303)
        self.assertEqual(self.client.get('/dashboard').status_code, 302)

    def test_invalid_credentials(self):
        self.register()
        for email, password in [('missing@example.test', 'test-password-123'), ('demo@example.test', 'wrong')]:
            self.assertEqual(self.post('/login', email=email, password=password).status_code, 401)

    def test_invalid_registration(self):
        for email, password in [('bad', 'test-password-123'), ('demo@example.test', 'short')]:
            self.assertEqual(self.post('/register', email=email, password=password).status_code, 400)

    def test_csrf(self):
        for token in ('', 'غير صالح'):
            self.assertEqual(self.client.post('/register', data={'csrf_token': token}).status_code, 400)

    def test_seeding_and_catalog(self):
        runner = self.app.test_cli_runner()
        for _ in range(2):
            self.assertEqual(runner.invoke(args=['seed-demo']).exit_code, 0)
        self.assertEqual(db.session.query(Product).count(), 2)
        page = self.client.get('/')
        self.assertEqual(page.status_code, 200)
        self.assertIn(b'AED 180.00', page.data)


if __name__ == '__main__':
    unittest.main()
