from sanic import Sanic
from sanic_jwt.decorators import protected
from sanic_security.authentication import requires_authentication

app = Sanic("MyHelloWorldApp")


# ruleid: sanic-route-unauthenticated
@app.route("/test", methods=["POST", "PUT"])
async def handler(request):
    return text("OK")


# ruleid: sanic-route-unauthenticated
app.add_route(handler, "/test")


# ruleid: sanic-route-unauthenticated
@app.get("/test")
async def handler(request):
    return text("OK")


# ruleid: sanic-route-authenticated
@app.route("/protected")
@protected()
async def protected_route(request):
    return json({"protected": True})


# ruleid: sanic-route-authenticated
@app.post("api/security/auth")
@requires_authentication()
async def on_authenticate(request, authentication_session):
    return json(
        "You have been authenticated.",
        authentication_session.bearer.json(),
    )
