"""
Config

Author: L. Saetta
"""

DEBUG = False

# can be also INSTANCE_PRINCIPAL
AUTH_TYPE = "API_KEY"

# for LLMs
REGION = "us-chicago-1"
# REGION = "eu-frankfurt-1"
SERVICE_ENDPOINT = f"https://inference.generativeai.{REGION}.oci.oraclecloud.com"

# this is the default model used
# MODEL_ID = "meta.llama-3.3-70b-instruct"
MODEL_ID = "xai.grok-3"

# these are the parameters used for the "non search" model
TEMPERATURE = 0.0
MAX_TOKENS = 2048

# the model for search on Internet
SEARCH_INFO_MODEL_ID = "openai.gpt-4o-search-preview"
FINAL_REPORT_MAX_TOKENS = 4000

# URL for local FastAPI
PORT = 8080
AGENT_API_URL = f"http://127.0.0.1:{PORT}/invoke"

# plan
# min, max # of sections in the report
DEFAULT_MIN_SECTIONS = 5
DEFAULT_MAX_SECTIONS = 7
