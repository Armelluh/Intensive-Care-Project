
############################################################
# Python assignment for course KT3401                     #
# 'Intensive Care and Computer Simulation'                #
# Week 1: Reconstruct patient status from                 #
# a database with clinical variables                      #
#                                                         #
# Author: Thijs Perenboom - Dec 2016                      #
# 1st revision: Nico Jansen - Dec 2018                    #
# 2nd revision: Nico Jansen - Nov 2019                    #
# 3rd revision: Michel Hu/Susana Jorge - October 2020     #
# 4th revision: Floor Hiemstra, Fleur Brouwer & Siri vd   #
# Meijden - Sept 2022                                     #
# 5th revision: Floor Hiemstra & Floor Smits - Sept 2024  #
############################################################


import pandas as pd
import matplotlib.pyplot as plt
from sumorders import sumPendingOrders

############################################################
## Part 1: Patients at the ICU
############################################################
# Seven patients are included, as example we're looking at patient #1 with
# PatientID = 107032. This ID is used as 'key' across databases, and can be
# used to select data for this specific patient.

# load table TPatients (be sure to add the data folder to your Python path)
TPatients = pd.read_csv('TPatients.csv')

# Hint: use parse_dates to load dates as datetime objects directly. You can look in the 
# pandas documentation how to do this. Look for the correct columns to parse as dates.

# Show the PatientID's in the table TPatients. Pandas DataFrames can be indexed
# by using '''' as separator:
allPatients = TPatients['PatientID'].values
#print(allPatients)

## Determine the time patient 1 stayed at the ICU
# Hint: extract the useful data from the table by using PatientID as an
# indexing tool.
# Indexing example: you want to index in a simple list of 
# Years = [1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999]
# Years[2]  # This will extract only the 3rd element of list Years
# Output: 1994

admDate = TPatients.loc[TPatients['PatientID'] == allPatients[4], "AdmissionDate"].values[0]
endDate = TPatients.loc[TPatients['PatientID'] == allPatients[4], "DischargeDate"].values[0]  # add your calculation
lengthStay = pd.to_datetime(endDate) - pd.to_datetime(admDate)  # add your calculation

# Hint: you may need to convert the date strings to datetime objects using 
# pd.to_datetime(date_string)

# You'll find this patient stayed at the ICU for almost 76 hrs
lengthStay_hours = lengthStay.total_seconds() / 3600
print(f'This patient ({allPatients[4]}) stayed at the ICU for {lengthStay_hours} hours')

############################################################
## Part 2: Measured parameters and their units: weight of patient
############################################################
# In table TSignals, all measurements on the patients are combined. The
# measured parameter is coded for by ParameterID, that is coupled to the
# table TParameters (here you can find ParameterName and UnitID). Each
# measurement has a Time of measurement and corresponding Value. UnitID is
# coupled to table TUnits, where UnitName (e.g. mg, degree Celsius etc) and
# conversion parameters are stored.
#
# First, let's find the weight of patient 1 by loading TSignals, TUnits and
# TParameters
TSignals = pd.read_csv('TSignals.csv')
TUnits = pd.read_csv('TUnits.csv')
TParameters = pd.read_csv('TParameters.csv')

# We will extract the weight from TSignals for patient 1, by looking for
# ParameterID == 80. You can verify that this ID is correct by finding the
# ParameterName corresponding to ParameterID 80.

# This should plot 'Gewicht' (i.e. Weight)
#print(TParameters.loc[TParameters['ParameterID'] == 80, 'ParameterName'])

