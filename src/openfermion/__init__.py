#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
OpenFermion

For more information, examples, or tutorials visit our website:

www.openfermion.org
"""

from openfermion import (gates, hamiltonians, measurements, ops, primitives,
                         testing, third_party, transforms, trotter, utils)

from openfermion.gates import (
    FSWAP, CRxxyy, CRyxxy, CubicFermionicSimulationGate, DoubleExcitation,
    DoubleExcitationGate, FSwapPowGate, ParityPreservingFermionicGate,
    QuadraticFermionicSimulationGate, QuarticFermionicSimulationGate, Rxxyy,
    Ryxxy, Rzz, fermionic_simulation_gates_from_interaction_operator, rot11,
    rot111)

from openfermion.hamiltonians import (
    FermiHubbardModel, HartreeFockFunctional, MolecularData, bose_hubbard,
    dual_basis_external_potential, dual_basis_jellium_model, dual_basis_kinetic,
    dual_basis_potential, fermi_hubbard, generate_hamiltonian,
    get_matrix_of_eigs,
    hypercube_grid_with_given_wigner_seitz_radius_and_filling, jellium_model,
    jordan_wigner_dual_basis_hamiltonian, jordan_wigner_dual_basis_jellium,
    load_molecular_hamiltonian, make_atom, make_atomic_lattice,
    make_atomic_ring, mean_field_dwave, periodic_table,
    plane_wave_external_potential, plane_wave_hamiltonian, plane_wave_kinetic,
    plane_wave_potential, rhf_minimization, rhf_params_to_matrix,
    wigner_seitz_length_scale)

from openfermion.measurements import (
    apply_constraints, binary_partition_iterator, constraint_matrix,
    linearize_term, one_body_fermion_constraints, partition_iterator,
    pauli_string_iterator, prony, two_body_fermion_constraints,
    unlinearize_term)

from openfermion.ops import (
    BinaryCode, BinaryPolynomial, BosonOperator, DiagonalCoulombHamiltonian,
    FermionOperator, InteractionOperator, InteractionRDM, IsingOperator,
    MajoranaOperator, PolynomialTensor, QuadOperator, QuadraticHamiltonian,
    QubitOperator, SymbolicOperator, down_index, general_basis_change, up_index)

from openfermion.primitives import (ffft, prepare_gaussian_state,
                                    prepare_slater_determinant)

from openfermion.primitives.bogoliubov_transform import (
    bogoliubov_transform,)

from openfermion.primitives.swap_network import (
    swap_network,)

from openfermion.third_party import (fixed_trace_positive_projection, heaviside,
                                     higham_polynomial, higham_root,
                                     map_to_matrix, map_to_tensor)

from openfermion.transforms import (
    binary_code_transform, bravyi_kitaev, bravyi_kitaev_code,
    bravyi_kitaev_fast, bravyi_kitaev_tree, checksum_code, dissolve,
    edit_hamiltonian_for_spin, get_boson_operator,
    get_diagonal_coulomb_hamiltonian, get_fermion_operator,
    get_interaction_operator, get_interaction_rdm, get_majorana_operator,
    get_molecular_data, get_number_preserving_sparse_operator,
    get_quad_operator, get_quadratic_hamiltonian, get_sparse_operator,
    interleaved_code, jordan_wigner, jordan_wigner_code, linearize_decoder,
    parity_code, project_onto_sector, projection_error, reverse_jordan_wigner,
    rotate_qubit_by_pauli, symmetric_ordering,
    symmetry_conserving_bravyi_kitaev, verstraete_cirac_2d_square,
    weight_one_binary_addressing_code, weight_one_segment_code,
    weight_two_segment_code, weyl_polynomial_quantization)

from openfermion.trotter import (
    simulate_trotter,)

from openfermion.utils import (
    Davidson, DavidsonOptions, Grid, HubbardSquareLattice, LinearQubitOperator,
    LinearQubitOperatorOptions, ParallelLinearQubitOperator, QubitDavidson,
    SparseDavidson, Spin, SpinPairs, amplitude_damping_channel, anticommutator,
    bch_expand, boson_ladder_sparse, boson_operator_sparse, chemist_ordered,
    commutator, count_qubits, dephasing_channel, depolarizing_channel,
    double_commutator, eigenspectrum, erpa_eom_hamiltonian, error_bound,
    error_operator, expectation, expectation_computational_basis_state,
    fourier_transform, freeze_orbitals, gaussian_state_preparation_circuit,
    generate_linear_qubit_operator, generate_parity_permutations,
    geometry_from_pubchem, get_chemist_two_body_coefficients,
    get_density_matrix, get_file_path, get_gap, get_ground_state,
    get_linear_qubit_operator_diagonal, group_into_tensor_product_basis_sets,
    haar_random_vector, hartree_fock_state_jellium, hermitian_conjugated,
    inline_sum, inner_product, inverse_fourier_transform, is_hermitian,
    is_identity, jordan_wigner_sparse, jw_configuration_state,
    jw_get_gaussian_state, jw_get_ground_state_at_particle_number,
    jw_hartree_fock_state, jw_number_restrict_operator,
    jw_number_restrict_state, jw_slater_determinant, jw_sz_restrict_operator,
    jw_sz_restrict_state, kronecker_delta, lambda_norm, load_operator,
    low_depth_second_order_trotter_error_bound,
    low_depth_second_order_trotter_error_operator,
    low_rank_two_body_decomposition, majorana_operator,
    make_reduced_hamiltonian, map_one_hole_dm_to_one_pdm,
    map_one_pdm_to_one_hole_dm, map_particle_hole_dm_to_one_pdm,
    map_particle_hole_dm_to_two_pdm, map_two_hole_dm_to_one_hole_dm,
    map_two_hole_dm_to_two_pdm, map_two_pdm_to_one_pdm,
    map_two_pdm_to_particle_hole_dm, map_two_pdm_to_two_hole_dm,
    module_importable, normal_ordered, number_operator, pauli_exp_to_qasm,
    prepare_one_body_squared_evolution,
    preprocess_lcu_coefficients_for_reversible_sampling, prune_unused_indices,
    qubit_operator_sparse, random_antisymmetric_matrix,
    random_diagonal_coulomb_hamiltonian, random_hermitian_matrix,
    random_interaction_operator, random_quadratic_hamiltonian,
    random_qubit_operator, random_unitary_matrix, reduce_number_of_terms,
    reorder, s_minus_operator, s_plus_operator, s_squared_operator,
    save_operator, singlet_erpa, slater_determinant_preparation_circuit,
    sparse_eigenspectrum, sx_operator, sy_operator, sz_operator,
    taper_off_qubits, trotter_operator_grouping, trotterize_exp_qubop_to_qasm,
    uccsd_convert_amplitude_format, uccsd_generator, uccsd_singlet_generator,
    uccsd_singlet_get_packed_amplitudes, uccsd_singlet_paramsize, up_then_down,
    variance, wedge)

from ._version import \
    __version__
