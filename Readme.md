Complete pseudo code implementation

1. download data every day at 11pm for all the systems
2. Refactor the data clean and transform it
3. upload the transformd data with timestamp to the GCP
4. Run the COP script and upload just cop, cooling_load, timestamps to gcp in separate folder for each system
5. Run the uncertainty script for last day upload it do different folder in GCP

COPData/
│
├── sitedata/
│   ├── data_2024-10-01.csv
│   ├── data_2024-10-02.csv
│   ├── data_2024-10-03.csv
│   └── ... (more files for each processed date)
│
├── transformed/
│   ├── 2024-10-01_transformed1.csv
│   ├── 2024-10-01_transformed2.csv
│   ├── 2024-10-02_transformed1.csv
│   ├── 2024-10-02_transformed2.csv
│   └── ... (more files for each processed date)
│
└── Results/
    ├── 2024-10-01_results1.csv
    ├── 2024-10-01_results2.csv
    ├── 2024-10-02_results1.csv
    ├── 2024-10-02_results2.csv
    └── ... (more files for each processed date)
