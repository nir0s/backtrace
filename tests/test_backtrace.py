# Copyright 2015,2016 Nir Cohen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import shlex

import pytest
import click.testing as clicktest

import backtrace


def _invoke(command):
    cli = clicktest.CliRunner()

    lexed_command = command if isinstance(command, list) \
        else shlex.split(command)
    func = lexed_command[0]
    params = lexed_command[1:]
    return cli.invoke(getattr(backtrace, func), params)


class TestGeneral:
    def test_base(self):
        backtrace.hook()
        try:
            test_message = 'Test message'
            with pytest.raises(RuntimeError) as ex:
                raise RuntimeError(test_message)
            assert ex._excinfo[0].__name__ == 'RuntimeError'
            assert test_message in str(ex)
        finally:
            backtrace.unhook()
