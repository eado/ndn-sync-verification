
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