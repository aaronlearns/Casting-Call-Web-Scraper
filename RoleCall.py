from datetime import datetime as dt

UNIONS = ["AABP", "SAG-AFTRA", "SAG-AFTRA Eligible", "AEA", "AEA (EMC)", "ACTRA", "ACTRA Apprentice", "AGVA", "AGMA", "BAE", "AAE", "BECTU", "CAEA", "CAEA Apprentice", "UBCP/ACTRA", "UBCP/ACTRA Apprentice", "Financial Core", "UDA", "UDA/ACTRA", "UDA Stagiaire","NON-UNION"]

class Role():
    def __init__(self):
        self.name = "" # The name of the character
        self.descripton = "" # Character breakdown/descripton
        self.gender = "" # Character gender STRING
        self.race = "" # Character race STRING
        self.ageRange = [] # Character ageRange LIST of INTS
        self.height = 0 # Character height in inches INT

# dateTime IS THE RUNTIME RETRIEVAL OF THE CALL, WHILE postDateTime IS THE TIME THE CALL WAS POSTED.
class Call():
    def __init__(self):
        self.roles = [] # A list of role objects.
        self.dateTime = dt.now() # Timestamp of runtime retrieval of data DATETIME
        self.location = "" # Location of job STRING
        self.medium = "" # Film, TV, Theatre, Voiceover etc. STRING
        self.name = "" # Name of the project STRING
        self.payRate = [0.0,""] # 2-long list: [per-diem $ rate FLOAT, the diem: "day","performance" etc. STRING]
        self.postDateTime = "" # Timestamp of the time the call was posted. STRING
        self.union = "" # SAG-AFTRA, UAE etc. STRING
