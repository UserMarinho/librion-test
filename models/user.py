# classe de usuário genérico
class User():
    def __init__(self, name: str, cep: str):
        self.name = name
        self.cep = cep
        self.admin = False