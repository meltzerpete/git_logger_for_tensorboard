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
"""Demo code."""
from pytorch_lightning.loggers import TensorBoardLogger
from torch.utils.tensorboard import SummaryWriter

from git_logger_for_tensorboard.git_logger import GitLightningLogger, GitLogger


def main():
    # with pytorch
    summary_writer = SummaryWriter(log_dir='demo_logs')
    GitLogger(summary_writer).log()

    # with pytorch_lightning
    tb_logger = TensorBoardLogger(save_dir='lightning_logs',
                                  name='my_model')
    GitLightningLogger(tb_logger).log()


if __name__ == "__main__":
    main()
