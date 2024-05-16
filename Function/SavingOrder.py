from .Utility import Order
from .Utility.ReplyMessage import SAVINGSUCCESS

def savingOrderMainFunction(message):
    BACK_TO_SELECTION_MODE = False
    try:
        Order.savingOrder()
        BACK_TO_SELECTION_MODE = True
        reply_message = SAVINGSUCCESS
        return reply_message, BACK_TO_SELECTION_MODE
    except Exception as e:
        return str(e), True