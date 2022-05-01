import jwt
import time

METABASE_SITE_URL = "https://metabase.komodote.ch"
METABASE_SECRET_KEY = "e6aaaaf3b3e03a4decc848226b4ac41f82a414ea79bf9dbadc221e5251d3b6ae"

GAME_REPORT_DASHBOARD_ID = 30


def get_dashboard_embed(game_id):
    payload = {
        "resource": {"dashboard": GAME_REPORT_DASHBOARD_ID},
        "params": {"id": game_id},
        "exp": round(time.time()) + (60 * 10)  # 10 minute expiration
    }
    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

    iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token + "#bordered=true&titled=true"
    return iframeUrl
