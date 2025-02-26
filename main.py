from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from movie_request import request_movie
from send_movie import send_movie
from admin_panel import add_movie, edit_movie, delete_movie, set_channel
from database import init_db

GET_MOVIE_ID = range(1)

def main():
    # Bot tokenini kiriting
    application = Application.builder().token("7202873256:AAE4xNb0SFn9eUd13mSMeYuK5R7PPb-xkhM").build()

    # Ma'lumotlar bazasini ishga tushirish
    init_db()

    # Kino so'rov dialogi
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("get_movie", request_movie)],
        states={
            GET_MOVIE_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, send_movie)],
        },
        fallbacks=[],
    )

    # Admin buyruqlari
    application.add_handler(CommandHandler("add_movie", add_movie))
    application.add_handler(CommandHandler("edit_movie", edit_movie))
    application.add_handler(CommandHandler("delete_movie", delete_movie))
    application.add_handler(CommandHandler("set_channel", set_channel))

    # Kino so'rov handleri
    application.add_handler(conv_handler)

    # Botni ishga tushirish
    application.run_polling()

if __name__ == "__main__":
    main()