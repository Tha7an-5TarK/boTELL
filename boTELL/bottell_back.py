from stud_cmds import *
from datetime import timedelta


def not_register(update: Update, context: CallbackContext):
    update.message.reply_text('Please wait a second, let me verify you first.')
    in_stud_rec, in_fac_rec = count_by_uid(student_record, update.message.from_user['id']),\
        count_by_uid(fac_record, update.message.from_user['id'])

    if in_stud_rec == 0 and in_fac_rec == 0:
        update.message.reply_text('You need to register first', reply_markup = keyboard_start)
        return START_CMD_CHOOSE

    elif in_fac_rec > 0:
        update.message.reply_text('Select what you would like to do\nYou can use /spoll command here, if you\'d like',
                                  reply_markup = keyboard_not_register)
        return NOT_REGISTER_FAC
    else:
        update.message.reply_text('Select what you would like to do',
                                  reply_markup = keyboard_not_register_stud)
        return NOT_REGISTER_STUD


def timeout(update: Update, context: CallbackContext):
    update.message.reply_text('The conversation has timed out. Use /start to restart the conversation.')
    return ConversationHandler.END



def main() -> None:
    updater = Updater("1677250824:AAGELIvkGnTlDkDY3glxjak5RS2H7sGmKIU")
    dispatcher = updater.dispatcher
    conversation_handler = ConversationHandler(
        entry_points = [ CommandHandler('start', start) ],

        states = {
            START_CMD_CHOOSE: [MessageHandler(Filters.regex('^(Register an account for me|Update)'), register_part1),
                               MessageHandler(Filters.regex('^(Classroom)'), not_register)
                               ],
            FACULTY_OR_STUDENT: [MessageHandler(Filters.text, register_part2)],
            DETAIL_ENTRY: [MessageHandler(Filters.text, register_part3)],
            DETAIL_INTERSTITIAL: [MessageHandler(Filters.text, register_part3_1)],
            DETAIL_VERIF: [MessageHandler(Filters.text, register_part4)],

            NOT_REGISTER_FAC: [MessageHandler(Filters.regex('^(Assign)'), assign_all),
                               MessageHandler(Filters.regex('^(Back)'), back),
                               MessageHandler(Filters.regex('^(Message)'), message_all),
                               MessageHandler(Filters.regex('^(Poll)'), poll_0),
                               CommandHandler('spoll', stop_poll),
                               MessageHandler(~Filters.regex('^(Assign|Back|Message|Poll)'), not_register_fac_fallback)
                               ],
            ASSIGN_ALL: [MessageHandler(Filters.document, assign_all_doc),
                         CommandHandler('done', stop_accepting),
                         MessageHandler(Filters.text, assign_all_text)
                         ],
            MSG_ALL: [MessageHandler(Filters.text, message_all_actual)],
            POLL: [MessageHandler(Filters.text, poll_1)],
            POLL_1: [MessageHandler(Filters.text, poll_2)],

            NOT_REGISTER_STUD: [MessageHandler(Filters.regex('^(Submit)'), submit),
                                MessageHandler(Filters.regex('^(Pending assignments)'), pending),
                                MessageHandler(Filters.regex('^(Back)'), back),
                                MessageHandler(~Filters.regex('^(Back|Pending assignments|Back)'),
                                               not_register_student_fallback),
                                ],
            SUBMIT: [MessageHandler(Filters.text, submit_actual)],
            SUBMIT_SEND_MSG: [MessageHandler(Filters.document | Filters.photo | (~Filters.regex('^(Done)')),
                                             submit_doc),
                              MessageHandler(Filters.regex('^(Done)'), stop_accepting_assigns)
                              ],

            ConversationHandler.TIMEOUT: [MessageHandler(Filters.text, timeout)]


        },
        fallbacks = [ MessageHandler(Filters.regex('^(quit|Quit)'), quit_) ],
        allow_reentry = True, conversation_timeout = timedelta(minutes = 5)

    )

    dispatcher.add_handler(conversation_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
