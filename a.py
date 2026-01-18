from infrastructure.connectionDB import SessionLocal
from models import Library

session = SessionLocal()
library = session.query(Library).filter(Library.id == 1).first()

library.name = "juazeiro"

session.commit()
session.close()