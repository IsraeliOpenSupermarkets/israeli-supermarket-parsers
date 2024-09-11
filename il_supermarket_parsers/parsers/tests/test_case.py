
import unittest
import os
import uuid
from il_supermarket_scarper.utils import FileTypesFilters
from il_supermarket_parsers.parser_factroy import ParserFactory
from il_supermarket_parsers.utils import get_sample_data


def make_test_case(scraper_enum, parser_enum, store_id):
    """create test suite for scraper"""

    class TestScapers(unittest.TestCase):
        """class with all the tests for scraper"""

        def __init__(self, name) -> None:
            super().__init__(name)
            self.scraper_enum = scraper_enum
            self.parser_enum = parser_enum
            self.folder_name = "temp"

        def _delete_folder_and_sub_folder(self, download_path):
            """delete a folder and all sub-folder"""
            files_found = os.listdir(download_path)
            for file in files_found:
                file_path = os.path.join(download_path, file)
                if os.path.isdir(file_path):
                    self._delete_folder_and_sub_folder(file_path)
                    os.rmdir(file_path)
                else:
                    os.remove(file_path)

        def _delete_download_folder(self, download_path):
            """delete the download folder"""
            if os.path.isdir(download_path):
                self._delete_folder_and_sub_folder(download_path)
                os.removedirs(download_path)

        def _make_sure_filter_work(
            self,
            files_found,
            file_type=None,
            limit=None,
            store_id=None,
            only_latest=False,
        ):
            """make sure the file type filter works"""
            if file_type:
                filtered_files = 0
                for f_type in file_type:
                    filtered_files += len(FileTypesFilters.filter(f_type, files_found))
                assert len(files_found) == filtered_files
            if store_id:
                store_mark = []
                for file in files_found:
                    store_mark.append(int(file.split("-")[1]))
                assert len(set(store_mark)) == 1 and len(store_mark) == len(files_found)
            if only_latest:
                files_sources = []
                for file in files_found:
                    source = file.split("-")[:2]
                    assert source not in files_sources
                    store_mark.append(source)

            assert (
                not limit or len(files_found) == limit
            ), f""" Found {files_found}
                                                                f"files but should be {limit}"""

        def _make_sure_file_contain_chain_ids(self, chain_ids, file):
            """make sure the scraper download only the chain id"""
            found_chain_id = False
            for possible_chain_ids in chain_ids:
                if possible_chain_ids in file:
                    found_chain_id = True
            assert found_chain_id, f"should be one of {chain_ids} but {file}"

        def _make_sure_file_extension_is_xml(self, file_name):
            """make sure the file extension is xml"""
            file_ext = file_name.split(".")[-1]
            assert file_ext == "xml", f" should be xml but {file_ext}, file:{file_name}"

        def _make_sure_file_is_not_empty(self, scraper, full_file_path):
            """make sure the files is not empty"""
            if not scraper.is_valid_file_empty(full_file_path):
                assert (
                    os.path.getsize(full_file_path) != 0
                ), f"{full_file_path} is empty file."

        def _parser_validate(
            self,
            scraper_enum,
            dump_path="temp"
        ):
            self._delete_download_folder(dump_path)
            os.makedirs(dump_path)

            init_scraper_function = ParserFactory.get(scraper_enum)
            
            df = init_scraper_function(folder_name=dump_path)

            assert df.shape[0] > 0


        def _get_temp_folder(self):
            """get a temp folder to download the files into"""
            return self.folder_name + str(uuid.uuid4().hex)

        def test_parsing_store(self):
            """scrape one file and make sure it exists"""
            get_sample_data(
                            "samples_store", 
                            FileTypesFilters.STORE_FILE.name,
                            enabled_scrapers=[self.scraper_enum.name]
                            )
            self._parser_validate(parser_enum, "samples_store", limit=1)

        def test_parsing_promo(self):
            """scrape one file and make sure it exists"""
            get_sample_data(
                            "samples_promo", 
                            FileTypesFilters.PROMO_FILE.name,
                            enabled_scrapers=[self.scraper_enum.name]
                            )
            self._parser_validate(parser_enum, "samples_promo", limit=1)

        def test_parsing_promo_all(self):
            """scrape one file and make sure it exists"""
            get_sample_data(
                            "samples_promo_all", 
                            FileTypesFilters.PROMO_FULL_FILE.name,
                            enabled_scrapers=[self.scraper_enum.name]
                            )
            self._parser_validate(parser_enum, "samples_promo_all", limit=1)

        def test_parsing_prices(self):
            """scrape one file and make sure it exists"""
            get_sample_data(
                            "samples_prices", 
                            FileTypesFilters.PRICE_FILE.name,
                            enabled_scrapers=[self.scraper_enum.name]
                            )
            self._parser_validate(parser_enum, "samples_prices", limit=1)

        def test_parsing_prices_all(self):
            """scrape one file and make sure it exists"""
            get_sample_data(
                            "samples_prices_all", 
                            FileTypesFilters.PRICE_FULL_FILE.name,
                            enabled_scrapers=[self.scraper_enum.name]
                            )
            self._parser_validate(parser_enum, "samples_prices_all", limit=1)


    return TestScapers