from typing import Type

from sqlalchemy import create_engine, MetaData, inspect, QueuePool, text, CHAR, Column, BIGINT, DATETIME, SMALLINT, \
    REAL, Integer, VARCHAR, distinct, func, and_
from sqlalchemy.orm import sessionmaker, declarative_base


# csilms_engine = create_engine(
#     f"fob_sybase+pyodbc://auditdba:Password@160.12.152.1/csilms?driver=Adaptive Server Enterprise&port=5000", pool_size=20,
#     poolclass=QueuePool, echo=True)
# Csilms_Session = sessionmaker(bind=csilms_engine)
# csilms_session = Csilms_Session()
# csilms_sybase_metadata = MetaData()
# Csilms_Base = declarative_base(metadata=csilms_sybase_metadata)
# csilms_inspector = inspect(csilms_engine)


# hp_unix_engine = create_engine(
#     f"fob_sybase+pyodbc://sa:password@160.16.2.175/csilms?driver=Adaptive Server Enterprise&port=5000", pool_size=20,
#     poolclass=QueuePool, echo=True)
# Hp_Unix_Session = sessionmaker(bind=hp_unix_engine)
# hp_unix_session = Hp_Unix_Session()
# hp_unix_sybase_metadata = MetaData()
# Hp_unix_Base = declarative_base(metadata=hp_unix_sybase_metadata)
# Hp_unix_inspector = inspect(hp_unix_engine)


dev_engine = create_engine(
    f"sybase+pyodbc://auditdba:password@160.12.152.10/csilms?driver=Adaptive Server Enterprise&port=5000", pool_size=20,
    poolclass=QueuePool, echo=True)
Dev_Session = sessionmaker(bind=dev_engine)
dev_session = Dev_Session()
dev_sybase_metadata = MetaData()
Dev_Base = declarative_base(metadata=dev_sybase_metadata)
dev_inspector = inspect(dev_engine)

class AuditLedgerTesting2(Dev_Base):
# class AuditLedgerTesting2(Hp_unix_Base):

    __tablename__ = 'AuditLedger'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    ItemCode = Column(CHAR(32), nullable=False)
    SHNo = Column(CHAR(3), nullable=False)
    DemandNo = Column(CHAR(7))
    CustomerCode = Column(CHAR(4))
    StationCode = Column(CHAR(1), nullable=True)
    IssueDateTime = Column(DATETIME)
    StockReleaseSerial = Column(SMALLINT)
    QtyReleased = Column(REAL)
    QtyReceipted = Column(REAL)
    StockSerial = Column(Integer)
    StoreReceiptNo = Column(CHAR(11))
    StockTransferKey = Column(DATETIME)
    StockTransferNo = Column(CHAR(13))
    NewItemCode = Column(CHAR(32))
    NewStockSerial = Column(Integer)
    Years = Column(CHAR(4), nullable=False)
    Months = Column(CHAR(3), nullable=False)
    AuditedByAuditor = Column(CHAR(8))
    DateTimeAuditedByAuditor = Column(DATETIME)
    AuditedByANLAO = Column(CHAR(8))
    DateTimeAuditedByANLAO = Column(DATETIME)
    AuditedByNLAO = Column(CHAR(8))
    DateTimeAuditedByNLAO = Column(DATETIME)
    LedgerNo = Column(CHAR(10))
    Folio = Column(CHAR(6))
    TransactionReference = Column(VARCHAR(60))
    CRPCategory = Column(CHAR(1))
    BatchNo = Column(CHAR(10))
    TransactionQtyLogical = Column(REAL(4))
    TransactionQtyGround = Column(REAL(4))
    SHNoNew = Column(CHAR(3))
    ConditionCode = Column(CHAR(3))
    QtyBalance = Column(REAL(4))
    TransactionDateTime = Column(DATETIME, nullable=False)


# class ItemLine(Csilms_Base):
class ItemLine(Dev_Base):
# class ItemLine(Hp_unix_Base):
    # class ItemLine(Dev_Base):
    __tablename__ = 'ItemLine'
    id = Column(Integer, primary_key=True)
    ItemCode = Column(CHAR(32), nullable=False)
    # ItemDesc = Column(CHAR(60), nullable=False)
    StationCode = Column(CHAR(1), nullable=False)
    SHNo = Column(CHAR(3), nullable=False)
    QtyMSL = Column(REAL(4), nullable=False)
    QtyACL = Column(REAL(4), nullable=False)
    QtyUSL = Column(REAL(4), nullable=False)


class StoreHouse(Dev_Base):
# class StoreHouse(Hp_unix_Base):
    __tablename__ = 'SH'
    SHNo = Column(CHAR(3), primary_key=True)
    SHDec = Column(CHAR(20), nullable=True)
    SHType = Column(CHAR(2), nullable=True)






#
# audit_ledger_query = (dev_session.query(AuditLedgerTesting2.SHNo, AuditLedgerTesting2.ItemCode)
#                       .join(StoreHouse, StoreHouse.SHNo == AuditLedgerTesting2.SHNo)
#                       .filter(AuditLedgerTesting2.StationCode.like('B'))
#                       .group_by(AuditLedgerTesting2.SHNo, AuditLedgerTesting2.ItemCode)
#                       .order_by(AuditLedgerTesting2.SHNo)
#                       )



# required_data: list[Ledger] = [Ledger(item.SHNo, 'All', "", "", item.ItemCode.strip(), 'NLAO') for item in ledger_testing1.all()]
# required_data: list[Ledger] = [Ledger(item.SHNo, 'All', "", "", item.ItemCode.strip(), 'NLAO') for item in
#                                audit_ledger_query.all()]

# for data in audit_ledger_query.all():
#     print(data)

for data in dev_session.execute(text('select 1 ')).all():
    print(data)