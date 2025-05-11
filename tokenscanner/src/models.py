from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Token(Base):
    # Tracks each token on the network
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    chain_id = Column(String, nullable=False)
    address = Column(String, unique=True, nullable=False, index=True)

    symbol = Column(String, nullable=True)
    largest_pool_id = Column(
        Integer,
        ForeignKey("pools.id", use_alter=True, name="fk_largest_pool_id"),
        nullable=True,
    )
    pool_count = Column(Integer, default=0, nullable=False)

    total_supply = Column(Numeric(precision=20, scale=4), default=0, nullable=True)
    total_liquidity_usd = Column(
        Numeric(precision=20, scale=4), default=0, nullable=False
    )

    largest_pool = relationship(
        "Pool", backref="largest_pool", foreign_keys=[largest_pool_id]
    )
    pools = relationship("Pool", backref="token", foreign_keys="[Pool.token_id]")


class Pool(Base):
    # Tracks each pool on the network
    __tablename__ = "pools"

    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(Integer, ForeignKey("tokens.id"), nullable=False)
    pool_address = Column(String, unique=True, nullable=False)
    pair_address = Column(String, nullable=False)
    liquidity_usd = Column(Numeric(precision=20, scale=4))
    quote_token_address = Column(String, nullable=False)
    name = Column(String, nullable=True)
