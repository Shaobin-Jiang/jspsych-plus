import importlib.metadata
import os

from .applications.jspsych import Jspsych

__version__ = importlib.metadata.version(__name__)
__basedir__ = os.path.dirname(__file__)
