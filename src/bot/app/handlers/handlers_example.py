"""
Example handlers for the Challenge Bot
This file demonstrates various dp.message() use cases
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
import aiohttp
from bot.app.config import settings


# 1. Command handlers
def register_command_handlers(dp):
    """Register command handlers"""
    
    @dp.message(CommandStart())
    async def start_handler(message: Message):
        """Handle /start command"""
        await message.answer("Welcome to Challenge Bot! Use /help to see available commands.")

    @dp.message(Command("help"))
    async def help_handler(message: Message):
        """Handle /help command"""
        help_text = """
Available commands:
/start - Start the bot
/help - Show this help
/challenges - List challenges
/create - Create new challenge
/profile - View your profile
        """
        await message.answer(help_text)

    @dp.message(Command("challenges"))
    async def list_challenges(message: Message):
        """List all challenges from backend"""
        try:
            async with aiohttp.ClientSession() as session:
                user = message.from_user
                async with session.get(f"{settings.BACKEND_URL}/api/v1/challenges?user_id={user.id}") as resp:
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
        
        await message.answer(text)

    @dp.message(Command("create"))
    async def create_challenge(message: Message):
        """Create a new challenge"""
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📝 Create Challenge", callback_data="create_challenge")],
            [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")]
        ])
        await message.answer("Choose an action:", reply_markup=keyboard)

    @dp.message(Command("profile"))
    async def profile_handler(message: Message):
        """Show user profile"""
        user = message.from_user
        profile_text = f"""
👤 Your Profile:
ID: {user.id}
Username: @{user.username or 'Not set'}
First Name: {user.first_name or 'Not set'}
Last Name: {user.last_name or 'Not set'}
        """
        await message.answer(profile_text)


# 2. Text-based filters
def register_text_handlers(dp):
    """Register text-based handlers"""
    
    @dp.message(F.text == "hello")
    async def hello_handler(message: Message):
        """Handle exact text 'hello'"""
        await message.answer("Hello! 👋")

    @dp.message(F.text.startswith("challenge"))
    async def challenge_text_handler(message: Message):
        """Handle messages starting with 'challenge'"""
        await message.answer("You mentioned challenges! Use /challenges to see available ones.")

    @dp.message(F.text.contains("help"))
    async def help_text_handler(message: Message):
        """Handle messages containing 'help'"""
        await message.answer("Need help? Use /help command!")


# 3. Message type filters
def register_message_type_handlers(dp):
    """Register message type handlers"""
    
    @dp.message(F.photo)
    async def photo_handler(message: Message):
        """Handle photo messages"""
        await message.answer("📸 Nice photo! I received your image.")

    @dp.message(F.document)
    async def document_handler(message: Message):
        """Handle document messages"""
        await message.answer("📄 Document received! I'll process it.")

    @dp.message(F.sticker)
    async def sticker_handler(message: Message):
        """Handle sticker messages"""
        await message.answer("😄 Cool sticker!")

    @dp.message(F.voice)
    async def voice_handler(message: Message):
        """Handle voice messages"""
        await message.answer("🎤 Voice message received! I can't process audio yet.")


# 4. User-specific handlers
def register_user_handlers(dp):
    """Register user-specific handlers"""
    
    @dp.message(F.from_user.id == 123456789)  # Replace with your user ID
    async def admin_handler(message: Message):
        """Handle messages from specific user (admin)"""
        await message.answer("🔧 Admin command received!")

    @dp.message(F.from_user.username.in_(["admin", "moderator"]))
    async def staff_handler(message: Message):
        """Handle messages from staff members"""
        await message.answer("👮 Staff message received!")


# 5. Callback query handlers (for inline keyboards)
def register_callback_handlers(dp):
    """Register callback query handlers"""
    
    @dp.callback_query(F.data == "create_challenge")
    async def create_challenge_callback(callback: CallbackQuery):
        """Handle create challenge button"""
        await callback.message.edit_text("Creating challenge... Please wait.")
        # Here you would implement challenge creation logic
        await callback.answer("Challenge creation started!")

    @dp.callback_query(F.data == "cancel")
    async def cancel_callback(callback: CallbackQuery):
        """Handle cancel button"""
        await callback.message.edit_text("Operation cancelled.")
        await callback.answer("Cancelled!")


# 6. Fallback handler
def register_fallback_handler(dp):
    """Register fallback handler (must be last)"""
    
    @dp.message()
    async def fallback_handler(message: Message):
        """Handle all other messages"""
        await message.answer("I didn't understand that. Use /help to see available commands.")


# Main registration function
def register_all_handlers(dp):
    """Register all handlers in the correct order"""
    register_command_handlers(dp)
    register_text_handlers(dp)
    register_message_type_handlers(dp)
    register_user_handlers(dp)
    register_callback_handlers(dp)
    register_fallback_handler(dp)  # Must be last
