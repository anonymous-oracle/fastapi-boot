from passlib.context import CryptContext


class Hash:
    def __init__(self) -> None:
        self.pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def bcrypt_(self, password: str):
        return self.pwd_cxt.hash(password)

    def verify(self, entered_password, hashed_password):
        return self.pwd_cxt.verify(entered_password, hashed_password)


hash = Hash()
