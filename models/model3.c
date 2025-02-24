
NodeState update_state(NodeState current, ModificationMsg msg) {
    // Check if the message indicates to increase the node's own counter
    if (msg.increase) {
        // Increase the first index of the state vector
        current.vector[0]++;
        // Return the updated state
        return current;
    }

    // Check if the message contains an updated state vector
    bool outOfSync = false;
    for (int i = 0; i < 5; i++) {
        if (msg.vector[i] > current.vector[i]) {
            // Update the current state vector with the received one
            current.vector[i] = msg.vector[i];
        } else if (msg.vector[i] < current.vector[i]) {
            // If any index in the message is less than the current state, mark as out of sync
            outOfSync = true;
        }
    }

    // If the message is out of sync, change the internal state to SUPPRESSION
    if (outOfSync) {
        current.state = SUPPRESSION;
    } else {
        // Otherwise, remain in the STABLE state
        current.state = STABLE;
    }

    // Return the updated state
    return current;
}