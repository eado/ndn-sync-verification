
NodeState update_state(NodeState current, ModificationMsg msg) {
    // Check if the message indicates to increase the node's own counter
    if (msg.increase) {
        // Increase the first index of the state vector
        current.vector[0]++;
    } else {
        // Compare the received state vector with the current state vector
        bool outOfSync = false;
        for (int i = 0; i < 5; i++) {
            if (msg.vector[i] < current.vector[i]) {
                // If any index in the message vector is less than the current vector, it's out of sync
                outOfSync = true;
                break;
            }
        }

        if (outOfSync) {
            // If out of sync, change the internal state to SUPPRESSION
            current.state = SUPPRESSION;
        } else {
            // Otherwise, update the current state vector with the received vector
            memcpy(current.vector, msg.vector, sizeof(StateVector));
            // Ensure the internal state is STABLE
            current.state = STABLE;
        }
    }

    // Return the updated NodeState
    return current;
}
