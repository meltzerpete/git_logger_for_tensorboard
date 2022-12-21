# Git Logger for Tensorboard with Pytorch
          
## Contents

- [Features](#Features)
- [Dependencies](#Dependencies)
- [Installation](#Installation)
- [Usage](#Usage)
  - [Logging](#Logging)
  - [Viewing the Logs](#Viewing-the-Logs)

## Features

- [x] log current git commit hash
- [x] diffs of current repo state
- [x] pytorch-lightning integration
- [x] view logs in terminal
- [x] view logs in tensorboard

## Dependencies

Requires:

- python + pip
- tensorboard
- pytorch
- OPTIONAL: tensorflow

Note: **Full tensorflow installation is required to view logs in tensorboard.** This is currently a requirement for
all custom plugins. The plugin will still log without tensorflow, and logs can be viewed in the terminal (see below).

## Installation

Ensure you have the above dependencies, then run:

```shell
pip install git+ssh://git@github.com/meltzerpete/git_logger_for_tensorboard.git#egg=git_logger_for_tensorboard
````

## Usage

### Logging

With pytorch-lightning:

```python
import pytorch_lightning as pl
from pytorch_lightning.loggers import TensorBoardLogger
from git_logger_for_tensorboard.git_logger import GitLightningLogger

tensorboard_logger = TensorBoardLogger(save_dir='lightning_logs',
                                       name='my_experiment')
tb_logger = TensorBoardLogger(save_dir='lightning_logs',
                              name='my_model')
GitLightningLogger(tb_logger).log('train')  # all git info/patches are logged to the current lightning run dir

trainer = pl.Trainer(*usual_args,
                     logger=tensorboard_logger)
...
```

With pytorch only:

```python
from torch.utils.tensorboard import SummaryWriter

from git_logger_for_tensorboard.git_logger import GitLogger

summary_writer = SummaryWriter(log_dir='demo6')
GitLogger(summary_writer).log('train')  # all git info/patches are logged to the log_dir

...
```

### Viewing the Logs

If tensorflow is installed, simply go to the `GIT_LOGGER` tab in tensorboard.

![](https://github.com/meltzerpete/git_logger_for_tensorboard/blob/main/img/Screenshot%202022-12-21%20at%2014.56.48.png)

If tensorflow is not installed, you can view the logs in the terminal by running (ensure you have restarted your shell
after installation from pip):

```shell
$ git_logger_view --logdir lightning_logs                                                                                                                                                                     main ✚ ✱ ◼

Run: lightning_logs/my_model/version_0
        - branch: main
        - remote_url: git@github.com:meltzerpete/git_logger_for_tensorboard.git
        - last_commit: b7f80b13961c5f66b4c7ca088457c3c979651a1d
        - last_upstream: b7f80b13961c5f66b4c7ca088457c3c979651a1d
        - patch: False
        - upstream_patch: True

...
```

`patch` and `upstream_patch` indicate if a patch is saved (because there were local differences against the commits),
and you can view these as follows:

```shell
$ git_logger_view --patch lightning_logs/my_model/version_0
#              or --upstream_patch
```

or save them to file with:

```shell
$ git_logger_view --patch lightning_logs/my_model/version_0 > my_diff.patch
#              or --upstream_patch
```
