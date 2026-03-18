from dataclasses import dataclass
from typing import Optional, List



# -------------------------
# PHOTO
# -------------------------

@dataclass
class Photo:
    photoData: Optional[str] = None
    photoUri: Optional[str] = None
    md5: Optional[str] = None
    fileName: Optional[str] = None
    fileType: Optional[str] = None
    description: Optional[str] = None


# -------------------------
# POSTER DESCRIPTION
# -------------------------

@dataclass
class PosterDescription:
    languageId: Optional[str] = None
    description: Optional[str] = None
    
    
    

# -------------------------
# CONTACT
# -------------------------

@dataclass
class Contact:
    name: Optional[str] = None
    state: Optional[str] = None
    phoneNumbers: Optional[List[str]] = None



# -------------------------
# LOCATION
# -------------------------

@dataclass
class Location:
    state: Optional[str] = None




# -------------------------
# CHILD
# -------------------------

@dataclass
class Child:
    firstName: Optional[str] = None
    middleName: Optional[str] = None
    lastName: Optional[str] = None

    dateOfBirth: Optional[str] = None
    ageNow: Optional[str] = None

    sex: Optional[str] = None
    races: Optional[List[str]] = None

    hairColor: Optional[str] = None
    eyeColor: Optional[str] = None

    description: Optional[str] = None
    ncicNumber: Optional[str] = None
    
    photos: Optional[List[Photo]] = None
    ageProgressionPhotos: Optional[List[Photo]] = None

    approximateAge: Optional[str] = None

    missingSince: Optional[str] = None
    missingCity: Optional[str] = None
    missingCounty: Optional[str] = None
    missingState: Optional[str] = None
    missingZip: Optional[str] = None
    missingCountry: Optional[str] = None

    dateFound: Optional[str] = None
    foundCity: Optional[str] = None
    foundCounty: Optional[str] = None
    foundState: Optional[str] = None
    foundZip: Optional[str] = None
    foundCountry: Optional[str] = None

    namus: Optional[str] = None


# -------------------------
# COMPANION
# -------------------------

@dataclass
class Companion:
    firstName: Optional[str] = None
    middleName: Optional[str] = None
    lastName: Optional[str] = None

    dateOfBirth: Optional[str] = None
    ageNow: Optional[str] = None

    sex: Optional[str] = None
    races: Optional[List[str]] = None

    hairColor: Optional[str] = None
    eyeColor: Optional[str] = None

    description: Optional[str] = None
    ncicNumber: Optional[str] = None

    photos: Optional[List[Photo]] = None        
    ageProgressionPhotos: Optional[List[Photo]] = None  

    companionType: Optional[str] = None




# -------------------------
# CLIENT
# -------------------------

@dataclass
class Client:
    clientId: Optional[str] = None
    clientSecret: Optional[str] = None


# -------------------------
# POSTER (MAIN OBJECT)
# -------------------------

@dataclass
class Poster:
    dateCreated: str = ""                                        # not nullable
    lastModified: str = ""                                       # not nullable
    id: Optional[str] = None

    organizationCode: Optional[str] = None
    organizationLogo: Optional[str] = None                       # string($uri) = str
    caseNumber: Optional[str] = None

    descriptions: Optional[List[PosterDescription]] = None      

    unidentified: Optional[bool] = None
    amberAlert: Optional[bool] = None

    children: Optional[List[Child]] = None                      
    companions: Optional[List[Companion]] = None                

    extraPhotos: Optional[List[Photo]] = None                   

    contacts: Optional[List[Contact]] = None                    

    distributionLocations: Optional[List[Location]] = None      
    



