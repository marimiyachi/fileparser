import csv, os, struct, sqlite3

class Parser:
	"""Converts text files to SQL rows given a column, width, and datatype.

    Attributes:
        specspath (str): location of specs files.
        datapath (str): location of data files.
        table_column_lengths (map): column names mapped to column widths.
        conn (obj): database connection.
        cursor (obj): controls database executions.

  """

	def __init__(self, database='fileparser.db', datapath='./resources/data/', specspath='./resources/specs/'):
		self.specspath = specspath
		self.datapath = datapath
		self.table_column_lengths = {}
		self.conn = sqlite3.connect(database)
		self.cursor = self.conn.cursor()

	def parse_specs(self):
		"""Creates tables for every specs file with appropriate column names and datatypes.

		Adds table name to self.table_column_lengths and maps to a list of column lengths.

		Raises:
        	Exception: if specified datatype is not supported. 

    """
		for filename in os.listdir(self.specspath):
			tablename = os.path.splitext(filename)[0] # expect format {tablename}.csv
			self.table_column_lengths[tablename] = []
			columns = []
			with open(os.path.join(self.specspath,filename)) as csvfile:
				reader = csv.reader(csvfile)
				next(reader, None) # skip the header
				for row in reader:
					name_datatype = Parser.convert_datatype(row[0], row[2])
					columns.append(name_datatype)
					self.table_column_lengths[tablename].append(int(row[1]))

			self.cursor.execute("create table if not exists {} ({})".format(tablename, ",".join(columns)))
			self.conn.commit()

	@staticmethod
	def convert_datatype(columnname, datatype):
		if datatype == "TEXT" or datatype == "INTEGER":
			return "{} {}".format(columnname, datatype)
		elif datatype == "BOOLEAN":
			return "{} {} CHECK ({} IN (0,1))".format(columnname, datatype, columnname)
		else:
			raise Exception('datatype {} is not supported'.format(datatype))

	def parse_data(self):
		"""Parses data files into appropriate tables.

		Fails on a per-file basis if values in a BOOLEAN column are not 0 or 1 value.
		This is a Sqlite-specific implementation. 

    """
		for filename in os.listdir(self.datapath):
			lines = open(os.path.join(self.datapath,filename)).readlines()

			values = []
			tablename = os.path.splitext(filename)[0].split("_")[0] # expect format {tablename}_{date}.txt

			fmtstring = ' '.join('{}{}'.format(fw, 's') for fw in self.table_column_lengths[tablename])
			fieldstruct = struct.Struct(fmtstring)

			for l in lines:
				fields = fieldstruct.unpack_from(l)
				values.append(fields)

			try:
				field_query = ','.join(['?']*len(self.table_column_lengths[tablename]))
				self.cursor.executemany("insert into {} values ({})".format(tablename, field_query), values)
				self.conn.commit()
			except sqlite3.IntegrityError:
				# BOOLEAN datatype values need to be 0 or 1
				self.conn.rollback()				

	def drop_tables(self):
		for tablename in self.table_column_lengths.keys():
			self.cursor.execute("drop table {}".format(tablename))
		self.conn.commit()

	def close_database(self):
		self.cursor.close()
		self.conn.close()

if __name__ == "__main__":
	p = Parser()
	p.parse_specs()
	p.parse_data()
	p.close_database()
