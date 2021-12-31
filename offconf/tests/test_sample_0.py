from json import dumps, load
from os import path
from unittest import TestCase
from unittest import main as unittest_main

from pkg_resources import resource_filename, resource_listdir

from offconf import replace_variables


class TestSample0(TestCase):
    @classmethod
    def setUpClass(cls):
        filename = "0.raw.json"
        if filename not in resource_listdir("offconf", "samples"):
            raise IOError("{filename} not found".format(filename=filename))

        file_location = path.join(
            path.dirname(resource_filename("offconf", "__init__.py")),
            "samples",
            filename,
        )
        with open(file_location, "rt") as f:
            cls.sample = load(f)
        with open(
            path.join(path.dirname(file_location), filename.replace("raw", "parsed")),
            "rt",
        ) as f:
            cls.parsed_sample = load(f)

    def test_parsing(self):
        self.assertEqual(
            replace_variables(
                dumps(self.sample),
                extra_env={"jar": "CAN"},
                variables={"foo": "HAZ", "bar": "BAR", "can_haz": "CAN_HAZ"},
            ),
            dumps(self.parsed_sample),
        )


if __name__ == "__main__":
    unittest_main()
