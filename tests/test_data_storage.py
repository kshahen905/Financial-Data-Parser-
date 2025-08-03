import unittest
import pandas as pd
from src.core.data_storage import DataStorage

class TestDataStorage(unittest.TestCase):

    def setUp(self):
        self.storage = DataStorage()
        self.df = pd.DataFrame({
            'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'Amount': [1000, 2000, 3000],
            'Category': ['A', 'B', 'A']
        })
        self.column_types = {
            'Date': 'date',
            'Amount': 'number',
            'Category': 'string'
        }
        self.dataset_name = 'TestSet'
        self.storage.store_data(self.dataset_name, self.df, self.column_types)

    def test_store_data(self):
        self.assertIn(self.dataset_name, self.storage.datasets)
        self.assertIn(self.dataset_name, self.storage.column_types)
        self.assertIn(self.dataset_name, self.storage.indexes)

        index = self.storage.indexes[self.dataset_name]
        self.assertEqual(index['date_cols'], ['Date'])
        self.assertEqual(index['amount_cols'], ['Amount'])
        self.assertEqual(index['string_cols'], ['Category'])

    def test_query(self):
        result = self.storage.query(self.dataset_name, 'Amount', lambda x: x > 1500)
        self.assertEqual(len(result), 2)
        self.assertTrue((result['Amount'] > 1500).all())

    def test_query_invalid_column(self):
        result = self.storage.query(self.dataset_name, 'NonExistent', lambda x: x > 0)
        self.assertTrue(result.empty)

    def test_aggregate_sum(self):
        result = self.storage.aggregate(self.dataset_name, 'Category', 'Amount', 'sum')
        self.assertEqual(len(result), 2)
        self.assertIn('Amount', result.columns)
        self.assertAlmostEqual(result[result['Category'] == 'A']['Amount'].iloc[0], 4000)

    def test_aggregate_invalid_column(self):
        result = self.storage.aggregate(self.dataset_name, 'Invalid', 'Amount')
        self.assertTrue(result.empty)

if __name__ == '__main__':
    unittest.main()
