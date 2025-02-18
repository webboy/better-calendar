# app/routes/routes.py
from app.services.router_service import RouterService
from app.controllers.auth_controller import AuthController

def configure_routes(router: RouterService):
    # Initialize controllers
    auth_controller = AuthController()

    # Register authentication routes
    router.register_command(
        "!register",
        auth_controller.register,
        min_args=1,
        max_args=1,
        help_text="Register with email. Usage: !register <email>"
    )

    router.register_command(
        "!validate",
        auth_controller.validate,
        min_args=2,
        max_args=2,
        help_text="Validate registration. Usage: !validate <email> <code>"
    )

    return router