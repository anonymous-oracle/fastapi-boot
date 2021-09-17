from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, declarative_base, relationship

# CREATING MAPPED CLASSES INSTEAD OF SIMPLE TABLE OBJECTS

mapper_registry = registry()

print(mapper_registry.metadata)

# SINCE THE MAPPED REGISTRY HAS A METADATA OBJECT, IT CAN BE USED TO GENERATE A BASE CLASS FROM WHICH THE ORM MAPPED CLASSES CAN DESCEND FROM
Base = mapper_registry.generate_base()


# ANOTHER WAY TO GET THE DECLARATIVE BASE IS AS FOLLOWS
Base = declarative_base()

# A BI-DIRECTIONAL RELATIONSHIP IS ALSO DEMONSTRATED
class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    fullname = Column(String)

    addresses = relationship("Address", back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    # THE NAMING IN RELATIONSHIP CAN BE UNDERSTOOD BY OBSERVING THE OTHER RELATIONSHIP IN THE MAPPED CLASS TO WHICH IT RELATES TO
    user = relationship("User", back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id}, email_address={self.email_address})"

user = User(name='Eren', fullname = 'Eren Krueger')

# CREATING THE TABLE 