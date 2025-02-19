# app/routes/routes.py
from app.services.router_service import RouterService
from app.controllers.auth_controller import AuthController
from app.controllers.event_controller import EventController
from app.controllers.reminder_controller import ReminderController

def configure_routes(router: RouterService):
    # Initialize controllers
    auth_controller = AuthController()
    event_controller = EventController()
    reminder_controller = ReminderController()

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

    router.register_command(
        "!events",
        event_controller.list_events,
        min_args=0,
        max_args=1,
        help_text="Get the list of today's events. Usage: !events"
    )

    router.register_command(
        "!reminder",
        reminder_controller.reminder,
        min_args=1,
        max_args=1,
        help_text="Set a reminder. Usage: !reminder <time>"
    )

    return router