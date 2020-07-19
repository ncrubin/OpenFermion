# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
A routine for constructing a circuit to exactly implement a unitary generated by
one-body rotations through the optimal Givens rotation network.  Construction
of this circuit can be found in Optica Vol. 3, Issue 12, pp. 1460-1465 (2016).
This Givens network improves upon the parallel Givens network for implementing
basis rotations in Phys. Rev. Lett. 120, 110501 (2018).
"""
from typing import cast, Iterable, Sequence, Tuple

import numpy
import cirq

from openfermion.ops._givens_rotations import (givens_matrix_elements,
                                               givens_rotate)
from openfermion import gates


class GivensTranspositionError(Exception):
    pass


class GivensMatrixError(Exception):
    pass


def optimal_givens_decomposition(qubits: Sequence[cirq.Qid],
                                 unitary: numpy.ndarray
                                ) -> Iterable[cirq.Operation]:
    r"""
    Implement a circuit that provides the unitary that is generated by
    single-particle fermion generators

    .. math::

        U(v) = exp(log(v)_{p,q}(a_{p}^{\dagger}a_{q} - a_{q}^{\dagger}a_{p})

    This can be used for implementing an exact single-body basis rotation

    Args:
        qubits: Sequence of qubits to apply the operations over.  The qubits
                should be ordered in linear physical order.
        unitary:
    """
    N = unitary.shape[0]
    right_rotations = []
    left_rotations = []
    for i in range(1, N):
        if i % 2 == 1:
            for j in range(0, i):
                # eliminate U[N - j, i - j] by mixing U[N - j, i - j],
                # U[N - j, i - j - 1] by right multiplication
                # of a givens rotation matrix in column [i - j, i - j + 1]
                gmat = givens_matrix_elements(unitary[N - j - 1, i - j - 1],
                                              unitary[N - j - 1, i - j - 1 + 1],
                                              which='left')
                right_rotations.append((gmat.T, (i - j - 1, i - j)))
                givens_rotate(unitary,
                              gmat.conj(),
                              i - j - 1,
                              i - j,
                              which='col')
        else:
            for j in range(1, i + 1):
                # elimination of U[N + j - i, j] by mixing U[N + j - i, j] and
                # U[N + j - i - 1, j] by left multiplication
                # of a givens rotation that rotates row space
                # [N + j - i - 1, N + j - i
                gmat = givens_matrix_elements(unitary[N + j - i - 1 - 1, j - 1],
                                              unitary[N + j - i - 1, j - 1],
                                              which='right')
                left_rotations.append((gmat, (N + j - i - 2, N + j - i - 1)))
                givens_rotate(unitary,
                              gmat,
                              N + j - i - 2,
                              N + j - i - 1,
                              which='row')

    new_left_rotations = []
    for (left_gmat, (i, j)) in reversed(left_rotations):
        phase_matrix = numpy.diag([unitary[i, i], unitary[j, j]])
        matrix_to_decompose = left_gmat.conj().T.dot(phase_matrix)
        new_givens_matrix = givens_matrix_elements(matrix_to_decompose[1, 0],
                                                   matrix_to_decompose[1, 1],
                                                   which='left')
        new_phase_matrix = matrix_to_decompose.dot(new_givens_matrix.T)

        # check if T_{m,n}^{-1}D  = D T.
        # coverage: ignore
        if not numpy.allclose(new_phase_matrix.dot(new_givens_matrix.conj()),
                              matrix_to_decompose):
            raise GivensTranspositionError("Failed to shift the phase matrix "
                                           "from right to left")
        # coverage: ignore

        unitary[i, i], unitary[j, j] = new_phase_matrix[0, 0], new_phase_matrix[
            1, 1]
        new_left_rotations.append((new_givens_matrix.conj(), (i, j)))

    phases = numpy.diag(unitary)
    rotations = []
    ordered_rotations = []
    for (gmat, (i, j)) in list(reversed(new_left_rotations)) + list(
            map(lambda x: (x[0].conj().T, x[1]), reversed(right_rotations))):
        ordered_rotations.append((gmat, (i, j)))

        # if this throws the impossible has happened
        # coverage: ignore
        if not numpy.isclose(gmat[0, 0].imag, 0.0):
            raise GivensMatrixError(
                "Givens matrix does not obey our convention that all elements "
                "in the first column are real")
        if not numpy.isclose(gmat[1, 0].imag, 0.0):
            raise GivensMatrixError(
                "Givens matrix does not obey our convention that all elements "
                "in the first column are real")
        # coverage: ignore

        theta = numpy.arcsin(numpy.real(gmat[1, 0]))
        phi = numpy.angle(gmat[1, 1])
        rotations.append((i, j, theta, phi))

    for op in reversed(rotations):
        i, j, theta, phi = cast(Tuple[int, int, float, float], op)
        if not numpy.isclose(phi, 0.0):
            yield cirq.Z(qubits[j])**(phi / numpy.pi)

        yield gates.Ryxxy(-theta).on(qubits[i], qubits[j])

    for idx, phase in enumerate(phases):
        yield cirq.Z(qubits[idx])**(numpy.angle(phase) / numpy.pi)
