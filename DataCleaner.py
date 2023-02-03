import pandas as pd
import numpy as np
import warnings

class DataCleaner:
    def __init__(self):
        #Initializing all variables
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
        if self._inputDF is None:
            raise Exception("Please load a df first using DataCleaner.load_DF()")
        else:
            #Replace everything containing KO and 24 OR Ö and 24 with E.ON STROM ÖKO 24
            self._outputDF.loc[self._outputDF["original_product_name"].str.contains('Ö*24|KO*24', regex=True) ,"original_product_name"] = "E.ON STROM ÖKO 24"

            #Replace everything containing KO or Ö BUT NOT 24 with E.ON STROM ÖKO
            self._outputDF.loc[(self._outputDF["original_product_name"].str.contains('Ö|KO', regex=True)) & ~(self._outputDF["original_product_name"].str.contains('24', regex=True)) ,"original_product_name"] = "E.ON STROM ÖKO"

            #Replace everything containing 24 but not Ö or KO with "E.ON STROM 24"
            self._outputDF.loc[(self._outputDF["original_product_name"].str.contains('24', regex=True)) & ~(self._outputDF["original_product_name"].str.contains('Ö|KO', regex=True)) ,"original_product_name"] = "E.ON STROM 24"

            self.cleanedProductName = True
            #Print success message
            print("Product Name cleaning successfull")


    #Method for cleaning the Postcode
    def cleanPostcode(self):
        #Exception if data is not loaded
        if self._inputDF is None:
            raise Exception("Please load a df first using DataCleaner.load_DF()")
        else:
            #Logic: Remove strings and then convert to Integer format. Then convert to String to avoid numeric interpretation of column
            #Technical: Converts the Postcode to a string --> then removes all letters --> then remove all special characters except . --> then transforms to float to keep the numeric attribute of postcodes saved as floats --> then to integer since float representation is not needed --> and then to string again to avoid numeric interpretation  
            self._outputDF["postcode_int"] = self._inputDF["postcode"].astype("str").str.replace("[a-zA-Z]",'', regex=True).replace("[^.0-9]",'', regex=True).astype("float").astype("int")
            #Set cleanedPostcode flag to true
            self.cleanedPostcode = True
            #Print success message
            print("Postcode cleaning successfull")


    def returnClean(self):
        #Exception if data is not loaded
        if self._inputDF is None:
            raise Exception("Please load a df first using DataCleaner.load_DF()")

        else:
            #Warn if postcode wasn't cleaned
            if self.cleanedPostcode==False:
                warnings.warn("WARNING: Returning the cleaned DF, but you haven't cleaned postcode yet!")
            #Warn if Bundesland wasn't cleaned
            if self.cleanedProductName==False:
                warnings.warn("WARNING: Returning the cleaned DF, but you haven't cleaned product_name yet!")
            
            return self._outputDF