# Unit of weight: first get the UnitID from TParameters using ParameterID, then 
# check corresponding UnitName in TUnits.
# weightUnitID = TParameters.loc[TParameters['ParameterID'] == 80, 'UnitID']
# weightUnit = TUnits.loc[TUnits['UnitID'] == weightUnitID.values[0], 'UnitName']
#
# # Weight of the first patient, use PatientID and (&) ParameterID
# patWeight = TSignals.loc[(TSignals['PatientID'] == allPatients[0]) & (TSignals['ParameterID'] == 80), 'Value']  # Fill in condition
# #print(patWeight)
#
# # You should see a variable with size 7x1 with value 95000, indicating that the weight
# # was measured multiple times during the ICU stay. Also extract the times
# # of measurement from table TSignals to check if this is correct.
# weightTimes = TSignals.loc[(TSignals['PatientID'] == allPatients[0]) & (TSignals['ParameterID'] == 80), 'Time']
#
# # You probably noticed that the weight unit (kg) and the Value in TSignals do
# # not correspond because that would mean that the patient has a weight of 95000kg!.
# # Therefore, you have to convert the Value by subtracting
# # "TUnits.Addition" and subsequently dividing by "TUnits.Multiplier". This
# # conversion should be done for every parameter you will later extract from
# # the database!
#
# weightAddition =  TUnits.loc[TUnits['UnitID'] == weightUnitID.values[0], 'Addition']
# weightMultiplier = TUnits.loc[TUnits['UnitID'] == weightUnitID.values[0], 'Multiplier']
#
# # Apply the addition and then multiplication correction to scale to
# # UnitName, resulting in the correct patient's weight (95 kg)
# patWeight = (patWeight - weightAddition.values[0]) / weightMultiplier.values[0]
# #print(f"\nThe weight of this patient is: {patWeight.iloc[0]:.1f} kg")
#
# # ############################################################
# # ## Part 3: Changing measurements over time: cardiac output
# # ############################################################
# # # You are now able to find a specific measurement from a patient and convert
# # # it. Let's plot changes in the signal over time, by looking at the Cardiac
# # # output of patient 107032. Cardiac output has parameterID = 27 and is also
# # # stored in TSignals.
# #
# # # Get the values and timepoints of cardiac output from patient 107032
# # values = TSignals.loc[(TSignals['PatientID'] == allPatients[0]) & (TSignals['ParameterID'] == 27), 'Value']
# # time = TSignals.loc[(TSignals['PatientID'] == allPatients[0]) & (TSignals['ParameterID'] == 27), 'Time']
# #
# # # For plotting purposes, it is easier to subtract the admission time from
# # # the timepoints. In that way, your plot starts at 0 and you don't have to
# # # bother with dates.
# # # It is possible that you need to convert the time difference to hours.
# # # For example by adding: .astype("timedelta64[s]").astype(float) / 3600.
# # # This depends on how you loaded the dates in earlier parts.
# # time_sub = pd.to_datetime(time) - pd.to_datetime(admDate)
# # time = time_sub.dt.total_seconds() / 3600
# #
# # # Get the unit of cardiac output from TUnits, to use as y-label
# # signal_unitID =  TParameters.loc[TParameters['ParameterID'] == 27, 'UnitID'].values[0]
# # signal_unit = TUnits.loc[TUnits['UnitID'] == signal_unitID, 'UnitName'].values[0]
# # # And the name of the parameter from TParameters, to use as plot title
# # signal_name = TParameters.loc[TParameters['ParameterID'] == 27, 'ParameterName'].values[0]
# #
# # # Convert the values using the addition and multipliers
# # signal_addition = TUnits.loc[TUnits['UnitID'] == signal_unitID, 'Addition'].values[0]
# # signal_multiplier = TUnits.loc[TUnits['UnitID'] == signal_unitID, 'Multiplier'].values[0]
# # values = (values - signal_addition) / signal_multiplier
# #
# # # Now let's plot! You can mark each measurement, or draw lines, or a
# # # combination. Also experiment with line width and line types.
# # plt.figure()
# # plt.plot(time, values, 'o-', label=signal_name)
# # plt.xlabel('Time (hours)')
# # plt.ylabel(signal_unit)
# # plt.title(f'Patient {allPatients[0]}: {signal_name}')
# # plt.legend()
# #
# # # If you plot more than one parameter (e.g. using subplots), it is useful
# # # to have the same x-axis. What would be a good range to plot of these
# # # values, that's comparable over all parameters?
# # plt.xlim(0, lengthStay_hours)
# # plt.grid()
# # #plt.show()

