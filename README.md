# 🗳️ Election Simulation Project

## 📌 Project Overview

This project models a simplified version of the Indian election system using synthetic data.

⚠️ **Disclaimer**

This project is for educational purposes only.
Not related to real Indian elections or any real-world election data.

## 🎯 Goal

To build a simulation of the election process, generate datasets for voters, constituencies, candidates, and polling booths, simulate voting day, and analyze the results.

The goal is to demonstrate how to:

1) Generate synthetic datasets (voters, candidates, constituencies, polling booths).
2) Simulate an election process with turnout, voting, and results.
3) Perform EDA (Exploratory Data Analysis) on the synthetic datasets.
4) Visualize the results with charts and treemaps.
5) Identify insights to potentially increase voter turnout (based on synthetic data).

## ⚙️ Tech Stack

* Python 3.x
* Pandas → data manipulation
* Matplotlib / Seaborn / Squarify → visualization (charts, treemaps)
* Numpy / Random → data generation and simulation

## 📂 Repository Structure

Election-Project/

│── Data/

│── candidate.py           # Generate candidate dataset

│── consituency.py         # Generate constituencies dataset

│── Polling_booth.py       # Generate polling booth dataset

│── voter_id_details.py    # Generate voters dataset

│── polling_day.py         # Simulate voting day

│── treemap.png            # Example visualization

│── README.md              # Project documentation

## ⚙️ Steps to Run

### 1️⃣ Clone Repository

```bash
git clone https://github.com/bmrudula22/Election-Project.git
cd Election-Project
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Generate Datasets

Run the following scripts:

```bash
python generate_synthetic_dataset.py
```

### 4️⃣ Run Voting Day Simulation

```bash
python polling_day.py
```

### 5️⃣ Analyze Results

Results will be available in:

* Tables (CSV/printed output)
* Visuals (pie chart, treemap, etc.)
* Majority Party result

## 📊 Example Output

* Table: Constituency vs Winning Candidate
* Pie Chart: Party-wise Seats Distribution
* Majority Party: "Party X forms the government"
