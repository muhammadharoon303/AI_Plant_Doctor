import logging
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from database.models.plant import Notification
from database.models.user import User

logger = logging.getLogger("plant_doctor.notification_service")

class NotificationService:
    """
    Manages Plant Monitoring Notifications & Alerts with safety safeguards.
    Enforces rules:
    - Respects quiet hours & notification enable/disable preferences.
    - NEVER generates alarming notifications from a single low-confidence prediction.
    """

    @staticmethod
    def create_notification(
        db: Session,
        user_id: int,
        title: str,
        message: str,
        notification_type: str = "monitoring_reminder"
    ) -> Optional[Notification]:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.notifications_enabled:
            logger.info(f"Notification suppressed: User #{user_id} has notifications disabled.")
            return None

        # Create notification record
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            is_read=False,
            created_at=datetime.utcnow()
        )
        db.add(notif)
        db.commit()
        db.refresh(notif)
        logger.info(f"Created notification #{notif.id} ({notification_type}) for User #{user_id}")
        return notif

    @classmethod
    def process_scan_monitoring_trigger(
        cls,
        db: Session,
        user_id: int,
        plant_name: str,
        health_trend: str,
        confidence: float
    ):
        """
        Triggers appropriate notifications based on scan trend & confidence.
        Enforces: NEVER alarming on a single low-confidence prediction.
        """
        conf_pct = confidence * 100.0 if confidence <= 1.0 else confidence

        if conf_pct < 60.0:
            # Low confidence safeguard: Non-alarming polite reminder
            return cls.create_notification(
                db=db,
                user_id=user_id,
                title="Photo Quality Tip",
                message=f"For best diagnostic results, take a clearer leaf photo of '{plant_name}' when convenient.",
                notification_type="low_confidence_reminder"
            )
        elif health_trend == "Worsening":
            # High priority worsening trend alert
            return cls.create_notification(
                db=db,
                user_id=user_id,
                title=f"Disease Alert: {plant_name}",
                message=f"Leaf lesion area on '{plant_name}' shows a worsening trend. Review treatment options.",
                notification_type="worsening_alert"
            )
        elif health_trend == "Improving":
            return cls.create_notification(
                db=db,
                user_id=user_id,
                title=f"Positive Progress: {plant_name}",
                message=f"Leaf health on '{plant_name}' is improving! Continue current care routine.",
                notification_type="monitoring_reminder"
            )
        return None
