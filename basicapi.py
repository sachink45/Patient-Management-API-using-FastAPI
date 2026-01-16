from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Optional, Literal


app = FastAPI()

# pydantic model for data validation
class patient_model(BaseModel):
    Id : Annotated[str, Field(..., description = 'Id for patient', example = 'p001')] 
    name : Annotated[str, Field(..., description = 'name for patient', example = 'sachin')] 
    city : Annotated[str, Field(..., description = 'city for patient', example = 'satara')] 
    age : Annotated[int,  Field(..., gt = 0, lt = 100, description = 'age for patient', example = 30)] 
    gender : Annotated[Literal ['male', 'female', 'others'], Field(..., description = 'gender for patient', example = 'male')] 
    height : Annotated[int, Field(..., gt =0, description = 'height for patient', example = '175 cm')] 
    weight : Annotated[float, Field(..., gt =0, description = 'weight for patient', example = '62 kg')] 

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / ((self.height / 100) ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5 :
            return 'Underweight'
        elif 18.6 < self.bmi < 30:
            return 'Normal'
        else:
            return 'Overweight'
        
# pydantic model for update
class patientupdate(BaseModel):
    name : Annotated[Optional[str], Field(default = None)]
    city : Annotated[Optional[str], Field(default = None)]
    age : Annotated[Optional[int], Field(default = None)]
    gender : Annotated[Optional[Literal['male', 'female']], Field(default = None)] 
    height : Annotated[Optional[int], Field(default = None, gt =0)]
    weight : Annotated[Optional[float], Field(default = None, gt  =0)]

# helper function
def loaddata():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return data

def savedata(data):
    with open('data.json', 'w') as file:
        json.dump(data, file)


# retrive endpoint
@app.get("/")
def hello():
    return {'message': 'Patient management system api'}

@app.get('/about')
def about():
    return {'ewww' : 'fully functional api to manage your patients records'}

@app.get('/view')
def view():
    data = loaddata()
    return data

@app.get('/view_patient/{patient_id}')
def view_patients(patient_id : str = Path(..., description = 'Please enter the patinets id', example = 'p001')):
    data = loaddata()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code = 404, detail = 'Patient not found')

@app.get('/selective_patient')
def selective_patient(sort_by : str = Query(..., description = 'Sort on the basis of age')):
    values = ['bmi', 'age']

    if sort_by not in values:
        raise HTTPException(status_code = 400, details = f'Invalid field selected from {values}')
    
    data = loaddata()


# create endpoint for post
@app.post('/create')
def create_patient(patient : patient_model):
    # load existing data
    data = loaddata()

    # check if id is already present
    if patient.Id in data:
        raise HTTPException(status_code = 404, detail =  'The patients details are already present in records')
    
    # add new record in data
    data[patient.Id] = patient.model_dump(exclude=['Id'])

    # save json file
    savedata(data)

    return JSONResponse(status_code = 201, content = {'message' : 'message created successfully'})

# update end point
@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, update_msg : patientupdate):
    data = loaddata()

    if patient_id not in data:
        raise HTTPException(status_code = 400, detail =  'The patients details are not present in records')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = update_msg.model_dump(exclude_unset = True)
    for i, j in updated_patient_info.items():
        existing_patient_info[i] = j


    # pop out computed fields and then update the details, these fields will be recalculated with updated details
    existing_patient_info.pop("bmi", None)
    existing_patient_info.pop("verdict", None)

    # creating id field in existing_patient_info as we need this field to create pydantic object because id field is required. 
    existing_patient_info['Id'] = patient_id

    # convert the dictionary in pydantic object to validate the data. it will take care of computed fileds like bmi and verdict
    patient_pydantic_object = patient_model(**existing_patient_info)

    # now again dump it to the dict 
    existing_patient_info = patient_pydantic_object.model_dump(exclude = {'Id'})

    # add this dictonary to data
    data[patient_id] = existing_patient_info

    # save data
    savedata(data)

    return JSONResponse(status_code = 200, content = {'message' : 'records has been updated successfully'})


# delete endpoint
@app.delete('/delete/{patient_id}')
def delete_record(patient_id):
    data = loaddata()

    if patient_id not in data:
        raise HTTPException(status_code = 400, detail =  'The patients details are not present in records')
    
    del data[patient_id]

    savedata(data)

    return JSONResponse(status_code = 200, content = {'message' : 'records has been deleted successfully'})
