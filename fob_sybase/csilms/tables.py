from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy import Column, Integer, CHAR, DATETIME, VARCHAR, REAL, DECIMAL, VARBINARY, SMALLINT, BIGINT, INT, Index, \
    TEXT, ForeignKey, Boolean, Numeric, BLOB
from sqlalchemy import event, func, or_ 
from fob_sybase.exceptions import DemandError
from fob_sybase.Connections import ConnectionsElement


class FSNCategory(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'FSNCategory'
    id = Column(Integer, primary_key=True)
    ItemCode = Column(CHAR(32), nullable=False)
    SHNo = Column(CHAR(3), nullable=False)
    Catg = Column(CHAR(1), nullable=False)
    RunSrl = Column(Integer, nullable=False)
    Srl = Column(Integer, nullable=False)
    Status = Column(CHAR(2), nullable=True)
    ItemCode_New = Column(CHAR(32), nullable=True)
    StationCode = Column(CHAR(1), nullable=False)
    HMLCategory = Column(CHAR(1), nullable=True)
    VerificationCycle = Column(CHAR(9), nullable=True)


class Orders(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'Orders'
    id = Column(Integer, primary_key=True)
    IndentNo = Column(CHAR(9), nullable=False)
    VendorCode = Column(CHAR(6), nullable=False)
    OrderDate = Column(DATETIME, nullable=False)
    ValueRs = Column(CHAR(8), nullable=False)
    InspectingAgencyType = Column(CHAR(8), nullable=False)
    InspectorCode = Column(CHAR(3), nullable=True)
    InspectionSiteCode = Column(CHAR(1), nullable=False)
    Remarks = Column(VARCHAR(255), nullable=True)
    QuoteKey = Column(DATETIME, nullable=True)
    SelectedQuoteDate = Column(DATETIME, nullable=True)
    DateTimeApproved = Column(DATETIME, nullable=True)
    ApprovedBy = Column(CHAR(8), nullable=True)
    TypeClosing = Column(CHAR(1), nullable=True)
    DateClosed = Column(DATETIME, nullable=True)
    ClosedBy = Column(CHAR(8), nullable=True)
    PackingInstruction = Column(VARCHAR(255), nullable=True)
    DespatchInstruction = Column(VARCHAR(120), nullable=True)
    InspectionInstruction = Column(VARCHAR(120), nullable=True)
    StationCode = Column(CHAR(1), nullable=False)
    Remarks1 = Column(TEXT, nullable=True)
    GeMOrderId = Column(VARCHAR(20), nullable=True)
    GeMSupplyOrderNo = Column(VARCHAR(255), nullable=True)
    ILMSKey = Column(VARCHAR(255), nullable=True)
    QRCode = Column(BLOB, nullable=True)


class TransportationDocument(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'TransportationDocument'
    id = Column(Integer, primary_key=True)
    TransportationDocumentNo = Column(CHAR(30), nullable=False)
    TransportationDocumentDate = Column(DATETIME, nullable=False)
    NoOfPackages = Column(Integer, nullable=False)
    ConsigneeCode = Column(CHAR(8), nullable=False)
    PlaceShippedFrom = Column(VARCHAR(30), nullable=False)
    InformationRef = Column(VARCHAR(60), nullable=False)
    TransportationMode = Column(CHAR(3), nullable=False)
    TransportNo = Column(CHAR(15), nullable=True)
    TransporterName = Column(VARCHAR(31), nullable=True)
    ETA = Column(DATETIME, nullable=False)
    CollectionPlace = Column(CHAR(20), nullable=True)
    AOTRRef = Column(VARCHAR(60), nullable=True)
    Remarks = Column(VARCHAR(180), nullable=True)
    DateReceived = Column(DATETIME, nullable=True)
    DateTimeApproved = Column(DATETIME, nullable=True)
    ApprovedBy = Column(CHAR(8), nullable=True)
    StationCode = Column(CHAR(1), nullable=False)


class Demurrage(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'Demurrage'
    id = Column(Integer, primary_key=True)
    TransportationDocumentNo = Column(CHAR(30), nullable=False)
    TransportationDocumentDate = Column(DATETIME, nullable=False)
    LotNo = Column(Integer, nullable=False)
    Amount = Column(CHAR(8), nullable=False)
    ModeOfPayment = Column(CHAR(2), nullable=False)
    PaymentDate = Column(DATETIME, nullable=True)
    PaymentVoucherRef = Column(VARCHAR(60), nullable=True)
    PaymentVoucherDate = Column(DATETIME, nullable=True)
    Remarks = Column(VARCHAR(120), nullable=True)
    DateTimeApproved = Column(DATETIME, nullable=True)
    ApprovedBy = Column(CHAR(8), nullable=True)
    StationCode = Column(CHAR(1), nullable=True)


class StockVerificationLineExternal(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'StockVerificationLineExternal'
    id = Column(Integer, primary_key=True)
    StockVerificationNo = Column(CHAR(20), nullable=False)
    StockVerificationLineNo = Column(Integer, nullable=False)
    RunSrl = Column(Integer, nullable=False)
    Srl = Column(Integer, nullable=False)
    Catg = Column(CHAR(1), nullable=False)
    ItemCode = Column(CHAR(32), nullable=False)
    StockSerial = Column(CHAR(4), nullable=False)
    QtyLogical = Column(CHAR(4), nullable=False)
    QtyGround = Column(CHAR(4), nullable=True)
    QtyVerified = Column(CHAR(4), nullable=True)
    LossStatementKey = Column(DATETIME, nullable=True)
    Remarks = Column(VARCHAR(120), nullable=True)
    VerifiedBy = Column(CHAR(8), nullable=True)
    DateTimeVerified = Column(DATETIME, nullable=True)
    StationCode = Column(CHAR(1), nullable=False)


class StockVerification(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'StockVerification'
    id = Column(Integer, primary_key=True)
    StockVerificationNo = Column(CHAR(20), nullable=False)
    DateFrom = Column(DATETIME, nullable=False)
    DateTill = Column(DATETIME, nullable=False)
    DateTimeApproved = Column(DATETIME, nullable=True)
    ApprovedBy = Column(CHAR(8), nullable=True)
    StockVerificationType = Column(CHAR(4), nullable=True)
    StationCode = Column(CHAR(1), nullable=False)
    AuthorityRef = Column(CHAR(20), nullable=True)
    AuthorityDate = Column(DATETIME, nullable=True)


class Price(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'Price'
    id = Column(Integer, primary_key=True)
    ItemCode = Column(CHAR(32), nullable=False)
    PriceType = Column(CHAR(1), nullable=False)
    PriceDate = Column(DATETIME, nullable=False)
    PriceRef = Column(VARCHAR(60), nullable=False)
    PriceCC = Column(CHAR(8), nullable=False)
    CurrencyCode = Column(CHAR(3), nullable=False)
    VendorCode = Column(CHAR(6), nullable=True)
    Qty = Column(REAL, nullable=True)
    DateTimeApproved = Column(DATETIME, nullable=True)
    ApprovedBy = Column(CHAR(8), nullable=True)
    StationCode = Column(CHAR(1), nullable=False)


class Discrepancy(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'Discrepancy'
    id = Column(Integer, primary_key=True)
    StoreReceiptNo = Column(CHAR(11), nullable=False)
    BatchNo = Column(CHAR(10), nullable=False)
    SerialNo = Column(SMALLINT, nullable=False)
    Qty = Column(REAL, nullable=False)
    DiscrepancyType = Column(CHAR(1), nullable=False)
    DiscrepancyRemarks = Column(VARCHAR(120), nullable=True)
    SettlementRemarks = Column(VARCHAR(120), nullable=True)
    DateSettled = Column(DATETIME, nullable=True)
    DateTimeClosed = Column(DATETIME, nullable=True)
    ClosedBy = Column(CHAR(8), nullable=True)
    DateTimeInitiated = Column(DATETIME, nullable=True)
    InitiatedBy = Column(CHAR(8), nullable=True)


class OrderLine(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'OrderLine'
    id = Column(Integer, primary_key=True)
    IndentNo = Column(CHAR(9), nullable=False)
    VendorCode = Column(CHAR(6), nullable=False)
    OrderDate = Column(DATETIME, nullable=False)
    OrderLineNo = Column(SMALLINT, nullable=False)
    ItemCode = Column(CHAR(32), nullable=False)
    ConsigneeCode = Column(CHAR(8), nullable=False)
    OrderLineDRB = Column(DATETIME, nullable=False)
    Specs = Column(CHAR(20), nullable=True)
    Qty = Column(REAL, nullable=False)
    UnitCostCC = Column(Numeric, nullable=False)
    PilotSampleDRB = Column(DATETIME, nullable=False)
    MIQPQty = Column(REAL, nullable=False)
    PackType = Column(CHAR(2), nullable=False)
    StationCode = Column(CHAR(1), nullable=False)
    ReReferencedItemCode = Column(CHAR(24), nullable=True)
    GeMProductCode = Column(VARCHAR(255), nullable=True)
    MaterialNo = Column(SMALLINT, nullable=True)


class UserRole(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'UserRole'
    id = Column(Integer, primary_key=True)
    LoginId = Column(CHAR(8))
    RoleName = Column(CHAR(15))
    StationCode = Column(CHAR(1))
    DateTimeClosed = Column(DATETIME)


# fob_postgres table names


#     inGateInDateTime + IntStoreReceiptNO +


# class DocumentReference(Base):
#     __tablename__ = 'DocumentReference'
#     id = Column(Integer, primary_key=True)
#     ReferenceKey = Column(Integer, nullable=False)
#     DocType = Column(CHAR(30), nullable=True)
#     StationCode = Column(CHAR(1), nullable=True)
#     DocumentNo = Column(VARCHAR(60), nullable=True)
#     DocumentDate = Column(DATETIME, nullable=True)
#     DateTimeAdded = Column(DATETIME, nullable=True)
#     Document = Column(BLOB, nullable=True)


# class DocumentReference(Base):
#     __tablename__ = 'ilmsimages..DocumentReference'
#     id = Column(Integer, primary_key=True)
#     ReferenceKey = Column(Integer, nullable=False)
#     DocType = Column(CHAR(30), nullable=True)
#     StationCode = Column(CHAR(1), nullable=True)
#     DocumentNo = Column(VARCHAR(60), nullable=True)
#     DocumentDate = Column(DATETIME, nullable=True)
#     DateTimeAdded = Column(DATETIME, nullable=True)
#     Document = Column(BLOB, nullable=True)

class Role(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'Roles'
    id = Column(Integer, primary_key=True)
    RoleName = Column(CHAR(15))


# class DocumentUploadMaster(Base):
#     __tablename__ = 'DocumentUploadMaster'
#     id = Column(Integer, primary_key=True)
#     TableName = Column(CHAR(30), nullable=False)
#     ColumnValue = Column(CHAR(32), nullable=False)
#     PrimaryKeyValue = Column(VARCHAR(30), nullable=False)
#     ImageLineNo = Column(Integer, nullable=False)
#     DateTimeAdded = Column(DATETIME, nullable=True)
#     AddedBy = Column(CHAR(8), nullable=True)
#     Remarks = Column(VARCHAR(250), nullable=True)
#     DateTimeClosed = Column(DATETIME, nullable=True)
#     ClosedBy = Column(CHAR(8), nullable=True)
#     StationCode = Column(CHAR(1), nullable=True)
#     ReferenceKey = Column(Integer, nullable=True)
#     ItemVendorCode = Column(VARCHAR(32), nullable=True)


# class DocumentUpload(Base):
#     __tablename__ = 'DocumentUpload'
#     id = Column(Integer, primary_key=True)
#     TableName = Column(CHAR(30), nullable=False)
#     ColumnValue = Column(CHAR(32), nullable=False)
#     PrimaryKeyValue = Column(VARCHAR(120), nullable=False)
#     ImageLineNo = Column(Integer, nullable=False)
#     DocumentType = Column(CHAR(30), nullable=False)
#     DateTimeAdded = Column(DATETIME, nullable=False)
#     AddedBy = Column(CHAR(8), nullable=False)
#     StationCode = Column(CHAR(1), nullable=False)
#     Remarks = Column(VARCHAR(250), nullable=False)
#     Document = Column(BLOB, nullable=False)


class Vendor(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'Vendor'
    VendorCode = Column(CHAR(6), primary_key=True)
    Name = Column(VARCHAR(256), nullable=False)
    Class = Column(CHAR(1), nullable=False)
    ManufacturerPriority = Column(CHAR(2), nullable=True)
    Addressee = Column(CHAR(30), nullable=False)
    AddressLine1 = Column(VARCHAR(255), nullable=False)
    AddressLine2 = Column(CHAR(30), nullable=True)
    AddressLine3 = Column(CHAR(30), nullable=True)
    City = Column(VARCHAR(80), nullable=False)
    State = Column(VARCHAR(80), nullable=False)
    PINCode = Column(CHAR(7), nullable=True)
    CountryCode = Column(CHAR(3), nullable=False)
    DateTimeApproved = Column(DATETIME, nullable=True)
    ApprovedBy = Column(CHAR(4), nullable=True)
    DateBannedUpto = Column(DATETIME, nullable=True)
    SectionHead = Column(CHAR(2), nullable=True)
    KompassControlNo = Column(CHAR(9), nullable=True)
    Remarks = Column(VARCHAR(120), nullable=True)
    StationCode = Column(CHAR(1), nullable=False)
    NCAGE = Column(CHAR(5), nullable=True)
    GEMSellerID = Column(VARCHAR(255), nullable=True)
    BusinessType = Column(VARCHAR(255), nullable=True)
    DefProcId = Column(VARCHAR(256), nullable=True)
    MSMERegistrationNo = Column(VARCHAR(32), nullable=True)
    GSTNo = Column(VARCHAR(15), nullable=True)
    PAN = Column(VARCHAR(10), nullable=True)


class Issue(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'Issue'
    id = Column(Integer, primary_key=True)
    CustomerCode = Column(CHAR(4), nullable=False)
    DemandNo = Column(CHAR(7), nullable=False)
    ItemCode = Column(CHAR(32), nullable=False)
    SHNo = Column(CHAR(3), nullable=False)
    Qty = Column(DECIMAL, nullable=False)
    PriceRs = Column(DECIMAL, nullable=False)
    DateTimeOBD = Column(DATETIME, nullable=True)
    IssueDateTime = Column(DATETIME, nullable=False)
    IssuedBy = Column(CHAR(8), nullable=False)
    StationCode = Column(CHAR(1), nullable=False)
    IssueType = Column(CHAR(1), nullable=True)


class SHAppointment(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'SHAppointment'
    # id = Column(Integer, primary_key=True)
    LoginId = Column(CHAR(8))
    RoleName = Column(CHAR(15))
    StationCode = Column(CHAR(1))
    SHNo = Column(CHAR(3))
    DateTimeClosed = Column(DATETIME)
    DateTimeActivated = Column(DATETIME, primary_key=True)


class Appointment(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'Appointment'
    id = Column(Integer, primary_key=True)
    LoginId = Column(CHAR(8))
    RoleName = Column(CHAR(15))
    StationCode = Column(CHAR(1))
    DeptSectionCode = Column(CHAR(3))
    DateTimeClosed = Column(DATETIME)


class SectionGroup(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'SectionGroup'
    id = Column(Integer, primary_key=True)
    DeptSectionCode = Column(CHAR(3))
    SectionHead = Column(CHAR(2))


class SHGroup(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'SHGroup'

    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    GroupID = Column(BIGINT, ForeignKey('Groups.GroupId'))
    DeptSectionCode = Column(CHAR(3), nullable=False)
    DateTimeActivated = Column(DATETIME, nullable=False, default=datetime.now())
    Description = Column(CHAR(30), nullable=False)
    DateTimeClosed = Column(DATETIME, nullable=True)
    StationCode = Column(CHAR(1), nullable=False)
    SHNo = Column(CHAR(1), nullable=False)
    LoginId = Column(CHAR(1), nullable=False)
    SectionType = Column(CHAR(20), nullable=False)


class syslogins(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'master..syslogins'
    id = Column(Integer, primary_key=True)
    name = Column(CHAR(30))
    password = Column(VARBINARY(128))


class GatePass(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'GatePass'
    GatePassNo = Column(CHAR(12), primary_key=True)
    GatePassKey = Column(DATETIME, nullable=False)
    AuthorityRef = Column(CHAR(20), nullable=True)
    TransportationMode = Column(CHAR(3), nullable=True)
    TransportNo = Column(CHAR(15), nullable=True)
    Destination = Column(CHAR(30), nullable=True)
    EscortName = Column(VARCHAR(30), nullable=True)
    Remarks = Column(VARCHAR(120), nullable=True)
    InitiatedBy = Column(CHAR(8), nullable=False)
    DateTimeApproved = Column(DATETIME, nullable=True)
    ApprovedBy = Column(CHAR(8), nullable=True)
    DateTimeGateOut = Column(DATETIME, nullable=True)
    GateOutBy = Column(CHAR(8), nullable=True)
    StationCode = Column(CHAR(1), nullable=False)
    Flag = Column(SMALLINT, nullable=False)


class AuditLedger(ConnectionsElement.get_csilms().App_Base):
    # __tablename__ = 'AuditLedger30MayBackup'
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
    NewStockSerial = Column(INT)
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


class CodeTable(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'CodeTable'
    id = Column(Integer, primary_key=True)
    ColumnName = Column(CHAR(30), nullable=False)
    CodeValue = Column(CHAR(10), nullable=False)
    Description = Column(CHAR(30), nullable=True)


class Users(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'Users'
    LoginId = Column(CHAR(8), primary_key=True)
    Id = Column(CHAR(8))
    Name = Column(CHAR(30))
    Rank = Column(CHAR(10))
    Department = Column(CHAR(8))
    StationCode = Column(CHAR(1))
    DateTimeLeft = Column(DATETIME)
    DateTimeJoined = Column(DATETIME)


class Item(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'Item'
    ItemCode = Column(CHAR(32), primary_key=True)
    SectionHead = Column(CHAR(2), nullable=False)
    ItemDesc = Column(CHAR(60), nullable=False)
    ItemDeno = Column(CHAR(3), nullable=False)
    CRPCategory = Column(CHAR(1), nullable=False)
    ABCCategory = Column(CHAR(1), nullable=False)


class SpecialDemand(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'SpecialDemand'
    id = Column(Integer, primary_key=True)
    CustomerCode = Column(CHAR(4), nullable=False)
    DemandNo = Column(CHAR(7), nullable=False)
    PriorityCode = Column(CHAR(1), nullable=False)
    RaisedOn = Column(CHAR(8), nullable=False)
    DateRaised = Column(DATETIME, nullable=False)
    ItemCode = Column(CHAR(32), nullable=False)
    Qty = Column(REAL(4), nullable=False)
    EqptItemCode = Column(CHAR(32), nullable=False)
    DTRB = Column(DATETIME, nullable=False)
    AuthorityType = Column(CHAR(3), nullable=False)
    PersonalNo = Column(CHAR(8), nullable=False)
    StationCode = Column(CHAR(1), nullable=False)
    StockDeliveryKey = Column(DATETIME, nullable=False)
    IssueDateTime = Column(DATETIME, nullable=False)
    StockReleaseSerial = Column(SMALLINT, nullable=False)
    DespatchItemKey = Column(DATETIME, nullable=False)
    DateAdded = Column(DATETIME, nullable=False)
    Srl = Column(CHAR(15), nullable=False)
    SHNo = Column(CHAR(3), nullable=False)
    ReturnVoucherNo = Column(CHAR(14), nullable=False)


class PackageOut(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'PackageOut'
    id = Column(Integer, primary_key=True)
    Marking = Column(VARCHAR(30), nullable=False)
    PackageType = Column(CHAR(2), nullable=False)
    WeightKgNet = Column(REAL(4), nullable=True)
    WeightKgTare = Column(REAL(4), nullable=True)
    WeightKgGross = Column(REAL(4), nullable=True)
    Dimensions = Column(CHAR(15), nullable=True)
    NoOfPackages = Column(SMALLINT, nullable=True)
    Remarks = Column(VARCHAR(120), nullable=True)
    DateTimeApproved = Column(DATETIME, nullable=True)
    DateTimeTakenOver = Column(DATETIME, nullable=True)
    TakenOverBy = Column(CHAR(8), nullable=True)
    GatePassKey = Column(DATETIME, nullable=True)
    ApprovedBy = Column(CHAR(8), nullable=True)
    PackageOutDocumentNo = Column(CHAR(30), nullable=True)
    PackageOutDocumentDate = Column(DATETIME, nullable=True)
    StationCode = Column(CHAR(1), nullable=False)


class NAC(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'NAC'
    id = Column(Integer, primary_key=True)
    CustomerCode = Column(CHAR(4), nullable=False)
    DemandNo = Column(CHAR(4), nullable=False)
    DateRequested = Column(DATETIME, nullable=False)
    QtyRequested = Column(REAL(4), nullable=False)
    QtyIssued = Column(REAL(4), nullable=True)
    DateTimeIssued = Column(DATETIME, nullable=True)
    ApprovedBy = Column(CHAR(8), nullable=True)
    Remarks = Column(VARCHAR(120), nullable=True)
    StationCode = Column(CHAR(1), nullable=False)
    FISNACNo = Column(CHAR(15), nullable=True)
    FISNACDate = Column(DATETIME, nullable=True)
    ENACFlag = Column(CHAR(1), nullable=True)
    ValidTill = Column(DATETIME, nullable=True)


class ItemLine(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ItemLine'
    id = Column(Integer, primary_key=True)
    ItemCode = Column(CHAR(32), nullable=False)
    # ItemDesc = Column(CHAR(60), nullable=False)
    QtyWarReserve = Column(REAL, nullable=False)
    StationCode = Column(CHAR(1), nullable=False)
    SHNo = Column(CHAR(3), nullable=False)
    QtyMSL = Column(REAL(4), nullable=False)
    QtyACL = Column(REAL(4), nullable=False)
    QtyUSL = Column(REAL(4), nullable=False)
    DaysLTProc = Column(SMALLINT, nullable=False)
    DateTimeAdded = Column(DATETIME, nullable=True)
    DateTimeClosed = Column(DATETIME, nullable=True)
    ItemLineSerial = Column(SMALLINT, nullable=False)


class StoreHouse(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'SH'
    SHNo = Column(CHAR(3), primary_key=True)
    SHDec = Column(CHAR(20), nullable=True)
    SHType = Column(CHAR(2), nullable=True)


class Survey(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'Survey'
    id = Column(Integer, primary_key=True)
    CustomerCode = Column(CHAR(4), nullable=False)
    SurveyNo = Column(CHAR(20), nullable=False)
    SurveyDate = Column(DATETIME, nullable=False)
    ItemCode = Column(CHAR(32), nullable=False)
    ConditionCode = Column(CHAR(3), nullable=False)
    Qty = Column(REAL, nullable=False)
    ReasonCode = Column(CHAR(1), nullable=False)
    IssueRef = Column(CHAR(60), nullable=True)
    EqptItemCode = Column(CHAR(32), nullable=True)
    DateSurveyed = Column(DATETIME, nullable=True)
    SurveyedBy = Column(CHAR(120), nullable=True)
    DateTimeApproved = Column(DATETIME, nullable=True)
    ApprovedBy = Column(CHAR(8), nullable=True)
    Remarks = Column(VARCHAR(120), nullable=True)
    NonINCATItemDesc = Column(VARCHAR(120), nullable=True)
    NonINCATItemDeno = Column(CHAR(120), nullable=True)
    StationCode = Column(CHAR(1), nullable=False)


class StoreReceiptLine(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'StoreReceiptLine'
    id = Column(Integer, primary_key=True)
    StoreReceiptNo = Column(CHAR(11), nullable=False)
    BatchNo = Column(CHAR(10), nullable=False)
    MIQPQty = Column(REAL, nullable=True)
    PackType = Column(CHAR(2), nullable=True)
    QtyReceived = Column(REAL, nullable=False)
    QtyOnCharge = Column(REAL, nullable=False)
    DateManufactured = Column(DATETIME, nullable=True)
    DateExpiry = Column(DATETIME, nullable=True)
    LocationMarking = Column(CHAR(18), nullable=True)
    StationCode = Column(CHAR(1), nullable=True)


class StoreReceipt(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'StoreReceipt'
    StoreReceiptNo = Column(CHAR(11), primary_key=True)
    ItemCode = Column(CHAR(32), nullable=False)
    SHNo = Column(CHAR(3), nullable=False)
    GateInDateTime = Column(DATETIME, nullable=True)
    DateTimeReceived = Column(DATETIME, nullable=False)
    StoreReceiptChoice = Column(CHAR(1), nullable=False)
    IndentNo = Column(CHAR(9), nullable=True)
    VendorCode = Column(CHAR(6), nullable=True)
    OrderDate = Column(DATETIME, nullable=True)
    OrderLineNo = Column(SMALLINT, nullable=True)
    SpecialDemandCustomerCode = Column(CHAR(4), nullable=True)
    DemandNo = Column(CHAR(7), nullable=True)
    CustomerCode = Column(CHAR(4), nullable=True)
    SurveyNo = Column(CHAR(20), nullable=True)
    Remarks = Column(VARCHAR(250), nullable=True)
    DateTimePrepared = Column(DATETIME, nullable=False)
    PreparedBy = Column(CHAR(8), nullable=False)
    DateTimeApproved = Column(DATETIME, nullable=True)
    ApprovedBy = Column(CHAR(8), nullable=True)
    Accessories = Column(VARCHAR(120), nullable=True)
    ConditionCode = Column(CHAR(3), nullable=True)
    StationCode = Column(CHAR(1), nullable=False)
    ProjectCode = Column(CHAR(15), nullable=True)
    CRACNo = Column(VARCHAR(255), nullable=True)
    CRACVerificationDate = Column(DATETIME, nullable=True)


class Customer(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'Customer'
    CustomerCode = Column(CHAR(4), primary_key=True)
    Name = Column(VARCHAR(31), unique=True)
    DateClosed = Column(DATETIME, nullable=True)
    StationCode = Column(CHAR(1), nullable=False)
    CustomerType = Column(CHAR(3), nullable=False)
    MotherDepot = Column(CHAR(8), nullable=False)
    Addressee = Column(CHAR(30), nullable=False)
    AddressLine1 = Column(CHAR(30), nullable=False)
    AddressLine2 = Column(CHAR(30), nullable=True)
    AddressLine3 = Column(VARCHAR(30), nullable=True)
    City = Column(CHAR(30), nullable=False)
    State = Column(CHAR(20), nullable=False)
    PINCode = Column(CHAR(7), nullable=True)
    # AllowanceAnnualRs = Column(REAL,nullable=False)
    # DateIntroduced = Column(CHAR(30),nullable=False)
    # DateClosed = Column(CHAR(30),nullable=False)
    # Remarks = Column(CHAR(30),nullable=False)
    # AdminAuthority = Column(CHAR(30),nullable=False)


class InternalGateIn(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'smms..InternalGateIn'

    id = Column(Integer, primary_key=True)
    IntGateInDateTime = Column(DATETIME, nullable=False)

    GatePassKey = Column(DATETIME, nullable=True)

    NoOfPackages = Column(Integer, nullable=False)

    PackageType = Column(CHAR(2), nullable=True)

    ReceivedFrom = Column(CHAR(8), nullable=False)

    TransportNo = Column(CHAR(15), nullable=True)

    TransporterName = Column(VARCHAR(30), nullable=True)

    DateTimeApproved = Column(DATETIME, nullable=True)

    ApprovedBy = Column(CHAR(8), nullable=True)

    StationCode = Column(CHAR(1), nullable=False)

    Remarks = Column(VARCHAR(120), nullable=True)

    CustomerCode = Column(CHAR(4), nullable=False)

    DeptCode = Column(CHAR(4), nullable=False)

    SubDeptCode = Column(CHAR(4), nullable=False)

    GateInType = Column(CHAR(1), nullable=False)

    OrderRef = Column(VARCHAR(120), nullable=True)

    OrderDate = Column(DATETIME, nullable=True)


class InternalReturn(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'smms..InternalReturn'

    id = Column(Integer, primary_key=True)
    ReturnId = Column(CHAR(12), nullable=False)

    MODemandNo = Column(CHAR(7), nullable=True)

    CustomerCode = Column(CHAR(4), nullable=False)

    StationCode = Column(CHAR(1), nullable=False)

    GatePassNo = Column(CHAR(12), nullable=True)

    ItemCode = Column(CHAR(32), nullable=False)

    NONMOItemCode = Column(CHAR(32), nullable=True)

    Qty = Column(REAL(4), nullable=False)

    InternalDemandNo = Column(CHAR(16), nullable=True)

    IntStockSerial = Column(SMALLINT, nullable=True)
    IDLineNo = Column(SMALLINT, nullable=True)

    ReturnTo = Column(CHAR(8), nullable=False)

    ReturnType = Column(CHAR(10), nullable=False)

    IntStoreReceiptNo = Column(CHAR(17), nullable=True)

    SerialNo = Column(SMALLINT, nullable=True)

    Remarks = Column(VARCHAR(255), nullable=True)

    ReturnReason = Column(CHAR(1), nullable=True)

    DateTimeAdded = Column(DATETIME, nullable=False)

    AddedBy = Column(CHAR(8), nullable=False)

    DateTimeApproved = Column(DATETIME, nullable=True)

    ApprovedBy = Column(CHAR(8), nullable=True)

    IntGatePassNo = Column(CHAR(12), nullable=True)

    IntGateInDateTime = Column(DATETIME, nullable=True)

    ClosingType = Column(CHAR(1), nullable=True)

    ClosedBy = Column(CHAR(8), nullable=True)

    DateTimeClosed = Column(DATETIME, nullable=True)

    DateTimeTakenOver = Column(DATETIME, nullable=True)

    TakenOverBy = Column(CHAR(8), nullable=True)


class InternalGatePass(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'smms..InternalGatePass'

    id = Column(Integer, primary_key=True)
    IntGatePassNo = Column(CHAR(12), nullable=False)

    IntGatePassKey = Column(DATETIME, nullable=False)

    AuthorityRef = Column(CHAR(20), nullable=True)

    TransportationMode = Column(CHAR(3), nullable=True)

    TransportNo = Column(CHAR(15), nullable=True)

    Destination = Column(CHAR(30), nullable=True)

    EscortName = Column(VARCHAR(30), nullable=True)

    Remarks = Column(VARCHAR(120), nullable=True)

    InitiatedBy = Column(CHAR(8), nullable=False)

    DateTimeApproved = Column(DATETIME, nullable=True)

    ApprovedBy = Column(CHAR(8), nullable=True)

    StationCode = Column(CHAR(1), nullable=False)

    CustomerCode = Column(CHAR(4), nullable=False)

    DeptCode = Column(CHAR(4), nullable=False)

    SubDeptCode = Column(CHAR(4), nullable=False)


class InternalStoreReceipt(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'smms..InternalStoreReceipt'

    id = Column(Integer, primary_key=True)
    IntStoreReceiptNo = Column(CHAR(17), nullable=False)

    ItemCode = Column(CHAR(32), nullable=False)

    SHNo = Column(CHAR(3), nullable=False)

    DateTimeReceived = Column(DATETIME, nullable=False)

    IntStoreReceiptChoice = Column(CHAR(1), nullable=False)

    CustomerCode = Column(CHAR(4), nullable=False)

    MODemandNo = Column(CHAR(7), nullable=True)

    InternalDemandNo = Column(CHAR(16), nullable=True)

    Remarks = Column(VARCHAR(250), nullable=True)

    DateTimePrepared = Column(DATETIME, nullable=False)

    PreparedBy = Column(CHAR(8), nullable=False)

    DateTimeApproved = Column(DATETIME, nullable=True)

    ApprovedBy = Column(CHAR(8), nullable=True)

    StationCode = Column(CHAR(1), nullable=False)

    MIQPQty = Column(REAL(4), nullable=True)

    PackType = Column(CHAR(2), nullable=True)

    QtyReceived = Column(REAL(4), nullable=True)

    QtyOnCharge = Column(REAL(4), nullable=True)

    DateManufactured = Column(DATETIME, nullable=True)

    DateExpiry = Column(DATETIME, nullable=True)

    LocationMarking = Column(CHAR(15), nullable=True)

    GatePassNo = Column(CHAR(12), nullable=True)

    IntGateInDateTime = Column(DATETIME, nullable=True)

    ReturnId = Column(CHAR(12), nullable=True)

    DeptCode = Column(CHAR(4), nullable=True)

    SubDeptCode = Column(CHAR(4), nullable=True)

    NONMOItemCode = Column(CHAR(32), nullable=True)

    RefitCustomerCode = Column(CHAR(4), nullable=True)

    ConditionCode = Column(CHAR(3), nullable=True)

    IDLineNo = Column(SMALLINT, nullable=True)

    IssueDateTime = Column(DATETIME, nullable=True)

    IssuedIntStockSerial = Column(INT, nullable=True)


class AuditCorrespondenceOfficers(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'AuditCorrespondenceOfficers'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    ObjectionId = Column(Integer, nullable=False)
    SentTo = Column(VARCHAR(8), nullable=False)
    SentBy = Column(VARCHAR(8), nullable=False)
    SentByRole = Column(CHAR(15), nullable=False)
    SentToRole = Column(CHAR(15), nullable=False)
    DateTimeSent = Column(DATETIME, nullable=False, default=datetime.now())
    DateTimeRead = Column(DATETIME, nullable=True)
    DateTimeClosed = Column(DATETIME, nullable=True)
    __table_args__ = (
        Index('uq_objection_officer', ObjectionId, SentTo, SentToRole, unique=True),
    )


class AuditObservation(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'AuditObservation'
    AuditObjectionType = Column(CHAR(4), nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    AuditObjectionSerial = Column(CHAR(21), nullable=False)
    ItemCode = Column(CHAR(32), nullable=True)
    Heading = Column(VARCHAR(120), nullable=False)
    TransactionRef = Column(VARCHAR(60), nullable=False)
    Controllerate = Column(CHAR(4), nullable=False)
    DateObjected = Column(DATETIME, nullable=False, default=datetime.now())
    ObjectedBy = Column(CHAR(8), nullable=False)
    DateTimeSettled = Column(DATETIME, nullable=True)
    DateTimeApproved = Column(DATETIME, nullable=True)
    ApprovedBy = Column(CHAR(8), nullable=True)
    StationCode = Column(CHAR(1), nullable=False)
    SettledBy = Column(CHAR(8), nullable=True)
    RecentReply = Column(VARCHAR(20), nullable=True)
    RecentReplyContent = Column(VARCHAR(30), nullable=True)
    RecentCorrespondence = Column(VARCHAR(20), nullable=True)


class AuditCorrespondence(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'AuditCorrespondence'
    id = Column(Integer, primary_key=True, autoincrement=True)
    AuditObjectionType = Column(CHAR(4), nullable=False)
    AuditObjectionSerial = Column(SMALLINT, nullable=False)
    DateTimeReplied = Column(DATETIME, nullable=False, default=datetime.now())
    AuditObjectionTextDateTime = Column(DATETIME, nullable=True)
    RLineNo = Column(INT, nullable=True)
    ForwardedBy = Column(CHAR(8), nullable=False)
    StationCode = Column(CHAR(1), nullable=False)
    RoleName = Column(CHAR(15), nullable=False)
    ToRole = Column(CHAR(15), nullable=False)
    Type = Column(CHAR(6), nullable=False)
    Remarks = Column(VARCHAR(255), nullable=True)


class AuditObservationText(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'AuditObservationText'
    id = Column(Integer, primary_key=True, autoincrement=True)
    AuditObjectionType = Column(CHAR(4), nullable=False)

    AuditObjectionId = Column(BIGINT, nullable=False)

    AuditObjectionTextDateTime = Column(DATETIME, nullable=True, default=datetime.now())

    Contents = Column(TEXT, nullable=False)

    StationCode = Column(CHAR(1), nullable=False)


class AuditResponse(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'AuditResponse'

    AuditObjectionType = Column(CHAR(4), nullable=False)
    ReplyId = Column(Integer, primary_key=True, autoincrement=True)
    AuditObjectionSerial = Column(Integer, ForeignKey('AuditObservation.id'))
    DateTimeReplied = Column(DATETIME, nullable=False)
    AuditObjectionTextDateTime = Column(DATETIME, nullable=True)
    AuditReplyText = Column(TEXT, nullable=False)
    RepliedBy = Column(CHAR(8), nullable=False)
    StationCode = Column(CHAR(1), nullable=False)
    IsApproved = Column(Boolean, nullable=False, default=False)


class Scheduling(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'Scheduling'

    id = Column(Integer, primary_key=True, autoincrement=True)
    SchedulingNo = Column(CHAR(13), unique=True, nullable=False)
    CustomerCode = Column(CHAR(10), nullable=True)
    SchedulingType = Column(VARCHAR(10), nullable=False)
    GeneratedBy = Column(CHAR(8), nullable=False)
    Roles = Column(CHAR(15), nullable=False)
    DateTimeGenerated = Column(DATETIME, nullable=False, default=datetime.now())
    DateFrom = Column(DATETIME, nullable=True)
    DateTo = Column(DATETIME, nullable=True)
    ApprovedBy = Column(CHAR(8), nullable=True)
    DateTimeApproved = Column(DATETIME, nullable=True)
    StationCode = Column(CHAR(1), nullable=False)


class SchedulingGLine(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'SchedulingGLine'

    SchedulingNo = Column(CHAR(13), nullable=False)

    GLineNo = Column(BIGINT, nullable=False, primary_key=True, autoincrement=True)

    StockTransferKey = Column(DATETIME, nullable=True)  # in case of transfer

    StockDeliveryKey = Column(DATETIME, nullable=True)  # in case of delivery , transfer and debit also

    ItemCode = Column(CHAR(32), nullable=True)  # for debit,

    StockSerial = Column(Integer, nullable=True)  # for debit

    Remarks = Column(TEXT, nullable=True)  #

    StationCode = Column(CHAR(1), nullable=False)

    VerifiedBy = Column(CHAR(8), nullable=True)

    DateTimeVerified = Column(DATETIME, nullable=True)

    QtyVerified = Column(REAL(4), nullable=True)

    IntGateInDateTime = Column(DATETIME, nullable=True)

    GatePassKey = Column(DATETIME, nullable=False)


class SchedulingSLine(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'SchedulingSLine'
    SchedulingNo = Column(CHAR(13), nullable=False)
    SLineNo = Column(Integer, primary_key=True, autoincrement=True)
    ItemCode = Column(CHAR(32), nullable=False)
    IndentNo = Column(CHAR(9), nullable=False)
    VendorCode = Column(CHAR(6), nullable=False)
    OrderDate = Column(DATETIME, nullable=False)
    OrderLineNo = Column(SMALLINT, nullable=False)
    CustomerCode = Column(CHAR(4), nullable=True)
    DemandNo = Column(CHAR(7), nullable=True)
    SurveyNo = Column(CHAR(20), nullable=True)
    StoreReceiptNo = Column(CHAR(11), nullable=False)
    QtyVerified = Column(REAL, nullable=True)
    DateTimeVerified = Column(DATETIME, nullable=True)
    Remarks = Column(VARCHAR(200), nullable=True)
    StationCode = Column(CHAR(1), nullable=False)
    VerifiedBy = Column(CHAR(8), nullable=True)
    StoreReceiptApprovedDate = Column(DATETIME, nullable=False)


class FOB_InternalDemand(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'FOB_InternalDemand'
    CustomerCode = Column(CHAR(4), nullable=False)
    InternalDemandNo = Column(CHAR(16), nullable=False, primary_key=True)
    StationCode = Column(CHAR(1), nullable=False)
    InternalDemandType = Column(CHAR(3), nullable=True)
    RaisedForCustomer = Column(CHAR(4), nullable=True)
    IWOSrl = Column(Integer, nullable=True)
    AuthorityType = Column(CHAR(3), nullable=True)
    RefitNo = Column(CHAR(5), nullable=True)
    RoleName = Column(CHAR(15), nullable=True)
    Remarks = Column(VARCHAR(255), nullable=True)
    RaisedBy = Column(CHAR(8), nullable=True)
    DateTimeRaised = Column(DATETIME, nullable=True)
    AuthorisedBy = Column(CHAR(8), nullable=True)
    DateTimeAuthorised = Column(DATETIME, nullable=True)
    ClosingCode = Column(CHAR(1), nullable=True)
    ClosedBy = Column(CHAR(8), nullable=True)
    DateTimeClosed = Column(DATETIME, nullable=True)
    Reason = Column(VARCHAR(255), nullable=True)
    DownloadDateTime = Column(DATETIME, nullable=True)
    DateTimeUpdated = Column(DATETIME, nullable=True)
    StatusFlag = Column(CHAR(2), nullable=True)
    MOStationCode = Column(CHAR(1), nullable=True)


class FOB_InternalDemandLine(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'FOB_InternalDemandLine'
    CustomerCode = Column(CHAR(4), nullable=False)
    InternalDemandNo = Column(CHAR(16), nullable=False, primary_key=True)
    IDLineNo = Column(Integer, nullable=False, primary_key=True)
    ItemCode = Column(CHAR(32), nullable=False)
    NONMOItemCode = Column(CHAR(32), nullable=True)
    Qty = Column(REAL, nullable=False)
    PriorityCode = Column(CHAR(1), nullable=False)
    EqptItemCode = Column(CHAR(32), nullable=True)
    AuthorityRef = Column(CHAR(20), nullable=True)
    AuthorityDate = Column(DATETIME, nullable=True)
    IDLActionType = Column(CHAR(3), nullable=False)
    StationCode = Column(CHAR(1), nullable=False)
    ActionBy = Column(CHAR(8), nullable=True)
    DateTimeAction = Column(DATETIME, nullable=True)
    ActionRemarks = Column(VARCHAR(120), nullable=True)
    ClosingCode = Column(CHAR(1), nullable=True)
    DateTimeClosed = Column(DATETIME, nullable=True)
    Reason = Column(VARCHAR(255), nullable=True)
    StatusFlag = Column(VARCHAR(2), nullable=True)
    MODemandNo = Column(CHAR(7), nullable=True)
    DownloadDateTime = Column(DATETIME, nullable=True)


class FOB_ErrorLog(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'FOB_ErrorLog'
    # ID = Column(Integer, primary_key=True)
    ErrorCode = Column(Integer, nullable=True)
    Remarks = Column(VARCHAR(255), nullable=True)
    StatusFlag = Column(CHAR(2), nullable=True)
    TableName = Column(CHAR(50), nullable=True)
    PrimaryKeyValue = Column(CHAR(100), nullable=True)
    DateTimeLogged = Column(DATETIME, primary_key=True)


class Demand(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'Demand'
    # ID = Column(Integer, primary_key=True)
    CustomerCode = Column(CHAR(4), nullable=False)
    DemandNo = Column(CHAR(7), nullable=False, primary_key=True, autoincrement=False)
    PriorityCode = Column(CHAR(1), nullable=False)
    DateRaised = Column(DATETIME, nullable=False)
    DateTimeRegistered = Column(DATETIME, nullable=False)
    ItemCode = Column(CHAR(32), nullable=False)
    Qty = Column(REAL(4), nullable=False)
    DTRB = Column(DATETIME, nullable=True)
    EqptItemCode = Column(CHAR(32), nullable=True)
    AuthorityType = Column(CHAR(3), nullable=False)
    AuthorityRef = Column(CHAR(20), nullable=True)
    AuthorityDate = Column(DATETIME, nullable=True)
    PersonalNo = Column(CHAR(8), nullable=False)
    ClosingCode = Column(CHAR(1), nullable=True)
    DateTimeClosed = Column(DATETIME, nullable=True)
    UrgencyRef = Column(CHAR(10), nullable=True)
    DateVetted = Column(DATETIME, nullable=True)
    RemarksVetting = Column(VARCHAR(120), nullable=True)
    VettedBy = Column(CHAR(8), nullable=True)
    StationCode = Column(CHAR(1), nullable=False)

    @validates('StationCode')
    def validate_station(self, key, value: str) -> str:
        if 1 != len(value.strip()) or value not in ['K', 'W', 'B', 'V', 'D', 'P']:
            raise DemandError(message='CONSTRAINT Demand_Stn_Cd CHECK', code=1010)
        return value

    @validates('Qty')
    def validate_qty(self, key, value: float) -> float:
        if value < 0:
            raise DemandError(message='CONSTRAINT Demand_Qty CHECK', code=1010)
        return value

    @validates('PersonalNo')
    def validate_personal_no(self, key, value: str) -> str:
        if value is None or 0 == len(value.strip()):
            raise DemandError(message='PersonalNo should be Not be NULL', code=68805)
        return value

    @validates('ClosingCode')
    def validate_closing_code(self, key, value: str) -> None:
        if value is not None:
            raise DemandError(message='ClosingCode should be NULL', code=68806)
        return None

    @validates('DateTimeClosed')
    def validate_date_time_closed(self, key, value: str) -> None:
        if value is not None:
            raise DemandError(message='DateTimeClosed should be NULL', code=68807)
        return None

    @validates('DateVetted')
    def validate_date_time_vetted(self, key, value: str) -> None:
        if value is not None:
            raise DemandError(message='DateVetted should be NULL', code=68808)
        return None

    @validates('VettedBy')
    def validate_vetted_by(self, key, value: str) -> None:
        if value is not None:
            raise DemandError(message='VettedBy should be NULL ', code=68809)
        return None

    @validates('AuthorityType')
    def validate_auth_type(self, key, value) -> str:
        if value is None or 3 != len(value.strip()):
            raise DemandError(message='Cannot insert the Demand as AuthorityType has blank character/s in it!',
                              code=68811)
        # if value == 'SVY' and
        return value

    @validates('PriorityCode')
    def validate_priority_code(self, key, value: str) -> str:
        if value is None or 1 != len(value.strip()) or value not in ["O", "U", "X", "Y", "Z", "S", "A", "D", "T", "P"]:
            raise DemandError(
                message='CONSTRAINT Demand_PriorityCode: Cannot insert the Demand as PriorityCode has CHECK',
                code=1010)
        return value

    @validates('DateRaised')
    def validate_date_raised(self, key, value: datetime) -> datetime:
        if value > datetime.now():
            raise DemandError(
                message='DateRaised is greater than today',
                code=68816)
        return value

    # @validates('DemandNo')
    # def validate_demand_no(self, key, value: str) -> str:
    #     from re import match
    #     regex_str:str = '[01289][0-9][A-Z]'
    #     if not match(regex_str,value):
    #         raise DemandError()
    #     if value is None or 1 != len(value.strip()) or value not in ["O", "U", "X", "Y", "Z", "S", "A", "D", "T", "P"]:
    #         raise DemandError(
    #             message='CONSTRAINT Demand_PriorityCode: Cannot insert the Demand as PriorityCode has CHECK',
    #             code='fk_check_priority_code')
    #     return value

    def __init__(self):
        """
        Warning:
                Avoid mass Inserts for Demand Table
                #TODO (function): write event to restrict all the mass inserts in table
        Raises:
                DemandError: if validation fails

        """
        ...


class Groups(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'Groups'
    GroupId = Column(Integer, primary_key=True, autoincrement=True)
    GroupNo = Column(VARCHAR(15), unique=True, nullable=False)
    GroupType = Column(CHAR(3), nullable=False)
    DateTimeActivated = Column(DATETIME, nullable=False, default=datetime.now())
    DateTimeClosed = Column(DATETIME, nullable=True)
    StationCode = Column(CHAR(1), nullable=False)


class GroupMembers(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'GroupMembers'

    __table_args__ = (Index('idx_ck1', 'LoginId', 'RoleName', 'GroupId'), Index('idx_ck2', 'LoginId', 'GroupId'),)
    GroupId = Column(Integer, ForeignKey('Groups.GroupId'))
    # GroupMembersId = Column(Integer, primary_key=True)
    GroupMembersId = Column(Integer, primary_key=True, autoincrement=True)
    LoginId = Column(CHAR(8), nullable=False)
    RoleName = Column(CHAR(15), nullable=False)


class Stock(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'Stock'
    id = Column(Integer, primary_key=True)
    ItemCode = Column(CHAR(32), nullable=False)
    StockSerial = Column(Integer, nullable=False)
    SHNo = Column(CHAR(3), nullable=False)
    BatchNo = Column(CHAR(10), nullable=False)
    ConditionCode = Column(CHAR(3), nullable=False)
    MIQPQty = Column(Numeric(10), nullable=False)
    PackType = Column(CHAR(2), nullable=False)
    LocationMarking = Column(CHAR(18), nullable=True)
    QtyGround = Column(CHAR(10), nullable=False)
    QtyLogical = Column(CHAR(10), nullable=False)
    StoreReceiptNo = Column(CHAR(11), nullable=False)
    StationCode = Column(CHAR(1), nullable=False)


class StockRelease(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'StockRelease'
    id = Column(Integer, primary_key=True)
    CustomerCode = Column(CHAR(4), nullable=False)
    DemandNo = Column(CHAR(7), nullable=False)
    IssueDateTime = Column(DATETIME, nullable=False)
    StockReleaseSerial = Column(SMALLINT, nullable=False)
    StockReleaseDateTime = Column(DATETIME, nullable=False)
    ItemCode = Column(CHAR(32), nullable=False)
    StockSerial = Column(Integer, nullable=False)
    Qty = Column(REAL, nullable=False)
    HandedOverBy = Column(CHAR(8), nullable=False)
    DateTimeTakenOver = Column(DATETIME, nullable=True)
    TakenOverBy = Column(CHAR(8), nullable=False)
    StationCode = Column(CHAR(1), nullable=False)


class GroupCustomers(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'GroupCustomers'
    GroupId = Column(Integer, ForeignKey('Groups.GroupId'))
    id = Column(Integer, primary_key=True, autoincrement=True)
    CustomerCode = Column(CHAR(4), nullable=False)
    CustomerType = Column(CHAR(3), nullable=True)


class StockDelivery(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'StockDelivery'
    id = Column(Integer, primary_key=True, )
    StockDeliveryKey = Column(DATETIME, nullable=False)
    CustomerCode = Column(CHAR(4), nullable=False)
    DemandNo = Column(CHAR(7), nullable=False)
    IssueDateTime = Column(DATETIME, nullable=False)
    StockReleaseSerial = Column(SMALLINT, nullable=False)
    QtyCarried = Column(REAL(4), nullable=False)
    GatePassKey = Column(DATETIME, nullable=True)
    Marking = Column(VARCHAR(30), nullable=True)
    DateTimeDelivered = Column(DATETIME, nullable=True)
    StationCode = Column(CHAR(1), nullable=False)


class StockDebit(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'StockDebit'
    id = Column(Integer, primary_key=True)
    ItemCode = Column(CHAR(32), nullable=False)
    StockSerial = Column(Integer, nullable=False)
    Qty = Column(REAL(4), nullable=False)
    IndentNo = Column(CHAR(9), nullable=True)
    VendorCode = Column(CHAR(6), nullable=True)
    OrderDate = Column(DATETIME, nullable=True)
    OrderLineNo = Column(SMALLINT, nullable=True)
    GatePassKey = Column(DATETIME, nullable=True)
    ApprovedBy = Column(CHAR(8), nullable=True)
    DateTimeApproved = Column(DATETIME, nullable=True)
    StationCode = Column(CHAR(1), nullable=False)
    RepairRequisitionNo = Column(CHAR(12), nullable=True)
    PreservationRequisitionNo = Column(CHAR(12), nullable=True)
    Marking = Column(CHAR(30), nullable=True)
    DebitedTo = Column(CHAR(3), nullable=True)
    DebitedBy = Column(CHAR(8), nullable=True)
    TakenOverBy = Column(CHAR(8), nullable=True)
    DateTimeDebited = Column(DATETIME, nullable=True)
    DateTimeTakenOver = Column(DATETIME, nullable=True)


class StockTransfer(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'StockTransfer'
    id = Column(Integer, primary_key=True)
    ItemCode = Column(CHAR(32), nullable=False)
    StockSerial = Column(Integer, nullable=False)
    ItemCodeNew = Column(CHAR(32), nullable=True)
    StockSerialNew = Column(Integer, nullable=True)
    SHNoNew = Column(CHAR(3), nullable=True)
    AuthorityRef = Column(VARCHAR(60), nullable=False)
    Qty = Column(REAL, nullable=False)
    Reason = Column(VARCHAR(120), nullable=False)
    HandedOverBy = Column(CHAR(8), nullable=True)
    DateTimeTakenOver = Column(DATETIME, nullable=True)
    TakenOverBy = Column(CHAR(8), nullable=True)
    LocationMarkingNew = Column(CHAR(15), nullable=True)
    LocationMarking = Column(CHAR(15), nullable=True)
    StockTransferNo = Column(CHAR(13), nullable=True)
    StockTransferKey = Column(DATETIME, nullable=True)
    GatePassKey = Column(DATETIME, nullable=True)
    ConditionCodeNew = Column(CHAR(3), nullable=True)
    StationCode = Column(CHAR(1), nullable=False)
    DateTimeTakenOver1 = Column(DATETIME, nullable=True)
    TakenOverBy1 = Column(CHAR(8), nullable=True)
    Marking = Column(VARCHAR(30), nullable=True)
    GateOutYN = Column(Integer, nullable=False)


class GateIn(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'GateIn'
    id = Column(Integer, primary_key=True)
    GateInDateTime = Column(DATETIME, nullable=False)
    TransportationDocumentNo = Column(CHAR(30), nullable=False)
    TransportationDocumentDate = Column(DATETIME, nullable=False)
    DeliveryDocumentRef = Column(VARCHAR(60), nullable=True)
    DeliveryDocumentDate = Column(DATETIME, nullable=True)
    Remarks = Column(VARCHAR(180), nullable=True)
    DateTimeApproved = Column(DATETIME, nullable=False)
    ApprovedBy = Column(CHAR(8), nullable=False)
    StationCode = Column(CHAR(1), nullable=False)
    ReferenceType = Column(SMALLINT, nullable=True)
    ReferenceKey = Column(VARCHAR(48), nullable=True)
    DirectDel = Column(SMALLINT, nullable=True)


class PackageIn(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'PackageIn'
    id = Column(Integer, primary_key=True)
    TransportationDocumentNo = Column(CHAR(30), nullable=False)
    TransportationDocumentDate = Column(DATETIME, nullable=False)
    LotNo = Column(SMALLINT, nullable=False)
    PackageType = Column(CHAR(2), nullable=False)
    Marking = Column(VARCHAR(30), nullable=True)
    Dimensions = Column(CHAR(15), nullable=True)
    Weightkg = Column(REAL, nullable=True)
    Condition = Column(CHAR(2), nullable=True)
    CollectionRef = Column(VARCHAR(60), nullable=True)
    DateTimeCollected = Column(DATETIME, nullable=True)
    UCName = Column(VARCHAR(31), nullable=True)
    Remarks = Column(VARCHAR(120), nullable=True)
    NoPackagesReceived = Column(SMALLINT, nullable=True)
    NoPackagesHandedOver = Column(SMALLINT, nullable=True)
    DateTimeHandedOver = Column(DATETIME, nullable=True)
    HandedOverBy = Column(CHAR(8), nullable=True)
    DateTimeTakenOver = Column(DATETIME, nullable=True)
    TakenOverBy = Column(CHAR(8), nullable=True)
    StationCode = Column(CHAR(1), nullable=False)
    TakenOverRemarks = Column(VARCHAR(120), nullable=True)
    GatePassKey = Column(DATETIME, nullable=True)


class AuditObjectionDocuments(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'AuditObservationDocuments'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    AuditObjectionID = Column(BIGINT, nullable=False)
    DocumentID = Column(BIGINT, nullable=False)
    IsApproved = Column(Boolean, nullable=False, default=False)


class AuditReplyDocuments(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'AuditResponseDocuments'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    AuditReplyID = Column(BIGINT, nullable=False)
    DocumentID = Column(BIGINT, nullable=False)


class AuditCorrespondenceDocuments(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'AuditCorrespondenceDocuments'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    AuditCorrespondenceID = Column(BIGINT, nullable=False)
    DocumentID = Column(BIGINT, nullable=False)


class Requisition(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'Requisition'
    __table_args__ = (Index('Requisition_540577983', 'RequisitionNo', 'StationCode'),)
    ID = Column(Integer, primary_key=True)
    RequisitionNo = Column(CHAR(12), nullable=False)
    RequisitionDate = Column(DATETIME, nullable=False)
    ItemCode = Column(CHAR(32), nullable=False)
    StockSerial = Column(INT, nullable=False)
    Qty = Column(REAL, nullable=False)
    WorkType = Column(CHAR(3), nullable=True)
    AgencyCode = Column(CHAR(3), nullable=True)
    AssessmentRemarks = Column(VARCHAR(120), nullable=True)
    DateTimeInitiated = Column(DATETIME, nullable=False)
    InitiatedBy = Column(CHAR(8), nullable=False)
    DateTimeApproved = Column(DATETIME, nullable=True)
    ApprovedBy = Column(CHAR(8), nullable=True)
    ProvCompletionDate = Column(DATETIME, nullable=True)
    EstimatedManDays = Column(SMALLINT, nullable=True)
    WorkOrderNo = Column(CHAR(12), nullable=True)
    CenterNo = Column(CHAR(10), nullable=True)
    LandingRef = Column(CHAR(13), nullable=True)
    LandedOn = Column(DATETIME, nullable=True)
    CompletedOn = Column(DATETIME, nullable=True)
    CompletionRemarks = Column(VARCHAR(120), nullable=True)
    IndentNo = Column(CHAR(9), nullable=True)
    StationCode = Column(CHAR(1), nullable=False)
    VendorCode = Column(CHAR(6), nullable=True)


class InternalDemand(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'smms..InternalDemand'

    id = Column(Integer, primary_key=True)
    ReturnId = Column(CHAR(12), nullable=False)




@event.listens_for(Demand, 'before_insert')
def receive_before_insert(mapper, connection, target):
    """
    only use select statement if global session object is being used
    """

    db_session = ConnectionsElement.get_csilms().app_session
    #TODO put checks required for Demand Insertion and put the errors in FOB_ErrorLog Table
    item_line_check = db_session.query(func.isnull(func.count(), 0).label("Count")).filter(
        ItemLine.ItemCode == target.ItemCode, ItemLine.DateTimeClosed.is_(None),
        ItemLine.StationCode == target.StationCode)
    demand_no_check = db_session.query(func.count().label("Count")).filter(Demand.DemandNo == target.DemandNo,
                                                                           Demand.StationCode == target.StationCode,
                                                                           Demand.CustomerCode == target.CustomerCode)
    code_table_check = db_session.query(func.count().label("Count")).filter(CodeTable.ColumnName == 'StationCode',
                                                                            CodeTable.CodeValue == target.StationCode)
    auth_type_check = db_session.query(func.count().label("Count")).filter(Item.ItemCode == target.ItemCode,
                                                                           or_(Item.CRPCategory == 'P',
                                                                               Item.CRPCategory == 'R'))
    code_table_auth_type_check = db_session.query(func.count().label("Count")).filter(
        CodeTable.ColumnName == 'AuthorityType', CodeTable.CodeValue == target.AuthorityType)
    customer_check = db_session.query(func.count().label("Count")).filter(Customer.CustomerCode == target.CustomerCode,
                                                                          Customer.DateClosed.is_(None))
    if demand_no_check.first().Count > 0:
        raise DemandError(message=f' Attempt to insert duplicate key {target.DemandNo}', code=2323)
        # raise DemandError(message=' Attempt to insert duplicate key', code='uq_Demand_10351477021')

    if target.DateRaised > target.DateTimeRegistered:
        raise DemandError(message='DateRaised is greater than DateTimeRegistered !', code=68817)
    if 0 == customer_check.first().Count:
        raise DemandError(message='Cannot insert Demand originated by a Closed Customer ! (ILMS  Trig-m)', code=68813)
    if 0 == code_table_auth_type_check.first().Count:
        raise DemandError(message='AuthorityType not found in CodeTable ILMS Trig', code=68812)

    if 0 == item_line_check.first().Count:
        raise DemandError(
            message='No Record in ItemLine Table for Inserted ItemCode & StationCode. Pse Introduce Item for your Station.',
            code=68803)

    if 0 == code_table_check.first().Count:
        raise DemandError(message='StationCode not found in CodeTable ILMS Triggers', code=68810)

    if target.AuthorityDate is None and target.AuthorityType == 'SVY':
        raise DemandError(message='AuthorityDate cannot be blank against Survey reference.', code=68824)

    if auth_type_check.first().Count > 1 and target.AuthorityType == 'REP':
        raise DemandError(
            message='Demanded AuthorityType "REP" is restricted for Permenant/Returnable nature of items.', code=57622)

    print(f'this is before insertion {type(mapper)} {type(connection)}  {type(target)} ')
