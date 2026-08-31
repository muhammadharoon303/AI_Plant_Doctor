from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    type: str # scan_reminder, monitoring_reminder, worsening_alert, low_confidence_reminder
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class NotificationListResponse(BaseModel):
    unread_count: int
    total: int
    items: List[NotificationResponse]

class NotificationSettingsUpdate(BaseModel):
    notifications_enabled: Optional[bool] = None
    reminder_frequency: Optional[str] = None # daily, weekly, biweekly
    quiet_hours_enabled: Optional[bool] = None
    quiet_hours_start: Optional[str] = None
    quiet_hours_end: Optional[str] = None

class NotificationSettingsResponse(BaseModel):
    notifications_enabled: bool
    reminder_frequency: str
    quiet_hours_enabled: bool
    quiet_hours_start: str
    quiet_hours_end: str

    class Config:
        from_attributes = True
