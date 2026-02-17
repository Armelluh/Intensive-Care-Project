""" 
Module with a function to sum pending orders over time. This function can be used in the main code for the assignment.
"""
import numpy as np 

def sumPendingOrders(lengthStay, order, startTime, endTime, values, continuous, resolution=0.5):
    # Calculates the total order administration per parameter, based on start and 
    # end times as provided in TPendingOrders.
    # Inputs:
    # - lengthStay: total duration of the patient's stay at ICU
    # - order: PlannedOrderID for all orders, to see which orders are part of
    # the same PlannedOrders (e.g. only change in settings).
    # - startTime: start of the order for this parameter
    # - endTime: end of the order for this parameter
    # - values: corresponding value per start/end time combination
    # - continuous: is the order applied continuously or not?
    # - resolution (optional): time resolution in hours [default = half hour (0.5)]
    #
    # Outputs:
    # - t: time vector containing the datetime points per row
    # - summedOrder: total medication dosage for the order over entire stay

    # Default precision is half hour
    # (Already implemented with resolution default)
    
    # number of different orders
    nOrder = np.unique(order)

    # create time vector based on precision and lengthStay
    hours = lengthStay / np.timedelta64(1, 'h')
    t = np.arange(0, hours + resolution/24, resolution)  

    # Convert start/end times from timedelta64 to hours
    start_h = startTime / np.timedelta64(1, 'h')
    end_h = endTime / np.timedelta64(1, 'h')

    # If variable is continuous, an order with equal PlannedOrder is just change of settings, not a new order.
    if continuous:
    
        # create empty matrix to put in values per order over time
        summedOrder = np.zeros((len(t), len(nOrder)))

        # put values in summedOrder between start and end time
        for iorder_idx, iorder in enumerate(nOrder):
            idx = (order == iorder)

            sTime = np.append(start_h[idx], hours)
            val = values[idx]

            for iidx in range(len(sTime) - 1):
                mask = (t >= sTime[iidx]) & (t <= sTime[iidx+1])
                summedOrder[mask, iorder_idx] = val.iloc[iidx]

    # If variable is not continuous, base the total administration on start and end times
    else:
        # find orders that are positive in time (end time after start time)
        idx = (end_h - start_h) > 0
        
        # create empty matrix to put in values per order over time
        summedOrder = np.zeros((len(t), np.sum(idx)))
        
        # put values in summedOrder between start and end time
        valid_indices = np.where(idx)[0]
        for k, i in enumerate(valid_indices):
            mask = (t >= start_h.iloc[i]) & (t <= end_h.iloc[i])
            summedOrder[mask, k] = values.iloc[i]

    # sum these values over time, to get total order administration
    summedOrder = np.sum(summedOrder, axis=1)

    return t, summedOrder
