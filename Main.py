from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

from Function.Utility.ReplyMessage import SELECTION_MESSAGE
from Function.Utility.ReplyMessage import SEARCH_KEY, ADD_KEY, EDIT_KEY, SUMUP_KEY, SAVE_KEY
from Function.Utility import Order
from Function import AddOrder, EditOrder, SearchOrder, SumUpOrder, SavingOrder

# ==========================================
# 每次使用前要先執行這個 py 檔
# 接著在終端機執行 "ngrok http 5000" 來埠轉發 flask
# 然後把得到的網址貼上 Line 開發者介面中的 Webhook URL 進行 update

app = Flask(__name__)

configuration = Configuration(access_token='your token')
handler = WebhookHandler('your URL')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

#=============================================
def reply(event,reply_message):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
        )

def selectionMode(message_text:str):
    if message_text == SEARCH_KEY:
        return "SEARCH"
    elif message_text == ADD_KEY:
        return "ADD"
    elif message_text == EDIT_KEY:
        return "EDIT"
    elif message_text == SUMUP_KEY:
        return "SUMUP"
    elif message_text == SAVE_KEY:
        return "SAVING"
    else:
        return -1

def forwardingToFunction(message):
    global CURRENT_STATE
    if CURRENT_STATE == "ADD":
        return AddOrder.addingOrderMainFunction(message)
    elif CURRENT_STATE == "SEARCH":
        return SearchOrder.searchngOrderMainFunction(message)
    elif CURRENT_STATE == "EDIT":
        return EditOrder.editingOrderMainFunction(message)
    elif CURRENT_STATE == "SUMUP":
        return SumUpOrder.sumUpMainFunction(message)
    elif CURRENT_STATE == "SAVING":
        return SavingOrder.savingOrderMainFunction(message)
    
#============= INITIAL PARAMETER ==============
CURRENT_STATE = "SELECTION"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    message_text = event.message.text
    global CURRENT_STATE
    BACK_TO_SELECTION_MODE = False
    if CURRENT_STATE == "SELECTION":
        condition = selectionMode(message_text)
        if condition == -1:
            reply_message = SELECTION_MESSAGE
        else:
            CURRENT_STATE = condition
            reply_message, BACK_TO_SELECTION_MODE = forwardingToFunction(message_text)
    else:
        reply_message, BACK_TO_SELECTION_MODE = forwardingToFunction(message_text)
        
    if BACK_TO_SELECTION_MODE == True:
        CURRENT_STATE = "SELECTION"
            
    reply(event, reply_message)


    


if __name__ == "__main__":
    Order.readOrderData()
    app.run()