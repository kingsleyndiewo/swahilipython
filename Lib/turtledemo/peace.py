#!/usr/bin/env python3
"""       turtle-example-suite:

              tdemo_peace.py

A simple drawing suitable kama a beginner's
programming example. Aside kutoka the
peacecolors assignment na the kila loop,
it only uses turtle commands.
"""

kutoka turtle agiza *

eleza main():
    peacecolors = ("red3",  "orange", "yellow",
                   "seagreen4", "orchid4",
                   "royalblue1", "dodgerblue4")

    reset()
    Screen()
    up()
    goto(-320,-195)
    width(70)

    kila pcolor kwenye peacecolors:
        color(pcolor)
        down()
        forward(640)
        up()
        backward(640)
        left(90)
        forward(66)
        right(90)

    width(25)
    color("white")
    goto(0,-170)
    down()

    circle(170)
    left(90)
    forward(340)
    up()
    left(180)
    forward(170)
    right(45)
    down()
    forward(170)
    up()
    backward(170)
    left(90)
    down()
    forward(170)
    up()

    goto(0,300) # vanish ikiwa hideturtle() ni sio available ;-)
    rudisha "Done!"

ikiwa __name__ == "__main__":
    main()
    mainloop()
