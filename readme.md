# Chilichallenge

Challenge friends on a hot and fun experience

## Installation

### Database

First time run:
$ python db_create.py

If classes added or minor changes run:
$ python db_migrate.py

If major constraints changed or db_migrate gives errors
delete app.db and the db_repository folder and rereate the db with
$ python db_create.py


To add test data to db run the "db_add_*tablename*" scripts
example: $ python db_add_products.py


## Usage

To start the server after database created and loaded with data:
$ python run.py



## Credits

Kandidatgruppen med mest SWAG

## License
MIT

© Copyright 2017, Chili Challenge
