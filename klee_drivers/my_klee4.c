#include <stdint.h> 
#include <stdio.h> 
#include <string.h> 
// #include <klee/klee.h> 
#include <stdbool.h> 

// ------------------------------- RUNNING INSTRUCTIONS ------------------------------- //
// 1. Get byte code ($ clang -I ../../include -emit-llvm -c -g -O0 -Xclang -disable-O0-optnone my_klee.c)
// 2. Run Klee ($ klee my_klee.bc)
// 3. Process tests

// QUESTION: Do we want to put more constraints on the values generated using 'klee_assume'?

// ------------------------------- RELEVANT TYPE DEFS ------------------------------- //
typedef enum {
	STABLE,
	SUPPRESSION
} InternalState;

typedef int StateVector[5];

typedef struct {
	StateVector vector;
	bool increase;
} ModificationMsg;

typedef struct {
	StateVector vector;
	InternalState state;
} NodeState;

// ------------------------------- EXAMPLE MODEL ------------------------------- //


NodeState update_state(NodeState current, ModificationMsg msg) {
    // Check if the message indicates an increase in the node's own counter
    if (msg.increase) {
        // Increment the first index of the node's state vector
        current.vector[0]++;
        // Return the updated NodeState with the incremented state vector
        return current;
    }

    // Update the node's state vector with the received state vector
    bool outOfSync = false;
    for (int i = 0; i < 5; i++) {
        if (msg.vector[i] > current.vector[i]) {
            // Update the current vector with the received value
            current.vector[i] = msg.vector[i];
        } else if (msg.vector[i] < current.vector[i]) {
            // If any index in the received vector is less, set outOfSync flag
            outOfSync = true;
        }
    }

    // Check for out-of-sync condition
    if (outOfSync) {
        // Set the internal state to SUPPRESSION
        current.state = SUPPRESSION;
    }

    // Return the updated NodeState
    return current;
}

// ------------------------------- KLEE DRIVER ------------------------------- //
int main() {
	// INPUT #1
	ModificationMsg msg;

	// Set up the state vector in the message
	StateVector x1;
	int y1;
	klee_make_symbolic(&y1, sizeof(y1), "msg_vector_1");
	klee_assume(y1 >= 1);
	klee_assume(y1 < 10);
	x1[0] = y1;
	int y2;
	klee_make_symbolic(&y2, sizeof(y2), "msg_vector_2");
	klee_assume(y2 >= 1);
	klee_assume(y2 < 10);
	x1[1] = y2;
	int y3;
	klee_make_symbolic(&y3, sizeof(y3), "msg_vector_3");
	klee_assume(y3 >= 1);
	klee_assume(y3 < 10);
	x1[2] = y3;
	int y4;
	klee_make_symbolic(&y4, sizeof(y4), "msg_vector_4");
	klee_assume(y4 >= 1);
	klee_assume(y4 < 10);
	x1[3] = y4;
	int y5;
	klee_make_symbolic(&y5, sizeof(y5), "msg_vector_5");
	klee_assume(y5 >= 1);
	klee_assume(y5 < 10);
	x1[4] = y5;

	// Set up the bool in the message
	bool x2;
	klee_make_symbolic(&x2, sizeof(x2), "msg_increase");

	// Make the message symbolic (using symbolic objects above)
	msg.vector[0] = x1[0];
	msg.vector[1] = x1[1];
	msg.vector[2] = x1[2];
	msg.vector[3] = x1[3];
	msg.vector[4] = x1[4];
	msg.increase = x2;

	// INPUT #2
	NodeState current;

	// Set up the state vector in the message
	StateVector x4;
	int z1;
	klee_make_symbolic(&z1, sizeof(z1), "current_vector_1");
	klee_assume(z1 >= 1);
	klee_assume(z1 < 10);
	x4[0] = z1;
	int z2;
	klee_make_symbolic(&z2, sizeof(z2), "current_vector_2");
	klee_assume(z2 >= 1);
	klee_assume(z2 < 10);
	x4[1] = z2;
	int z3;
	klee_make_symbolic(&z3, sizeof(z3), "current_vector_3");
	klee_assume(z3 >= 1);
	klee_assume(z3 < 10);
	x4[2] = z3;
	int z4;
	klee_make_symbolic(&z4, sizeof(z4), "current_vector_4");
	klee_assume(z4 >= 1);
	klee_assume(z4 < 10);
	x4[3] = z4;
	int z5;
	klee_make_symbolic(&z5, sizeof(z5), "current_vector_5");
	klee_assume(z5 >= 1);
	klee_assume(z5 < 10);
	x4[4] = z5;

	// Set up the bool in the message
	InternalState x5;
	klee_make_symbolic(&x5, sizeof(x5), "current_state");
	klee_assume(x5 >= 0); // bounding the enum
	klee_assume(x5 < 2);

	// Make the state symbolic (using symbolic objects above)
	current.vector[0] = x4[0];
	current.vector[1] = x4[1];
	current.vector[2] = x4[2];
	current.vector[3] = x4[3];
	current.vector[4] = x4[4];
	current.state = x5;

	// update_state(NodeState current, ModificationMsg msg)
	update_state(current, msg);

	return 0;
}