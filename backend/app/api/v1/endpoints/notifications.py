from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.notification import (
    NotificationResponse, NotificationListResponse,
    NotificationSettingsResponse, NotificationSettingsUpdate
)
from database.models.plant import Notification
from database.models.user import User

router = APIRouter()

@router.get("", response_model=NotificationListResponse)
def get_user_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve user notification alerts."""
    notifs = db.query(Notification).filter(Notification.user_id == current_user.id).order_by(Notification.created_at.desc()).all()
    unread_count = sum(1 for n in notifs if not n.is_read)
    return NotificationListResponse(
        unread_count=unread_count,
        total=len(notifs),
        items=notifs
    )

@router.put("/{notif_id}/read", response_model=NotificationResponse)
def mark_notification_read(
    notif_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a notification as read."""
    notif = db.query(Notification).filter(Notification.id == notif_id, Notification.user_id == current_user.id).first()
    if not notif:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    notif.is_read = True
    db.commit()
    db.refresh(notif)
    return notif

@router.get("/settings", response_model=NotificationSettingsResponse)
def get_notification_settings(
    current_user: User = Depends(get_current_user)
):
    """Get current user notification preferences (frequency, quiet hours)."""
    return NotificationSettingsResponse(
        notifications_enabled=current_user.notifications_enabled,
        reminder_frequency=current_user.reminder_frequency,
        quiet_hours_enabled=current_user.quiet_hours_enabled,
        quiet_hours_start=current_user.quiet_hours_start,
        quiet_hours_end=current_user.quiet_hours_end
    )

@router.put("/settings", response_model=NotificationSettingsResponse)
def update_notification_settings(
    settings_in: NotificationSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Configure notification preferences: enable/disable, frequency, quiet hours."""
    update_data = settings_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return NotificationSettingsResponse(
        notifications_enabled=current_user.notifications_enabled,
        reminder_frequency=current_user.reminder_frequency,
        quiet_hours_enabled=current_user.quiet_hours_enabled,
        quiet_hours_start=current_user.quiet_hours_start,
        quiet_hours_end=current_user.quiet_hours_end
    )
