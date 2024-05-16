from uvicorn import run

from traveling_sso.config import settings

if __name__ == "__main__":
    run("traveling_sso.main:app", host=str(settings.SSO_HOST), port=int(settings.SSO_PORT))
