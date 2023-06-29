from starlette.responses import JSONResponse

def ok(data):
    return JSONResponse({"code": 200, "data": data})

def fail(msg):
    return JSONResponse({"code": 400, "msg": msg})