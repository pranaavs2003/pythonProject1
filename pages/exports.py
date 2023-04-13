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
        n = len(group_by_route_name.get_group(i))
        data = group_by_route_name.get_group(i)
        for j in range(n):
            #worksheet.write('A'+str(j+2), data.iloc[j].semester)
            worksheet.write('A'+str(j+2), data.iloc[j].route_name)
            worksheet.write('B'+str(j+2), data.iloc[j].registration_number)
            worksheet.write('C'+str(j+2), data.iloc[j].student_name)
            #worksheet.write('E'+str(j+2), data.iloc[j].gender)
            worksheet.write('D'+str(j+2), data.iloc[j].destination)
            

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

def combined(df):
    route_names = df['route_name'].unique()
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    group_by_route_name = df.groupby('destination')

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

def getRouteCount(df):
    if('route_number' in df.columns):
        unique_routes = df['route_name'].unique()
        dic = {}
        for i in unique_routes:
            dic[i] = []

        for i in range(df.shape[0]):
            curr_route = df.iloc[i]['route_name']
            curr_num = df.iloc[i]['route_number']
            if curr_num not in dic[curr_route]:
                dic[curr_route].append(curr_num)

        for i in list(dic.keys()):
            res = ""
            for j in dic[i]:
                res += str(j) + ', '
            dic[i] = res
        droute_name = list(dic.keys())
        droute_number = [dic[i] for i in droute_name]

        df_number = pd.DataFrame(list(zip(droute_name, droute_number)), columns=['Name', 'route_number'])
        #print(df_number)
            
            #Main code
    route_names = df['route_name'].unique()
    group_by_route_name = df.groupby('route_name')
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})

    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Route_Name')
    worksheet.write('B1', 'Count')
    worksheet.write('C1', 'route_number')

    c = 0
    for j in route_names:
        worksheet.write('A' + str(c + 2), j)
        worksheet.write('B' + str(c + 2), str(len(df[df['route_name'] == j])))
        #try:
        #print("🃏" ,'C'+str(c+2), df_number.iloc[c].route_number)
        worksheet.write('C'+str(c+2), df_number.iloc[c].route_number)
        # except:
        #     pass
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


    