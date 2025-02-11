# Zaxxon for the Atari 400/800

This is the 16kb Tape version for the Atari 400/800.

I recorded both sides and converted them into CAS files. Then I wrote a Python script to extract the 4 parts out of it. A compare showed that both sides generate identical code.

The first part is a tiny loaded to $00DF and at the bottom of the stack. This then loads the startup loader with the title screen, which has some decryption in it. My script removes the decryption. The startup loader is launched by jumping to $3400. It loads the main application at $400 (also encrypted) and a tiny block of $c0 bytes at the beginning of the stack. The game is then started by jumping to $400. The tiny bytes on the stack contain 2 subroutines and a table. Feels like kind of a anti-hacking scheme.

