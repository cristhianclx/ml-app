import unittest

from fastapi.testclient import TestClient

from challenge import app


class TestBase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "OK"})


class TestBatchPipeline(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_should_get_predict_success(self):
        data = {
            "flights": [
                {
                    "OPERA": "Latin American Wings",
                    "TIPOVUELO": "N",
                    "MES": 7,
                },
            ],
        }
        # api
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"predict": [1]})

    def test_should_get_predict(self):
        data = {
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas",
                    "TIPOVUELO": "N",
                    "MES": 3,
                },
            ],
        }
        # api
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"predict": [0]})

    def test_should_failed_unkown_column_1(self):
        data = {
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas",
                    "TIPOVUELO": "N",
                    "MES": 13,
                },
            ],
        }
        # api
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 400)

    def test_should_failed_unkown_column_2(self):
        data = {
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas",
                    "TIPOVUELO": "O",
                    "MES": 13,
                },
            ],
        }
        # api
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 400)

    def test_should_failed_unkown_column_3(self):
        data = {
            "flights": [
                {
                    "OPERA": "Argentinas",
                    "TIPOVUELO": "O",
                    "MES": 13,
                },
            ],
        }
        # api
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 400)
