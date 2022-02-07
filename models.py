from sqlalchemy import Column, Enum, ForeignKey, Integer, Numeric, String, Table  # noqa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# create the compound_assay association table model
compound_assay = Table(
    "compound_assay",
    Base.metadata,
    Column("compound_id", Integer, ForeignKey("compound.compound_id")),
    Column("result_id", Integer, ForeignKey("assay.result_id")),
)


# define the Compound class model to the compound database table
class Compound(Base):
    __tablename__ = "compound"
    compound_id = Column(Integer, primary_key=True)
    smiles = Column(String)
    molecular_weight = Column(Numeric)
    ALogP = Column(Numeric)
    molecular_formula = Column(String)
    num_rings = Column(Numeric)
    image = Column(String)
    assay_results = relationship(
        "Assay", secondary=compound_assay, back_populates="compounds"
    )

    def __repr__(self):
        return (
            f"<Compound object with compound_id={self.compound_id}, "
            f"molecular_formula={self.molecular_formula}>"
        )


# define the Assay class model to the assay database table
class Assay(Base):
    __tablename__ = "assay"
    result_id = Column(Integer, primary_key=True)
    target = Column(String)
    result = Column(Enum("IC50", "Ki", "Kd"))
    operator = Column(Enum("=", ">", "<", "<=", ">=", "~", "*"))
    value = Column(Integer)
    unit = Column(String)
    compounds = relationship(
        "Compound", secondary=compound_assay, back_populates="assay_results"
    )

    def __repr__(self):
        return f"<Assay object with result_id={self.result_id}>"
