## Knee MRI dataset Viewer

### Dataset Link
```
wget https://download.cs.stanford.edu/deep/MRNet-v1.0.zip
```

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
┣ 📜 train_meniscus.ipynb
┣ 📜 valid_abnormal.csv
┣ 📜 valid_acl.csv
┣ 📜 valid_meniscus.ipynb
```


### Install With Poetry

```
poetry install
poetry run python main.py
```

### Install With Miniconda

```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Screen Shot

![expect](https://github.com/patrashu/MRI_Viewer/assets/78347296/ffd692e0-fef2-45fd-9160-9fc01dc613f0)


### Function

- [x] See jpg file with Scroll
- [x] Drag and Drop .npy file
- [x] Convert .npy to jpg
- [ ] visualize csv file