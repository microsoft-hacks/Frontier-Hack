"""Typed API models for the Smart Industry machines scenario."""

from enum import Enum

from pydantic import BaseModel, Field


class MachineStatus(str, Enum):
    online = "online"
    alert = "alert"
    offline = "offline"


class AlertLevel(str, Enum):
    warn = "warn"
    critical = "critical"
    offline = "offline"


class Telemetry(BaseModel):
    temp: float = Field(..., description="Temperatura atual em °C.")
    vib: float = Field(..., description="Vibração atual em mm/s.")
    usage: float = Field(..., description="Taxa de utilização atual em %.")


class Params(BaseModel):
    mode: str = Field(..., description="Modo de operação: auto, paused ou off.")
    modeLabel: str = Field(..., description="Rótulo legível do modo de operação.")
    speed: float = Field(..., description="Velocidade configurada em %.")
    targetTemp: float = Field(..., description="Temperatura alvo em °C.")
    tempLimit: float = Field(..., description="Limite de temperatura em °C.")
    vibLimit: float = Field(..., description="Limite de vibração em mm/s.")
    cycleTime: float = Field(..., description="Tempo de ciclo em segundos.")


class Alert(BaseModel):
    metric: str | None = Field(None, description="Métrica em alerta (temp ou vib). Ausente em perda de comunicação.")
    kind: str | None = Field(None, description="Tipo do alerta quando não é de métrica, por exemplo communication_lost.")
    level: AlertLevel = Field(..., description="Severidade do alerta: warn, critical ou offline.")
    value: float | None = Field(None, description="Valor medido que violou o limite.")
    limit: float | None = Field(None, description="Limite excedido.")
    unit: str | None = Field(None, description="Unidade do valor e do limite.")
    initialSimulatedSilenceMinutes: float | None = Field(
        None, description="Minutos simulados sem comunicação no cadastro inicial (perda de comunicação)."
    )


class Machine(BaseModel):
    id: str = Field(..., description="ID da máquina, por exemplo CNC-003.")
    name: str
    type: str = Field(..., description="Tipo da máquina: cnc, robot, conveyor, forklift, injector, press ou welder.")
    typeLabel: str
    status: MachineStatus = Field(..., description="Status da máquina: online, alert ou offline.")
    statusLabel: str
    commLost: bool = Field(..., description="Verdadeiro quando a comunicação com a máquina foi perdida.")
    telemetryQuality: str = Field(..., description="Qualidade da telemetria, por exemplo simulated_reference.")
    telemetry: Telemetry
    params: Params
    reasons: list[str] = Field(..., description="Motivos legíveis do status atual; vazio quando online.")
    alerts: list[Alert] = Field(..., description="Alertas estruturados; vazio quando online.")


class Summary(BaseModel):
    total: int
    online: int
    alert: int
    offline: int
    machinesWithCriticalTemperature: int
    alertMachineIds: list[str]
    offlineMachineIds: list[str]


class PlantStatus(BaseModel):
    company: str
    plant: str
    timestamp: str
    units: dict[str, str] = Field(..., description="Unidade de cada campo, por exemplo telemetry.temp: °C.")
    summary: Summary


class MachineList(BaseModel):
    company: str
    plant: str
    timestamp: str
    count: int
    machines: list[Machine]


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Human-readable error message.")
