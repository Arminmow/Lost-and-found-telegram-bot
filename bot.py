from telegram import Update , ChatMember
from telegram.ext import Application , CommandHandler , CallbackContext , CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_TOKEN

# /start command - welcomes the user
async def start(update: Update , context : CallbackContext):
    user_id = update.effective_user.id
    
    is_member = await check_channel_membership(user_id, context)
    print(f"User ID: {user_id}, Is Member: {is_member}")


    if is_member:
        welcome_message = (
            "Welcome to the Lost and Found Bot!\n\n"
            "You can now use the bot.\n\n"
            "Commands:\n"
            "/report_lost - Report a lost item\n"
            "/report_found - Report a found item\n"
            "/latest_found - View the latest found items\n"
            "/help - Get help with commands"
        )
        await update.message.reply_text(welcome_message)
        print(f"User {update.effective_user.first_name} started the bot.")


    else:
        notification_message = (
            "You must join our channel before using this bot. Please join the channel:\n"
        )
        join_button = InlineKeyboardButton("Join Channel", url="https://t.me/idontfuxkingknow")
        reply_markup = InlineKeyboardMarkup([[join_button]])

        await update.message.reply_text(notification_message, reply_markup=reply_markup)
        
# Check for channels membership
async def check_channel_membership(user_id:int , context:CallbackContext):
    try:
        #Check if the user is a member of channel
        chat_member = await context.bot.get_chat_member('@idontfuxkingknow',user_id)
        print(f"Chat Member Status for user_id {user_id}: {chat_member.status}")
        return chat_member.status in [ChatMember.ADMINISTRATOR, ChatMember.MEMBER , ChatMember.OWNER]
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Add the /start command handler
    application.add_handler(CommandHandler("start", start))

    # Start polling for updates
    print("Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
   main()