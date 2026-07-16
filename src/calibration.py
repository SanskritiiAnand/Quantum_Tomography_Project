import numpy as np
import pandas as pd
from qiskit import QuantumCircuit
from itertools import product

def computational_basis_labels(num_qubits):
    """
    Return computational basis labels for the given number of qubits.
    """
    return ["".join(bits) for bits in product("01", repeat= num_qubits)]

def build_basis_calibration(num_qubits):
   """
   Build readout calibration circuits for all computational basis states. 
   Returns a dictionary keyed by basis labels
   """
   circuits= {}
   labels= computational_basis_labels(num_qubits)

   for label in labels:
      qc= QuantumCircuit(num_qubits, num_qubits)

      for qubit, bit in enumerate(reversed(label)):
         if bit == "1":
            qc.x(qubit)
      qc.measure(range(num_qubits), range(num_qubits))
      circuits[label]= qc
    
   return circuits

def counts_to_probability_vector(counts, labels):
   """
   Convert counts into a probability vector ordered by the provided labels.
   """
   total= sum(counts.values())
   if total == 0:
      raise ValueError("calibration counts cannot be empty")
   
   return np.array([counts.get(label, 0) / total for label in labels], dtype= float)

def counts_to_count_vector(counts, labels):
   """
   Convert counts into a raw count vector ordered by the provided labels
   """
   return np.array([counts.get(label,0) for label in labels], dtype= float)

def build_assignment_matrix(counts_dict, num_qubits):
   """
   Build the assignment matrix A where,
    A[y,x]= P(measured y | prepared x), using computartional basis labels in lexicographic order
   """
   labels= computational_basis_labels(num_qubits)

   for label in labels:
      if label not in counts_dict:
         raise ValueError(f"counts_dict must contain calibration counts for '{label}'")
      
   columns= []
   for prepared_label in labels:
      prob_vector= counts_to_probability_vector(counts_dict[prepared_label], labels)
      columns.append(prob_vector)

   return np.column_stack(columns)

def build_mitigation_matrix(assignment_matrix):
   """
   Return the mitigation matrix as the pseudoinverse of the assignemnt matrix
   """
   return np.linalg.pinv(assignment_matrix)

def apply_readout_mitigation(prob_vector, mitigation_matrix, clip=True, renormalize=True):
   """
   Apply readout mitigation to an observed probability vector
   """
   mitigated= mitigation_matrix @ prob_vector

   if clip:
      mitigated= np.clip(mitigated, 0.0, None)

   if renormalize:
      total= mitigated.sum()
      if total > 0:
         mitigated= mitigated / total
   return mitigated

def counts_to_mitigated_pv(counts, mitigation_matrix, labels):
   """
   Convert counts to observed probabilities and apply readout mitigation
   """
   observed_prob_vector= counts_to_probability_vector(counts, labels)
   return apply_readout_mitigation(observed_prob_vector, mitigation_matrix)

def readout_fidelity(assignment_matrix):
   """
   Return the average assignment fidelity
   """
   dim= assignment_matrix.shape[0]
   return np.trace(assignment_matrix) / dim

def assignment_matrix_dataframe(assignment_matrix, num_qubits):
   """
   Return a labeled dataframe for the assignment matrix
   """
   labels= computational_basis_labels(num_qubits)
   return pd.DataFrame( assignment_matrix,
                       index=[f"measured {label}" for label in labels],
                       columns= [f"prepared {label}" for label in labels]
                      )

def mitigation_matrix_dataframe(mitigation_matrix, num_qubits):
   """
   Return a labeled dataframe for the mitigation matrix
   """
   labels= computational_basis_labels(num_qubits)
   return pd.DataFrame(mitigation_matrix,
                       index= [f"ideal {label}" for label in labels],
                       columns= [f"observed {label}" for label in labels]
                      )

def build_single_qubit_calibration():
   """
   Backward-compatible wrapper for stage 3
   """
   return build_basis_calibration(num_qubits=1)

def build_single_qubit_am(counts_dict):
   
   return build_assignment_matrix( counts_dict, num_qubits=1)

def build_two_qubit_calibration():
   """
   Convenience wrapper for ball-state
   """
   return build_basis_calibration(num_qubits=2)

def build_two_qubit_am(counts_dict):
   
   return build_assignment_matrix(counts_dict, num_qubits=2)
