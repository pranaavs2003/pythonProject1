import pandas as pd
from io import BytesIO
import xlsxwriter

def group_by_route(df):
    route_names = df['route_name'].unique()
    group_by_route_name = df.groupby('route_name')
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})

    for i in route_names:
        worksheet = workbook.add_worksheet(name=i)
        #worksheet.write('A1', 'semester')
        worksheet.write('A1', 'route_name')
        worksheet.write('B1', 'registration_number')
        worksheet.write('C1', 'student_name')
        #worksheet.write('E1', 'gender')
        worksheet.write('D1', 'destination')
        worksheet.write('E1', 'fp_reference_number')
        n = len(group_by_route_name.get_group(i))
        data = group_by_route_name.get_group(i)
        for j in range(n):
            #worksheet.write('A'+str(j+2), data.iloc[j].semester)
            worksheet.write('A'+str(j+2), data.iloc[j].route_name)
            worksheet.write('B'+str(j+2), data.iloc[j].registration_number)
            worksheet.write('C'+str(j+2), data.iloc[j].student_name)
            #worksheet.write('E'+str(j+2), data.iloc[j].gender)
            worksheet.write('D'+str(j+2), data.iloc[j].destination)
            try:
                worksheet.write('E'+str(j+2), data.iloc[j].fp_reference_number)
            except:
                pass

    workbook.close()
    return output

def group_by_destination(df):
    destination_names = df['destination'].unique()
    group_by_destination_name = df.groupby('destination')
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})

    for i in destination_names:
        worksheet = workbook.add_worksheet(name=i[:31])
        #worksheet.write('A1', 'semester')
        worksheet.write('A1', 'route_name')
        worksheet.write('B1', 'registration_number')
        worksheet.write('C1', 'student_name')
        #worksheet.write('E1', 'gender')
        worksheet.write('D1', 'destination')
        worksheet.write('E1', 'fp_reference_number')
        n = len(group_by_destination_name.get_group(i))
        data = group_by_destination_name.get_group(i)
        for j in range(n):
            #worksheet.write('A'+str(j+2), data.iloc[j].semester)
            worksheet.write('A'+str(j+2), data.iloc[j].route_name)
            worksheet.write('B'+str(j+2), data.iloc[j].registration_number)
            worksheet.write('C'+str(j+2), data.iloc[j].student_name)
            #worksheet.write('E'+str(j+2), data.iloc[j].gender)
            worksheet.write('D'+str(j+2), data.iloc[j].destination)
            try:
                worksheet.write('E'+str(j+2), data.iloc[j].fp_reference_number)
            except:
                pass

    workbook.close()
    return output

def getRouteCount(df):
    route_names = df['route_name'].unique()
    group_by_route_name = df.groupby('route_name')
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})

    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Route_Name')
    worksheet.write('B1', 'Count')

    c = 0
    for j in route_names:
        worksheet.write('A' + str(c + 2), j)
        worksheet.write('B' + str(c + 2), str(len(df[df['route_name'] == j])))
        c += 1

    workbook.close()
    return output


def getDestinationCount(df):
    destination_names = df['destination'].unique()
    group_by_destination_name = df.groupby('destination')
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})

    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Destination_Name')
    worksheet.write('B1', 'Count')

    c = 0
    for j in destination_names:
        worksheet.write('A' + str(c + 2), j)
        worksheet.write('B' + str(c + 2), str(len(df[df['destination'] == j])))
        c += 1

    workbook.close()
    return output


    