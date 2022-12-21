import json
import os
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

from tensorboard.backend.event_processing import event_accumulator


def parse_tensorboard(path, patch=None):
    """returns a dictionary of pandas dataframes for each requested scalar"""
    ea = event_accumulator.EventAccumulator(
        path,
        size_guidance={event_accumulator.TENSORS: 0},
    )
    _absorb_print = ea.Reload()

    for t in ea.Tensors('git_logger'):
        try:
            string = t.tensor_proto.string_val[0].decode('utf-8')
            data = json.loads(string)
            if patch == 'patch':
                _display_patch(data)
            elif patch == 'upstream':
                _display_upstream(data)
            else:
                _display(path, data)
        except Exception as e:
            print(e)


def _display(run, data):
    print('\nRun:', run)
    print('\t- branch:', data['branch'])
    print('\t- remote_url:', data['remote_url'])
    print('\t- last_commit:', data['last_commit'])
    print('\t- last_upstream:', data['last_upstream'])
    print('\t- patch:', data['patch'] is not None)
    print('\t- upstream_patch:', data['upstream_patch'] is not None)


def _display_patch(data):
    print(data['patch'])


def _display_upstream(data):
    print(data['upstream_patch'])


def main():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--logdir', type=str, default='./',
                        help='root directory containing tb logs')
    parser.add_argument('--patch', type=str, default=None,
                        help='pass the path for a single run as --patch arg to view patch')
    parser.add_argument('--upstream_patch', type=str, default=None,
                        help='pass the path for a single run as --upstream_patch arg to view upstream patch')
    args = parser.parse_args()

    if args.patch and args.upstream_patch:
        raise ValueError('Cannot set --patch and --upstream_patch, use one at a time.')

    if args.patch:
        parse_tensorboard(args.patch, patch='patch')
    elif args.upstream_patch:
        pass
    else:
        for root, dirs, files in os.walk(args.logdir):
            if len(list(filter(lambda f: f.startswith('events.out.tfevents'), files))) > 0:
                parse_tensorboard(root)


if __name__ == '__main__':
    main()