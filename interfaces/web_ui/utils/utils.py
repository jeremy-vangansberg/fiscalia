import time
import streamlit as st
import os
import requests

USE_AUTH = os.getenv("USE_AUTH", "false").lower() == "true"

def call_private_api(question, API_URL, timeout):
    headers = {}
    if USE_AUTH:
        from google.auth.transport.requests import Request
        from google.oauth2 import id_token
        token = id_token.fetch_id_token(Request(), API_URL)
        headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(API_URL, headers=headers, json={"question": question}, timeout=timeout)
    return response