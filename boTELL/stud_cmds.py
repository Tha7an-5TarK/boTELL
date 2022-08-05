from fac_cmds import *

keyboard_not_register_stud = ReplyKeyboardMarkup([['Submit', 'Pending assignments'],
                                                  ['Back']], one_time_keyboard = True)

SUBMIT, SUBMIT_SEND_MSG, PENDING = range(13, 16)


def submit(update: Update, context: CallbackContext):
    update.message.reply_text('Enter assignment ID')
    return SUBMIT


def submit_actual(update: Update, context: CallbackContext):
    assign_id = update.message.text
    pending = pending_assigns(update.message.chat_id)
    if assign_id not in pending:
        update.message.reply_text('No such assignment found/pending. Kindly check again.',
                                  reply_markup = keyboard_start)
        return START_CMD_CHOOSE


    update.message.reply_text('Attach documents, if any. You can attach multiple documents.'
                              'Click \'done\' when you\'re done',
                              reply_markup = keyboard_done)
    context.user_data['assign_id'] = assign_id
    # print(find_assigner(assign_id, update.message.chat_id))
    return SUBMIT_SEND_MSG


def submit_doc(update: Update, context: CallbackContext):
    # print('Hi')
    # print(context.user_data['assign_id'])
    to = find_assigner(context.user_data['assign_id'], update.message.chat_id)
    _from = update.message.chat_id
    context.bot.forward_message(chat_id = to, from_chat_id = _from, message_id = update.message.message_id)
    context.bot.send_message(chat_id = to, text = f"Assignment ID: {context.user_data['assign_id']}")
    del_assign(context.user_data['assign_id'], update.message.chat_id)
    update.message.reply_text('Forwarded successfully.')
    return SUBMIT


def stop_accepting_assigns(update: Update, context: CallbackContext):
    update.message.reply_text('Select what you\'d like to do now.', reply_markup=keyboard_not_register_stud)
    return NOT_REGISTER_STUD


def not_register_student_fallback(update: Update, context: CallbackContext):
    update.message.reply_text('Didn\'t get you.')
    update.message.reply_text('Select what you\'d like to do', reply_markup = keyboard_not_register_stud)
    return SUBMIT



def pending(update: Update, context: CallbackContext):
    pending_ = pending_assigns(update.message.chat_id)
    if len(pending_) == 0:
        update.message.reply_text('Congrats, No assignments pending! :)', reply_markup = keyboard_start)
        return START_CMD_CHOOSE
    update.message.reply_text(f'Following are the assignments which are pending:\n'
                              f'Assignment IDs: {", ".join(pending_)}\n'
                              f'Complete them soon!', reply_markup = keyboard_start)
    return START_CMD_CHOOSE

