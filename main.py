from dotenv import load_dotenv
import os
from ncmec_sdk.client import NCMECClient
from ncmec_sdk.repl import NCMECRepl

load_dotenv()
client_id = os.getenv("NCMEC_CLIENTID")
client_secret = os.getenv("NCMEC_CLIENTSECRET")

if not client_id or not client_secret:
    raise ValueError("NCMEC_CLIENTID and NCMEC_CLIENTSECRET must be set in environment variables.")

if __name__ == "__main__":
    client = NCMECClient(client_id, client_secret)
    NCMECRepl(client).run()