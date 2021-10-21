UNIONS = ["AABP", "SAG-AFTRA", "SAG-AFTRA Eligible", "AEA", "AEA (EMC)", "ACTRA", "ACTRA Apprentice", "AGVA", "AGMA", "BAE", "AAE", "BECTU", "CAEA", "CAEA Apprentice", "UBCP/ACTRA", "UBCP/ACTRA Apprentice", "Financial Core", "UDA", "UDA/ACTRA", "UDA Stagiaire","NON-UNION"]



class call():
    def __init__(self,roles=[],dateTime="",location="",medium="",payRate=0.0,postDateTime="",union=""):
        self.roles = roles # A list of role objects.
        self.dateTime = dateTime # Timestamp of runtime retrieval of data
        self.location = location # Location of job
        self.medium = medium # Film, TV or theatre
        self.payRate = payRate # 2-long tuple: (FLOAT $00.00, STRING per "day","performance" etc.)
        self.postDateTime = postDateTime # Timestamp of the time the call was posted.
        self.union = union # SAG-AFTRA, UAE etc.
    
newCall = call([])
print(newCall.medium)