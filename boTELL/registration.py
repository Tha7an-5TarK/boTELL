from datetime import datetime
from telegram.error import BadRequest
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from utils import *
from mongo_util import *
from time import sleep
from threading import Thread
from fac_cmds import *



keyboard_start_keys = [
    ['Register an account for me'],
    ['Classroom', 'Update'],
    ['Quit']
     ]

keyboard_start = ReplyKeyboardMarkup(keyboard_start_keys, one_time_keyboard = True)

keyboard_stud_fac = ReplyKeyboardMarkup([['I\'m a student', 'I\'m a faculty']], one_time_keyboard = True)

keyboard_yes_no = ReplyKeyboardMarkup([['Yes', 'No']], one_time_keyboard = True)

keyboard_pre_registered = ReplyKeyboardMarkup([['Oh right! My mistake', 'I want to re-enter the details']],
                                              one_time_keyboard = True)


START_CMD_CHOOSE, FACULTY_OR_STUDENT, DETAIL_ENTRY, DETAIL_VERIF, DETAIL_INTERSTITIAL = range(5)
is_update = False



def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome to botTELL v0.1. Since I am still in developmental phase, '
                              'kindly don\'t mind the bugs/glitches and report them at @sneked or @apelling.\n'
                              'Select the option that suits you the best. You can always type /start to restart the'
                              ' conversation anytime.',
                              reply_markup = keyboard_start
                              )
    print(update.message.chat_id)
    # print(context.bot.get_chat_members_count(chat_id = '-1001259811997'))
    # print(update.message.text)
    return START_CMD_CHOOSE




def quit_(update: Update, context: CallbackContext):
    update.message.reply_text('Goodbye, see you around!')
    return ConversationHandler.END


def register_part1(update: Update, context: CallbackContext):
    msg = update.message.text.lower()
    global is_update

    purpose = 'registration'
    if msg == 'update':
        purpose = 'updation'
        is_update = True

    update.message.reply_text('Please wait a second, let me verify you first.')
    in_stud_rec, in_fac_rec = count_by_uid(student_record, update.message.from_user['id']), \
                              count_by_uid(fac_record, update.message.from_user['id'])

    if in_fac_rec == 0 and in_stud_rec == 0 and is_update:
        update.message.reply_text('You need to register first', reply_markup = keyboard_start)
        is_update = False
        # print('hi')
        return START_CMD_CHOOSE

    elif in_fac_rec > 0 and not is_update:
        update.message.reply_text('You\'re already registered as a faculty. Contact the administrator right away '
                                  'if you think this is a mistake.', reply_markup = keyboard_start)
        return START_CMD_CHOOSE

    elif in_stud_rec > 0 and not is_update:
        update.message.reply_text('You\'re already registered as a student. Contact the administrator right away '
                                  'if you think this is a mistake.', reply_markup=keyboard_start)
        return START_CMD_CHOOSE

    elif (msg != 'quit') and (msg != 'register an account for me') and (msg != 'update') and\
        (msg != 'Classroom'):
        update.message.reply_text('Sorry, didn\'t get you', reply_markup = keyboard_start)
        return START_CMD_CHOOSE

    update.message.reply_text(f'Let me walk you through the {purpose} procedure.')
    update.message.reply_text('Are you a faculty or a student?', reply_markup = keyboard_stud_fac)
    return FACULTY_OR_STUDENT


def register_part2(update: Update, context: CallbackContext):
    if update.message.text == 'I\'m a student' or update.message.text == 'I\'m a faculty':
        context.user_data['acct_type'] = update.message.text.split()[2]
        reply_text = 'Great! Enter your NAME, ID, DEPT (CIV/MECH/CSE/ECE/EEE), DOB (DD MM YYYY)' \
                     ' and EMAIL (each on a new line)'
        update.message.reply_text(reply_text)
        return DETAIL_ENTRY
    else:
        update.message.reply_text('Please select an option from the ones given :)', reply_markup = keyboard_stud_fac)
        return FACULTY_OR_STUDENT


