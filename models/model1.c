
NodeState update_state(NodeState current, ModificationMsg msg) {
    // Check if the message indicates to increase the node's own counter
    if (msg.increase) {
        // Increase the first index of the state vector
        current.vector[0]++;
        // Return the updated state
        return current;
    }

    // Check if the received state vector is newer or outdated
    bool isOutdated = false;
    for (int i = 0; i < 5; i++) {
        if (msg.vector[i] < current.vector[i]) {
            isOutdated = true;
            break;
        }
    }

    if (isOutdated) {
        // If the message is outdated, move to SUPPRESSION state
        current.state = SUPPRESSION;
        // Return the current state with SUPPRESSION state
        return current;
    } else {
        // If the message is not outdated, update the state vector
        for (int i = 0; i < 5; i++) {
            if (msg.vector[i] > current.vector[i]) {
                current.vector[i] = msg.vector[i];
            }
        }
        // Return the updated state
        return current;
    }
}