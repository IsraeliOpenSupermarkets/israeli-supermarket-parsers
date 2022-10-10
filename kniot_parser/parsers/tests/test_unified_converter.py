import shutil
from kniot_parser.parsers import UnifiedConverter
from kniot_parser.utils import read_dump_folder,get_sample_data

def test_unified():
    """ test converting to data frame """

    folder = "samples"
    get_sample_data(folder)

    files_to_scan = read_dump_folder(folder=folder)

    for _, row in files_to_scan.iterrows():

        converter = UnifiedConverter(row['store_name'],row['file_type'])
        data_frame = converter.convert(row['full_path'])

        assert data_frame.empty or len(data_frame[converter.get_key_column()].value_counts()
            ) == data_frame.shape[0],f"{row['full_path']}, key is not unique."
            #assert converter.should_convert_to_incremental()



    shutil.rmtree(folder)
