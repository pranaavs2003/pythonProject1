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
        st.title('Transport Management System')
        st.write('##')
        st.subheader('Instructions to be followed before uploading your Dataset.')
        st.markdown('* Make sure that the uploaded dataset is in CSV format.')
        st.markdown('* Make sure that the uploaded file is less than 200Mb')
        st.markdown('* The Name, Register Number, Route and Destination in the dataset must not have null values.')
        st.write('##')

        self.dataset_container = st.container()
        self.instruction_container = st.container()
        self.output_container = st.container()
        self.overview_container = st.container()
        self.slot_con = st.container()
        self.date_con = st.container()
        self.combine_con  = st.container()

    # def instructions(self):
    #     with self.instruction_container:
    #         st.subheader('Instructions to be followed before uploading your Dataset.')
    #         st.markdown('* Make sure that the uploaded dataset is in CSV format.')
    #         st.markdown('* Make sure that the uploaded file is less than 200Mb')
    #         st.markdown('* The Name, Register Number, Route and Destination in the dataset must not have null values.')
        

    def upload(self):
        #Preprocessing is done inside this function it self
        #uploaded_file = st.multiselect("Upload a CSV file.",["fat_wise_1.csv", "TransportRegistrationCSVnew.csv"])
        # uploaded_file1 = st.file_uploader("Upload a CSV file.", type={"csv", "txt"},key='unique_key1')
        file1 = st.file_uploader("Choose the Transpotation file:")
        file2 = st.file_uploader("Choose the Examination file:")
        if file1 and file2:
        # Do something with the files
            st.success("Transpotation Files uploaded successfully!")
        else:
            st.warning("Please upload both files.") 
        if file1 is not None :
                self.df = pd.read_csv(file1, encoding='latin1')

                with st.spinner('Preprocessing your Transpotation Dataset, Wait a Second...'):
                    time.sleep(3)
                st.success('Your Transpotation Dataset is precessed Successfully!')
                st.write('##')
                st.markdown('Preview of the processed Transpotation Dataset')
                st.write(process(self.df))
                st.download_button(
                    "Download the processed Transpotation Data",
                    self.df.to_csv(index=False).encode('latin1'),
                    "Processed_dataset.csv",
                    "text/csv",
                    key='download-csv'
                )
                self.overview(self.df)
        if file2 is not None:
                self.df1 = pd.read_csv(file2,encoding='latin1')
                self.df1.rename(columns = {'EXAM TYPE':'exam_type', 'EXAM DATE':'exam_date', 'SESSION NAME':'session_name', 'SLOT NAME':'slot_name', 'REG NO':'registration_number', 'STUDENT NAME':'student_name'}, inplace=True)

                with st.spinner('Preprocessing your Dataset, Wait a Second...'):
                    time.sleep(3)
                st.success('Your Examination Dataset is precessed Successfully!')
                st.write('##')
                st.markdown('Preview of the Processed Examination Dataset')
                st.write(fatprocess(self.df1))

                # st.write(fatprocess(self.df))
                st.download_button(
                    "Download the processed Examination Data",
                    self.df.to_csv(index=False).encode('latin1'),
                    "Processed_dataset.csv",
                    "text/csv",
                    key='download-csv1'
                )
                
        # if file2 is not None :
        #         self.df1 = pd.read_csv(file1, encoding='latin1')
        #         with st.spinner('Preprocessing Fat Dataset, Wait a Second...'):
        #             time.sleep(3)
        #         st.success('Fat Dataset is precessed Successfully!')
        #         st.write('##')
        #         st.markdown('Preview of the Dataset')
                

    # def preprocess(self):
        # uploaded_file = self.upload()
            # if uploaded_file is not None :
            #     self.df = pd.read_csv(uploaded_file, encoding='latin1')

            #     with st.spinner('Preprocessing your Dataset, Wait a Second...'):
            #         time.sleep(3)
            #     st.success('Your Dataset is precessed Successfully!')
            #     st.write('##')
            #     st.markdown('Preview of the Dataset')
            #     st.write(process(self.df))
            #     st.download_button(
            #         "Download the processed Data",
            #         self.df.to_csv(index=False).encode('latin1'),
            #         "Processed_dataset.csv",
            #         "text/csv",
            #         key='download-csv'
            #     )

    def dataset(self):
        with self.dataset_container:
            st.subheader('Upload Transpotation and Examination Dataset')
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
            destination_route_count.append(round((random.random() * 10) + 1))
        df2 = pd.DataFrame(list(zip(destination_names, destination_count, destination_route_count)),
                           columns=['Name', 'Student Count', 'Route Count'])

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
            # st.write(self.match1)
        # st.text('Route and destination wise count for ',a)
        

        # st.write(self.match)  

    def slotcon(self):
        if self.df is not None and self.df1 is not None:
            with self.slot_con:
                self.checkslot()


    def datecon(self):
        if self.df is not None and self.df1 is not None:
            with self.date_con:
                self.checkdate()





    # def side(self):
    #     st.sidebar.header("Navigation")
    #     with self.dataset_container:
    #         if st.sidebar().button("Run my_function"):
    #             self.checkslot()

def main():
    transport = Transport()

    transport.initialize_container()
    # transport.instructions()

    transport.dataset()
    transport.outputcon()
    # transport.comb()
    transport.slotcon()
    # transport.checkslot()
    transport.datecon()
    # transport.checkdate()


if __name__ == '__main__':
    main()