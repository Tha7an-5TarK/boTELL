from registration import *

keyboard_not_register_keys = [['Assign'],
                              ['Message', 'Poll'],
                              ['Back']]

keyboard_done = ReplyKeyboardMarkup([['Done']], one_time_keyboard = True)

keyboard_not_register = ReplyKeyboardMarkup(keyboard_not_register_keys, one_time_keyboard = True)

NOT_REGISTER_FAC, NOT_REGISTER_STUD, ASSIGN_ALL, STATUS, MSG_ALL, POLL, POLL_1 = range(5, 12)


def stop_accepting(update: Update, context: CallbackContext):
    update.message.reply_text('Select what you\'d like to do now.', reply_markup = keyboard_not_register)
    return NOT_REGISTER_FAC


def stop_poll(update: Update, context: CallbackContext):
    try:
        res = context.bot.stop_poll(chat_id = '-1001259811997', message_id = update.message.text.split()[1])
        res_to_display = f'Results for "{res["question"]}" are as follows:\n'
        # print(res)

        for option in res['options']:
            res_to_display += f"{option['text']} - {option['voter_count']}\n"
        update.message.reply_text(res_to_display)
    except BadRequest:
        update.message.reply_text('The poll has been closed already', reply_markup = keyboard_not_register)
    except Exception as e:
        update.message.reply_text('Please add poll ID as well', reply_markup = keyboard_not_register)
    return NOT_REGISTER_FAC


def assign_all(update: Update, context: CallbackContext):
    update.message.reply_text('Attach a document here.', reply_markup = keyboard_done)
    return ASSIGN_ALL


def assign_all_doc(update: Update, context: CallbackContext):
    update.message.reply_text('Got it. I\'ve sent it to them. You can attach more if you want. Click on done'
                              ' when you\'re done', reply_markup = keyboard_done)
    msg = context.bot.forward_message(chat_id = '-1001259811997', from_chat_id = update.message.chat_id,
                                message_id = update.message.message_id)
    assign_id = msg["message_id"]
    context.bot.send_message(chat_id = '-1001259811997', text = f'Assignment ID: {assign_id}')
    add_assign(assign_id, update.message.chat_id)

    return ASSIGN_ALL


def assign_all_text(update: Update, context: CallbackContext):
    update.message.reply_text('If you want to assign via text, use the "message all/specific" option',
                              reply_markup = keyboard_not_register)
    return NOT_REGISTER_FAC



def back(update: Update, context: CallbackContext):
    update.message.reply_text('Sure', reply_markup = keyboard_start)
    return START_CMD_CHOOSE


def message_all(update: Update, context: CallbackContext):
    update.message.reply_text('Type your message here')
    return MSG_ALL


def message_all_actual(update: Update, context: CallbackContext):
    update.message.reply_text('Got it. I\'ve sent your message', reply_markup = keyboard_not_register)
    context.bot.send_message(chat_id='-1001259811997', text = update.message.text)
    return NOT_REGISTER_FAC


def poll_0(update: Update, context: CallbackContext):
    # context.chat_data['from'] = update.message.from_user['id']
    context.chat_data['mid'] = update.message.message_id
    update.message.reply_text('Enter the question')
    return POLL


def poll_1(update: Update, context: CallbackContext):
    context.chat_data['poll_ques'] = update.message.text
    update.message.reply_text('Enter each option in a new line')
    return POLL_1


def poll_2(update: Update, context: CallbackContext):
    options = update.message.text.split('\n')
    update.message.reply_text('Great, I\'ve sent the poll', reply_markup = keyboard_not_register)
    poll = context.bot.send_poll(chat_id = '-1001259811997', question = context.chat_data['poll_ques'], options = options)
    update.message.reply_text(f'Unique identifier for this poll is: {poll["message_id"]}. '
                              f'You can stop this poll by typing "/spoll {poll["message_id"]}". If you do, i\'ll send '
                              f'you the final results of the poll.',
                              reply_markup = keyboard_not_register)
    return NOT_REGISTER_FAC


def not_register_fac_fallback(update: Update, context: CallbackContext):
    update.message.reply_text('Didn\'t get you', reply_markup = keyboard_not_register)
    return NOT_REGISTER_FAC


