import os
import json
import secrets
import urllib.parse
import requests
from typing import Dict, Any, Optional

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")

# Provider Configs
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

FACEBOOK_APP_ID = os.environ.get("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET = os.environ.get("FACEBOOK_APP_SECRET")

INSTAGRAM_APP_ID = os.environ.get("INSTAGRAM_APP_ID")
INSTAGRAM_APP_SECRET = os.environ.get("INSTAGRAM_APP_SECRET")

def get_oauth_config_status() -> Dict[str, bool]:
    return {
        "google_configured": bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET),
        "facebook_configured": bool(FACEBOOK_APP_ID and FACEBOOK_APP_SECRET),
        "instagram_configured": bool(INSTAGRAM_APP_ID and INSTAGRAM_APP_SECRET)
    }

def generate_oauth_state(role: str) -> str:
    csrf_token = secrets.token_hex(16)
    return json.dumps({"role": role, "csrf": csrf_token})

def parse_oauth_state(state_str: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(state_str)
    except Exception:
        return None

def get_authorization_url(provider: str, role: str) -> str:
    state = generate_oauth_state(role)
    redirect_uri = f"{BACKEND_URL}/auth/{provider}/callback"

    if provider == "google":
        if not GOOGLE_CLIENT_ID:
            return f"{FRONTEND_URL}/login?oauth_error=google_not_configured"
        params = {
            "client_id": GOOGLE_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid profile email",
            "state": state,
            "access_type": "online",
            "prompt": "select_account"
        }
        return f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"

    elif provider == "facebook":
        if not FACEBOOK_APP_ID:
            return f"{FRONTEND_URL}/login?oauth_error=facebook_not_configured"
        params = {
            "client_id": FACEBOOK_APP_ID,
            "redirect_uri": redirect_uri,
            "scope": "email,public_profile",
            "state": state,
            "response_type": "code"
        }
        return f"https://www.facebook.com/v18.0/dialog/oauth?{urllib.parse.urlencode(params)}"

    elif provider == "instagram":
        if not INSTAGRAM_APP_ID:
            return f"{FRONTEND_URL}/login?oauth_error=instagram_not_configured"
        params = {
            "client_id": INSTAGRAM_APP_ID,
            "redirect_uri": redirect_uri,
            "scope": "user_profile,user_media",
            "response_type": "code",
            "state": state
        }
        return f"https://api.instagram.com/oauth/authorize?{urllib.parse.urlencode(params)}"

    return f"{FRONTEND_URL}/login?oauth_error=invalid_provider"

def exchange_code_for_user_info(provider: str, code: str) -> Optional[Dict[str, Any]]:
    redirect_uri = f"{BACKEND_URL}/auth/{provider}/callback"

    try:
        if provider == "google":
            token_res = requests.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": redirect_uri
                },
                timeout=10
            )
            if token_res.status_code != 200:
                return None
            token_data = token_res.json()
            access_token = token_data.get("access_token")

            user_res = requests.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10
            )
            if user_res.status_code != 200:
                return None
            info = user_res.json()
            return {
                "provider_user_id": info["id"],
                "email": info.get("email"),
                "display_name": info.get("name"),
                "avatar_url": info.get("picture")
            }

        elif provider == "facebook":
            token_res = requests.get(
                "https://graph.facebook.com/v18.0/oauth/access_token",
                params={
                    "client_id": FACEBOOK_APP_ID,
                    "client_secret": FACEBOOK_APP_SECRET,
                    "code": code,
                    "redirect_uri": redirect_uri
                },
                timeout=10
            )
            if token_res.status_code != 200:
                return None
            access_token = token_res.json().get("access_token")

            user_res = requests.get(
                "https://graph.facebook.com/me",
                params={"fields": "id,name,email,picture.type(large)", "access_token": access_token},
                timeout=10
            )
            if user_res.status_code != 200:
                return None
            info = user_res.json()
            avatar = info.get("picture", {}).get("data", {}).get("url")
            return {
                "provider_user_id": info["id"],
                "email": info.get("email"),
                "display_name": info.get("name"),
                "avatar_url": avatar
            }

        elif provider == "instagram":
            # Instagram basic display token exchange
            token_res = requests.post(
                "https://api.instagram.com/oauth/access_token",
                data={
                    "client_id": INSTAGRAM_APP_ID,
                    "client_secret": INSTAGRAM_APP_SECRET,
                    "grant_type": "authorization_code",
                    "redirect_uri": redirect_uri,
                    "code": code
                },
                timeout=10
            )
            if token_res.status_code != 200:
                return None
            info = token_res.json()
            return {
                "provider_user_id": str(info.get("user_id")),
                "email": f"ig_{info.get('user_id')}@instagram.user",
                "display_name": f"Instagram User #{info.get('user_id')}",
                "avatar_url": None
            }

    except Exception as e:
        print(f"Error during OAuth code exchange for {provider}: {e}")
        return None

    return None
