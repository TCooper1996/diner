
import asyncio
import copy
from dataclasses import dataclass
from itertools import chain
from queue import Empty, Queue
import threading
from typing import Dict, List, Tuple, TypeVar
from src import tui
from src.application.start_application import main as _main
from src.common.event_manager import EventManager
from src.common.events import *





def main():
    _main()

if __name__ == "__main__":
    main()

