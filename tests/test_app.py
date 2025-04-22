import unittest
from app import app, init_db
import tempfile
import os

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        # Test configuratie
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.client = app.test_client()
        init_db()

    def tearDown(self):
        # Schoonmaken na tests
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_home_page(self):
        """Test of de homepagina correct wordt geladen"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Kwetsbare Flask Applicatie', response.data)

    def test_login(self):
        """Test of login werkt met correcte gegevens"""
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'wachtwoord123!'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welkom', response.data)

    def test_search(self):
        """Test of de zoekfunctie werkt"""
        response = self.client.get('/search?q=test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Zoekresultaten voor: test', response.data)

    def test_security_sql_injection(self):
        """Test op SQL injectie kwetsbaarheid"""
        response = self.client.post('/login', data={
            'username': "' OR 1=1 --",
            'password': 'anything'
        }, follow_redirects=True)
        # Als de kwetsbaarheid aanwezig is, zou dit moeten slagen
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welkom', response.data)

if __name__ == '__main__':
    unittest.main()