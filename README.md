To use the AI with the ludopy framework, do the following:

1. Create an instance of the AI-class with the filename of the Q-table. This should only be done once in the beginning of your file.
2. Call the onePass function on the AI with the relevant parameters each time it should perform an action. It returns the index of the piece it chooses to move

If you want to train the AI, do the above, but call the reset-function before each episode starts, even the first