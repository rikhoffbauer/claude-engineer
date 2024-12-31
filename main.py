import os
from dotenv import load_dotenv
import json
from tavily import TavilyClient
import base64
from PIL import Image
import io
import re
from anthropic import Anthropic, APIStatusError, APIError
import difflib
import time
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown
import asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
import glob
import speech_recognition as sr
import websockets
from pydub import AudioSegment
from pydub.playback import play
import datetime
import venv
import sys
import signal
import logging
from typing import Tuple, Optional, Dict, Any, List, Union
import mimetypes
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
import subprocess
import shutil
import httpx
from config import Config
