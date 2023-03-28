import pandas as pd

#Function to remove leading and trailing spaces
def removeLTspaces(s):
    start_index = 0
    stop_index = 0
    for i in range(len(s)):
        if s[i]!=' ':
            start_index = i
            break
    for i in range(len(s)-1,0,-1):
        if s[i]!=' ':
            stop_index = i+1
            break
    return s[start_index:stop_index]

def process(df):
    semester_value = 'CH2022231'
    column_names = ['route_name', 'registration_number', 'student_name', 'student_name', 'gender',
                    'destination', 'fp_reference_number']

    # Set the Semester value for NaN value
    #df['semester'] = df['semester'].apply(lambda x: semester_value)

    # Convert all values to UPPERCASE
    df['route_name'] = df['route_name'].apply(lambda x: 'NOT FOUND' if type(x)==float else x.upper())
    df['student_name'] = df['student_name'].apply(lambda x: 'NOT FOUND' if type(x)==float else x.upper())
    df['destination'] = df['destination'].apply(lambda x: 'NOT FOUND' if type(x)==float else x.upper())

    # Remove \xa0, empty_space from the route_name, and destination
    df['route_name'] = df['route_name'].apply(lambda x: removeLTspaces(x.replace('\xa0', '').replace(',', '')))
    df['destination'] = df['destination'].apply(lambda x: removeLTspaces(x.replace('\xa0', '').replace(',', '')))

    # Correct the typos in the Route_names
    df['route_name'] = df['route_name'].apply(lambda x: x.replace('ADAYAR AAVIN', 'ADYAR AAVIN'))
    df['route_name'] = df['route_name'].apply(lambda x: x.replace('ANNA NAGAR ROUNDTANA', 'ANNA NAGAR ROUNTANA'))
    df['route_name'] = df['route_name'].apply(lambda x: x.replace('AYYANAVARAM', 'AYANAVARAM'))
    df['route_name'] = df['route_name'].apply(lambda x: x.replace('AYANVAVARAM', 'AYANAVARAM'))
    df['route_name'] = df['route_name'].apply(lambda x: x.replace('MANDEVELI', 'MANDAVELI'))
    df['route_name'] = df['route_name'].apply(lambda x: x.replace('MOOLAKKADAI', 'MOOLAKADAI'))
    df['route_name'] = df['route_name'].apply(lambda x: x.replace('REDHILLS', 'RED HILLS'))
    df['route_name'] = df['route_name'].apply(lambda x: 'RAMAPURAM JUNCTION' if x == 'RAMAPURAM' else x)
    df['route_name'] = df['route_name'].apply(
        lambda x: 'PERAMBUR CHURCH' if x == 'PERAMBUR' or x == 'PARAMBUR CHURCH' else x)
    df['route_name'] = df['route_name'].apply(
        lambda x: 'ANNA NAGAR ROUNTANA' if x == 'ANNA NAGAR ROUNDTANA' or x == 'ANNANAGAR ROUNDTANA' else x)
    df['route_name'] = df['route_name'].apply(lambda x: 'ANNA NAGAR' if x == 'ANNANAGAR' else x)
    df['route_name'] = df['route_name'].apply(lambda x: 'NATRAJA THEATER' if x == 'NATRAJ THEATRE' else x)

    # Correct the typos in the destination_names
    df['destination'] = df['destination'].apply(lambda x: x.replace('VANNANTHURAI', 'VANNANDURAI'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('ADAYAR AAVIN', 'ADYAR AAVIN'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('ADAYAR DEPOT.', 'ADYAR DEPOT'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('AMJIGIKARAI', 'AMINJIKARAI'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('AVICHI SCHOOLL', 'AVICHI SCHOOL'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('AYANVAVARAM', 'AYANAVARAM'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('CHROMPETBUS STAND', 'CHROMPET BUS STAND'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('KASI THEATER', 'KASI THEATRE'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('KELAMPAKKAM', 'KELAMBAKKAM'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('LIBERTY.', 'LIBERTY'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('PERUGALATHUR', 'PERUNGALATHUR'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('PADUR HINDUSTAN CLG', 'PADUR HINDUSTAN COLLEGE'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('SOLINGANALLUR', 'SHOLINGANALLUR'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('SHOLINGANALUR', 'SHOLINGANALLUR'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('ANNA NAGAR ROUNDTANA', 'ANNA NAGAR ROUNTANA'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('AVACHI SCHOO', 'AVICHI SCHOOL'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('AVACHI SCHOOLL', 'AVICHI SCHOOL'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('AYANAVARAM(ESI HSPTL)', 'AYANAVARAM'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('ESI HOSPITEL', 'ESI HOSPITAL'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('SHANTHI  COLANI', 'SHANTHI  COLONY'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('NATHAMUNI', 'NADHAMUNI'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('KK NAGAR BUS DEPOT.', 'KK NAGAR DEPOT'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('CHROMPET - BUS STAND', 'CHROMPET BUS STAND'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('VELACHERRY BUS STAND', 'VELACHERY  BUS STAND'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('MAPPED', 'MAPPEDU'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('SENTIL NAGAR', 'SENTHEL NAGAR'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('SENTHIL NAGAR', 'SENTHEL NAGAR'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('SHOLINGANALUR', 'SHOLINGANALLUR'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('THIRUVANMAYUR JAYANTHI', 'THIRUVANMIYUR JAYANTHI'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('PERUNKALATHUR', 'PERUNGALATHUR'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('MGR UNIVERCITY', 'MGR UNIVERSITY'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('AMBATHUR OT', 'AMBATTUR OT'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('THIRU.VI.KA.NAGAR', 'THIRU. VI.KA NAGAR'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('SARAVANA STORES(PORUR', 'SARAVANA STORE (PORUR)'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('AYOTHYA MANDAPAM', 'AYODHYA MANDAPAM'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('GANDHIMANDABAM', 'GANDHI MANDAPAM'))
    df['destination'] = df['destination'].apply(lambda x: x.replace('VIT UNIVERSITY', 'VIT'))
    df['destination'] = df['destination'].apply(lambda x: 'VIT' if x == 'VIT UNIVERSTIY' else x)
    df['destination'] = df['destination'].apply(lambda x: x.replace('VELACHERRY', 'VELACHERY'))
    df['destination'] = df['destination'].apply(lambda x: 'MANDAVELI BSNL OFFICE' if x == 'MADAVELI BSNL' else x)
    df['destination'] = df['destination'].apply(lambda x: 'MEDAVAKKAM' if x == 'MEDAVAKKAM      ( LEFT  )' else x)
    df['destination'] = df['destination'].apply(lambda x: 'RETTERI' if x == 'RETTERI JUNCTION' else x)
    df['destination'] = df['destination'].apply(lambda x: 'EKKATUTHANGAL' if x == 'EKKATTU THANGAL' else x)
    df['destination'] = df['destination'].apply(lambda x: 'RETTERI' if x == 'RETTERIJUNCTION' else x)
    df['destination'] = df['destination'].apply(
        lambda x: 'IYYAPPANTHANGAL' if x == 'IYYANPANTHANGAL' or x == 'AYYAPPANTHANGAL' else x)
    df['destination'] = df['destination'].apply(
        lambda x: 'MAPPEDU' if x == 'MAPPEDUUUUUUU' or x == 'MAPPEDUUUUUUUU' else x)
    df['destination'] = df['destination'].apply(
        lambda x: 'IYYAPPANTHANGAL' if x == 'IYYANPANTHANGAL' or x == 'AYYAPPANTHANGAL' else x)
    df['destination'] = df['destination'].apply(
        lambda x: 'IYYAPPANTHANGAL' if x == 'IYYANPANTHANGAL' or x == 'AYYAPPANTHANGAL' else x)

    # Sort the values in the dataframe
    df = df.sort_values(by=['route_name', 'destination', 'registration_number', 'student_name'])


    # print(df['semester'].isna().sum())
    return df

def fatprocess(df):

    df['slot_name'] = df['slot_name'].apply(lambda x: 'A1+TA1' if x=='A+TA' else x)
    df['slot_name'] = df['slot_name'].apply(lambda x: 'B1+TB1' if x=='B+TB' else x)
    df['slot_name'] = df['slot_name'].apply(lambda x: 'C1+TC1' if x=='C+TC' else x)
    df['slot_name'] = df['slot_name'].apply(lambda x: 'D1+TD1' if x=='D+TD' else x)
    df['slot_name'] = df['slot_name'].apply(lambda x: 'E1+TE1' if x=='E+TE' else x)
    df['slot_name'] = df['slot_name'].apply(lambda x: 'F1+TF1' if x=='F+TF' else x)

    df['slot_name'] = df['slot_name'].apply(lambda x: 'A1+TA1+TAA1' if x=='A+TA+TAA' else x)
    df['slot_name'] = df['slot_name'].apply(lambda x: 'B1+TB1+TBB1' if x=='B+TB+TBB' else x)
    df['slot_name'] = df['slot_name'].apply(lambda x: 'C1+TC1+TCC1' if x=='C+TC+TCC' else x)
    df['slot_name'] = df['slot_name'].apply(lambda x: 'D1+TD1+TDD1' if x=='D+TD+TDD' else x)
    df['slot_name'] = df['slot_name'].apply(lambda x: 'E1+TE1+TEE1' if x=='E+TE+TEE' else x)
    df['slot_name'] = df['slot_name'].apply(lambda x: 'F1+TF1+TFF1' if x=='F+TF+TFF' else x)

    return df