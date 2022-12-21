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
"""Summaries for the example_basic plugin."""
import json

from tensorboard.compat.proto import summary_pb2
from tensorboard.compat.proto.summary_pb2 import SummaryMetadata, Summary
from tensorboard.compat.proto.tensor_pb2 import TensorProto
from tensorboard.compat.proto.tensor_shape_pb2 import TensorShapeProto
from torch.utils.tensorboard import SummaryWriter

from git_logger_for_tensorboard import metadata
from git_logger_for_tensorboard.code_state import CodeState
from git_logger_for_tensorboard.git_repo import GitRepo


class GitLogger:
    def __init__(self, summary_writer: SummaryWriter):
        self.summary_writer = summary_writer

    def log(self, tag):
        writer = self.summary_writer._get_file_writer()
        tensor = TensorProto(
            dtype="DT_STRING",
            string_val=[_create_git_summary().encode(encoding="utf_8")],
            tensor_shape=TensorShapeProto(dim=[TensorShapeProto.Dim(size=1)]),
        )
        summary = Summary(
            value=[Summary.Value(tag=tag, metadata=_create_summary_metadata(), tensor=tensor)]
        )
        writer.add_summary(summary)


def _create_summary_metadata():
    return SummaryMetadata(
        summary_description='git logger',
        plugin_data=summary_pb2.SummaryMetadata.PluginData(
            plugin_name=metadata.PLUGIN_NAME,
            content=b"",  # no need for summary-specific metadata
        ),
        data_class=summary_pb2.DATA_CLASS_TENSOR,
    )


def _create_git_summary():
    repo = GitRepo()
    code_state = CodeState(repo)
    patch = code_state.patch
    upstream_patch = code_state.upstream_patch

    summary = {
        'branch': repo.branch,
        'last_commit': repo.last_commit,
        'remote_url': repo.remote_url,
        'last_upstream': str(repo.get_upstream_fork_point()),
        'patch': patch,
        'upstream_patch': upstream_patch
    }
    return json.dumps(summary)
