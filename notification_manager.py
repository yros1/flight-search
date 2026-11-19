import logging
import os

from twilio.rest import Client

from flight_data import FlightData

logger = logging.getLogger(__name__)


class NotificationManager:
    """Send Twilio WhatsApp notifications containing flight deal details."""

    def __init__(self):
        """Initialize the Twilio client and flight formatting helper."""
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

        if not account_sid:
            logger.error("TWILIO_ACCOUNT_SID environment variable is not set")
            raise RuntimeError("Environment variable TWILIO_ACCOUNT_SID is not set")
        if not auth_token:
            logger.error("TWILIO_AUTH_TOKEN environment variable is not set")
            raise RuntimeError("Environment variable TWILIO_AUTH_TOKEN is not set")

        self.__client = Client(account_sid, auth_token)
        self.flight_data = FlightData()

    def send_notification(self, flight):
        """Send a WhatsApp flight deal notification."""
        text = self.flight_data.format(flight=flight)

        from_number = os.environ.get("TWILIO_WHATSAPP_FROM")
        to_number = os.environ.get("TWILIO_WHATSAPP_TO")

        if not from_number:
            logger.error("TWILIO_WHATSAPP_FROM environment variable is not set")
            raise RuntimeError(
                "Environment variable TWILIO_WHATSAPP_FROM is not set"
            )
        if not to_number:
            logger.error("TWILIO_WHATSAPP_TO environment variable is not set")
            raise RuntimeError(
                "Environment variable TWILIO_WHATSAPP_TO is not set"
            )

        logger.info("Sending WhatsApp flight notification")
        message = self.__client.messages.create(
            from_=from_number,
            body=text,
            to=to_number,
        )

        logger.info(
            "Notification sent: SID=%s, status=%s",
            message.sid,
            message.status,
        )
