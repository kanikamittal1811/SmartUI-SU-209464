### SMART UI

### SU-209464

---

### Team Information


| Name | Email |Profile Link|
| - | - | - |
| Kanika Mittal | mkanika1811@gmail.com | [![Website Badge](https://img.shields.io/badge/-kanika.github-teal?style=flat-square&url=https://github.com/kanikamittal1811)](https://github.com/kanikamittal1811)|
| Pradyumn Jain | pradyumn25jain@gmail.com |[![Website Badge](https://img.shields.io/badge/-pradyumn.github-teal?style=flat-square&url=https://github.com/pradyumnjain)](https://github.com/pradyumnjain) |

---

### Problem Statement

To develop a code which generates a json file(output.json) describing various ui elements present in the input image of a wireframe.

---

### Requirements

* Windows 
* Pip
* Anaconda / python 3.5

### Setup

1. Fetching repository
    ```
    git clone https://github.com/kanikamittal1811/SMART-UI-SU-209464.git
    ```
2. Fetching model weights and east files
   1. Download model weights from this [link](https://drive.google.com/drive/folders/16nfPu91UwW-Vv3TLnYOJ3rK0iBAFZPmb?usp=sharing) 
      ```
      https://drive.google.com/drive/folders/16nfPu91UwW-Vv3TLnYOJ3rK0iBAFZPmb?usp=sharing
      ```
   2. unzip `east` folder
   3. place the `cnn.h5` in 
      ```
      SMART-UI-SU-209464/model/
      ``` 
   4. Verfiy `SMART-UI-SU-209464/model` directory structure
      ```
       SMART-UI-SU-209464/model
                           │   cnn.h5
                           └───east
                               │   model.ckpt-49491.index
                               │   model.ckpt-49491.data-00000-
                               │   checkpoint
                               |   model.ckpt-49491.meta
      ```
   
3. Create Virtual Environment

    > 1. <ins>With Anaconda</ins>
    >
    >     a. Check conda installation
    >
    >     ```
    >     conda -V
    >     ```
    >     b. Update conda
    >     ```
    >     conda update conda
    >     ```
    >     c. Create a virtual environment 
    >
    >     ```
    >     conda create -n yourenvname python=3.5 anaconda
    >     ```
    >     d. Activate virtual environment 
    >
    >     ```
    >     source activate yourenvname
    >     ```
    > for more detailed steps [link](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/)

    > 2. <ins>Without Anaconda</ins> (python version 3.5)
    >
    >     a. Check pip installation
    >
    >     ```
    >     pip -h
    >     ```
    >     b. Install the virtualenv package 
    >
    >     ```
    >     pip install virtualenv
    >     ```
    >     c. Create the virtual environment
    >
    >     ```
    >     virtualenv mypython
    >     ```
    >     d. Activate Virtual environment
    >     - for Mac Os/ git bash 
    >
    >       ```
    >       source mypython/bin/activate
    >       ```
    >     - for Windows 
    >
    >       ```
    >       mypython\Scripts\activate
    >       ```
    >
    > for more detailed steps [link](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)
    
4. Setup Tesseract
    1. Download the Tesseract executable [link](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.1.0.20190314.exe)
        ```
        https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.1.0.20190314.exe
        ```
        
    2. Install the executable with all default settings.
    3. Note the installation path (will be used later)
    4. Open "Edit the system environment variables"
    5. Click "Advanced” section of “System properties” then click “Environment Variables"
    6. In the “System variables” table click on the variable called “Path” and then click “Edit” 
    
    ![alt text](https://miro.medium.com/max/2400/1*_sHl5FSnvjZcBj5E7C_pgQ.png)
    
    7. Go to “Edit environment variable” click on “New”. You will get a blank space where you can add some text. Here, add your directory name where all your Tesseract-OCR files        are stored.
    8. To check successful installation
        ```
        tesseract --version
        ```
    
5. Install Dependencies 
   - 1. unix based cmd tools (git bash)
      ```
      cat requirements.txt | sed -e '/^\s*#.*$/d' -e '/^\s*$/d' | xargs -n 1 python -m pip install
      ```
   - 2. other cmd tools
      <br> install dependencies one by one 
      <br> example
      ```
      pip install numpy==1.14.5
      ```
 6. Install shapely
    - using conda
        ```
        conda config --add channels conda-forge
        conda install shapely
        ```
    - for more detailed steps [link](https://towardsdatascience.com/install-shapely-on-windows-72b6581bb46c) 
---

### Run

* To run the file execute command 
  ```
  python run_single.py "input file path" "output folder path"
  ```

  > *make sure the virtual environment is activated*

---

### Output

* for html (text +component) 
    - output json: `output_path\out_image\compo_html.json` 
    - output html:`output_path\out_image\output.html` 
    - output image:`output_path\out_image\result.jpg`
* for image model 
    - output json:`output_path\out_imagename\ip\clf_1.json` -
    - output image:`output_path\out_imagename\ip\result.jpg`
* for react output 
    - react page: `output_path\out_imagename\react\block.js`
    
<br>Example

- Input image
![alt text](https://raw.githubusercontent.com/kanikamittal1811/SMART-UI-SU-209464/main/data/input/wireframe/1.png?token=AKQEPALDCCMGU6GYKCEW7NC77XSW6)
- Output html
![alt text](https://raw.githubusercontent.com/kanikamittal1811/SMART-UI-SU-209464/main/data/input/out.PNG?token=AKQEPAOQZNCXRZ5FIDWNPIC77XSUE)
---

### Models

* East text extractor: A deep learning model that extracts text areas for the input wireframe images 

* Tesseract : Recognizes text extracted form the input image

* Element Recognizer: A CNN model that detects Various Elements such as Button, EditText, Imageview etc  

* Color Exractor: Utilizes kmeans clustering model to get the color of the component

* Compiler: A Python Scripts that converts compo_html.json to html webpage/ React page

---
