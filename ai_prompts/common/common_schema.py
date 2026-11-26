from enum import Enum
from typing import Any, List, Optional
from pydantic import BaseModel, Field


class ResponseStatus(str, Enum):
    SUCCESS = "success"
    NEEDS_CLARIFICATION = "needs_clarification"
    OUT_OF_SCOPE = "out_of_scope"
    ERROR = "error"


class DetectedLanguage(str, Enum):
    SI = "si"
    TA = "ta"
    EN = "en"
    SINGLISH = "singlish"
    TANGLISH = "tanglish"


class ReplyLanguage(str, Enum):
    SI = "si"
    TA = "ta"
    EN = "en"


class DepartmentCode(str, Enum):
    DMT = "DMT"                  # Department of Motor Traffic
    IMMIGRATION = "IMMIGRATION"  # Dept. of Immigration & Emigration
    DS_GN = "DS_GN"              # Divisional Secretariat & Grama Niladhari
    UNKNOWN = "UNKNOWN"


class CommonAIResponse(BaseModel):
    status: ResponseStatus
    detected_language: DetectedLanguage
    reply_language: ReplyLanguage
    department: DepartmentCode
    pii_redacted: bool = Field(
        description="True if raw NIC, phone, or address was masked/omitted per zero-storage rule."
    )
    confidence: float = Field(ge=0.0, le=1.0)
    data: Optional[Any] = Field(
        default=None,
        description="Module-specific structured payload"
    )
    clarifying_questions: List[str] = Field(
        default_factory=list,
        description="Questions in reply_language if status is needs_clarification"
    )
    disclaimer: str = Field(
        description="Short reminder in reply_language to verify latest fees/hours with the official office."
    )