# The 'Vid
## Anti-Rona Task Force

### Authors
- Clay Beabout (AD)
- Brandon Pramann (AD)
- Bailey Srimoungchanh (TS)
- Jon Volden (TS)
- Benjamin Wyss (Cl)

---

### Data
- U.S. County Census Data. [link](https://covid19.census.gov/datasets/21843f238cbb46b08615fc53e19e0daf/data?geometry=136.810%2C28.795%2C-136.179%2C67.148).
- New York Times Live, Historical, and Mask Use Data. [link](https://github.com/nytimes/covid-19-data).
- Kaggle Lockdown Data. [link](https://www.kaggle.com/lin0li/us-lockdown-dates-dataset).

---

### Devops 
When the repo is pulled, run the following to update submodules:

```
git submodule init
git submodule update --remote --recursive
```

---

### The Project

The COVID-19 epidemic continues to have an unprecedented negative impact on our economy and communities. 

For this project, we focus on U.S. COVID-19 related data sets to analyze and diagnose total cases, total deaths, survival rates, state success stories and anomalies in infection numbers.

We identify three main data science problems that exist in U.S. COVID-19 related data sets that we seek to answer:

1. Can we predict future U.S. COVID-19 trends based on historical data?

2. Is the overall rate of infection related to state and county responses?

3. Can we detect and explain anomalies in U.S. COVID-19 infections?

In short, we find that the answer to these questions are yes, yes, and yes. For more detailed answers and analysis, check out our presentation in the /details/ folder or at the link provided at the bottom of this README.

---

### Repository Structure

- /data/ contains raw and processed datasets used in our analysis.
- /details/ contains our project proposal and presentation pdfs.
- /notebooks/ contains jupyter notebooks detailing most of our exploratory data analysis.
- /src/ contains python map generation code that was better suited as standalone code than jupyter notebooks.
- /visualizations/ contains some basic visualizations generated from our data. More advanced visualizations are found in our formal presentation. 

---

### Presentation 
To view our animated formal presentation including analysis, process, and results, click [here](https://docs.google.com/presentation/d/1kg-K-5UqdrL2nfIIDklv58beWXhHF-lpX1oGpWL_rGI/edit?usp=sharing).

An unanimated pdf version of our presentation is also available within the /details/ folder.
