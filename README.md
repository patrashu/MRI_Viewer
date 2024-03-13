## Knee MRI dataset Viewer

### Dataset Structure
```
📦${DATASET_ROOT}
┣ 📂 train
┃ ┣ 📂 axial
┃ ┣ 📂 coronal
┃ ┣ 📂 sagittal
┣ 📂 valid
┃ ┣ 📂 axial
┃ ┣ 📂 coronal
┃ ┣ 📂 sagittal
┣ 📜 train_abnormal.csv
┣ 📜 train_acl.csv
┣ 📜 train_meniscus.csv
┣ 📜 valid_abnormal.csv
┣ 📜 valid_acl.csv
┣ 📜 valid_meniscus.csv
```


### Install With Poetry

```
poetry install
poetry run python main.py  # pyqt
poetry run uvicorn backend:app --reload  # fastapi
```

### Install With VirtualEnv

Before install, check your python version==3.10

```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py  # pyqt
uvicorn backend:app --reload  # fastapi
```

### Install With Miniconda

```
conda create -n mri-vis python=3.10 -y
conda activate mri-vis
pip install -r requirements.txt
python main.py  # pyqt
uvicorn backend:app --reload  # fastapi
```

### Function

- [x] See jpg file with Scroll
- [x] Drag and Drop .npy file
- [x] Convert .npy to jpg
- [x] visualize csv file
- [x] Add fastapi Test code
