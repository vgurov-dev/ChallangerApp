from bot.app.config import settings


class CustomService:
    def  __int__(self):
        self.base_url: str = "unknown"

    def __execute_query(self):
        pass


class BackendService(CustomService):
    def __init__(self, args, kwargs):
        CustomService.__init__(self, *args, **kwargs)
        self.base_url = settings.BACKEND_BASE_URL or "backend-service"

    def post_challenge(self):
        pass

    def put_challenge(self):
        pass

    def delete_challenge(self):
        pass

    def get_challenge(self):
        pass

    def get_challenge_days(self):
        pass