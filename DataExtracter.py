import pandas as pd
import re

def extract_vt_data(data, length, width, physical_property, outlier_threshold):
    all_dies_data = pd.DataFrame()
    qualified_data_all_dies = pd.DataFrame()

    for die in range(0, 26):  # Adjust die range as needed
        pattern = rf'\bIdVg(?:#\d+)?\.{physical_property}\b'
        device_data = data[(data['Module'].str.contains(rf'\bL{length}W{width}-\d+\b', regex=True)) &
                           (data['Name'].str.contains(pattern, regex=True)) &
                           (data['Die'] == die)]

        # Exclude outliers and aggregate the qualified data
        qualified_data = device_data[device_data['Data'] < outlier_threshold]
        qualified_data_all_dies = pd.concat([qualified_data_all_dies, qualified_data])

        vt_values = qualified_data['Data'].values
        stats = pd.Series(vt_values).describe() if len(vt_values) > 0 else pd.Series(dtype=float)
        yield_percentage = (len(vt_values) / 10.0) * 100  # Assuming 5 devices per die
        stats['yield'] = yield_percentage

        stats['DieX'] = qualified_data.iloc[0]['DieX'] if not qualified_data.empty else None
        stats['DieY'] = qualified_data.iloc[0]['DieY'] if not qualified_data.empty else None
        stats.name = die
        all_dies_data = pd.concat([all_dies_data, stats], axis=1)

    all_dies_data = all_dies_data.transpose()
    all_dies_data.index.name = 'Die'
    all_dies_data.reset_index(inplace=True)

    return all_dies_data, qualified_data_all_dies

def extract_and_combine_data(data, combined_sizes, physical_property, outlier_threshold):
    # Initialize a DataFrame to hold the combined data for all dies
    all_dies_combined_data = pd.DataFrame()

    # Process each die
    for die in range(0, 26):  # Adjust die range as needed
        combined_device_data = pd.DataFrame()

        for length, width in combined_sizes:
            # Construct a regex pattern to match the Name column entries for this device
            pattern = rf'\bIdVg(?:#\d+)?\.{physical_property}\b'

            # Filter data for this device size, die, and pattern
            device_data = data[(data['Module'].str.contains(rf'\bL{length}W{width}-\d+\b', regex=True)) &
                               (data['Name'].str.contains(pattern, regex=True)) &
                               (data['Die'] == die)]

            # Exclude outliers
            device_data = device_data[device_data['Data'] < outlier_threshold]

            # Combine data for the specified device sizes
            combined_device_data = pd.concat([combined_device_data, device_data], ignore_index=True)

        # Extract and aggregate the values
        values = combined_device_data['Data'].values

        # Calculate statistics and yield
        if len(values) > 0:
            stats = pd.Series(values).describe()
            # Calculate yield as a percentage
            yield_percentage = (len(values) / (10 * len(combined_sizes))) * 100  # Adjust the denominator based on the number of devices per die
            stats['yield'] = yield_percentage

            # Include DieX and DieY values from the first entry of combined_device_data
            if not combined_device_data.empty:
                stats['DieX'] = combined_device_data.iloc[0]['DieX']
                stats['DieY'] = combined_device_data.iloc[0]['DieY']

            stats.name = die
            all_dies_combined_data = pd.concat([all_dies_combined_data, stats], axis=1)
    
    # Transpose DataFrame so that each die is a row
    all_dies_combined_data = all_dies_combined_data.transpose()

    # Rename the index to 'Die' and keep DieX and DieY
    all_dies_combined_data.index.name = 'Die'
    all_dies_combined_data.reset_index(inplace=True)

    return all_dies_combined_data

# Main interaction
if __name__ == '__main__':
    file_path = input("Enter the path of your CSV file: ")
    physical_property = input("Enter the physical property for the extractor (e.g., Vtlci_lin, Gmmax_lin, Sst_lin, Fdibl): ")
    outlier_threshold = float(input("Enter the outlier threshold value: "))
    data = pd.read_csv(file_path)

    device_sizes = [(500, 700), (200, 700), (150, 700), (100, 700), (60, 700)]

    combined_sizes_500 = [(500, 350), (500, 700)]
    combined_sizes_200 = [(200, 350), (200, 700)]
    combined_sizes_150 = [(150, 350), (150, 700)]

    output_file_name = input("Enter the name of the Excel file to save (e.g., 'output.xlsx'): ")
    writer = pd.ExcelWriter(output_file_name, engine='xlsxwriter')

    try:
        # Process individual device sizes
        for length, width in device_sizes:
            stats_df, qualified_data_df = extract_vt_data(data, length, width, physical_property, outlier_threshold)
            sheet_name = f'L{length}W{width}'
            if not stats_df.empty:
                stats_df.to_excel(writer, sheet_name=sheet_name)
                qualified_sheet_name = f'Qualified_{sheet_name}'
                qualified_data_df.to_excel(writer, sheet_name=qualified_sheet_name)
                print(f"Data for {sheet_name} processed successfully.")

        # Process combined sizes 500
        combined_data_500 = extract_and_combine_data(data, combined_sizes_500, physical_property, outlier_threshold)
        if not combined_data_500.empty:
            combined_data_500.to_excel(writer, sheet_name='L500 W350 and W700')

        # Process combined sizes 200
        combined_data_200 = extract_and_combine_data(data, combined_sizes_200, physical_property, outlier_threshold)
        if not combined_data_200.empty:
            combined_data_200.to_excel(writer, sheet_name='L200 W350 and W700')
        
        # Process combined sizes 150
        combined_data_150 = extract_and_combine_data(data, combined_sizes_150, physical_property, outlier_threshold)
        if not combined_data_200.empty:
            combined_data_150.to_excel(writer, sheet_name='L150 W350 and W700')

        # Close the Pandas Excel writer and save the Excel file
        writer.close()
        print(f"All data saved to {output_file_name}")

    except Exception as e:
        print(f"An error occurred: {e}")
