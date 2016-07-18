# fileparser

## Setup
This relies on a sqlite database connection. Run the following commands to use and run tests for this application.

	> sqlite fileparser.db
	> sqlite test.db

## Tests
Run the following command.

	> python test.py

## Execute
Place csv files in the resources/specs/ directory and txt files in resources/data/ directory.

Run the following command.

	> python parser.py

Data will be populated in the sqlite db under a table that matches your spec filename. 

## Areas of improvement
* add tests for static methods
* consider failing data imports on a per line instead of per file basis
* better integer/text type checking
* better format checking if data does not match spec
* add csv/txt extension checks