############################################################
## Part 4: plotting of multiple parameters
############################################################
# Other parameters then Cardiac output are also of interest to check the
# hemodynamic status of patients. Use a for-loop over multiple
# parameterID's to (sub)plot all these values by combining the steps you've
# seen before.

# ParameterID's of interest are: 10, 13, 27, 326, 627, 7500, 7518
# Note that not all parameters are measured in all patients, so think of a
# way to use a loop even when a parameter is not measured (hint: you can
# check if the values vector are 'empty' and in that case 'continue' 
# the loop).

# Example of a for loop
# You can use a for loop to repeat a certain action
# Here we have a simple for loop where we want to add +1 to each element in
# a list that is 10 elements long
# (P.S. if you want to continue coding in Python, these types of for loops
# are usually not recommended because you can use vectorized operations
# with libraries like NumPy, which are much faster. This example is only
# meant to illustrate what a for loop is.)

# test = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# new = []
# for i in range(10):
#     new.append(test[i] + 1)

def plot_multiple_param(parameterIDs, patient_number):
    # 1. Identify the correct patient
    current_patient_id = allPatients[patient_number]
    print(f"Plotting for Patient ID: {current_patient_id}")

    # 2. Get the admission date for THIS specific patient
    # Casting to pd.to_datetime immediately prevents calculation errors later
    adm_date_raw = TPatients.loc[TPatients['PatientID'] == current_patient_id, "AdmissionDate"].values[0]
    admDate = pd.to_datetime(adm_date_raw)

    plt.figure(figsize=(12, 16))
    plt.suptitle(f'Hemodynamic Status - Patient: {current_patient_id}')

    axes = []
    plot_count = 0

    for prmID in parameterIDs:
        # 3. Create a mask for the specific Patient AND Parameter
        mask = (TSignals['PatientID'] == current_patient_id) & (TSignals['ParameterID'] == prmID)

        if not any(mask):
            print(f"ID {prmID}: No data found for this patient. [x]")
            continue

        # 4. Extract data
        # We use .copy() to avoid SettingWithCopy warnings when we manipulate values
        p_data = TSignals.loc[mask].copy()

        # 5. Convert Time to hours since admission
        p_data['Time'] = pd.to_datetime(p_data['Time'])
        p_data['Hours'] = (p_data['Time'] - admDate).dt.total_seconds() / 3600

        # 6. Lookup Units and Name
        signal_name = TParameters.loc[TParameters['ParameterID'] == prmID, 'ParameterName'].values[0]
        unitID = TParameters.loc[TParameters['ParameterID'] == prmID, 'UnitID'].values[0]

        unit_info = TUnits.loc[TUnits['UnitID'] == unitID]
        unit_name = unit_info['UnitName'].values[0]
        multiplier = unit_info['Multiplier'].values[0]
        addition = unit_info['Addition'].values[0]

        # 7. Apply conversion
        p_data['ConvertedValue'] = (p_data['Value'] - addition) / multiplier

        # 8. SORT DATA BY TIME
        # This is the most common reason for messy plots in clinical databases
        p_data = p_data.sort_values(by='Hours')

        # 9. Plotting
        plot_count += 1
        ax = plt.subplot(len(parameterIDs), 1, plot_count)
        axes.append(ax)

        ax.plot(p_data['Hours'], p_data['ConvertedValue'], label=signal_name)
        ax.set_ylabel(unit_name)
        ax.set_title(f"{signal_name} (ID: {prmID})")
        ax.grid(True, alpha=0.3)

        # Share x-axis with the first plot
        if len(axes) > 1:
            ax.sharex(axes[0])

    # Final formatting
    if axes:
        axes[-1].set_xlabel('Time since Admission (hours)')
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()
    else:
        print("No plots generated. Check if ParameterIDs exist for this patient.")

    # Example usage:
    # keywords = ['Cardiac Output', 'Heart rate']
    # p_ids = find_parameter(keywords)
    # plot_multiple_param(p_ids, patient_number=4)

    # Link all subplots along the x-axis


    axes = []
