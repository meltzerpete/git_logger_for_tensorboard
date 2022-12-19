# Basic example TensorBoard plugin

## Overview

In this example, we define a custom summary op `greeting(name, guest)`, use it to write values from Python, and surface the data in TensorBoard's frontend. For a complete guide to plugin development, see [`ADDING_A_PLUGIN`](../../../../ADDING_A_PLUGIN.md).

![Screenshot](../../../../docs/images/example_basic.png "Basic example")

## Running the example

Generate some sample Greeting summaries by running [`demo.py`][demo_py]. Alternatively, to write Greetings from your own Python program, import [`summary_v2.py`][summary_v2_py], create a summary file writer, and call `summary_v2.greeting("very important people", "you", step)`.

[demo_py]: tensorboard_plugin_git_logger/demo.py
[summary_v2_py]: tensorboard_plugin_git_logger/summary_v2.py

Copy the directory `tensorboard/examples/plugins/example_basic` into a desired folder. In a virtualenv with TensorBoard installed, run:

```
python setup.py develop
```

This will link the plugin into your virtualenv. Then, just run

```
tensorboard --logdir /tmp/runs_containing_greetings
```

and open TensorBoard to the basic example tab.

After making changes to the Python code, you must restart TensorBoard for your changes to take effect. The example plugin serves web assets at runtime, so changes reflected upon reloading the page.

To uninstall, you can run

```
python setup.py develop --uninstall
```

to unlink the plugin from your virtualenv, after which you can also delete the `tensorboard_plugin_example.egg-info/` directory that the original `setup.py` invocation created.

# Git Logger for Tensorboard

## Features

- [ ] Log current git commit hash 
- [ ] diff of current repo state
- [ ] pytorch-lightning integration

## Usage

With pytorch-lightning:

```python
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

from tensorboard_plugin_git_logger import summary_v2

# create a SummaryWriter as normal
writer = summary.create_file_writer("demo_logs")
with writer.as_default():
    # log an entry
    summary_v2.greeting()
```