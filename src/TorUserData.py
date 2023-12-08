from dataclasses import dataclass

@dataclass
class TorUserData:
    port: int
    user_agent: str