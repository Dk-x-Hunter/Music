

from dataclasses import dataclass, field
from typing import Optional, Any
import asyncio


@dataclass
class Song:
    title: str
    url: str
    stream_url: Optional[str] = None
    duration: int = 0
    requested_by: Optional[int] = None
    thumbnail: Optional[str] = None


@dataclass
class ChatState:
    chat_id: int

    # Music queue
    queue: list[Song] = field(default_factory=list)

    # Currently playing song
    current: Optional[Song] = None

    # Playback state
    is_playing: bool = False
    is_paused: bool = False

    # Voice chat state
    assistant_joined: bool = False

    # Volume
    volume: int = 100

    # Lock prevents two play requests modifying the same queue
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)


# --------------------------------------------------
# Global runtime state
# --------------------------------------------------

CHATS: dict[int, ChatState] = {}

# Active voice chats
ACTIVE_VCS: set[int] = set()

# Users allowed to use sudo commands
SUDO_USERS: set[int] = set()

# Temporary downloaded files
TEMP_FILES: set[str] = set()

# Bot statistics
STATS: dict[str, int] = {
    "plays": 0,
    "skips": 0,
    "songs_finished": 0,
    "joins": 0,
    "leaves": 0,
}


# --------------------------------------------------
# Chat state helpers
# --------------------------------------------------

def get_chat(chat_id: int) -> ChatState:
    """
    Get an existing chat state or create a new one.
    """

    if chat_id not in CHATS:
        CHATS[chat_id] = ChatState(chat_id=chat_id)

    return CHATS[chat_id]


def remove_chat(chat_id: int) -> None:
    """
    Remove all runtime state for a chat.
    """

    CHATS.pop(chat_id, None)
    ACTIVE_VCS.discard(chat_id)


# --------------------------------------------------
# Queue helpers
# --------------------------------------------------

def add_song(chat_id: int, song: Song) -> None:
    """
    Add a song to the chat queue.
    """

    chat = get_chat(chat_id)
    chat.queue.append(song)


def get_next_song(chat_id: int) -> Optional[Song]:
    """
    Remove and return the next song from the queue.
    """

    chat = get_chat(chat_id)

    if not chat.queue:
        return None

    return chat.queue.pop(0)


def clear_queue(chat_id: int) -> None:
    """
    Clear the entire queue.
    """

    chat = get_chat(chat_id)
    chat.queue.clear()


def queue_size(chat_id: int) -> int:
    """
    Return number of queued songs.
    """

    return len(get_chat(chat_id).queue)


# --------------------------------------------------
# Playback helpers
# --------------------------------------------------

def set_current(chat_id: int, song: Optional[Song]) -> None:
    """
    Set the currently playing song.
    """

    chat = get_chat(chat_id)
    chat.current = song

    if song is None:
        chat.is_playing = False
        chat.is_paused = False


def set_playing(chat_id: int, value: bool = True) -> None:
    chat = get_chat(chat_id)
    chat.is_playing = value

    if value:
        chat.is_paused = False


def set_paused(chat_id: int, value: bool = True) -> None:
    chat = get_chat(chat_id)
    chat.is_paused = value

    if value:
        chat.is_playing = False


# --------------------------------------------------
# Voice chat helpers
# --------------------------------------------------

def mark_vc_active(chat_id: int) -> None:
    ACTIVE_VCS.add(chat_id)

    chat = get_chat(chat_id)
    chat.assistant_joined = True

    STATS["joins"] += 1


def mark_vc_inactive(chat_id: int) -> None:
    ACTIVE_VCS.discard(chat_id)

    if chat_id in CHATS:
        CHATS[chat_id].assistant_joined = False

    STATS["leaves"] += 1


def is_vc_active(chat_id: int) -> bool:
    return chat_id in ACTIVE_VCS


# --------------------------------------------------
# Sudo helpers
# --------------------------------------------------

def add_sudo(user_id: int) -> None:
    SUDO_USERS.add(user_id)


def remove_sudo(user_id: int) -> None:
    SUDO_USERS.discard(user_id)


def is_sudo(user_id: int, owner_id: int) -> bool:
    """
    Owner automatically has sudo privileges.
    """

    return user_id == owner_id or user_id in SUDO_USERS


# --------------------------------------------------
# Statistics
# --------------------------------------------------

def increment_stat(name: str, amount: int = 1) -> None:
    if name not in STATS:
        STATS[name] = 0

    STATS[name] += amount


def get_stats() -> dict[str, int]:
    return STATS.copy()


# --------------------------------------------------
# Full reset
# --------------------------------------------------

def reset_all() -> None:
    """
    Clear runtime data.
    """

    CHATS.clear()
    ACTIVE_VCS.clear()
    TEMP_FILES.clear()

    for key in STATS:
        STATS[key] = 0