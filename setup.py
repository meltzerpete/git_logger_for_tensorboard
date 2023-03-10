# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
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
# ==============================================================================


import setuptools


setuptools.setup(
    name="git_logger_for_tensorboard",
    version="0.1.0",
    description="Automatically log git repo info and patches to tensorboard.",
    packages=["git_logger_for_tensorboard"],
    package_data={
        "git_logger_for_tensorboard": ["static/**"],
    },
    entry_points={
        "tensorboard_plugins": [
            "git_logger = git_logger_for_tensorboard.plugin:ExamplePlugin",
        ],
        "console_scripts": [
            "git_logger_view = git_logger_for_tensorboard.view:main"
        ]
    },
    install_requires=["GitPython>=1.0.0"],
)
