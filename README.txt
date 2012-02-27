When using the HW7 Socket Server:
Occasionally when you CTRL+C (KeyboardInterrupt) the program, the port will get 'stuck' in a bound state.
In testing on Debian Squeeze this port will unstick itself after a brief timeout period of around 60 seconds.
I've tried to play around with ways to make sure the sock gets closed during the KeyboardInterrupt runtime but no dice.
I'll do some testing on OSX asap and see how it works there, although I assume since it is Unix-based that the timeout will exist there as well.

When testing:
1. Ensure you are the base of the repository. /meep
2. Ensure meep.save does not exist. If you have run tests previously it needs to be removed or if you have just fetched my repo all is well.
3. Ensure the app server is running. eg. python serve.py
4. Run 'nosetests'!

meeplib for CSE 491, 2012, at MSU.  YYY something else!

Titus Brown, ctb@msu.edu.

meep!
