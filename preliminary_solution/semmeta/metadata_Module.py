import os, sys, glob
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ExifTags # Image processing and metadata
import json
 

# SEMMetaData Class Initialization
class SEMMetaData:
    def __init__(self, image_metadata={}, semext=('tif', 'TIF'), semInsTag=[34118]):
        
        # Accepted SEM image file extensions
        self.semext = semext 
        
        # Dictionary to store extracted metadata per image      
        self.image_metadata = image_metadata
        
        # SEM-specific EXIF tag identifiers used for instrument metadata extraction
        self.semInsTag = semInsTag
        
        # Array to store image tag values (initialized empty)
        self.image_tags = np.array([], dtype='int')
        
        
        
    # Export SEM Metadata to JSON Format    
    def WriteSEMJson(self,file, semdict):   
     
        """
        Open the file in write mode and serialize the metadata dictionary
        """
        
        with open(file, "w") as semoutfile:
            json.dump(semdict, semoutfile)
        return       
 

    def OpenCheckImage(self, image):
    
        """
        Opens an image file and verifies its accessibility and format.
        Returns the opened image object if successful,
        """
        
        if image.endswith(self.semext):
            try:
                img = Image.open(image)
                return img
            except IOError:
                print('[ERROR]', image)
                return False


    def ImageMetadata(self, img):

        """
        Extracts raw metadata and tag identifiers including 34118 
        from a SEM image.
        """
        
        self.image_metadata = img.tag
        self.image_tags = np.array(self.image_metadata) 
        return self.image_metadata, self.image_tags
        

    @property    
    def SEMEXIF(self):

        """
        Provides access to standard EXIF tag mappings from PIL.
        
        Returns:
            - exif_keys (list): Human-readable EXIF tag names
            - exif_number (list): Corresponding numeric tag identifiers used in image metadata.
        """
        
        # Reverse the PIL EXIF tag dictionary to map names to numeric keys
        exif_dict = {k: v for v, k in ExifTags.TAGS.items()}
        # or
        #exif_dict = dict([ (k, v) for v, k in ExifTags.TAGS.items() ])

        # Extract all tag names (keys) from the reversed dictionary
        exif_keys = [key for key in exif_dict]
        
        # Extract corresponding numeric identifiers for each tag name
        exif_number = [exif_dict[k] for k in exif_keys]
        return exif_keys, exif_number 
        

    # Extract Standard EXIF Metadata from SEM Image
    def GetExifMetadata(self, img, exif_keys, exif_number):
    
        """
        Extracts standard EXIF metadata from a SEM image.
        """
      
        # based on std EXIF TAGS (from PIL), we store exif metadata in found_exif_metadata variable
        found_exif_metadata=[(img.tag[idx][:], word) for idx, word in zip(exif_number, exif_keys) if idx in self.image_tags]
        
        # if the key is not available in the image save its value as none
        none_exif_metadata = [(word, None) for num, word in zip(exif_number, exif_keys)  if num not in self.image_tags] 
        return found_exif_metadata, none_exif_metadata


    # Construct Unified EXIF Metadata Dictionary
    def ExifMetaDict(self, found_exif_metadata, none_exif_metadata):

        """
        Creates a unified dictionary from found and missing EXIF metadata entries.
        Returns:
            - dict: Combined dictionary of EXIF metadata, excluding 'ColorMap' entries.         
        """ 

        found_metadict = dict((subl[1], subl[0][0]) for subl in found_exif_metadata if subl[1]!="ColorMap")
        none_metadict = dict((subl[0], subl[1]) for subl in none_exif_metadata if subl[0]!="ColorMap")
        allexif_metadict = {**found_metadict, **none_metadict}
        return allexif_metadict 


    @property
    def GetInsMetadata(self):

        '''
        Extracts instrument-specific metadata from SEM image EXIF tag 34118.
        Returns:
            - list: a cleaned and escaped list of instrument metadata strings.
            - and an empty list if tag 34118 is not found.
        ''' 
        try:
            # Extract the value associated with EXIF tag 34118
            pairs = [params for tag, params in self.image_metadata.items() if tag == self.semInsTag[0]]
            
            # Unpack the first matching entry (instrument metadata)
            instrument_metadata,*_ = pairs[0]  

            # Clean the instrument metadata by skipping the first N lines (random numbers and header content)   
            random_size_tag = 35
            instrument_metadata = [instrument_metadata][0].split("\r\n")[random_size_tag:]          

        # Tag 34118 not found - likely not a SEM image       
        except IndexError:
            instrument_metadata = []
        return instrument_metadata


    # Parse Instrument Metadata from Tag 34118
    def InsMetaDict(self, list):

        """
        Converts a flat list of instrument metadata into a structured dictionary.
        Returns:
            - dict: of all the information contained in the 34118 tag  
            - and an empty dictionary if parsing fails.      
        """
        try:
            # Separate keys and values based on alternating index positions
            ins_keys, ins_values = [], []
            for idx, val in enumerate(list):
                if idx %2==0:
                    ins_keys.append(val)
                else:
                    ins_values.append(val)

            # Combine keys and values into a dictionary
            instrument_meta_dict = {k:v for k,v in zip(ins_keys, ins_values)}
            # or:
            #instrument_meta_dict = dict(zip(ins_keys, ins_values))

        # Handle malformed input gracefully; case of no ins. tag 34118
        except Exception as e:            
            print("Error parsing instrument metadata:", str(e))
            instrument_meta_dict = {}
        return instrument_meta_dict       
   
