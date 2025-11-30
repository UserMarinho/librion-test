from infrastructure.connectionDB import SessionLocal

def get_session():
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
