# VT Data Extraction and Aggregation

This project contains scripts to extract and aggregate VT data from a CSV file. It processes the data for individual device sizes and combined device sizes, excluding outliers based on a specified threshold.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Functions](#functions)
  - [extract_vt_data](#extract_vt_data)
  - [extract_and_combine_data](#extract_and_combine_data)
- [Contributing](#contributing)
- [License](#license)
- [Contact Information](#contact-information)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Kampfer0083/DataExtracter.git
    ```
2. Navigate to the project directory:
    ```sh
    cd DataExtracter
    ```
3. Install the required dependencies:
    ```sh
    pip install pandas xlsxwriter
    ```

## Usage

1. Run the script:
    ```sh
    python DataExtracter.py
    ```
2. Provide the required inputs when prompted:
    - Path of your CSV file
    - Physical property for extraction (e.g., Vtlci_lin, Gmmax_lin, Sst_lin, Fdibl)
    - Outlier threshold value
    - Name of the Excel file to save the results

3. The script processes the data for individual device sizes and combined device sizes and saves the results to an Excel file.

## Functions

### extract_vt_data

This function extracts and aggregates VT data for a specific device size.

- **Parameters:**
  - `data`: DataFrame containing the input data.
  - `length`: Length of the device.
  - `width`: Width of the device.
  - `physical_property`: The physical property to filter the data.
  - `outlier_threshold`: Threshold to exclude outliers.

- **Returns:**
  - `all_dies_data`: DataFrame containing the aggregated data for all dies.
  - `qualified_data_all_dies`: DataFrame containing the qualified data for all dies.

### extract_and_combine_data

This function extracts and aggregates VT data for combined device sizes.

- **Parameters:**
  - `data`: DataFrame containing the input data.
  - `combined_sizes`: List of tuples with device sizes to combine.
  - `physical_property`: The physical property to filter the data.
  - `outlier_threshold`: Threshold to exclude outliers.

- **Device Sizes:**
  - Here are the default size sets in this program. Modify here for different data sets. - 
  - device_sizes = [(500, 700), (200, 700), (150, 700), (100, 700), (60, 700)]
      combined_sizes_500 = [(500, 350), (500, 700)]
      combined_sizes_200 = [(200, 350), (200, 700)]
      combined_sizes_150 = [(150, 350), (150, 700)]


- **Returns:**
  - `all_dies_combined_data`: DataFrame containing the aggregated data for all dies.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact Information

Your Name - [kampfer.lu@gmail.com](mailto:your-email@example.com)

Project Link: [https://github.com/Kampfer0083/DataExtracter](https://github.com/your-username/your-repo-name)
