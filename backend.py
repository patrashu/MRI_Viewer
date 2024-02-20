import cv2
import numpy as np
from PIL import Image

import uvicorn
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel, Base64Bytes, ConfigDict
from fastapi.middleware.cors import CORSMiddleware


###################################################################
# Define Controller class.
class Controller:
    """ 
    This Class is a controller for the FastAPI. 
    It will handle the request from the client and save inference results by dictionary.
    So, the client can get the result by call function get_res_dict_item_by_key.
    
    Here is the structure of the result dictionary.
    self.res_dict = {
        'coronal': {
            'idx': {
                'original': 'base64 string',
                'gradcam': 'base64 string',
            }
        },
        'sagittal': {
            ...
        },
        'axial': {
            ...
        }
    }    
    """
    def __init__(self):
        self.__res_dict = {}
        
    def get_res_dict(self) -> dict:
        """ Get all of the result dictionary """
        return self.__res_dict
    
    def get_res_dict_item(self, plane: str, idx: int, method: str) -> np.ndarray:
        """ Get result item by the given key """
        return self.__res_dict[plane][idx][method]
    
    def clear_res_dict(self) -> None:
        """ 
        This function will clear the result dictionary.
        It will be called when the client want to set result dictionary by new data.
        """
        self.__res_dict.clear()
        
    def clear_res_dict_by_plane(self, plane: str) -> None:
        """ 
        This function will clear the result dictionary by the given key.
        It will be called when the client want to set result dictionary by new data.
        """
        del self.__res_dict[plane]
        
    def is_empty(self) -> bool:
        """ Check if the result dictionary is empty """
        return len(self.__res_dict) == 0
    
    def set_res_dict(self, np_img: np.ndarray, plane: str) -> None:
        if self.__res_dict.get(plane, -1) != -1:
            print("The result dictionary is not empty. Auto Removing...")
            self.clear_res_dict_by_plane(plane)
        print(np_img.shape)
        _plane_dict=  {}
        for i in range(np_img.shape[0]):
            _plane_dict[i] = {
                "original": np_img[i, :, :],
                "gradcam": np_img[i, :, :]
            }
        
        self.__res_dict[plane] = _plane_dict


###################################################################
# Inference Model
class MRIKneePredictor:
    pass



###################################################################
# Define return type.
class ResultItems(BaseModel):
    original: Base64Bytes
    gradcam: Base64Bytes
    

class ResultItem(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='ignore') 
    img: list | Base64Bytes


class TestResult(BaseModel):
    plane: str
    idx: int
    method: str

###################################################################
app = FastAPI()
controller = Controller()

# CORS 설정 추가
origins = ["*"]  # 또는 필요한 도메인 리스트
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/preprocess") 
async def preprocess(file: UploadFile = File(...), plane: str = "sagittal") -> dict:        
    np_array = np.load(file.file)
    # add model inference
    
    controller.set_res_dict(np_array, plane)
    print(controller.get_res_dict())
    return {"length": np_array.shape[0]}


@app.get("/result/{plane}/{idx}/{method}", response_model=ResultItem)
async def get_result_by_idx(plane: str, idx: int, method: str) -> ResultItem:
    """ 
    This function will return the result by the given index and method.
    Please note that the result is a dictionary, so the client can get the result by call function get_res_dict_item_by_key.
    """
    res_item = controller.get_res_dict_item(plane, idx, method)
    return { 
        "img": res_item.tolist(),
    }
    
    
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)