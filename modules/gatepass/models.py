import dataclasses


@dataclasses.dataclass
class FOB_InternalDemandArgs:
    FOBInternalDemandNo: str
    MoDemandNo: str
    IDLineNo: int
