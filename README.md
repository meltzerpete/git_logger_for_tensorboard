# Git Logger for Tensorboard

## Features

- [x] Log current git commit hash
- [x] diff of current repo state
- [ ] pytorch-lightning integration

## Usage

With pytorch-lightning:

```python
from pytorch_lightning.loggers import TensorBoardLogger
from git_logger import

tensorboard_logger = TensorBoardLogger(save_dir='lightning_logs',
                                       name='my_experiment')
git_logger = GitLightningLogger(lightning_tb_logger=tensorboard_logger)

trainer = pl.Trainer(*usual_args,
                     logger=[tensorboard_logger, git_logger])

# train and test as normal
# every call to train, validate or test will create a log entry
trainer.fit()
trainer.test()
```

Without pytorch-lightning:

```python
from tensorflow import summary
from git_logger_for_tensorboard import git_logger

writer = summary.create_file_writer("demo_logs")
with writer.as_default():
    git_logger.log(tag='train', step=0)
```