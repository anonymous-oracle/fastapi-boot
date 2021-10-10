from passlib.context import CryptContext


class Hash:
    def __init__(self) -> None:
        self.pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def bcrypt_(self, password: str):
        return self.pwd_cxt.hash(password)


hash = Hash()
