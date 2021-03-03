
from os import listdir, remove
def check_for_and_del_io_files():
    list_dir = listdir()
    for i in list_dir:
        if i == 'currency_pair.txt':
            remove("currency_pair.txt")
        if i == 'currency_pair_history.csv':
            remove("currency_pair_history.csv")
        if i == 'trade_order.p':
            remove("trade_order.p")
    pass
