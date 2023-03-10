import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if 'unittest' in sys.modules.keys(): 
  engine = create_engine('sqlite:///test.sqlite')
else: # pragma: no cover
  engine = create_engine('sqlite:///aplicacion.sqlite')
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()