

NodeState update_state(NodeState current, ModificationMsg msg) {
    // Step 1: Check if the message indicates an increase in the node's own counter
    if (msg.increase) {
        current.vector[0]++;  // Increment the node's own counter
    }

    // Step 2: Update the node's state vector with the received message
    bool out_of_sync = false;
    for (int i = 0; i < 5; i++) {
        if (msg.vector[i] > current.vector[i]) {
            current.vector[i] = msg.vector[i];
        } else if (msg.vector[i] < current.vector[i]) {
            out_of_sync = true;
        }
    }

    // Step 3: Determine the node's internal state
    if (out_of_sync) {
        current.state = SUPPRESSION;
    } else {
        current.state = STABLE;
    }

    // Step 4: Return the updated NodeState
    return current;
}