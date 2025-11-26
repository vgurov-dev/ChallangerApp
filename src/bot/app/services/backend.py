from bot.app.config import settings
import aiohttp


class CustomService:
    def  __init__(self):
        self.base_url: str = "unknown"
        self.is_code_validation: bool = False
        self.http_success_code: int = 200

    async def __execute_query(self, endpoint: str, params: dict):
        """List all challenges from backend"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{settings.BACKEND_URL}/api/v1/challenges/") as resp:
                    if resp.status == 200:
                        challenges = await resp.json()
                        if challenges:
                            text = "📋 Available Challenges:\n\n"
                            for i, challenge in enumerate(challenges, 1):
                                text += f"{i}. {challenge.get('name', 'Unknown')}\n"
                        else:
                            text = "No challenges available yet."
                    else:
                        text = "❌ Error fetching challenges."
        except Exception as e:
            text = f"❌ Error: {str(e)}"



class BackendService(CustomService):
    def __init__(self):
        super().__init__()
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