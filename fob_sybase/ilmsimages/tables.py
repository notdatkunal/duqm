import datetime
from sqlalchemy import Column,DATETIME, VARCHAR, BIGINT, TEXT
from fob_sybase.Connections import ConnectionsElement


class AuditDocuments(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ilmsimages..AuditDocuments'
    DocumentID = Column(BIGINT, primary_key=True, autoincrement=True)
    DocumentName = Column(VARCHAR(255), nullable=False)
    DocumentType = Column(VARCHAR(255), nullable=False)
    DocumentExtension = Column(VARCHAR(20), nullable=False)
    DateTimeCreated = Column(DATETIME, nullable=False, default=datetime.datetime.now())
    DocumentSize = Column(BIGINT, nullable=False)
    Base64Content = Column(TEXT, nullable=False)
