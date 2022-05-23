To use the AI with the ludopy framework, do the following:

1. Create an instance of the AI-class with the desired parameters. This should only be done once in the beginning of your file.
2. Call the reset function on the AI at the beginning of each new game. This resets the state of the AI, among other things.
3. Call the onePass function on the AI with the relevant parameters each time it should perform an action. It returns the index of the piece it chooses to move