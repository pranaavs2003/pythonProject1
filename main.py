import streamlit as st
import pandas as pd
import time
import xlsxwriter
from io import BytesIO
import random

from preprocessing import process
from exports import group_by_route
from exports import group_by_destination
from exports import getRouteCount
from exports import getDestinationCount

st.set_page_config(
    page_title="Transport Management System",
    page_icon="👋",
)

st.sidebar.success("Select a page above.")

class Transport():

    def __init__(self, df = None, dataset_container = [], instruction_container = [], output_container = [], overview_container = []):
        self.df = df
        self.dataset_container = dataset_container
        self.instruction_container = instruction_container
        self.output_container = output_container
        self.overview_container = overview_container

    def initialize_containers(self):
        st.title('Transport Management System')
        st.write('##')
        self.dataset_container = st.container()
        self.instruction_container = st.container()
        self.output_container = st.container()
        self.overview_container = st.container()

    def instructions(self):
        with self.instruction_container:
            st.subheader('Instructions to be followed before uploading your Dataset.')
            st.markdown('* Make sure that the uploaded dataset is in CSV format.')
            st.markdown('* The uploaded transportation CSV file mush have the following columns with the same name, registration_number, student_name, destination, route_name.')
            st.markdown('* The registration_number, student_name, destination, route_name fields in the dataset must not have null values.')

    def upload(self):
        #Preprocessing is done inside this function it self
        uploaded_file = st.file_uploader("Upload a CSV file.", type={"csv", "txt"})
        return uploaded_file

    def preprocess(self):
        uploaded_file = self.upload()
        if uploaded_file is not None:
            self.df = pd.read_csv(uploaded_file, encoding='latin1')
            with st.spinner('Preprocessing your Dataset, Wait a Second...'):
                time.sleep(3)
            st.success('Your Dataset is precessed Successfully!')
            st.write('##')
            st.markdown('Preview of the Dataset')
            st.write(process(self.df))
            st.download_button(
                "Download the processed Data",
                self.df.to_csv(index=False).encode('latin1'),
                "Processed_dataset.csv",
                "text/csv",
                key='download-csv'
            )

    def dataset(self):
        with self.dataset_container:
            st.subheader('Upload your Dataset')
            # try:
            self.preprocess()
            # except:
            #     st.title(
            #         'Make sure that the uploaded Dataset is formated according to the instructions and the documentation.')
            #     st.write('If the uploaded dataset is not correct, you will not get the output.')
            #     st.write('Make sure that the uploaded dataset is formatted properly and try again!')

    def group_by_route(self):
        if self.df is not None:
            output = group_by_route(self.df)
            st.download_button(
                label="Download",
                data=output.getvalue(),
                file_name="Route_grouped.xlsx",
                mime="application/vnd.ms-excel"
            )

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

    def getCount(self):
        route_names = self.df['route_name'].unique()
        group_by_route_name = self.df.groupby('route_name')
        destination_names = self.df['destination'].unique()
        group_by_destination_name = self.df.groupby('destination')

        route_count = []
        for i in route_names:
            route_count.append(len(self.df[self.df['route_name'] == i]))
        df1 = pd.DataFrame(list(zip(route_names, route_count)),
                           columns=['Name', 'Count'])

        destination_count = []
        destination_route_count = []
        for i in destination_names:
            destination_count.append(len(self.df[self.df['destination'] == i]))
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


    def overview(self):
        if self.df is not None:
            with st.spinner('Preprocessing your Dataset, Wait a Second...'):
                time.sleep(3)
            with self.overview_container:
                for i in range(3):
                    st.write('##')
                st.header('Overview of the Data')
                tab1, tab2 = st.tabs(["📈 Route", "📍 Destiantion"])
                cont1 = st.container()
                cont2 = st.container()
                df1, df2 = self.getCount()

                with cont1:
                    tab1.subheader('Routes')
                    tab1.write(df1)
                    output = getRouteCount(self.df)
                    #print('🀄', self.df)
                    tab1.download_button(
                        label="Download",
                        data=output.getvalue(),
                        file_name="Route_count.xlsx",
                        mime="application/vnd.ms-excel3"
                    )

                with cont2:
                    tab2.subheader('Destination')
                    tab2.write(df2)
                    output = getDestinationCount(self.df)
                    tab2.download_button(
                        label="Download",
                        data=output.getvalue(),
                        file_name="Destination_count.xlsx",
                        mime="application/vnd.ms-excel4"
                    )

def main():
    transport = Transport()
    transport.initialize_containers()
    transport.instructions()
    transport.dataset()
    #try:
    transport.output()
    transport.overview()
    #except:
        #st.text('Make sure that the uploaded Dataset is formated according to the instructions and the documentation.')

if __name__ == '__main__':
    main()