# parameterIDs = [10, 13, 27, 326, 627, 7500, 7518]

    # for iprm in range(len(parameterIDs)):
    #     if not any(TSignals['ParameterID'] == parameterIDs[iprm]):
    #         continue
    #     # Get all relevant information about the parameter
    #     values = TSignals.loc[(TSignals['PatientID'] == allPatients[0]) & (TSignals['ParameterID'] == parameterIDs[iprm]), 'Value']
    #     time = TSignals.loc[(TSignals['PatientID'] == allPatients[0]) & (TSignals['ParameterID'] == parameterIDs[iprm]), 'Time']
    #
    #     time_sub = pd.to_datetime(time) - pd.to_datetime(admDate)
    #     time = time_sub.dt.total_seconds() / 3600
    #
    #
    #     signal_unitID =  TParameters.loc[TParameters['ParameterID'] == parameterIDs[iprm], 'UnitID'].values[0]
    #     signal_unit = TUnits.loc[TUnits['UnitID'] == signal_unitID, 'UnitName'].values[0]
    #
    #     signal_name = TParameters.loc[TParameters['ParameterID'] == parameterIDs[iprm], 'ParameterName'].values[0]
    #
    #     signal_addition = TUnits.loc[TUnits['UnitID'] == signal_unitID, 'Addition'].values[0]
    #     signal_multiplier = TUnits.loc[TUnits['UnitID'] == signal_unitID, 'Multiplier'].values[0]
    #     values = (values - signal_addition) / signal_multiplier
    #
    #     # Create subplot and store axis handle
    #     ax = plt.subplot(len(parameterIDs), 1, iprm + 1)
    #     axes.append(ax)
    #
    #     # Do all your plotting per parameter here
    #     ax.plot(time, values, '-', label=signal_name)
    #     ax.set_xlabel('Time of stay (hours)')
    #     ax.set_ylabel(signal_unit)
    #     ax.set_title(f'Patient {allPatients[0]}: {signal_name}')
    #     ax.legend()
    #     ax.grid()
    #
    #
    # # Link all subplots along the x-axis
    #     for ax in axes[1:]:
    #         ax.sharex(axes[0])
    #     #plt.show()
    #     plt.tight_layout()


############################################################
## Part 5: Plotting of Pending Orders: dobutamine
############################################################
# Not only can we plot signals that are measured, also pending orders are of
# interest to monitor the hemodynamic status of patients. Examples are the
# administration of medication like dobutamine, or blood transfusions.
# These values are stored in tables TPendingOrders, TPendingRangeSignals,
# TPlannedOrders. The last table we need is TDripUnits, containing
# information about the time parameter of the order (e.g. per minute, per
# hour etc).

# Load the relevant tables
TPendingOrders = pd.read_csv('TPendingOrders.csv')
TPendingRangeSignals = pd.read_csv('TPendingRangeSignals.csv')
TPlannedOrders = pd.read_csv('TPlannedOrders.csv')
TDripUnits = pd.read_csv('TDripUnits.csv')

# Dobutamine has parameterID 363, define as variable for later use
prmID = 363

# TPendingRangeSignals contains StartTime, EndTime and Values of the
# orders, and the corresponding DripUnitID to look up in TDripUnits.
# However, we only have to look at orders with Status == 2 in
# TPendingOrders, only these are really performed (and not just ordered).

# Here, we will combine both tables, by joining them using PendingOrderID
TPending = pd.merge(TPendingOrders, TPendingRangeSignals, on='PendingOrderID')

