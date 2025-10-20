def ok(message: str = "ok", **extra):
    return {"status": "ok", "message": message, **extra}


def err(message: str, **extra):
    return {"status": "error", "message": message, **extra}
