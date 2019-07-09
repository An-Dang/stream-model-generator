import datetime
import time
from datetime import datetime

from input import Input
from markovchain import MarkovChain
from clustering import Clustering


states = ["INITIAL","login","View_Items","home","logout","View_Items_quantity","Add_to_Cart","shoppingcart",
          "remove","deferorder","purchasecart","inventory","sellinventory","clearcart","cancelorder","$"]

# Data imports
PATH = "../data/raw/"
sessions_file = (PATH+'sessions.dat')


# main-method
if __name__ == '__main__':

    #TODO: Summary for time, reuse past clustering

    start_time = datetime.now()
    # Input data
    input = Input(sessions_file)
    print('load data done', datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    start, stop = 0, 1000
    step_size = 500
    iteration = 5
    diff_dict = {}
    for _ in enumerate(range(iteration)):
        print("Iteration:", _)
        if _ == (0, 0):
            pass
        else:
            start += step_size
            stop += step_size

        # Slice sessions @sessions(None, None)
        next_step = input.sessions(start, stop)

        if _ >= (1, 1):
            past_start = (start-step_size)
            past_stop = (stop-step_size)
            past_step = input.sessions(past_start, past_stop)

            # Compute transition matrix next
            mc_next = MarkovChain(next_step, states)
            mc_next = mc_next.csr_sparse_matrix()

            # Compute transition matrix past
            mc_past = MarkovChain(past_step, states)
            mc_past = mc_past.csr_sparse_matrix()

            print('matrix done', datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
            print('start clustering')

            # DBSCAN
            dbscan_next = Clustering(mc_next)
            dbscan_past = Clustering(mc_past)

            print("End clustering", datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), '\n')

            # Compute the clustering compromise
            result1 = dbscan_next.compare_results()
            result2 = dbscan_past.compare_results()
            print('result_1:', result1)
            print('result_2:', result2)

            tmp = []

            for key in result1:
                tmp.append(key)
                if key in result2:
                    diff_dict[key] = (result1[key] - result2[key])

            if len(tmp) != len(result2):
                for key in result2:
                    if key not in result1.keys():
                        diff_dict[key] = result2[key]
            print(diff_dict)
            break

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))