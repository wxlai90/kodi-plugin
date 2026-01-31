from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Playable:
    url: str
    subtitles: List[str] = field(default_factory=list)
