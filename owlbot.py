# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import shutil

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

# ----------------------------------------------------------------------------
# Copy the generated client from the owl-bot staging directory
# ----------------------------------------------------------------------------

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    # Work around gapic generator bug https://github.com/googleapis/gapic-generator-python/issues/902
    s.replace(library / f"google/cloud/service_usage_{library.name}/types/serviceusage.py",
                r""".
    Attributes:""",
                r""".\n
    Attributes:""",
    )

    # There is an extra space in one of the doc strings
    # Submitted cl/379042419 to fix this formatting issue upstream
    s.replace(library / f"google/cloud/service_usage_{library.name}/types/serviceusage.py",
                r"        page\_size \(int\)\:\n"
                "            Requested size of the next page of data.\n"
                "            Requested page size cannot exceed 200.\n"
                "             If not set, the default page size is 50.",
                "        page_size (int):\n"
                "            Requested size of the next page of data.\n"
                "            Requested page size cannot exceed 200.\n"
                "            If not set, the default page size is 50."
    )

    s.move(library, excludes=["setup.py", "README.rst", "docs/index.rst"])

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = gcp.CommonTemplates().py_library(microgenerator=True)
python.py_samples(skip_readmes=True)
s.move(templated_files, excludes=[".coveragerc"]) # the microgenerator has a good coveragerc file

# ----------------------------------------------------------------------------
# Run blacken session
# ----------------------------------------------------------------------------

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
