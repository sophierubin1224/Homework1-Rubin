from ib_insync import *
from os import listdir, remove
from time import sleep
import pickle
from helper_functions import *
# Define variables ###########################################################################################
sampling_rate = 1
# For TWS Paper account, default port is 7497
# For IBG Paper account, default port is 4002
port = 7497
# choose your master id.
master_client_id = 1
# order id
orders_client_id = 1111
# account number
acc_number = 'DU230008'
########################################################################################################################

# Run helper function to clear out any io files left over from old runs
check_for_and_del_io_files()

# Create an IB app; an instance of the IB() class from the ib_insync package
ib = IB()
# Connect app to a running instance of IBG or TWS
ib.connect(host='127.0.0.1', port=port, clientId=master_client_id)

# Make sure connected -- stay in while loop until ib.isConnected() is True.
while not ib.isConnected():
    sleep(.01)

# If connected, script proceeds and prints a success message.
print('Great Success! Very Nice!')

# Main while loop of the app. Stay in this loop until the app is stopped by the user.
while True:
    # If the app finds a file named 'currency_pair.txt' in the current directory, enter this code block.
    if 'currency_pair.txt' in listdir():
        # Code goes here...
        file = open('currency_pair.txt', 'r')
        value = file.read()
        remove("currency_pair.txt")
        contract = Forex(value)
        bars      = ib.reqHistoricalData(contract, endDateTime='', durationStr='30 D', barSizeSetting='1 hour', whatToShow='MIDPOINT', useRTH=True
            )
        df = util.df(bars)
        df.to_csv("currency_pair_history.csv")
        pass

    # If there's a file named trade_order.p in listdir(), then enter the loop below.
    if 'trade_order.p' in listdir():
        trd_ordr = pickle.load(open("trade_order.p", "rb"))
        ##fix this
        contract = Forex(trd_ordr['trade_currency'])
        order = MarketOrder(trd_ordr['action'],trd_ordr['trade_amt'], account=acc_number)
        #set account to acc_number

        # Create a special instance of IB() JUST for entering orders.
        ib_orders = IB()
        ib_orders.connect(host='127.0.0.1', port=port, clientId=orders_client_id)
        new_order = ib_orders.placeOrder(contract, order)
    # The new_order object returned by the call to ib_orders.placeOrder()
        # In this while loop, wait for confirmation that new_order filled.
        while not new_order.orderStatus.status == 'Filled':
            ib_orders.sleep(0) # we use ib_orders.sleep(0) from the ib_insync module because the async socket connection
                                   # is not built for the normal time.sleep() function.
        remove("trade_order.p")
        ib_orders.disconnect()
        pass

    # sleep for the while loop.
    ib.sleep(sampling_rate)
