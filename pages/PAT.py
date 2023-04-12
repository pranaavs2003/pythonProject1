import streamlit as st
import pandas as pd
import time
import xlsxwriter
from io import BytesIO
import random

from preprocessing import process
from preprocessing import fatprocess
from exports import group_by_route
from exports import group_by_destination
from exports import getRouteCount
from exports import getDestinationCount

def combined(df):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet(name='Combined')

    for i in range(df.shape[1]):
        if('registration_number' in df.columns):
            worksheet.write('A1', 'registration_number')
        if('student_name_x' in df.columns):
            worksheet.write('B1', 'student_name_x')
        if('destination' in df.columns):
            worksheet.write('C1', 'destination')
        if('route_number' in df.columns):
            worksheet.write('D1', 'route_number')
        if('route_name' in df.columns):
            worksheet.write('E1', 'route_name')
        for j in range(df.shape[0]):
            if('registration_number' in df.columns):
                worksheet.write('A'+str(j+2), df.iloc[j].registration_number)
            if('student_name_x' in df.columns):
                worksheet.write('B'+str(j+2), df.iloc[j].student_name_x)
            if('destination' in df.columns):
                worksheet.write('C'+str(j+2), df.iloc[j].destination)
            if('route_number' in df.columns):
                worksheet.write('D'+str(j+2), df.iloc[j].route_number)
            if('route_name' in df.columns):
                worksheet.write('E'+str(j+2), df.iloc[j].route_name)
    workbook.close()
    return output

