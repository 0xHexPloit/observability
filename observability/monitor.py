import pandas as pd

from typing import Protocol

class Monitor(Protocol):
    def start_monitoring(self) -> None:
        ...

    def stop_monitoring(self) -> pd.DataFrame:
        ...