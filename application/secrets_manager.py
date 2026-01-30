import streamlit
from typing import Any, Optional


__all__ = ["get"]


def get(key_name: str) -> Optional[Any]:
    return streamlit.secrets.get(key_name)
