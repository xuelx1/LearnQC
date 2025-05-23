# LearnQC
 ### Some Simple Quantum Algorithms 
 I've stopped updating this project and I'll start a new stage of learning quantum algorithms, which can be found in another github repo of this user name. I plan to implement some VQEs, for example QAOA, and other more advanced applications. If this repo helped you in your learning, it is my great pleasure! 

 ### Contact me
 My email:  [xuelx@mail2.sysu.edu.cn] 
 QQ:  [2414181961]

 ### Includes:

 1. hello_ibm, hello_qiskit. "Hello world" in Quantum Computing, to show how to build a simple quantum circuit and run it.
 1.1. Before starting, I writed some frequently-used functions in funcs.py and test_funs.py. I will use them in the following codes.
 2. superdense coding. Use one qubit to send two bits of information.
 3. quantum teleportation. Use two classical bits to send one qubit of information.
 4. oracle. How to build a quantum oracle, which appears in Deustch-Jozsa algorithm and Simon algorithm.
 5. adjacency matrix. Given a adjacency matrix, use it to generate a quantum circuit to judge whether two given vertices are connected. In other words, how to use quantum circuit to store a graph.
 6. Deustch-Jozsa algorithm. Judge if a function is const or balanced.
 7. Simon algorithm. Given a function, find a string s st. f(x) = f(y), iff x = (y xor s) or x = y.
 8. exp2oracle. Given a boolean expression, convert it to a quantum circuit.
 8.1 examples below need some rotation gates, I collected them in simplecircuit.ipynb.
 9. phase_estimation. Estimate the phase of a given function.
 10. qft. Quantum Fourier Transform. And Inverse Quantum Fourier Transform.
 11. modular. Modular addition and multiplication. 
 11. add_mul. non-modular addition and multiplication in quantum computing. 
 12. shor. Shor's algorithm. Factoring a number. 
 13. grover. Grover's algorithm. Searching for a string. 
 14. error_correction. Quantum Error Correction, or Shor's 9 qubit code.
 

### envs:
1. qiskit  1.1.0
2. qiskit_aer  0.14.1
3. qiskit_ibm_run  0.23.0
4. matplotlib  3.9.1
5. pylatexenc  2.10

## Acknowledgments  
  
I sincerely thank the following projects and individuals for their contributions:  
  
- [shor_qiskit] (link: https://github.com/kazawai/shor_qiskit): This project provided [qpe_period_finding in Shor], which played a crucial role in our project. We particularly appreciate the generous sharing and excellent work of owner of this project.  
  