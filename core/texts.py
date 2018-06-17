MSG_USER_UNKNOWN = 'No such user'

MSG_NEW_GROUP_ADMIN = """Welcome our new administrator: @{}!
Check the commands list with /help command"""
MSG_NEW_GROUP_ADMIN_EXISTS = '@{} already has administrator rights'


MSG_DEL_GROUP_ADMIN_NOT_EXIST = '@{} never had any power here!'
MSG_DEL_GROUP_ADMIN = '@{}, now you have no power here!'

MSG_NEW_GLOBAL_ADMIN = 'New global administrator: @{}!'
MSG_NEW_GLOBAL_ADMIN_EXISTS = '@{} already has global administrator rights'

MSG_DEL_GLOBAL_ADMIN_NOT_EXIST = '{} never had any global rights!'
MSG_DEL_GLOBAL_ADMIN = '@{} now you have no global rights'

MSG_NEW_SUPER_ADMIN = 'New super administrator: @{}!'
MSG_NEW_SUPER_ADMIN_EXISTS = '@{} is already a super administrator!'


MSG_LIST_ADMINS_HEADER = 'Administrators list:\n'
MSG_LIST_ADMINS_FORMAT = '{} @{} {} {}\n'
MSG_LIST_ADMINS_USER_FORMAT = '@{} {} {}\n'

MSG_EMPTY = '[Empty]\n'

MSG_START_WELCOME = 'Greetings, soldier! I am the Soul Bot of 🥔Nomadic Entrepreneurs! ' \
                    ' '
MSG_ADMIN_WELCOME = 'Welcome, master!'


MSG_HELP_GLOBAL_ADMIN = """Welcome commands:
/enable_welcome — enable welcome message.
/disable_welcome — disable welcome message.
/set_welcome <text> — set welcome message. \
->Can contain %username% — will be shown as @username, %ign% - will show user ingame name, \
if not set to First and Last name, or ID, 
using %last_name%, %first_name%, %id%. <-i don't think this still exists *deleted probably*
/show_welcome — show welcome message.
Trigger commands:
Reply to a message or file with /set_trigger <trigger text> — \
set message to reply with on a trigger (only current chat)
/del_trigger <trigger> — delete trigger.
/list_triggers — show all triggers.
Reply to a message or file with /set_global_trigger <trigger text> — \
set message to reply with on a trigger (all chats)
/del_global_trigger <trigger> — delete trigger.
Super administrator commands:
/add_admin <user> — add administrator to current chat.
/del_admin <user> — delete administrator from current chat.
/list_admins — show list of current chat administrators.
/enable_trigger — allow everyone to call trigger.
/disable_trigger — forbid everyone to call trigger.
/find <user> - Show user status by telegram user name  *might be removed*
/findc <ign> - Show user status by ingame name        *might be removed*
/findi <id> - Show user status by telegram uquique id  *might be removed*
Free text commands:
allow everyone to trigger - Allow every member to call triggers
prevent everyone from triggering - Allow only admins to call triggers
allow everyone to pin - Allow all members to pin messages 
prevent everyone from pinning - Allow only admins to pin messages
Reply any message with Pin to Pin it (admins always can do that, other members if its enabled)
Reply any message with Pin and notify to pin and send notificaion
Reply any message with Delete to delete it 
"""

MSG_HELP_GROUP_ADMIN = """Welcome commands:
/enable_welcome — enable welcome message.
/disable_welcome — disable welcome message.
/set_welcome <text> — set welcome message. \
Can contain %username% — will be shown as @username, \
if not set to First and Last name, or ID, 
using %last_name%, %first_name%, %id%. <-*might be deleted*
/show_welcome — show welcome message.
Free text commands:
allow everyone to trigger - Allow every member to call triggers
prevent everyone from triggering - Allow only admins to call triggers
allow everyone to pin - Allow all members to pin messages 
prevent everyone from pinning - Allow only admins to pin messages
squad - mention every squad member
Reply any message with Pin to Pin it (admins always can do that, other members if its enabled)
Reply any message with Pin and notify to pin and send notificaion
Reply any message with Delete to delete it 
"""


MSG_HELP_USER = "/list_triggers — show all triggers."

MSG_PING = 'Go and dig some soulz, @{}!'


MSG_PERSONAL_SITE_LINK = 'Your personal link: {}'

MSG_GROUP_STATUS_CHOOSE_CHAT = 'Choose chat'

MSG_GROUP_STATUS = """Group: {}
Admins:
{}
Welcome: {}
Trigger allowed: {}"""

