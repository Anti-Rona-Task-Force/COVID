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
- U.S. County Census Data. [link](https://covid19.census.gov/datasets/21843f238cbb46b08615fc53e19e0daf/data?geometry=136.810%2C28.795%2C-136.179%2C67.148)
- New York Times Live, Historical, and Mask Use Data. [link](https://github.com/nytimes/covid-19-data)
- Kaggle Lockdown Data. [link](https://www.kaggle.com/lin0li/us-lockdown-dates-dataset)

---

### Devops 
When the repo is pulled, run the following to update submodules:

```
git submodule init
git submodule update --remote --recursive
```

---

### Repository Structure

- /data/ contains raw and processed datasets used in our analysis
- /details/ contains our project proposal
- /notebooks/ contains jupyter notebooks detailing most of our exploratory data analysis
- /scipts/ contains computationally intensive scripts used to generate county adjacency data
- /src/ contains python map generation code that was better suited as standalone code than jupyter notebooks
- /visualizations/ contains some basic visualizations used to aid our presentation. More advanced visualizations are found in the /data/processed/ folder and in our presentation linked below

---

### Presentation 
To view the formal presentation including our analysis, process and results click [here](https://docs.google.com/presentation/d/1kg-K-5UqdrL2nfIIDklv58beWXhHF-lpX1oGpWL_rGI/edit?usp=sharing)
