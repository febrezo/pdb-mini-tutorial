# Debugging in Python: PDB Mini tutorial

This repository is intended to help people writing code in Python to debug their scripts using PDB.
[PDB](https://docs.python.org/3/library/pdb.html) is a native Python 3 module that can be used to inspect the 

## License

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

## The Code

In the `tutorial.py` you can find a tiny example that will be used to learn the basics.
This is the code:

```
import sys

def main(params):
    length = len(params)
    print(f"Total params: {length}")

    print("Listing parameters…")
    for i, p in enumerate(params):
        print(f"\t- Param #{i}: {p}")

    print("Finishing execution…")

if __name__ == "__main__":
    print(f"Params: {sys.argv}")
    main(sys.argv)
```

Basically, the scripts reads the number of parameters provided when running and show them in the terminal.
You can try it from the command line:

```
$ python3 tutorial.py 
Params: ['tutorial.py']
Total params: 1
Listing parameters…
	- Param #0: tutorial.py
Finishing execution…
$ python3 tutorial.py a bc def ghij
Params: ['tutorial.py', 'a', 'bc', 'def', 'ghij']
Total params: 5
Listing parameters…
	- Param #0: tutorial.py
	- Param #1: a
	- Param #2: bc
	- Param #3: def
	- Param #4: ghij
Finishing execution…
```

## Entering the Debugger

PDB can be used on any Python script by calling the `pdb` module.

```
$ python3 -m pdb tutorial.py a bc def ghij
> /tmp/pdb-mini-tutorial/tutorial.py(1)<module>()
-> import sys
(Pdb)
```

Although the [official docs](https://docs.python.org/3/library/pdb.html) are pretty well documented, PDB counts with an interactive help that can be invoked with the `help` command or with its short form, `h`.

```
(Pdb) h

Documented commands (type help <topic>):
========================================
EOF    c          d        h         list      q        rv       undisplay
a      cl         debug    help      ll        quit     s        unt      
alias  clear      disable  ignore    longlist  r        source   until    
args   commands   display  interact  n         restart  step     up       
b      condition  down     j         next      return   tbreak   w        
break  cont       enable   jump      p         retval   u        whatis   
bt     continue   exit     l         pp        run      unalias  where    

Miscellaneous help topics:
==========================
exec  pdb

(Pdb) 
```

`help` can also be used to get more information about other commands.

```
(Pdb) help p
p expression
        Print the value of the expression.
(Pdb) h l
l(ist) [first [,last] | .]

        List source code for the current file.  Without arguments,
        list 11 lines around the current line or continue the previous
        listing.  With . as argument, list 11 lines around the current
        line.  With one argument, list 11 lines starting at that line.
        With two arguments, list the given range; if the second
        argument is less than the first, it is a count.

        The current line in the current frame is indicated by "->".
        If an exception is being debugged, the line where the
        exception was originally raised or propagated is indicated by
        ">>", if it differs from the current line.
```

Wow. 
We can then use this command to print the code interactively.

```
(Pdb) l 0
  1  ->	import sys
  2  	
  3  	def main(params):
  4  	    length = len(params)
  5  	    print(f"Total params: {length}")
  6  	
  7  	    print("Listing parameters…")
  8  	    for i, p in enumerate(params):
  9  	        print(f"\t- Param #{i}: {p}")
 10  	
 11  	    print("Finishing execution…")
```

Can you see that `->` in the output?
That's the current position of the stack.
You'll see later how this arrow is being moved through the program.

## Running the Program

So, how we can start executing the code? 
The `r` and `restart` commands will be helpful for you here to run the program since the very begining.
There are several options, being the most relevant the following:

- `c` or `continue`. It continues the execution but only stops if a breakpoint is found.

```
(Pdb) c
Params: ['tutorial.py', 'a', 'bc', 'def', 'ghij']
Total params: 5
Listing parameters…
	- Param #0: tutorial.py
	- Param #1: a
	- Param #2: bc
	- Param #3: def
	- Param #4: ghij
Finishing execution…
The program finished and will be restarted
> /tmp/pdb-mini-tutorial/tutorial.py(1)<module>()
-> import sys
```

- `b` or `break`. If provided, it sets a breakpoint on a line number. Different files can be specified using the `<filename>:<line_num>` syntax. All the breakpoints can be shown using `b`, without parameters. To remove it you can use either `cl tutorial.py:5` or `cl <BREAKPOINT_INDEX>` where `<BREAKPOINT_INDEX>` is the ID assigned by PDB to the breakpoint. The `b` is really really powerful because it can also receive a condition that SHOULD be met to raise the breakpoint. We'll leave this for now, but check the docs if you are curious about this.

```
(Pdb) b 5
Breakpoint 1 at /tmp/pdb-mini-tutorial/tutorial.py:5
(Pdb) l
  1  ->	import sys
  2  	
  3  	def main(params):
  4  	    length = len(params)
  5 B	    print(f"Total params: {length}")
  6  	
  7  	    print("Listing parameters…")
  8  	    for i, p in enumerate(params):
  9  	        print(f"\t- Param #{i}: {p}")
 10  	
 11  	    print("Finishing execution…")
(Pdb) c
Params: ['tutorial.py', 'a', 'bc', 'def', 'ghij']
> /tmp/pdb-mini-tutorial/tutorial.py(5)main()
-> print(f"Total params: {length}")
```

- `n` or `next`. It executes the line on the current function BUT does NOT enter onto called functions. It runs them as a single line. This is useful if you want to avoid entering low-level methods called from the function you are debugging. We can try it setting a breakpoint on line 15.

```
(Pdb) l
 10  	
 11  	    print("Finishing execution…")
 12  	
 13  	if __name__ == "__main__":
 14  	    print(f"Params: {sys.argv}")
 15 B->	    main(sys.argv)
[EOF]
(Pdb) n
Total params: 5
Listing parameters…
	- Param #0: tutorial.py
	- Param #1: a
	- Param #2: bc
	- Param #3: def
	- Param #4: ghij
Finishing execution…
--Return--
> /tmp/pdb-mini-tutorial/tutorial.py(15)<module>()->None
-> main(sys.argv)
```

- `s` or `step`. It executes the line on a line-by-line basis. See the difference with using `s`.

```
(Pdb) c
Params: ['tutorial.py', 'a', 'bc', 'def', 'ghij']
> /tmp/pdb-mini-tutorial/tutorial.py(15)<module>()
-> main(sys.argv)
(Pdb) l
 10  	
 11  	    print("Finishing execution…")
 12  	
 13  	if __name__ == "__main__":
 14  	    print(f"Params: {sys.argv}")
 15 B->	    main(sys.argv)
[EOF]
(Pdb) s
--Call--
> /tmp/pdb-mini-tutorial/tutorial.py(3)main()
-> def main(params):
(Pdb) l
  1  	import sys
  2  	
  3  ->	def main(params):
  4  	    length = len(params)
  5  	    print(f"Total params: {length}")
  6  	
  7  	    print("Listing parameters…")
  8  	    for i, p in enumerate(params):
  9  	        print(f"\t- Param #{i}: {p}")
 10  	
 11  	    print("Finishing execution…")
(Pdb) s
> /tmp/pdb-mini-tutorial/tutorial.py(4)main()
-> length = len(params)
```

## Inspecting the contents

So we are navigating the function but, how can we inspect the contents of the variables?
First, set a breakpoint in line 5.

```
(Pdb) b tutorial.py:5
Breakpoint 6 at /tmp/pdb-mini-tutorial/tutorial.py:5
(Pdb) b
Num Type         Disp Enb   Where
6   breakpoint   keep yes   at /tmp/pdb-mini-tutorial/tutorial.py:5
	breakpoint already hit 1 time
```

So let's run the program until the breakpoint:

```
(Pdb) c
Params: ['tutorial.py', 'a', 'bc', 'def', 'ghij']
> /tmp/pdb-mini-tutorial/tutorial.py(5)main()
-> print(f"Total params: {length}")
```

We can now show the full content of the current function using `ll`.


Oh. 
The function received a parameter.
As Python is not a typed language, we may want to know what is the type of the parameter.
`whatis` can help us!

```
(Pdb) whatis params
<class 'list'>
```

So it's a list. 
Let's check the value of the list then!

```
(Pdb) p params
['tutorial.py', 'a', 'bc', 'def', 'ghij']
```

Gotcha! 
Now we are closer to understand what happens.
We see that there is a local variable `length` which, if we are reading correctly the method should have a value of of 5.

```
(Pdb) p length
5
```

Yes, we are understanding what it is happening here!
Time to move through the function executing the contents with `n`, `s` or `c` depending on the needs!

## Final Remarks

PDB is a really powerful tool that WILL help us on debugging our own Python code.
Python being an untyped language makes some things easy to code abstacting us from dealing with many errors and type matching issues.
This is nice for prototyping things but can be really messy if we lost our focus.
PDB is here to help us.
The guidelines shown in this article are only a small of example of the capabilities.
Do not hesitate on investing (yeah, that's the word, _invest_) some time on understanding it better.
I bet that you'll see the benefits of knowing it sooner than you expect.