# From the created table TPending, lookup the StartTime, EndTime and
# Values for each Order, based on PatientID, ParameterID (dobutamine in this case) and Status. First,
# you can create an indices variable as you need the same indices (of all the
# times that the same order is given) multiple times.
idcs = TPending.loc[(TPending['PatientID'] == allPatients[0]) & (TPending['ParameterID'] == prmID) & (TPending['Status'] == 2)].index

startTime = pd.to_datetime(TPending.loc[idcs, 'StartTime']) - pd.to_datetime(admDate)
endTime = pd.to_datetime(TPending.loc[idcs, 'EndTime']) - pd.to_datetime(admDate)

# Correct values extraction: it should come from TPending (which includes TPendingRangeSignals' Value),
# not TSignals, and should correspond to the specific pending order identified by 'idcs'.
values = TPending.loc[idcs, 'Value']

# Also find the parameter's name in TParameters
signal_name = TParameters.loc[TParameters['ParameterID'] == prmID, 'ParameterName'].values[0]

# And lookup the UnitName and conversion factors
signal_unitID = TParameters.loc[TParameters['ParameterID'] == prmID, 'UnitID'].values[0]
signal_unit = TUnits.loc[TUnits['UnitID'] == signal_unitID, 'UnitName'].values[0]
signal_multiplier = TUnits.loc[TUnits['UnitID'] == signal_unitID, 'Multiplier'].values[0]
signal_addition = TUnits.loc[TUnits['UnitID'] == signal_unitID, 'Addition'].values[0]

# These values also have a time depending component, that can be found in
# TDripUnits. But not all parameters have a dripUnit, so you have to
# account for this by checking if the value is not 'isempty'. First find
# the corresponding timeUnitID in TDripUnits with the DripUnitID, this timeUnitID
# can be checked again in TParameters as UnitID to find the unit name.


if not TDripUnits.loc[TDripUnits['DripUnitID'] == TPending.loc[idcs, 'DripUnitID'].unique()[0]].empty:
                signal_timeUnitID = TDripUnits.loc[TDripUnits['DripUnitID'] == TPending.loc[idcs, 'DripUnitID'].unique()[0],'TimeUnitID'].values[0]
                signal_unit_time = TUnits.loc[TUnits['UnitID'] == signal_timeUnitID, 'UnitName'].values[0]
                signal_dripUnit_multiplier = TUnits.loc[TUnits['UnitID'] == signal_timeUnitID, 'Multiplier'].values[0]
                signal_dripUnit_addition = TUnits.loc[TUnits['UnitID'] == signal_timeUnitID, 'Addition'].values[0]

# Apply the value conversion, by first converting for the Unit and then for
# DripUnit. Note that DripUnit is defined 'per time', and should therefore
# not divided by the multiplier, but multiplied by this number.
values = (values - signal_addition) / signal_multiplier
values = (values - signal_dripUnit_addition) * signal_dripUnit_multiplier

# Some of these parameters are administered on a continuous time scale,
# while others are provided just once per order. This is registered in the
# table TPlannedOrders by the variable "Continuous". First lookup the
# PlannedOrderID's for all relevant orders in table TPending (hint: use
# your earlier defined "idcs" again).
signal_plannedOrder = TPending.loc[idcs, 'PlannedOrderID']
#signal_plannedOrder = TPlannedOrders.loc[TPlannedOrders['PlannedOrderID'] == PlannedOrderIDs, 'PlannedOrderID']

# Here we check if a parameter is continuously is administered or not
if not signal_plannedOrder.empty:

    signal_continuous = TPlannedOrders.loc[TPlannedOrders['PlannedOrderID'] == signal_plannedOrder.iloc[0], 'Continuous'].values[0]
else:
    signal_continuous = 0   # You can leave this 0 as is, it should be there.

# By now, you have all information needed to calculate the administration of
# dobutamine. This is done by looking at the Value and Time points over
# the entire stay at the ICU.

# Calculate the total medication dosage over time using the function
# sumPendingOrders that was already created for you in the module sumorders.
# Check its code to see how to call the function, what it returns and how it works.
# Try changing the 'resolution' parameter to see what the effect is.


