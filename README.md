# 🧩 Group Exercise — Image Processing Pipeline with Git and Python

## 🎯 Objective
In this exercise, you will work in a **group of three students** to build a simple **data processing pipeline** using Python and GitHub.  
Each student will be responsible for one part of the workflow — from reading an image and converting it to JSON, to extracting features, and finally visualizing results.

---

## 🧑‍🤝‍🧑 Group Setup

1. **Create a GitHub repository** for your group project.  
   - The repository name should follow this format:  
     ```
     data-infra-name-of-the-group
     ``` 

2. They push the cloned content to their group repo:

   git remote remove origin
   git remote add origin https://github.com/...../data-infra-name-of-the-group.git
   git push -u origin main

3. Each student should:
   - **Clone** the repository.
   - **Create and work on their own branch**, named according to their assigned task:
     - `metadata_extractor_module`
     - `json_cleaner_module`
     - `visualizer_module`

---

## 🧠 Tasks

### 🧩 Task 1 — Metadata Extractor Module

**Responsible student:** Branch `metadata_extractor_module`

1. Update semmeta/metadata_extractor_module.py in order to define a **Python class** that:
   - Reads the `name_of_image.tif` image from imgs folder.
   - Converts the image data and metadata into a **JSON structure**.

2. Save the resulting JSON file in the repository (e.g., `output/name_of_image_raw.json`).

**Suggested libraries:** `Pillow`, `numpy`, `json`

---

### 🧩 Task 2 — Json Cleaner Module

**Responsible student:** Branch `json_cleaner_module`

1. Update the semmeta/json_cleaner_module.py in order to write a **Python class** that:
  
   - Reads the `output/name_of_image_raw.json` file created in Task 1.
   - Filters out all features whose values are `"null"` or `None`.
   - Saves the new cleaned JSON file as `output/name_of_image_cleaned.json`.
  
2. Ensure your code handles missing keys gracefully (`output/name_of_image_cleaned.json` should have a key and a value for each feature.)

**Suggested libraries:** `json`, `pandas`

---

### 🧩 Task 3 — Extraction and Visualization

**Responsible student:** Branch `visualizer_module`

1. Update semmeta/visualizer_module.py  i order to write **Python script or class** that:
   - From `output/name_of_image_cleaned.json` extract the following features: AP_WD; AP_BEAM_TIME; AP_IMAGE_PIXEL_SIZE; AP_HOLDER_HEIGHT, AP_BEAM_CURRENT, AP_HOLDER_DIAMETER
   - Plots the original `.tif` image.
   - Displays a table (or printed DataFrame) showing the **keys and values** of the extracted features:
  
**Suggested libraries:** `matplotlib`, `pandas`, `Pillow`
  
### 🧩 Task 4 — Execution

Update the main.py file to write a function that allows executing the program by: 
   - asking for the name of the `name_of_image.tif` file** as input (e.g., via `input()` or a command-line argument).
   - calling all modules from previous tasks.



---

## 🔄 Collaboration and Integration

- Each student works independently on their branch.
- After finishing, open a **Pull Request** to merge your branch into the main branch.
- Review each other’s code before merging.
- Ensure that the final main branch contains a **complete, working pipeline**.

---



