PROGRAM BY: CABUNGCAL, CULALA, UY  S14

This is a simple Multitape Turing Machine Simulator

To use the program, you must have downloaded python within your machine 
then follow the following step:
1. Open cmd and change the directory to where the source code was installed (ex. cd D:/Downloads/src)
2. Make sure the "machine_def.txt" follow this format

Example:
3 /* number of states */
A B C /* list of states */
3 /* number of tapes */
0 1 /* list of inputs */
2 /* number of transitions */
A 1 B _ R | A 0 B _ R | A 1 B _ R /* transitions in the format  [qr i qn c m "|" <- if there's another tape]*/
B 0 C _ R | B 1 C _ R | B 0 C _ R 
A /* initial state */
C /* final state */

(Note: There's already a sample definition file that accepts wcw | w E {a.b}* [accepts tape1: abcab tape2: _]
                                                                            - tape2 should always be blank)

3. Run the code by typing in the cmd "python mtm_gui.py"
4. Put your inputs for each tape you have initialized. You may leave the input blank or add "_" for blank spaces
5. Press start to run your inputs
6. Press step to proceed to next transition
[WARNING!!!: This program can't detect infinite loops therefore there's a possibility that nothing will happen
 as you click "step" - it will be endless. Just close the window if you find that its already an infinite loop]
7. Once the run is done, you will be prompted if the series of inputs are accepted or not.
8. You can press "New Input" to put new instance of inputs
9. Enjoy!

In case you don't have python, you may run the .exe file in the dist folder. Just make sure that the "machine_def.txt" 
is in the same directory as the exe file to run the program properly.