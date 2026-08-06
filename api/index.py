import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from mangum import Mangum
from main import app

handler = Mangum(app)