def register_part3(update: Update, context: CallbackContext):
    # other checking left
    if update.message.text == 'Oh right! My mistake':
        update.message.reply_text('Alright!', reply_markup = keyboard_start)
        return START_CMD_CHOOSE

    try:
        i = iter(range(5))
        for key in ['name', 'id', 'dept', 'dob', 'email']:
            context.user_data[key] = update.message.text.split('\n')[next(i)]
    except IndexError:
        update.message.reply_text('Enter the details as told. (5 entries in total, each on a separate line.)')
        return DETAIL_ENTRY

    else:
        if not check_email(context.user_data['email']):
            update.message.reply_text('Email is incorrect, kindly re-enter the details')
            return DETAIL_ENTRY
        else:
            update.message.reply_text('Done?', reply_markup = keyboard_yes_no)
            return DETAIL_INTERSTITIAL


def register_part3_1(update: Update, context: CallbackContext):
    if update.message.text.lower() == 'no':
        update.message.reply_text('Well then, enter the details again')
        return DETAIL_ENTRY
    elif update.message.text.lower() == 'yes':
        acct_type = context.user_data["acct_type"]
        name = context.user_data["name"]
        id = context.user_data["id"]
        dept = context.user_data["dept"]
        dob = context.user_data["dob"]
        email = context.user_data["email"]

        update.message.reply_text(f'Awesome! These are the details I\'m left with:\n'
                                  f'Account type: {acct_type}\n'
                                  f'Name: {name}\nID: {id}\n'
                                  f'Department: {dept}\nDate of birth: {dob}\n'
                                  f'Email: {email}\n'
                                  )
        update.message.reply_text('Are these correct?', reply_markup=keyboard_yes_no)
        return DETAIL_VERIF
    else:
        update.message.reply_text('C\'mon, options are there right in front of you. Select from them!',
                                  reply_markup = keyboard_yes_no)
        return DETAIL_INTERSTITIAL



def register_part4(update: Update, context: CallbackContext):
    global is_update

    if update.message.text.lower() == 'no':
        update.message.reply_text('It\'s okay, enter your details again')
        return DETAIL_ENTRY

    elif update.message.text.lower() == 'yes':
        acct_type = context.user_data["acct_type"]
        name = context.user_data["name"]
        id = context.user_data["id"]
        dept = context.user_data["dept"]
        dob = context.user_data["dob"]
        email = context.user_data["email"]

        if not is_update:
            try:
                if acct_type.lower() == 'student':
                    insert_(name, id, dept, dob, email, update.message.from_user['id'], student_record)
                else:
                    insert_(name, id, dept, dob, email, update.message.from_user['id'], fac_record)
            except DuplicateKeyError:
                update.message.reply_text('Your account is pre-registered! Kindly check the details!',
                                          reply_markup = keyboard_pre_registered)
                return DETAIL_ENTRY
            else:
                # context.bot.send_message(chat_id='-1001259811997', text = f'Welcome, {name}!')
                link_generator = Thread(target = link_procedure, args = (update, context))
                link_generator.start()

        else:
            try:
                update.message.reply_text('Please wait a moment...')
                if acct_type.lower() == 'student':
                    if count_by_id(student_record, id) == 0:
                        update.message.reply_text('No such account exists.', reply_markup = keyboard_start)
                        is_update = False
                        return START_CMD_CHOOSE
                    else:
                        update_record(name, id, dept, dob, email, student_record)
                else:
                    if count_by_id(fac_record, id) == 0:
                        update.message.reply_text('No such account exists.', reply_markup = keyboard_start)
                        is_update = False
                        return START_CMD_CHOOSE
                    else:
                        update_record(name, id, dept, dob, email, fac_record)
            except Exception as e:
                print(e)
                update.message.reply_text('Some error has occurred, let\'s go back', reply_markup = keyboard_start)
                return START_CMD_CHOOSE
            else:
                update.message.reply_text('Updated Successfully!')
            finally:
                is_update = False

        return ConversationHandler.END

    else:
        update.message.reply_text('Please select an option from the ones give (yes/no)', reply_markup = keyboard_yes_no)
        return DETAIL_VERIF


def link_procedure(update: Update, context: CallbackContext):
    link = context.bot.createChatInviteLink(chat_id="-1001259811997").invite_link
    if context.user_data['acct_type'] == 'student':
        update.message.reply_text(f'Click on the following link:\n{link}')
    else:
        update.message.reply_text(f'You may or may not join the channel:\n{link}')

    sleep(10)
    context.bot.revoke_chat_invite_link(chat_id="-1001259811997", invite_link=link)