[timeVec, summedOrder] = sumPendingOrders(lengthStay, signal_plannedOrder, startTime, endTime, values, signal_continuous, 0.25)
#
# # Now you can plot the output of sumPendingOrders as you did with the
# # values from TSignals. Again, try different settings to find out what is
# # the best option for plotting this data.
# plt.figure()
# plt.plot(timeVec, summedOrder, linestyle='-', label=signal_name)
#
#
# # The y-label is a bit more complicated, because you also need to include
# # the DripUnit. You can build the label using an f-string inside ax.set_ylabel().
# # Make sure that signal_unit and signal_unit_time are strings; if they come
# # from a pandas DataFrame, they usually already are. Otherwise, convert them
# # using str().
# # Only include signal_unit_time in the label if it was successfully found
# y_label_text = f"{signal_name} ({signal_unit}/{signal_unit_time})" if signal_unit_time else f"{signal_name} ({signal_unit})"
# plt.ylabel(y_label_text)
# plt.title(f'{signal_name} administration for Patient {allPatients[0]}')
# plt.xlabel('Time from Admission (hours)')
# # plt.xlim([0, ])
# plt.grid(True)
# plt.legend()
# plt.show()

############################################################
## Part 6: Overview of pending orders
############################################################
# Other administrations then dobutamine output are also of interest to check the
# hemodynamic status of patients. Use a for-loop over multiple
# parameterID's to (sub)plot all these values by combining the steps you've
# seen before.
pIDS = [363, 8218, 8202, 18054]
# ParameterID's of interest are: 363, 8218, 8202, 18054
# Note that not all parameters are measured in all patients, so think of a
# way to use a loop even when a parameter is not measured (hint: you can
# check if the returned value vector 'isempty').
def plot_multiple_pending(pIDS,patient):
    plt.figure(figsize=(12, 16))
    plt.suptitle(f'Patient: {allPatients[patient]}')
    axes = []

    for idx, prmID in enumerate(pIDS):
        idcs = TPending.loc[(TPending['PatientID'] == allPatients[patient]) & (TPending['ParameterID'] == prmID) & (TPending['Status'] == 2)].index

        signal_name = TParameters.loc[TParameters['ParameterID'] == prmID, 'ParameterName'].values[0]

        if idcs.empty:
            print(f"No instances of {signal_name} (ID: {prmID}) for patient {allPatients[patient]}")
            continue

        print(f"Plotting {signal_name} for patient {allPatients[patient]}...")
        startTime = pd.to_datetime(TPending.loc[idcs, 'StartTime']) - pd.to_datetime(admDate)
        endTime = pd.to_datetime(TPending.loc[idcs, 'EndTime']) - pd.to_datetime(admDate)
        values = TPending.loc[idcs, 'Value']

        signal_name = TParameters.loc[TParameters['ParameterID'] == prmID, 'ParameterName'].values[0]
        signal_unitID = TParameters.loc[TParameters['ParameterID'] == prmID,'UnitID'].values[0]
        signal_unit = TUnits.loc[TUnits['UnitID'] == signal_unitID, 'UnitName'].values[0]

        signal_multiplier = TUnits.loc[TUnits['UnitID'] == signal_unitID, 'Multiplier'].values[0]
        signal_addition = TUnits.loc[TUnits['UnitID'] == signal_unitID,'Addition'].values[0]


        if len(TPending.loc[idcs, 'DripUnitID'].unique()) > 0:
            if not TDripUnits.loc[TDripUnits['DripUnitID'] == TPending.loc[idcs, 'DripUnitID'].unique()[0]].empty:
                signal_timeUnitID = TDripUnits.loc[TDripUnits['DripUnitID'] == TPending.loc[idcs, 'DripUnitID'].unique()[0], 'TimeUnitID'].values[0]
                signal_unit_time = TUnits.loc[TUnits['UnitID'] == signal_timeUnitID,'UnitName'].values[0]
                signal_dripUnit_multiplier = TUnits.loc[TUnits['UnitID'] == signal_timeUnitID,'Multiplier'].values[0]
                signal_dripUnit_addition = TUnits.loc[TUnits['UnitID'] == signal_timeUnitID,'Addition'].values[0]
            else:
                print(f"T{Pending.loc[idcs, 'DripUnitID']} is empty for patient {allPatients[patient]}")
                continue
        else:
            print(f"T{Pending.loc[idcs, 'DripUnitID']} is empty for patient {allPatients[patient]}")
            continue

        values = (values - signal_addition) / signal_multiplier
        values = (values - signal_dripUnit_addition) * signal_dripUnit_multiplier

        signal_plannedOrder = TPending.loc[idcs, 'PlannedOrderID']

        if not signal_plannedOrder.empty:
            signal_continuous = TPlannedOrders.loc[TPlannedOrders['PlannedOrderID'] == signal_plannedOrder.iloc[0], 'Continuous'].values[0]
        else:
            signal_continuous = 0

        timeVec, summedOrder = sumPendingOrders(lengthStay, signal_plannedOrder, startTime, endTime, values, signal_continuous, 0.25)


        ax = plt.subplot(len(pIDS), 1, idx + 1)
        axes.append(ax)

        y_label_text = (f"{signal_name} ({signal_unit}/{signal_unit_time})" if signal_unit_time else f"{signal_name} ({signal_unit})")

        ax.plot(timeVec, summedOrder, linestyle='-', label=signal_name)
        ax.set_xlabel('Time from Admission (hours)')
        ax.set_ylabel(y_label_text)
        ax.set_title(f'Patient {allPatients[patient]}: {signal_name}')
        ax.set_xlim([0, lengthStay_hours])
        ax.legend()
        ax.grid()

    if len(axes) > 1:
        for ax in axes[1:]:
            ax.sharex(axes[0])

    plt.tight_layout()
    plt.show()
    plt.tight_layout()
    plt.show()


