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
