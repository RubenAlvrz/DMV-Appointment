import pandas as pd
import json
import itertools


def customer_file():
    """Read Json file Customers and return to DataFrame"""

    input_file = open('CustomerData.json')
    json_array = json.load(input_file)

    id = []
    type_ = []
    duration = []

    for i in json_array['Customer']:
        id.append(i['Id'])
        type_.append(i['type'])
        duration.append(i['duration'])

        customer = [(a, b, c) for (a, b, c) in itertools.zip_longest(
            id, type_, duration)]

        customer = pd.DataFrame(customer, columns=['id', 'type', 'duration'])

    return customer


def teller_file():
    """Read Json file Teller and return to DataFrame"""

    input_file = open('TellerData.json')
    json_array = json.load(input_file)

    teller_id = []
    specialtyType = []
    multiplier = []

    for i in json_array['Teller']:
        teller_id.append(i['ID'])
        specialtyType.append(i['SpecialtyType'])
        multiplier.append(i['Multiplier'])

        teller = [(a, b, c) for (a, b, c) in itertools.zip_longest(
            teller_id, specialtyType, multiplier)]

        teller = pd.DataFrame(
            teller, columns=['ID', 'SpecialtyType', 'Multiplier'])

    return teller


def group_tellertype(df: pd.DataFrame):
    """Group all tellers by SpecialtyType and assign to list"""

    tellerStype1 = []
    tellerStype2 = []
    tellerStype3 = []
    tellerStype0 = []

    for id, val, mul in df.itertuples(index=False):

        if val == '1':

            tellerStype1.append((id, mul))

        if val == '2':
            tellerStype2.append((id, mul))

        if val == '3':
            tellerStype3.append((id, mul))

        if val == '0':
            tellerStype0.append((id, mul))

    return tellerStype1, tellerStype2, tellerStype3, tellerStype0


def get_all_appointments(customer: pd.DataFrame, tellerStype1, tellerStype2, tellerStype3, tellerStype0):
    """Create all the appointments and customer/teller by type
       At the end append all lists to a master list file all all_appointments"""

    appointment_type1 = []
    appointment_type2 = []
    appointment_type3 = []
    appointment_type4 = []

    h = 0
    x = 0
    y = 0
    n = 0

    if h < int(len(list(customer))):
        for id, val, dur in customer.itertuples(index=False):
            if val == '1':
                appointment_type1.append((tellerStype1[h], id, dur))
                h += 1
            if h == len(tellerStype1):
                h = 0

    if x < int(len(list(customer))):
        for id, val, dur in customer.itertuples(index=False):
            if val == '2':
                appointment_type2.append((tellerStype2[x], id, dur))
                x += 1
            if x == len(tellerStype2):
                x = 0

    if y < int(len(list(customer))):
        for id, val, dur in customer.itertuples(index=False):

            if val == '3':
                appointment_type3.append((tellerStype3[y], id, dur))
                y += 1
            if y == len(tellerStype3):
                y = 0

    if n < int(len(list(customer))):
        for id, val, dur in customer.itertuples(index=False):

            if val == '4':
                appointment_type4.append((tellerStype0[n], id, dur))
                n += 1
            if n == len(tellerStype0):
                n = 0

    all_appointments = []
    all_appointments.extend(appointment_type1)
    all_appointments.extend(appointment_type2)
    all_appointments.extend(appointment_type3)
    all_appointments.extend(appointment_type4)

    return all_appointments


def transform_appointments(all_appointments: list):
    """Transform the all_appointments data to provide the final information
       total time , total customers  by teller. We can also add other agg functions """

    df = pd.DataFrame(all_appointments, columns=[
                      't', 'customer_id', 'duration'])

    df['teller_id'], df['multiplier'] = zip(*df.t)

    df[["multiplier", "duration"]] = df[[
        "multiplier", "duration"]].apply(pd.to_numeric)

    df1 = df.drop(columns='t')

    df1['total_time'] = df1['duration'] * df1['multiplier']

    df_group = df1.groupby('teller_id')['total_time'].agg(['sum', 'count']).reset_index(
    ).rename(columns={"sum": "total_time", "count": "total_customers"})

    return df_group


if __name__ == "__main__":

    print('Getting Json data and lists from Customer and Teller')

    teller = teller_file()  # Get teller data

    customer = customer_file()  # Get customer data

    print('Creating all the appointments and customer/teller by type')

    tellerStype1, tellerStype2, tellerStype3, tellerStype0 = group_tellertype(
        teller)  # Get grouped teller type lists

    all_appointments = get_all_appointments(customer, tellerStype1,
                                            tellerStype2, tellerStype3, tellerStype0)  # Get all_appointments list

    print('Getting all appointments')

    final = transform_appointments(all_appointments)  # transform lists

    print('Finally transforming data to get information')

    print('The total max customers assigned is {} and min {}'.format(
        final.total_customers.max(), final.total_customers.min()))

    print('The total max time is {} and min time {}'.format(
        final.total_time.max(), final.total_time.min()))

    print('The total avg total time is {} and the avg total customer per teller {}'.format(
        final.total_time.mean(), final.total_customers.mean()))
