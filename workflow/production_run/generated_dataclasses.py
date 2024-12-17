"""
The dataclasses are automatically generated from the given yaml schema
"""
from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class WoodData:
    wood_id: str
    cw_wood_id: str
    cb_wood_id: str

@dataclass
class Start:
    cw: str
    cb: str

@dataclass
class FetchRapid:
    cw_rapid_needed: str
    cb_rapid_needed: str

@dataclass
class General:
    wood_data: WoodData

@dataclass
class Blue:
    request_part_data: str
    new_data_ready: str
    cw_ack: str
    cb_ack: str
    cw_req: str
    cb_req: str

@dataclass
class Red:
    fetch_rapid: FetchRapid

@dataclass
class FromProcessorToPlc:
    blue: Blue
    red: Red

@dataclass
class FromPlcToProcessor:
    blue: Blue
    red: Red

@dataclass
class Milling:
    cw: List[str]
    cb: List[str]

@dataclass
class Clamping:
    cw: str
    cb: str

@dataclass
class Plank:
    cw: str
    cb: str

@dataclass
class Done:
    cw: str
    cb: str

@dataclass
class Pickup:
    start: Start
    done: Done
    plank: Plank

@dataclass
class DropOff:
    cw: str
    cb: str

@dataclass
class StatusFlags:
    pickup: Pickup
    clamping: Clamping
    milling: Milling
    drop_off: DropOff
    process_end: List[str]

@dataclass
class Lector:
    wood_id: str
    scan_start: str
    scan_done: str

@dataclass
class Production:
    general: General
    from_processor_to_plc: FromProcessorToPlc
    from_plc_to_processor: FromPlcToProcessor
    lector: Lector

@dataclass
class RootSchema:
    production: Production
    status_flags: StatusFlags