# Requirements Change for Process Compliance (RC4PC)
Impact Analysis of Regulatory Requirement Changes on Business Process Compliance


**RC4PC** is a research prototype for analyzing the **impact of changes in regulatory requirements on business process compliance**. It provides a three-step pipeline that leverages AI-assisted analysis (via GPT-4.1) and scripted logic to identify and assess changes and their implications on process compliance.

This repository accompanies the experiments and figures presented in the related research paper.

---

## Repository Structure

```
├── data/          # Input regulatory texts and output results
├── notebooks/     # Jupyter notebooks implementing the 3-step pipeline
├── scripts/       # Core scripts for change detection and evaluation
├── figures/       # Figures generated for the paper
├── environment.yml
├── config/         # Contains api_keys.json
├── ground_truth_sum_analysis_results/ # Includes an Excel sheet summarizing the ground truth and analyzing the results
```

### 1. `data/`
Contains both input and output data:
- Raw compliance requirements (old and new versions)
- Intermediate outputs from each pipeline step (i.e., step 1 and 2)
- Final impact analysis results (i.e., step 3)

### 2. `notebooks/`
Contains a Jupyter notebooks that implement the RC4PC pipeline:
- **Step 1:** Automatically formalizes compliance requirements provided in natural language text (calls OpenAI GPT-4.1)
- **Step 2:** Compute atomic change operations (calls script from `scripts/`)
- **Step 3:** Assess impact on compliance (calls OpenAI GPT-4.1 again)

### 3. `scripts/`
Includes Python scripts to:
- Identify atomic change operations between old and new versions of a formalized compliance requirement
- Evaluate the outputs of each step
- Support additional utility and analysis functions

### 4. `figures/`
All the figures and diagrams included in the paper are stored here.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone HERE_ADD_FINAL_REPOSITORY_URL/rc4pc.git
cd rc4pc
```

### 2. Set Up the Environment

Create a virtual environment and install the required packages:

```bash
conda env create -f environment.yml
conda activate rc4pc
```

### 3. Add Your Configuration

#### a. API Keys

Create a file named `api_keys.json` in the root directory with the following content:

```json
{
  "api_openai": "your_openai_api_key"
}
```

> This is required for steps that use OpenAI GPT-4.1.


## How to Run the Pipeline

Before starting, make a copy of the folder `data/output_template` and rename it to `data/output`.  
This folder provides the required structure for saving all test results.  
Each step is executed in a separate code cell within the Jupyter Notebook `AnalyzeImpactRequirementChangesProcessCompliance.ipynb`.


---

## Notes

- OpenAI API usage may incur costs. Use with caution and monitor your usage.
- All intermediate and final data artifacts are saved in the `data/` folder.
- The evaluation results used in the paper are stored in `data/output_to_eval`.

---

## Citation

If you use this codebase or results in your work, please cite the associated research paper (TO_COMPLETE). BibTeX will be provided once the paper is published.



