############################################################
## Part 7: Other parameters of interest for assessment of hemodynamic status
############################################################
# So far, we have plotted parameters using the ParameterID. However, other
# parameters may be of relevance of assessment of hemodynamic status in
# this patient. For example, one potential parameter would be heart rate.

# In order to find the relevant ParameterID for heart rate, you can use the 
# function 'contains()' (hint: note that you can search for parts of a string).
# prmIDi = TParameters['ParameterName'].str.contains('Cardiac output', case=False, na=False)
# prmIDs = TParameters.loc[prmIDi,'ParameterID']
# # print(prmID)

def find_parameter(keywords):
    found_prmIDs = []
    for keyword in keywords:
        prmIDi = TParameters['ParameterName'].str.contains(keyword, case=False, na=False)
        matched_params = TParameters.loc[prmIDi, ['ParameterID', 'ParameterName']]
        print()
        print(f"Found the following parameters for keyword {keyword}:")
        prmIDs = matched_params['ParameterID'].unique().tolist()
        found_prmIDs.extend(prmIDs)
        for index, row in matched_params.iterrows():
            print(f"ID: {row['ParameterID']} - Name: {row['ParameterName']}")
    print()

    return found_prmIDs

keywords = ['spo2']
# find_parameter(keywords)

# plot_multiple_param(find_parameter(keywords),patient_number = 0)
# plot_multiple_pending(pIDS = find_parameter(keywords),patient = 4)
plot_multiple_param([18],patient_number = 0)
# plot_multiple_pending(pIDS = [326],patient = 0)

#prmIDi = TParameters['ParameterName'].str.contains([], case=False, na=False)
#print(TParameters[prmIDi])

# Now that you have found the relevant ParameterIDs, plot its values as you
# did for cardiac output in part 4 (or part 3 if you have a single parameter to plot).

# What other parameters may be informative for evaluating the hemodynamic 
# status of patients? Use the steps above to recover the ParameterIDs of
# these parameters and plot them.
