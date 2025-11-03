import datetime
from sqlalchemy import Column, Integer, CHAR, DATETIME, VARCHAR, REAL, DECIMAL, VARBINARY, SMALLINT, BIGINT, INT, Index, \
    TEXT, ForeignKey, Boolean, Numeric, FLOAT
from fob_sybase.Connections import ConnectionsElement


class IVMS_SHGroup(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..SHGroup'

    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    GroupID = Column(BIGINT, ForeignKey('Groups.GroupId'))
    DeptSectionCode = Column(CHAR(3), nullable=False)
    DateTimeActivated = Column(DATETIME, nullable=False, default=datetime.datetime.now())
    Description = Column(CHAR(30), nullable=False)
    DateTimeClosed = Column(DATETIME, nullable=True)
    StationCode = Column(CHAR(1), nullable=False)
    SHNo = Column(CHAR(1), nullable=False)
    LoginId = Column(CHAR(1), nullable=False)
    SectionType = Column(CHAR(20), nullable=False)


class IVMS_AuditLedger(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..AuditLedger'
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
    # LedgerNo = Column(CHAR(10))
    # Folio = Column(CHAR(6))
    TransactionReference = Column(VARCHAR(60))
    # # CRPCategory = Column(CHAR(1))
    # BatchNo = Column(CHAR(10))
    # TransactionQtyLogical = Column(REAL(4))
    # TransactionQtyGround = Column(REAL(4))
    SHNoNew = Column(CHAR(3))
    # ConditionCode = Column(CHAR(3))
    QtyBalance = Column(REAL(4))
    TransactionDateTime = Column(DATETIME, nullable=False)


class IVMS_AuditCorrespondenceOfficers(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..AuditCorrespondenceOfficers'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    ObjectionId = Column(Integer, nullable=False)
    SentTo = Column(VARCHAR(8), nullable=False)
    SentBy = Column(VARCHAR(8), nullable=False)
    SentByRole = Column(CHAR(15), nullable=False)
    SentToRole = Column(CHAR(15), nullable=False)
    DateTimeSent = Column(DATETIME, nullable=False, default=datetime.datetime.now())
    DateTimeRead = Column(DATETIME, nullable=True)
    DateTimeClosed = Column(DATETIME, nullable=True)
    __table_args__ = (
        Index('uq_objection_officer', ObjectionId, SentTo, SentToRole, unique=True),
    )


class IVMS_AuditObservation(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..AuditObservation'
    AuditObjectionType = Column(CHAR(4), nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    AuditObjectionSerial = Column(CHAR(21), nullable=False)
    ItemCode = Column(CHAR(32), nullable=True)
    Heading = Column(VARCHAR(120), nullable=False)
    TransactionRef = Column(VARCHAR(60), nullable=False)
    Controllerate = Column(CHAR(4), nullable=False)
    DateObjected = Column(DATETIME, nullable=False, default=datetime.datetime.now())
    ObjectedBy = Column(CHAR(8), nullable=False)
    DateTimeSettled = Column(DATETIME, nullable=True)
    DateTimeApproved = Column(DATETIME, nullable=True)
    ApprovedBy = Column(CHAR(8), nullable=True)
    StationCode = Column(CHAR(1), nullable=False)
    SettledBy = Column(CHAR(8), nullable=True)
    RecentReply = Column(VARCHAR(20), nullable=True)
    RecentReplyContent = Column(VARCHAR(30), nullable=True)
    RecentCorrespondence = Column(VARCHAR(20), nullable=True)


class IVMS_AuditCorrespondence(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..AuditCorrespondence'
    id = Column(Integer, primary_key=True, autoincrement=True)
    AuditObjectionType = Column(CHAR(4), nullable=False)
    AuditObjectionSerial = Column(SMALLINT, nullable=False)
    DateTimeReplied = Column(DATETIME, nullable=False, default=datetime.datetime.now())
    AuditObjectionTextDateTime = Column(DATETIME, nullable=True)
    RLineNo = Column(INT, nullable=True)
    ForwardedBy = Column(CHAR(8), nullable=False)
    StationCode = Column(CHAR(1), nullable=False)
    RoleName = Column(CHAR(15), nullable=False)
    ToRole = Column(CHAR(15), nullable=False)
    Type = Column(CHAR(6), nullable=False)
    Remarks = Column(VARCHAR(255), nullable=True)


class IVMS_AuditObservationText(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..AuditObservationText'
    id = Column(Integer, primary_key=True, autoincrement=True)
    AuditObjectionType = Column(CHAR(4), nullable=False)

    AuditObjectionId = Column(BIGINT, nullable=False)

    AuditObjectionTextDateTime = Column(DATETIME, nullable=True, default=datetime.datetime.now())

    Contents = Column(TEXT, nullable=False)

    StationCode = Column(CHAR(1), nullable=False)


class IVMS_AuditResponse(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..AuditResponse'

    AuditObjectionType = Column(CHAR(4), nullable=False)
    ReplyId = Column(Integer, primary_key=True, autoincrement=True)
    AuditObjectionSerial = Column(Integer, ForeignKey('AuditObservation.id'))
    DateTimeReplied = Column(DATETIME, nullable=False)
    AuditObjectionTextDateTime = Column(DATETIME, nullable=True)
    AuditReplyText = Column(TEXT, nullable=False)
    RepliedBy = Column(CHAR(8), nullable=False)
    StationCode = Column(CHAR(1), nullable=False)
    IsApproved = Column(Boolean, nullable=False, default=False)


class IVMS_Scheduling(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..Scheduling'

    id = Column(Integer, primary_key=True, autoincrement=True)
    SchedulingNo = Column(CHAR(13), unique=True, nullable=False)
    CustomerCode = Column(CHAR(10), nullable=True)
    SchedulingType = Column(VARCHAR(10), nullable=False)
    GeneratedBy = Column(CHAR(8), nullable=False)
    Roles = Column(CHAR(15), nullable=False)
    DateTimeGenerated = Column(DATETIME, nullable=False, default=datetime.datetime.now())
    DateFrom = Column(DATETIME, nullable=True)
    DateTo = Column(DATETIME, nullable=True)
    ApprovedBy = Column(CHAR(8), nullable=True)
    DateTimeApproved = Column(DATETIME, nullable=True)
    StationCode = Column(CHAR(1), nullable=False)


# @event.listens_for(Scheduling, 'before_insert')
# def receive_before_insert(mapper, connection, target):
#     if target.SchedulingNo[5] is not 'R':
#         return
#     from audit_application.helpers.utils imports get_n_digit_number
#     from audit_application.services.sybase_db imports get_running_scheduling_index
#     s_part = target.SchedulingNo[:-4]
#     # s_index = target.SchedulingNo[-4:]
#     partial_index: str = f'{get_running_scheduling_index(s_part, target.SchedulingType, "R", __csilms.csilms_session)}'
#     r_index = get_n_digit_number(partial_index, 4)
#     target.SchedulingNo = s_part+r_index
#     print(f'this is before insertion {type(mapper)} {type(connection)}  {type(target)} {target.SchedulingNo}')


class IVMS_SchedulingGLine(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..SchedulingGLine'

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


class IVMS_SchedulingSLine(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..SchedulingSLine'
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


class IVMS_Groups(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..Groups'
    GroupId = Column(Integer, primary_key=True, autoincrement=True)
    GroupNo = Column(VARCHAR(15), unique=True, nullable=False)
    GroupType = Column(CHAR(3), nullable=False)
    DateTimeActivated = Column(DATETIME, nullable=False, default=datetime.datetime.now())
    DateTimeClosed = Column(DATETIME, nullable=True)
    StationCode = Column(CHAR(1), nullable=False)


class IVMS_GroupMembers(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..GroupMembers'

    __table_args__ = (Index('idx_ck1', 'LoginId', 'RoleName', 'GroupId'), Index('idx_ck2', 'LoginId', 'GroupId'),)
    GroupId = Column(Integer, ForeignKey('Groups.GroupId'))
    # GroupMembersId = Column(Integer, primary_key=True)
    GroupMembersId = Column(Integer, primary_key=True, autoincrement=True)
    LoginId = Column(CHAR(8), nullable=False)
    RoleName = Column(CHAR(15), nullable=False)


class IVMS_GroupCustomers(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..GroupCustomers'
    GroupId = Column(Integer, ForeignKey('Groups.GroupId'))
    id = Column(Integer, primary_key=True, autoincrement=True)
    CustomerCode = Column(CHAR(4), nullable=False)
    CustomerType = Column(CHAR(3), nullable=True)


class IVMS_AuditObjectionDocuments(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..AuditObservationDocuments'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    AuditObjectionID = Column(BIGINT, nullable=False)
    DocumentID = Column(BIGINT, nullable=False)
    IsApproved = Column(Boolean, nullable=False, default=False)


class IVMS_AuditReplyDocuments(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..AuditResponseDocuments'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    AuditReplyID = Column(BIGINT, nullable=False)
    DocumentID = Column(BIGINT, nullable=False)


class IVMS_AuditCorrespondenceDocuments(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..AuditCorrespondenceDocuments'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    AuditCorrespondenceID = Column(BIGINT, nullable=False)
    DocumentID = Column(BIGINT, nullable=False)


class IVMS_StoreReceipt(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..StoreReceipt'
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
    # CRACNo = Column(VARCHAR(255), nullable=True)
    # CRACVerificationDate = Column(DATETIME, nullable=True)


class IVMS_StoreReceiptLine(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..StoreReceiptLine'
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


class IVMS_Stock(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..Stock'
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


class IVMS_Discrepancy(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..Discrepancy'
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


class IVMS_GatePass(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..GatePass'
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


class IVMS_Customer(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..Customer'
    CustomerCode = Column(CHAR(4), primary_key=True)
    Name = Column(VARCHAR(31), unique=True)
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


class IVMS_UserRole(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..UserRole'
    id = Column(Integer, primary_key=True)
    LoginId = Column(CHAR(8))
    RoleName = Column(CHAR(15))
    StationCode = Column(CHAR(1))
    DateTimeClosed = Column(DATETIME)


class IVMS_Users(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..Users'
    LoginId = Column(CHAR(8), primary_key=True)
    Id = Column(CHAR(8))
    Name = Column(CHAR(30))
    Rank = Column(CHAR(10))
    Department = Column(CHAR(8))
    StationCode = Column(CHAR(1))
    DateTimeLeft = Column(DATETIME)
    DateTimeJoined = Column(DATETIME)


class IVMS_GateIn(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..GateIn'
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


# class IVMS_StoreReceipt(ConnectionsElement.get_csilms().App_Base):
#     __tablename__ = 'ivms..StoreReceipt'
#     StoreReceiptNo = Column(CHAR(11), primary_key=True)
#     ItemCode = Column(CHAR(32), nullable=False)
#     SHNo = Column(CHAR(3), nullable=False)
#     GateInDateTime = Column(DATETIME, nullable=True)
#     DateTimeReceived = Column(DATETIME, nullable=False)
#     StoreReceiptChoice = Column(CHAR(1), nullable=False)
#     IndentNo = Column(CHAR(9), nullable=True)
#     VendorCode = Column(CHAR(6), nullable=True)
#     OrderDate = Column(DATETIME, nullable=True)
#     OrderLineNo = Column(SMALLINT, nullable=True)
#     SpecialDemandCustomerCode = Column(CHAR(4), nullable=True)
#     DemandNo = Column(CHAR(7), nullable=True)
#     CustomerCode = Column(CHAR(4), nullable=True)
#     SurveyNo = Column(CHAR(20), nullable=True)
#     Remarks = Column(VARCHAR(250), nullable=True)
#     DateTimePrepared = Column(DATETIME, nullable=False)
#     PreparedBy = Column(CHAR(8), nullable=False)
#     DateTimeApproved = Column(DATETIME, nullable=True)
#     ApprovedBy = Column(CHAR(8), nullable=True)
#     Accessories = Column(VARCHAR(120), nullable=True)
#     ConditionCode = Column(CHAR(3), nullable=True)
#     StationCode = Column(CHAR(1), nullable=False)
#     ProjectCode = Column(CHAR(15), nullable=True)
#     CRACNo = Column(VARCHAR(255), nullable=True)
#     CRACVerificationDate = Column(DATETIME, nullable=True)


class IVMS_PackageIn(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..PackageIn'
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


class IVMS_Demand(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..Demand'
    ID = Column(Integer, primary_key=True)
    CustomerCode = Column(CHAR(4), nullable=False)
    DemandNo = Column(CHAR(7), nullable=False)
    PriorityCode = Column(CHAR(1), nullable=False)
    DateRaised = Column(DATETIME, nullable=False)
    DateTimeRegistered = Column(DATETIME, nullable=False)
    ItemCode = Column(CHAR(32), nullable=False)
    Qty = Column(REAL(4), nullable=False)
    DTRB = Column(DATETIME, nullable=False)
    EqptItemCode = Column(CHAR(32), nullable=False)
    AuthorityType = Column(CHAR(3), nullable=False)
    AuthorityRef = Column(CHAR(20), nullable=False)
    AuthorityDate = Column(DATETIME, nullable=False)
    PersonalNo = Column(CHAR(8), nullable=False)
    ClosingCode = Column(CHAR(1), nullable=False)
    DateTimeClosed = Column(DATETIME, nullable=False)
    UrgencyRef = Column(CHAR(10), nullable=False)
    DateVetted = Column(DATETIME, nullable=False)
    RemarksVetting = Column(VARCHAR(120), nullable=False)
    VettedBy = Column(CHAR(8), nullable=False)
    StationCode = Column(CHAR(1), nullable=False)


class IVMS_OrderLine(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..OrderLine'
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


class IVMS_StockTransfer(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..StockTransfer'
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


class IVMS_PackageOut(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..PackageOut'
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


class IVMS_StockDelivery(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..StockDelivery'
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


class IVMS_CodeTable(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..CodeTable'
    id = Column(Integer, primary_key=True)
    ColumnName = Column(CHAR(30), nullable=False)
    CodeValue = Column(CHAR(10), nullable=False)
    Description = Column(CHAR(30), nullable=True)


class IVMS_Vendor(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..Vendor'
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


class IVMS_StockRelease(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..StockRelease'
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


class IVMS_Issue(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..Issue'
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


class IVMS_Conversion(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..Conversion'
    StationCode = Column(CHAR(1), nullable=False)
    ReceivedFrom = Column(VARCHAR(6), nullable=True)
    PreparedBy = Column(CHAR(8), nullable=True)
    IssuedTo = Column(VARCHAR(6), nullable=True)
    DateTimePrepared = Column(DATETIME, nullable=True)
    DateTimeApproved = Column(DATETIME, nullable=True)
    ConversionNo = Column(CHAR(11), nullable=False, primary_key=True)
    ConversionDate = Column(DATETIME, nullable=False)
    ApprovedBy = Column(CHAR(8), nullable=True)


class IVMS_ConversionLine(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..ConversionLine'
    ConversionNo = Column(CHAR(11), nullable=False, primary_key=True)
    IssuedItemCode = Column(CHAR(32), nullable=False)
    IssueQty = Column(DECIMAL, nullable=False)
    ProcessCode = Column(CHAR(1), nullable=False)
    ReceivedItemCode = Column(CHAR(32), nullable=False)
    ReceiptQty = Column(DECIMAL, nullable=False)
    ReceivedItemPackType = Column(CHAR(2), nullable=False)
    ReceivedItemStSer = Column(INT, nullable=True)
    WastagePCT = Column(FLOAT, nullable=False)
    WastageQty = Column(DECIMAL, nullable=False)
    ByProductItemCode = Column(CHAR(32), nullable=True)
    ByProductQty = Column(DECIMAL, nullable=True)
    ByProductPackType = Column(CHAR(2), nullable=True)
    ByProductStSer = Column(INT, nullable=True)
    StockSerial = Column(INT, nullable=False)
    StationCode = Column(CHAR(1), nullable=True)


class IVMS_Wastage(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..Wastage'
    WastageNo = Column(CHAR(11), primary_key=True)
    WastageDate = Column(DATETIME, nullable=False)
    DateFrom = Column(DATETIME, nullable=False)
    DateTill = Column(DATETIME, nullable=False)
    PreparedBy = Column(CHAR(8), nullable=False)
    DateTimePrepared = Column(DATETIME, nullable=False)
    ApprovedBy = Column(CHAR(8), nullable=True)
    DateTimeApproved = Column(DATETIME, nullable=True)
    Remarks = Column(VARCHAR(120), nullable=True)
    StationCode = Column(CHAR(1), nullable=False)


class IVMS_WastageLine(ConnectionsElement.get_csilms().App_Base):
    __tablename__ = 'ivms..WastageLine'
    WastageNo = Column(CHAR(11), nullable=False, primary_key=True)
    ItemCode = Column(CHAR(32), nullable=False)
    WastagePct = Column(DECIMAL, nullable=False)
    VetQty = Column(DECIMAL, nullable=False)
    WastageQty = Column(DECIMAL, nullable=True)
    TotQtyIssued = Column(DECIMAL, nullable=False)
    StockSerial = Column(INT, nullable=True)
    StationCode = Column(CHAR(1), nullable=True)

#
# class IVMS_Discrepancy(ConnectionsElement.get_csilms().App_Base):
#     __tablename__ = 'ivms..Discrepancy'
#     id = Column(Integer, primary_key=True)
#     StoreReceiptNo = Column(CHAR(11), nullable=False)
#     BatchNo = Column(CHAR(10), nullable=False)
#     SerialNo = Column(SMALLINT, nullable=False)
#     Qty = Column(REAL, nullable=False)
#     DiscrepancyType = Column(CHAR(1), nullable=False)
#     DiscrepancyRemarks = Column(VARCHAR(120), nullable=True)
#     SettlementRemarks = Column(VARCHAR(120), nullable=True)
#     DateSettled = Column(DATETIME, nullable=True)
#     DateTimeClosed = Column(DATETIME, nullable=True)
#     ClosedBy = Column(CHAR(8), nullable=True)
#     DateTimeInitiated = Column(DATETIME, nullable=True)
#     InitiatedBy = Column(CHAR(8), nullable=True)
