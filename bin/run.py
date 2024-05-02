from uvicorn import run


if __name__ == "__main__":
    run("traveling_sso.main:app", host="0.0.0.0", port=80)