class Transport():

    def __init__(self, df = None,df1= None, dataset_container = [], instruction_container = [], output_container = [], overview_container = [], slot_con = [], date_con = [],combine_con = [], combined=None):
        self.df = df
        self.df1 = df1
        self.dataset_container = dataset_container
        self.instruction_container = instruction_container
        self.output_container = output_container
        self.overview_container = overview_container
        self.slot_con = slot_con
        self.date_con = date_con
        self.combine_con = combine_con
        self.combined=combined


    def initialize_container(self):
        st.title('Transport Management System for Examinations')
        st.write('##')
        st.subheader('Instructions to be followed before uploading your Dataset.')
        st.markdown('* Make sure that the uploaded dataset is in CSV format.')
        st.markdown('* The uploaded transportation CSV file mush have the following columns with the same name, registration_number, student_name, destination, route_number, route_name.')
        st.markdown('* The uploaded examination CSV file mush have the following columns with the same name exam_date, registration_number, student_name, session_name, slot_name.')
        st.markdown('* Wait for few seconds after the first dataset has processed, and then upload the second dataset.')
        st.write('##')

        self.dataset_container = st.container()
        self.instruction_container = st.container()
        self.output_container = st.container()
        self.overview_container = st.container()
        self.slot_con = st.container()
        self.date_con = st.container()
        self.combine_con  = st.container()

    def upload(self):
        file1 = st.file_uploader("Choose the Transportation file:")
        file2 = st.file_uploader("Choose the PAT file:")
        if file1 and file2:
            st.success("PAT File uploaded successfully!")
        else:
            st.warning("Please upload both files.") 
        if file1 is not None :
                self.df = pd.read_csv(file1, encoding='latin1')

                with st.spinner('Preprocessing your Transportation Dataset, Wait a Second...'):
                    time.sleep(3)
                st.success('Your Transportation Dataset is precessed Successfully!')
                st.write('##')
                st.markdown('Preview of the processed Transportation Dataset')
                try:
                    st.write(process(self.df))
                    st.download_button(
                        "Download the processed Transportation Data",
                        self.df.to_csv(index=False).encode('latin1'),
                        "Processed_dataset.csv",
                        "text/csv",
                        key='download-csv'
                    )
                    self.overview(self.df)
                except:
                    st.title(
                        'Make sure that the uploaded Dataset is formated according to the instructions and the documentation.')
                    st.write('If the uploaded dataset is not correct, you will not get the output.')
                    st.write('Make sure that the uploaded dataset is formatted properly and try again!')

        if file2 is not None:
                self.df1 = pd.read_csv(file2,encoding='latin1')
                self.df1.rename(columns = {'REG NO':'registration_number', 'STUDENT NAME':'student_name'}, inplace=True)

                with st.spinner('Preprocessing your Dataset, Wait a Second...'):
                    time.sleep(3)
                st.success('Your Pat Dataset is precessed Successfully!')
                st.write('##')
                st.markdown('Preview of the Processed Pat Dataset')
                #try:
                st.write(self.df1)
                st.download_button(
                        "Download the processed Examination Data",
                        self.df.to_csv(index=False).encode('latin1'),
                        "Processed_dataset.csv",
                        "text/csv",
                        key='download-csv1'
                )
                # except:
                #     st.title(
                #         'Make sure that the uploaded Dataset is formated according to the instructions and the documentation.')
                #     st.write('If the uploaded dataset is not correct, you will not get the output.')
                #     st.write('Make sure that the uploaded dataset is formatted properly and try again!')

    def dataset(self):
        with self.dataset_container:
            st.subheader('Upload Transportation and Examination Dataset')
            self.upload()

    def group_by_route(self):
        if self.df is not None:
            output = group_by_route(self.df)
            st.download_button(
                label="Download",
                data=output.getvalue(),
                file_name="Route_grouped.xlsx",
                mime="application/vnd.ms-excel"
            )

    def outputcon(self):
        if self.df is not None and self.df1 is not None:
            with self.output_container:
                self.output()
                self.combine()
    def output(self):
        if self.df is not None:
            for i in range(2):
                st.write('##')
            st.header('Export the Grouped Files')
            con1 = st.container()
            con2 = st.container()
            con3 = st.container()
            done1, done2, done3 = False, False, False
            with con1:
                st.text('Download grouped by Route Name')
                if self.df is not None:
                    output = group_by_route(self.df)
                    st.download_button(
                        label="Download",
                        data=output.getvalue(),
                        file_name="Route_grouped.xlsx",
                        mime="application/vnd.ms-excel1",
                        disabled=done1
                    )
            with con2:
                st.text('Download grouped by Destination Name')
                if self.df is not None:
                    output = group_by_destination(self.df)
                    st.download_button(
                        label="Download",
                        data=output.getvalue(),
                        file_name="Destination_grouped.xlsx",
                        mime="application/vnd.ms-excel2",
                        disabled=done2
                    )
            for i in range(4):
                st.write('##')

    def getCount(self,d):
        route_names = d['route_name'].unique()
        group_by_route_name = d.groupby('route_name')
        destination_names = d['destination'].unique()
        group_by_destination_name = d.groupby('destination')

        route_count = []
        for i in route_names:
            route_count.append(len(d[d['route_name'] == i]))
        df1 = pd.DataFrame(list(zip(route_names, route_count)),
                           columns=['Name', 'Count'])

        destination_count = []
        destination_route_count = []
        for i in destination_names:
            destination_count.append(len(d[d['destination'] == i]))
            #destination_route_count.append(round((random.random() * 10) + 1))
        df2 = pd.DataFrame(list(zip(destination_names, destination_count)),
                           columns=['Name', 'Student Count'])
        
        if('route_number' in self.df.columns):
            unique_routes = self.df['route_name'].unique()
            dic = {}
            for i in unique_routes:
                dic[i] = []

            for i in range(self.df.shape[0]):
                curr_route = self.df.iloc[i]['route_name']
                curr_num = self.df.iloc[i]['route_number']
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
            for i in range(df1.shape[0]):
                df1['route_number'] = df_number['route_number']   

        return df1, df2


    def overview(self,d):
        if d is not None:
            with st.spinner('Preprocessing your Dataset, Wait a Second...'):
                time.sleep(3)
            # with self.overview_container:
            for i in range(3):
                st.write('##')
            st.header('Overview of the Data')
            tab1, tab2 = st.tabs(["📈 Route", "📍 Destination"])
            cont1 = st.container()
            cont2 = st.container()
            df1, df2 = self.getCount(d)

            with cont1:
                tab1.subheader('Routes')
                tab1.write(df1)
                output = getRouteCount(d)
                tab1.download_button(
                    label="Download",
                    data=output.getvalue(),
                    file_name="Route_count.xlsx",
                    mime="application/vnd.ms-excel3"
                )

            with cont2:
                tab2.subheader('Destination')
                tab2.write(df2)
                output = getDestinationCount(d)
                tab2.download_button(
                    label="Download",
                    data=output.getvalue(),
                    file_name="Destination_count.xlsx",
                    mime="application/vnd.ms-excel4"
                    )
    
        

    def checkdate(self):
        a=sorted(self.df1['exam_date'].unique())
        st.title('select Date:')

        checkbox_values = st.multiselect('Select options',a)
        st.write('You selected:')
        for option in checkbox_values:
            # st.write(option)
            self.date(option)

    def comb(self):
        with self.combine_con:
            self.combine()

    def combine(self):
        st.subheader("Preview of the Combined Dataset")
        self.combined = pd.merge(self.df1,self.df, on='registration_number')
        st.write(self.combined)
        output_combined = combined(self.combined)
        cn1 = st.container()
        cn1.download_button(
            label="Download",
            data=output_combined.getvalue(),
            file_name="Combined_student_data.xlsx",
            mime="application/vnd.ms-excel3"
        )
        
        for i in range(4):
            st.write('##')
    
    def date(self,a):
        self.match=self.combined[self.combined['exam_date']==a]
        st.write(self.match)
        self.overview(self.match)
        # st.write(self.match)

    def checkslot(self):
        a=sorted(self.df1['slot_name'].unique())
        st.title('select Slot:')

        checkbox_values = st.multiselect('Select options',a)
        self.match1 = pd.DataFrame()

        for option in checkbox_values:
            st.write('You selected:',option)
            # st.write(option)
            self.slot(option)
        st.write(self.match1)
        if len(checkbox_values):
            self.overview(self.match1)


    def slot(self,a):
        if a is not None:
            self.match=self.combined[self.combined['slot_name']==a]
            self.match1=pd.concat([self.match1,self.match])

    def slotcon(self):
        if self.df is not None and self.df1 is not None:
            with self.slot_con:
                self.checkslot()


    def datecon(self):
        if self.df is not None and self.df1 is not None:
            with self.date_con:
                self.checkdate()


def main():
    transport = Transport()

    transport.initialize_container()
    # transport.instructions()

    transport.dataset()
    #try:
    transport.outputcon()
    # transport.slotcon()
    # transport.datecon()
    # except:
    #     st.title(
    #         'Make sure that the uploaded Dataset is formated according to the instructions and the documentation.')
    #     st.write('If the uploaded dataset is not correct, you will not get the output.')
    #     st.write('Make sure that the uploaded dataset is formatted properly and try again!')

if __name__ == '__main__':
    main()