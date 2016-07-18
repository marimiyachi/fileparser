import parser, unittest

class TestParser(unittest.TestCase):
  def setUp(self):
    self.p = parser.Parser('test.db', './resources/test/data/', './resources/test/specs/')

  def tearDown(self):
    try: 
      self.p.drop_tables()
    except Exception:
      pass
    finally:
      self.p.close_database()
      self.p = None

  def test_init(self):
    self.assertEqual(self.p.table_column_lengths, {})

  def test_parse_specs(self):
    self.p.parse_specs()

    self.p.cursor.execute('pragma table_info(simple)')
    self.assertEqual((0, 'name', 'TEXT', 0, None, 0), self.p.cursor.fetchone())
    self.assertEqual((1, 'valid', 'BOOLEAN', 0, None, 0), self.p.cursor.fetchone())
    self.assertEqual((2, 'count', 'INTEGER', 0, None, 0), self.p.cursor.fetchone())
    self.assertEqual(0, len(self.p.cursor.fetchall()))

    self.assertEqual(self.p.table_column_lengths, {'simple': [10,1,3]})

  def test_parse_specs_datatype_error(self):
    self.p = parser.Parser('test.db', './resources/test/data/', './resources/test/specs_error/')
    with self.assertRaises(Exception):
        self.p.parse_specs()

  def test_parse_data(self):
    self.p = parser.Parser('test.db', './resources/test/data/', './resources/test/specs/')
    self.p.parse_specs()
    self.p.parse_data()

    self.p.cursor.execute('select * from simple')
    self.assertEqual(('Foonyor   ', 1, 1), self.p.cursor.fetchone())
    self.assertEqual(('Barzane   ', 0, -12), self.p.cursor.fetchone())
    self.assertEqual(('Quuxitude ', 1, 103), self.p.cursor.fetchone())
    self.assertEqual(('Don       ', 0, 1), self.p.cursor.fetchone())
    self.assertEqual(0, len(self.p.cursor.fetchall()))

  def test_parse_data_datatype_error(self):
    self.p = parser.Parser('test.db', './resources/test/data_error/', './resources/test/specs/')
    self.p.parse_specs()
    self.p.parse_data()

    self.p.cursor.execute('select * from simple')
    self.assertEqual(0, len(self.p.cursor.fetchall()))

if __name__ == '__main__':
    unittest.main()