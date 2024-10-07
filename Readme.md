# HVAC Data Processing Backend

This project provides a pipeline for downloading, processing, and uploading HVAC system data. It leverages various scripts to handle data transformation, COP calculation, uncertainty summary generation, and uploads the results to Google Cloud Platform (GCP) in an organized file structure.

## Project Structure

```markdown
.
├── main.py                   # Script for downloading data for the past 2 weeks daily.
├── sandbox.py                # Main script with all processing logic:
│   ├── Downloads data for the past 2 weeks
│   ├── Transforms data using Ahmad's scripts
│   ├── Calculates COP
│   ├── Generates uncertainty summary
│   └── Uploads resulting files to GCP
├── app.py                    # Backend logic for the dashboard.
└── README.md                 # Project documentation.
```

## GCP File Structure

The processed data is organized in the following structure in Google Cloud Storage (GCS):

```
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
├── Results/
│   ├── 2024-10-01_results1.csv
│   ├── 2024-10-01_results2.csv
│   ├── 2024-10-02_results1.csv
│   ├── 2024-10-02_results2.csv
│   └── ... (more files for each processed date)
│
└── uncertainity_summary/
    ├── file_2024-10-01.csv
    ├── file_2024-10-02.csv
    ├── file_2024-10-03.csv
    ├── file_2024-10-04.csv
    └── ... (more files for each processed date)
```

## Features

- **Data Download**: Automatically downloads HVAC data for the past two weeks daily.
- **Data Processing**: Passes the data through transformation scripts, calculates COP, and generates uncertainty summaries.
- **Cloud Upload**: Organizes and uploads processed files to Google Cloud Storage with a defined file structure.

## Requirements

- Python 3.x
- Required libraries:
  - `requests`
  - `pandas`
  - `google-cloud-storage`
  - `env` (for environment variables)
  - Any other dependencies used in Ahmad's scripts.

