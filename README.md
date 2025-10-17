# 🧩 Group Exercise — Image Processing Pipeline with Git and Python

## 🎯 Objective
In this exercise, you will work in a **group of three students** to build a simple **data processing pipeline** using Python and GitHub.  
Each student will be responsible for one part of the workflow — from reading an image and converting it to JSON, to extracting features, and finally visualizing results.

---

## 🧑‍🤝‍🧑 Group Setup

1. **Create a GitHub repository** for your group project.  
   - The repository name should follow this format:  
     ```
     data-infra-groupX
     ```
     *(replace X with your group number)*  

2. **Add the given `.tif` image** (provided by the instructor) to the repository root directory.

3. Each student should:
   - **Clone** the repository.
   - **Create and work on their own branch**, named according to their assigned task:
     - `task1`
     - `task2`
     - `task3`

---

## 🧠 Tasks

### 🧩 Task 1 — Image to JSON Conversion

**Responsible student:** Branch `task1`

1. Write a **Python class** (e.g., `ImageToJson`) that:
   - Reads the `.tif` image from disk.
   - Converts the image data and metadata into a **JSON structure**.
   - Filters out all features whose values are `"null"` or `None`.

2. Save the resulting JSON file in the repository (e.g., `data.json`).

**Suggested libraries:** `Pillow`, `numpy`, `json`

---

### 🧩 Task 2 — Feature Extraction

**Responsible student:** Branch `task2`

1. Write a **Python class** (e.g., `FeatureExtractor`) that:
   - Reads the `data.json` file created in Task 1.
   - Extracts **six specific features** (AP_WD; AP_BEAM_TIME; AP_IMAGE_PIXEL_SIZE; AP_HOLDER_HEIGHT, AP_BEAM_CURRENT, AP_HOLDER_DIAMETER).
   - Saves the selected features into a new JSON file (e.g., `selected_features.json`).

2. Ensure your code handles missing keys gracefully.

**Suggested libraries:** `json`, `pandas`

---

### 🧩 Task 3 — Visualization and Execution

**Responsible student:** Branch `task3`

1. Write a **Python script or class** (e.g., `Visualizer`) that:
   - Plots the original `.tif` image.
   - Displays a table (or printed DataFrame) showing the **keys and values** of the features selected in Task 2.

2. The final program should be **runnable by a user** as follows:
   - When executed, it should **ask for the name of the `.tif` file** as input (e.g., via `input()` or a command-line argument).
   - After the user provides the filename, the program should automatically perform:
     - Image reading  
     - JSON creation (Task 1)  
     - Feature extraction (Task 2)  
     - Visualization (Task 3)

**Suggested libraries:** `matplotlib`, `pandas`, `Pillow`

---

## 🔄 Collaboration and Integration

- Each student works independently on their branch.
- After finishing, open a **Pull Request** to merge your branch into the main branch.
- Review each other’s code before merging.
- Ensure that the final main branch contains a **complete, working pipeline**.

---

## ✅ Deliverables

Your final GitHub repository should include:
- The `.tif` image.
- The Python scripts for Task 1, Task 2, and Task 3.
- The generated JSON files (`data.json`, `selected_features.json`).
- A short `README.md` describing:
  - The group members.
  - The purpose of each script.
  - How to run the pipeline.

---

💡 *Tip:* Make sure your code is well-documented and modular — each class should be reusable and callable from the main program in Task 3.
