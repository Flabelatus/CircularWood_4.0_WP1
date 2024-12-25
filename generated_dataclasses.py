"""
The dataclasses are automatically generated from the given yaml schema
"""
from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class Ports:
    command_port: int
    response_port: int

@dataclass
class Lector:
    ip: str
    ports: Ports

@dataclass
class Blue:
    request_part_data: str
    new_data_ready: str
    cw_ack: str
    cb_ack: str
    cw_req: str
    cb_req: str

@dataclass
class FetchRapid:
    cw_rapid_needed: str
    cb_rapid_needed: str

@dataclass
class Red:
    fetch_rapid: FetchRapid

@dataclass
class FromPlcToProcessor:
    blue: Blue
    red: Red

@dataclass
class Credentials:
    username: str
    password: str

@dataclass
class RedRobot:
    ip: str
    credentials: Credentials
    directory: str

@dataclass
class BlueRobot:
    ip: str
    credentials: Credentials
    directory: str

@dataclass
class RobotConfiguration:
    blue_robot: BlueRobot
    red_robot: RedRobot

@dataclass
class Dns:
    gateway_ip: str
    broadcast_ip: str

@dataclass
class WoodData:
    wood_id: str
    cw_wood_id: str
    cb_wood_id: str

@dataclass
class General:
    wood_data: WoodData

@dataclass
class FromProcessorToPlc:
    blue: Blue
    red: Red

@dataclass
class Production:
    general: General
    from_processor_to_plc: FromProcessorToPlc
    from_plc_to_processor: FromPlcToProcessor
    lector: Lector

@dataclass
class Development:
    base_url: str

@dataclass
class Environments:
    development: Development
    production: Production

@dataclass
class DatabaseService:
    environments: Environments
    credentials: Credentials

@dataclass
class Http:
    database_service: DatabaseService

@dataclass
class Service:
    title: str
    openapi_version: str
    openapi_url_prefix: str
    openapi_swagger_ui_path: str
    openapi_swagger_ui_url: str

@dataclass
class Documentation:
    endpoint: str
    service: Service

@dataclass
class Ftp:
    robot_configuration: RobotConfiguration

@dataclass
class Done:
    cw: str
    cb: str

@dataclass
class Database:
    server: str
    host: str
    port: str
    user: str
    password: str
    dbname: str
    sslmode: str
    timezone: str
    connect_timeout: int
    middleware: str
    uri: str
    track_modifications: int

@dataclass
class ProductionEnv:
    hosting_system: str
    vendor: str
    url: str
    logging: str

@dataclass
class DevelopmentEnv:
    url: str
    logging: str

@dataclass
class Modes:
    development_env: DevelopmentEnv
    production_env: ProductionEnv

@dataclass
class Robots:
    title: str
    controller_series: str
    model: str
    device: str

@dataclass
class Framing:
    opening: str
    end: str

@dataclass
class Commands:
    start_command: int
    stop_command: int
    framing: Framing

@dataclass
class ControlSystem:
    unit: str
    model: str

@dataclass
class AuxiliaryDevices:
    title: str
    unit: str
    model: str
    commands: Commands

@dataclass
class Equipment:
    robots: List[Robots]
    auxiliary_devices: List[AuxiliaryDevices]

@dataclass
class HardwareComponents:
    control_system: ControlSystem
    equipment: Equipment

@dataclass
class Ipv4:
    dns: Dns
    subnet_mask: str

@dataclass
class Ethernet:
    interface: str
    ipv4: Ipv4

@dataclass
class Settings:
    dhcp: str
    ethernet: Ethernet

@dataclass
class NetworkConfiguration:
    type: str
    settings: Settings

@dataclass
class Redis:
    host: str
    port: int
    expiration_time: int

@dataclass
class LabelPrinter:
    ip: str
    ports: Ports

@dataclass
class Connections:
    lector: Lector
    label_printer: LabelPrinter

@dataclass
class Tcp:
    connections: Connections

@dataclass
class Start:
    cw: str
    cb: str

@dataclass
class Plank:
    cw: str
    cb: str

@dataclass
class Pickup:
    start: Start
    done: Done
    plank: Plank

@dataclass
class Milling:
    cw: List[str]
    cb: List[str]

@dataclass
class Clamping:
    cw: str
    cb: str

@dataclass
class Cors:
    access_control_allow_credentials: int
    allow_headers: List[str]
    allowed_origins: List[str]

@dataclass
class Profinet:
    section: str

@dataclass
class BrokerInfo:
    hostname: str
    port: int

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
class Topics:
    production: Production
    status_flags: StatusFlags

@dataclass
class Mqtt:
    broker_info: BrokerInfo
    topics: Topics

@dataclass
class CommunicationProtocols:
    ftp: Ftp
    tcp: Tcp
    mqtt: Mqtt
    http: Http
    profinet: Profinet

@dataclass
class ProductionRun:
    title: str
    network_configuration: NetworkConfiguration
    hardware_components: HardwareComponents
    communication_protocols: CommunicationProtocols

@dataclass
class Clients:
    name: str

@dataclass
class ApiHttpClient:
    clients: List[Clients]

@dataclass
class WorkflowManager:
    api_http_client: ApiHttpClient
    production_run: ProductionRun

@dataclass
class RateLimiting:
    requests_per_minute: int
    burst: int

@dataclass
class Jwt:
    secret: str
    issuer: str
    audience: str
    expiration_time: int

@dataclass
class CookieSettings:
    same_site: str
    token_location: str
    cookie_secure: int
    csrf_in_cookies: int
    http_only: int

@dataclass
class Security:
    cookie_settings: CookieSettings
    jwt: Jwt

@dataclass
class FrontendApps:
    url: List[str]

@dataclass
class Environment:
    selected_mode: str
    modes: Modes

@dataclass
class Server:
    port: int
    host: str
    environment: Environment

@dataclass
class Idemat:
    path: str

@dataclass
class Logging:
    format: str
    output: str

@dataclass
class Apis:
    url: List[str]
    api_keys: List[Any]

@dataclass
class Configs:
    secret_key: str
    propogate_exceptions: int
    rate_limiting: RateLimiting
    cors: Cors
    max_content_length: int

@dataclass
class Tools:
    idemat: Idemat

@dataclass
class External:
    apis: Apis
    tools: Tools
    frontend_apps: FrontendApps

@dataclass
class Cache:
    redis: Redis

@dataclass
class DataServiceApi:
    title: str
    version: str
    description: str
    developers: List[str]
    contact: List[str]
    external: External
    server: Server
    configs: Configs
    database: Database
    documentation: Documentation
    security: Security
    logging: Logging
    cache: Cache

@dataclass
class RootSchema:
    data_service_api: DataServiceApi
    workflow_manager: WorkflowManager