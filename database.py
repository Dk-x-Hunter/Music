

import logging
from typing import Any, Optional

from config import MONGO_URI

logger = logging.getLogger(__name__)

# MongoDB imports are optional.
try:
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError

    MONGO_AVAILABLE = True
except ImportError:
    MongoClient = None
    PyMongoError = Exception
    MONGO_AVAILABLE = False


class Database:
    """
    Optional MongoDB wrapper.

    MongoDB is NEVER required for music playback.
    If MongoDB is unavailable or fails, methods safely return
    fallback values instead of crashing the bot.
    """

    def __init__(self):
        self.client = None
        self.db = None
        self.enabled = False

        if not MONGO_URI:
            logger.info("MongoDB URI not configured. Running without MongoDB.")
            return

        if not MONGO_AVAILABLE:
            logger.warning(
                "pymongo is not installed. Running without MongoDB."
            )
            return

        try:
            self.client = MongoClient(
                MONGO_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000,
            )

            # Actually test the connection.
            self.client.admin.command("ping")

            self.db = self.client["music_bot"]
            self.enabled = True

            logger.info("MongoDB connected successfully.")

        except Exception as exc:
            self.enabled = False
            self.client = None
            self.db = None

            logger.warning(
                "MongoDB unavailable: %s. "
                "Bot will continue without MongoDB.",
                exc,
            )

    # --------------------------------------------------
    # Connection
    # --------------------------------------------------

    def is_available(self) -> bool:
        return self.enabled and self.db is not None

    def close(self) -> None:
        if self.client:
            try:
                self.client.close()
            except Exception:
                pass

        self.client = None
        self.db = None
        self.enabled = False

    # --------------------------------------------------
    # Generic helpers
    # --------------------------------------------------

    def _collection(self, name: str):
        if not self.is_available():
            return None

        try:
            return self.db[name]
        except Exception as exc:
            logger.warning("MongoDB collection error: %s", exc)
            return None

    # --------------------------------------------------
    # Settings
    # --------------------------------------------------

    def get_setting(
        self,
        chat_id: int,
        key: str,
        default: Any = None,
    ) -> Any:

        collection = self._collection("settings")

        if collection is None:
            return default

        try:
            document = collection.find_one(
                {"chat_id": chat_id},
                {key: 1},
            )

            if not document:
                return default

            return document.get(key, default)

        except Exception as exc:
            logger.warning("MongoDB get_setting failed: %s", exc)
            return default

    def set_setting(
        self,
        chat_id: int,
        key: str,
        value: Any,
    ) -> bool:

        collection = self._collection("settings")

        if collection is None:
            return False

        try:
            collection.update_one(
                {"chat_id": chat_id},
                {
                    "$set": {
                        key: value,
                    }
                },
                upsert=True,
            )

            return True

        except Exception as exc:
            logger.warning("MongoDB set_setting failed: %s", exc)
            return False

    # --------------------------------------------------
    # Sudo users
    # --------------------------------------------------

    def get_sudo_users(self) -> list[int]:

        collection = self._collection("bot_data")

        if collection is None:
            return []

        try:
            document = collection.find_one(
                {"type": "sudo_users"}
            )

            if not document:
                return []

            return [
                int(user_id)
                for user_id in document.get("users", [])
            ]

        except Exception as exc:
            logger.warning(
                "MongoDB get_sudo_users failed: %s",
                exc,
            )
            return []

    def save_sudo_users(self, users: list[int]) -> bool:

        collection = self._collection("bot_data")

        if collection is None:
            return False

        try:
            collection.update_one(
                {"type": "sudo_users"},
                {
                    "$set": {
                        "users": list(set(users)),
                    }
                },
                upsert=True,
            )

            return True

        except Exception as exc:
            logger.warning(
                "MongoDB save_sudo_users failed: %s",
                exc,
            )
            return False

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    def increment_stat(
        self,
        name: str,
        amount: int = 1,
    ) -> bool:

        collection = self._collection("statistics")

        if collection is None:
            return False

        try:
            collection.update_one(
                {"type": "global"},
                {
                    "$inc": {
                        name: amount,
                    }
                },
                upsert=True,
            )

            return True

        except Exception as exc:
            logger.warning(
                "MongoDB increment_stat failed: %s",
                exc,
            )
            return False

    def get_statistics(self) -> dict:

        collection = self._collection("statistics")

        if collection is None:
            return {}

        try:
            document = collection.find_one(
                {"type": "global"}
            )

            if not document:
                return {}

            document.pop("_id", None)
            document.pop("type", None)

            return document

        except Exception as exc:
            logger.warning(
                "MongoDB get_statistics failed: %s",
                exc,
            )
            return {}


# ------------------------------------------------------
# Global database object
# ------------------------------------------------------

db = Database()