# Copyright 2018 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Unit tests for the CirqDevice class
"""
from unittest.mock import patch

import cirq
import pennylane as qml
import pytest

from pennylane_cirq.cirq_device import CirqDevice


@patch.multiple(CirqDevice, __abstractmethods__=set())
class TestCirqDeviceInit:
    """Tests the routines of the CirqDevice class."""

    def test_default_init(self):
        """Tests that the device is properly initialized."""

        dev = CirqDevice(3, 100)

        assert dev.num_wires == 3
        assert dev.shots == 100

    def test_default_init_of_qubits(self):
        """Tests the default initialization of CirqDevice.qubits."""

        dev = CirqDevice(3, 100)

        assert len(dev.qubits) == 3
        assert dev.qubits[0] == cirq.LineQubit(0)
        assert dev.qubits[1] == cirq.LineQubit(1)
        assert dev.qubits[2] == cirq.LineQubit(2)

    def test_outer_init_of_qubits(self):
        """Tests that giving qubits as parameters to CirqDevice works."""

        qubits = [
            cirq.GridQubit(0, 0),
            cirq.GridQubit(0, 1),
            cirq.GridQubit(1, 0),
            cirq.GridQubit(1, 1),
        ]

        dev = CirqDevice(4, 100, qubits=qubits)

        assert len(dev.qubits) == 4
        assert dev.qubits[0] == cirq.GridQubit(0, 0)
        assert dev.qubits[1] == cirq.GridQubit(0, 1)
        assert dev.qubits[2] == cirq.GridQubit(1, 0)
        assert dev.qubits[3] == cirq.GridQubit(1, 1)

    def test_outer_init_of_qubits_error(self):
        """Tests that giving the wrong number of qubits as parameters to CirqDevice raises an error."""

        qubits = [
            cirq.GridQubit(0, 0),
            cirq.GridQubit(0, 1),
            cirq.GridQubit(1, 0),
            cirq.GridQubit(1, 1),
        ]

        with pytest.raises(
            qml.DeviceError,
            match="The number of given qubits and the specified number of wires have to match",
        ):
            dev = CirqDevice(3, 100, qubits=qubits)


@pytest.fixture(scope="function")
def cirq_device_1_wire():
    """A mock instance of the abstract Device class"""

    with patch.multiple(CirqDevice, __abstractmethods__=set()):
        yield CirqDevice(1, 0)


class TestOperations:
    """Tests that the CirqDevice correctly handles the requested operations."""

    def test_pre_apply(self, cirq_device_1_wire):
        """Tests that pre_apply resets the internal circuit."""

        assert cirq_device_1_wire.circuit is None

        cirq_device_1_wire.pre_apply()

        # Check if circuit is an empty cirq.Circuit
        assert cirq_device_1_wire.circuit == cirq.Circuit()