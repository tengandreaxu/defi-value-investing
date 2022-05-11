import os
from dataclasses import dataclass


@dataclass(frozen=True)
class DuneCredentials:

    username = os.environ["DUNE_USER"]
    password = os.environ["DUNE_PASS"]
