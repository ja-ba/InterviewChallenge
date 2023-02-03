import pandas as pd
import numpy as np
import warnings

class DataCleaner:
    #define class
    def __init__(self):
        #Initializing all variables (input and output dataframes as well as booleans tracking which fields have been cleaned)
        self._inputDF = None
        self._outputDF = None
        self.cleanedPostcode = False
        self.cleanedProductName = False

    #Loading the df from user-proved path and setting _outputDF to _inputDF
    def load_DF(self, path):
        self._inputDF = pd.read_csv(path, low_memory=False)
        self._outputDF = self._inputDF
        print("Dataset loaded successfully!")


    def cleanProductName(self):
        #Exception if data is not loaded yet
        if self._inputDF is None:
            raise Exception("Please load a df first using DataCleaner.load_DF()")
        else:

            #Create new column
            self._outputDF["original_product_name_cleaned"] = self._outputDF["original_product_name"]

            #Replace everything containing (Ö and 24) OR (K and 24) with "E.ON STROM ÖKO 24"
            self._outputDF.loc[self._outputDF["original_product_name"].str.contains('Ö*24|K*24', regex=True) ,"original_product_name_cleaned"] = "E.ON STROM ÖKO 24"

            #Replace everything containing (Ö or K) BUT NOT 24 with "E.ON STROM ÖKO"
            self._outputDF.loc[(self._outputDF["original_product_name"].str.contains('Ö|K', regex=True)) & ~(self._outputDF["original_product_name"].str.contains('24', regex=True)) ,"original_product_name_cleaned"] = "E.ON STROM ÖKO"
            
            #Replace everything containing 24 BUT NOT (Ö or K) with "E.ON STROM 24"
            self._outputDF.loc[(self._outputDF["original_product_name"].str.contains('24', regex=True)) & ~(self._outputDF["original_product_name"].str.contains('Ö|K', regex=True)) ,"original_product_name_cleaned"] = "E.ON STROM 24"
            
            self.cleanedProductName = True
            #Print success message
            print("Product Name cleaning successfull")


    #Method for cleaning the Postcode
    def cleanPostcode(self):
        #Exception if data is not loaded yet
        if self._inputDF is None:
            raise Exception("Please load a df first using DataCleaner.load_DF()")
        else:
            #Logic: Remove strings and then convert to Integer format. Then convert to String to avoid numeric interpretation of column
            #Technical: Converts the Postcode to a string --> then removes all letters --> then remove all special characters except . --> then transforms to float to keep the numeric attribute of postcodes saved as floats --> then to integer since float representation is not needed --> and then to string again to avoid numeric interpretation  
            self._outputDF["postcode_cleaned"] = self._inputDF["postcode"].astype("str").str.replace("[a-zA-Z]",'', regex=True).replace("[^.0-9]",'', regex=True).astype("float").astype("int").astype("str")
            #Set cleanedPostcode flag to true
            self.cleanedPostcode = True
            #Print success message
            print("Postcode cleaning successfull")


    def returnClean(self):
        #Exception if data is not loaded yet
        if self._inputDF is None:
            raise Exception("Please load a df first using DataCleaner.load_DF()")

        else:
            #Warn if postcode wasn't cleaned
            if self.cleanedPostcode==False:
                warnings.warn("WARNING: Returning the cleaned DF, but you haven't cleaned postcode yet!")
            #Warn if product_name wasn't cleaned
            if self.cleanedProductName==False:
                warnings.warn("WARNING: Returning the cleaned DF, but you haven't cleaned product_name yet!")
            
            return self._outputDF
