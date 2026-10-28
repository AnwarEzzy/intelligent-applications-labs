import unittest

from data_processing import filter_vehicles, load_vehicles
from model import predict_consumption, train_model


class TP2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vehicles = load_vehicles()

    def test_dataset_and_filters(self):
        vehicles = self.vehicles
        self.assertEqual(len(vehicles), 398)
        self.assertEqual(int(vehicles["horsepower"].isna().sum()), 6)
        self.assertAlmostEqual(vehicles["consumption_l_100km"].mean(), 11.21, places=2)
        selected = filter_vehicles(vehicles, ["japan"], (1975, 1980), [4], 25.0)
        self.assertGreater(len(selected), 0)
        self.assertTrue(selected["origin"].eq("japan").all())
        self.assertTrue(selected["year"].between(1975, 1980).all())
        self.assertTrue(selected["cylinders"].eq(4).all())
        self.assertTrue(selected["mpg"].ge(25.0).all())

    def test_model_predicts_and_reports_holdout_quality(self):
        result = train_model(self.vehicles)
        self.assertEqual((result.train_size, result.test_size), (318, 80))
        self.assertLess(result.mae, 2.0)
        self.assertGreater(result.r2, 0.75)
        consumption, mpg = predict_consumption(
            result,
            cylinders=4,
            displacement=140.0,
            horsepower=90.0,
            weight_kg=1150.0,
            acceleration=15.0,
            year=1976,
            origin="usa",
        )
        self.assertGreater(consumption, 0)
        self.assertAlmostEqual(consumption * mpg, 235.214583, places=5)


if __name__ == "__main__":
    unittest.main()