MSG_GROUP_STATUS_ADMIN_FORMAT = '{} @{} {} {}\n'
MSG_GROUP_STATUS_DEL_ADMIN = 'Demote {} {}'


MSG_ON = 'Enabled'
MSG_OFF = 'Disabled'
MSG_SYMBOL_ON = '✅'
MSG_SYMBOL_OFF = '❌'
MSG_BACK = '🔙Back'

MSG_ORDER_PIN = '✅Pin'
MSG_ORDER_NO_PIN = '❌No pin'
MSG_ORDER_BUTTON = '✅Button'
MSG_ORDER_NO_BUTTON = '❌No button'

MSG_ORDER_CLEARED_BY_HEADER = 'Order accepted by:\n'

MSG_ORDER_SENT = 'Message is sent'

MSG_ORDER_CLEARED = 'Recorded, soldier!'


MSG_ORDER_CLEARED_ERROR = 'STOP! You do not belong here!!!!'
MSG_ORDER_SEND_HEADER = 'Where to send?'

MSG_ORDER_GROUP_CONFIG_HEADER = 'Group settings: {}'


MSG_NEWBIE = """There is a new player in chat!\n
Hurry up and welcome %username%!"""

MSG_FLAG_CHOOSE_HEADER = 'Choose a grave or send me the order'

# main.py texts
# -----------------------
MSG_BUILD_REPORT_EXISTS = 'This report already exists!'
MSG_BUILD_REPORT_OK = 'Thanks for the help! This is your {} report.'
MSG_BUILD_REPORT_FORWARDED = 'Do not send me any more reports from alternative accounts !!! '
MSG_BUILD_REPORT_TOO_OLD = 'This report is very old, I can not accept it.'

MSG_REPORT_OLD = 'Your report stinks like rotten corpse, next time try to send it within a minute after receiving."'
MSG_REPORT_EXISTS = 'The report for this battle has already been submitted.'
MSG_REPORT_OK = 'Thank you. Do not forget to forward reports on every battle.'


MSG_TRIGGER_NEW = 'The trigger for the phrase "{}" is set.'
MSG_TRIGGER_GLOBAL = '<b>Global:</b>\n'
MSG_TRIGGER_LOCAL = '\n<b>Local:</b>\n'
MSG_TRIGGER_NEW_ERROR = 'Your thoughts are not clear, try one more time'
MSG_TRIGGER_EXISTS = 'Trigger "{}" already exists, select another one.'
MSG_TRIGGER_ALL_ENABLED = 'Now everything can call triggers.'
MSG_TRIGGER_ALL_DISABLED = 'Now only admins can call triggers.'
MSG_TRIGGER_DEL = 'The trigger for "{}" has been deleted.'
MSG_TRIGGER_DEL_ERROR = 'Where did you see such a trigger? 0_o'
MSG_TRIGGER_LIST_HEADER = 'List of current triggers: \n'


MSG_WELCOME_DEFAULT = 'Hi, %username%!'
MSG_WELCOME_SET = 'The welcome text is set.'
MSG_WELCOME_ENABLED = 'Welcome enabled'
MSG_WELCOME_DISABLED = 'Welcome disabled'


MSG_PIN_ALL_ENABLED = 'Anyone can pin'
MSG_PIN_ALL_DISABLED = 'Now only admins can pin😡'


MSG_ORDER_CLEARED_BY_DUMMY = 'The requested is being processed \
because of high server load due to continuous updates'


MSG_CLEARED = 'Done'

MSG_IN_DEV = 'Under construction=('


MSG_ALREADY_BANNED = 'This user is already banned. The reason is: {2}.'
MSG_USER_BANNED = '{} violated the rules and was kicked off!'
MSG_USER_BANNED_TRAITOR = 'Et tu, Brute? {} pledged allegiance to another clan, we will remember you!'
MSG_YOU_BANNED = 'You were banned because: {}'
MSG_BAN_COMPLETE = 'Soldier successfully banned'
MSG_USER_NOT_BANNED = 'This soldier is not banned'
MSG_USER_UNBANNED = '{} is no longer banned.'
MSG_YOU_UNBANNED = 'We can talk again 🌚'


BTN_YES = '✅YES'
BTN_NO = '❌NO'

BTN_LEAVE = 'Leave'

BTN_ACCEPT = '✅Accept'
BTN_DECLINE = '❌Decline'

MSG_LAST_UPDATE = '🕑 Last Update'
MSG_GO_AWAY = 'Go Away!'

MSG_NO_REASON = 'Reason not specified'
MSG_REASON_TRAITOR = 'User changed clans'
