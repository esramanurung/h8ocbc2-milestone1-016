import unittest
from app import connex_app 


class TestAPI(unittest.TestCase):

    # Test get all directors jika status code 200
    def test_all_directors(self):
        connex_app.app.testing=True
        data = connex_app.app.test_client(self)
        response = data.get("/api/director")
        self.assertEqual(response.status_code, 200)

    # Test get all movies jika status code 200
    def test_all_movies(self):
        connex_app.app.testing=True
        data = connex_app.app.test_client(self)
        response = data.get("/api/movies")
        self.assertEqual(response.status_code, 200)

    # Test get director by id jika status code 200
    def test_director_byId(self):
        connex_app.app.testing=True
        data = connex_app.app.test_client(self)
        response = data.get("/api/director/4770")
        self.assertEqual(response.status_code, 200)

    # Test get director by id jika salah dan status code 404
    def test_director_byId_false(self):
        connex_app.app.testing=True
        data = connex_app.app.test_client(self)
        response = data.get("/api/director/-1")
        self.assertEqual(response.status_code, 404)

    # Test get director by gender jika status code 200
    def test_director_byGender(self):
        connex_app.app.testing=True
        data = connex_app.app.test_client(self)
        response = data.get("/api/director/gender/0")
        self.assertEqual(response.status_code, 200)

    # Test get movies byId jika status code 200
    def test_movies_byId(self):
        connex_app.app.testing=True
        data = connex_app.app.test_client(self)
        response = data.get("/api/director/4770/movies/43710")
        self.assertEqual(response.status_code, 200)

    # Test get movies by Id jika id tidak ditemukan / 404
    def test_movies_byId_false(self):
        connex_app.app.testing=True
        data = connex_app.app.test_client(self)
        response = data.get("/api/director/-1/movies/-1")
        self.assertEqual(response.status_code, 404)

    # Test get movies by (lebih dari budget) jika status code 200
    def test_movies_budget(self):
        connex_app.app.testing=True
        data = connex_app.app.test_client(self)
        response = data.get("/api/movies/budgetMore/1000000")
        self.assertEqual(response.status_code, 200)

    # Test get movies by (lebih dari budget) jika input tidak berupa integer maka 404
    def test_movies_budget_false(self):
        connex_app.app.testing=True
        data = connex_app.app.test_client(self)
        response = data.get("/api/movies/budgetMore/abc")
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()