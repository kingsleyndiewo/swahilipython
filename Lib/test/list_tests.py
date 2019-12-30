"""
Tests common to list na UserList.UserList
"""

agiza sys
agiza os
kutoka functools agiza cmp_to_key

kutoka test agiza support, seq_tests


kundi CommonTest(seq_tests.CommonTest):

    eleza test_init(self):
        # Iterable arg ni optional
        self.assertEqual(self.type2test([]), self.type2test())

        # Init clears previous values
        a = self.type2test([1, 2, 3])
        a.__init__()
        self.assertEqual(a, self.type2test([]))

        # Init overwrites previous values
        a = self.type2test([1, 2, 3])
        a.__init__([4, 5, 6])
        self.assertEqual(a, self.type2test([4, 5, 6]))

        # Mutables always rudisha a new object
        b = self.type2test(a)
        self.assertNotEqual(id(a), id(b))
        self.assertEqual(a, b)

    eleza test_getitem_error(self):
        a = []
        msg = "list indices must be integers ama slices"
        ukijumuisha self.assertRaisesRegex(TypeError, msg):
            a['a']

    eleza test_setitem_error(self):
        a = []
        msg = "list indices must be integers ama slices"
        ukijumuisha self.assertRaisesRegex(TypeError, msg):
            a['a'] = "python"

    eleza test_repr(self):
        l0 = []
        l2 = [0, 1, 2]
        a0 = self.type2test(l0)
        a2 = self.type2test(l2)

        self.assertEqual(str(a0), str(l0))
        self.assertEqual(repr(a0), repr(l0))
        self.assertEqual(repr(a2), repr(l2))
        self.assertEqual(str(a2), "[0, 1, 2]")
        self.assertEqual(repr(a2), "[0, 1, 2]")

        a2.append(a2)
        a2.append(3)
        self.assertEqual(str(a2), "[0, 1, 2, [...], 3]")
        self.assertEqual(repr(a2), "[0, 1, 2, [...], 3]")

    eleza test_repr_deep(self):
        a = self.type2test([])
        kila i kwenye range(sys.getrecursionlimit() + 100):
            a = self.type2test([a])
        self.assertRaises(RecursionError, repr, a)

    eleza test_andika(self):
        d = self.type2test(range(200))
        d.append(d)
        d.extend(range(200,400))
        d.append(d)
        d.append(400)
        jaribu:
            ukijumuisha open(support.TESTFN, "w") kama fo:
                fo.write(str(d))
            ukijumuisha open(support.TESTFN, "r") kama fo:
                self.assertEqual(fo.read(), repr(d))
        mwishowe:
            os.remove(support.TESTFN)

    eleza test_set_subscript(self):
        a = self.type2test(range(20))
        self.assertRaises(ValueError, a.__setitem__, slice(0, 10, 0), [1,2,3])
        self.assertRaises(TypeError, a.__setitem__, slice(0, 10), 1)
        self.assertRaises(ValueError, a.__setitem__, slice(0, 10, 2), [1,2])
        self.assertRaises(TypeError, a.__getitem__, 'x', 1)
        a[slice(2,10,3)] = [1,2,3]
        self.assertEqual(a, self.type2test([0, 1, 1, 3, 4, 2, 6, 7, 3,
                                            9, 10, 11, 12, 13, 14, 15,
                                            16, 17, 18, 19]))

    eleza test_reversed(self):
        a = self.type2test(range(20))
        r = reversed(a)
        self.assertEqual(list(r), self.type2test(range(19, -1, -1)))
        self.assertRaises(StopIteration, next, r)
        self.assertEqual(list(reversed(self.type2test())),
                         self.type2test())
        # Bug 3689: make sure list-reversed-iterator doesn't have __len__
        self.assertRaises(TypeError, len, reversed([1,2,3]))

    eleza test_setitem(self):
        a = self.type2test([0, 1])
        a[0] = 0
        a[1] = 100
        self.assertEqual(a, self.type2test([0, 100]))
        a[-1] = 200
        self.assertEqual(a, self.type2test([0, 200]))
        a[-2] = 100
        self.assertEqual(a, self.type2test([100, 200]))
        self.assertRaises(IndexError, a.__setitem__, -3, 200)
        self.assertRaises(IndexError, a.__setitem__, 2, 200)

        a = self.type2test([])
        self.assertRaises(IndexError, a.__setitem__, 0, 200)
        self.assertRaises(IndexError, a.__setitem__, -1, 200)
        self.assertRaises(TypeError, a.__setitem__)

        a = self.type2test([0,1,2,3,4])
        a[0] = 1
        a[1] = 2
        a[2] = 3
        self.assertEqual(a, self.type2test([1,2,3,3,4]))
        a[0] = 5
        a[1] = 6
        a[2] = 7
        self.assertEqual(a, self.type2test([5,6,7,3,4]))
        a[-2] = 88
        a[-1] = 99
        self.assertEqual(a, self.type2test([5,6,7,88,99]))
        a[-2] = 8
        a[-1] = 9
        self.assertEqual(a, self.type2test([5,6,7,8,9]))

        msg = "list indices must be integers ama slices"
        ukijumuisha self.assertRaisesRegex(TypeError, msg):
            a['a'] = "python"

    eleza test_delitem(self):
        a = self.type2test([0, 1])
        toa a[1]
        self.assertEqual(a, [0])
        toa a[0]
        self.assertEqual(a, [])

        a = self.type2test([0, 1])
        toa a[-2]
        self.assertEqual(a, [1])
        toa a[-1]
        self.assertEqual(a, [])

        a = self.type2test([0, 1])
        self.assertRaises(IndexError, a.__delitem__, -3)
        self.assertRaises(IndexError, a.__delitem__, 2)

        a = self.type2test([])
        self.assertRaises(IndexError, a.__delitem__, 0)

        self.assertRaises(TypeError, a.__delitem__)

    eleza test_setslice(self):
        l = [0, 1]
        a = self.type2test(l)

        kila i kwenye range(-3, 4):
            a[:i] = l[:i]
            self.assertEqual(a, l)
            a2 = a[:]
            a2[:i] = a[:i]
            self.assertEqual(a2, a)
            a[i:] = l[i:]
            self.assertEqual(a, l)
            a2 = a[:]
            a2[i:] = a[i:]
            self.assertEqual(a2, a)
            kila j kwenye range(-3, 4):
                a[i:j] = l[i:j]
                self.assertEqual(a, l)
                a2 = a[:]
                a2[i:j] = a[i:j]
                self.assertEqual(a2, a)

        aa2 = a2[:]
        aa2[:0] = [-2, -1]
        self.assertEqual(aa2, [-2, -1, 0, 1])
        aa2[0:] = []
        self.assertEqual(aa2, [])

        a = self.type2test([1, 2, 3, 4, 5])
        a[:-1] = a
        self.assertEqual(a, self.type2test([1, 2, 3, 4, 5, 5]))
        a = self.type2test([1, 2, 3, 4, 5])
        a[1:] = a
        self.assertEqual(a, self.type2test([1, 1, 2, 3, 4, 5]))
        a = self.type2test([1, 2, 3, 4, 5])
        a[1:-1] = a
        self.assertEqual(a, self.type2test([1, 1, 2, 3, 4, 5, 5]))

        a = self.type2test([])
        a[:] = tuple(range(10))
        self.assertEqual(a, self.type2test(range(10)))

        self.assertRaises(TypeError, a.__setitem__, slice(0, 1, 5))

        self.assertRaises(TypeError, a.__setitem__)

    eleza test_delslice(self):
        a = self.type2test([0, 1])
        toa a[1:2]
        toa a[0:1]
        self.assertEqual(a, self.type2test([]))

        a = self.type2test([0, 1])
        toa a[1:2]
        toa a[0:1]
        self.assertEqual(a, self.type2test([]))

        a = self.type2test([0, 1])
        toa a[-2:-1]
        self.assertEqual(a, self.type2test([1]))

        a = self.type2test([0, 1])
        toa a[-2:-1]
        self.assertEqual(a, self.type2test([1]))

        a = self.type2test([0, 1])
        toa a[1:]
        toa a[:1]
        self.assertEqual(a, self.type2test([]))

        a = self.type2test([0, 1])
        toa a[1:]
        toa a[:1]
        self.assertEqual(a, self.type2test([]))

        a = self.type2test([0, 1])
        toa a[-1:]
        self.assertEqual(a, self.type2test([0]))

        a = self.type2test([0, 1])
        toa a[-1:]
        self.assertEqual(a, self.type2test([0]))

        a = self.type2test([0, 1])
        toa a[:]
        self.assertEqual(a, self.type2test([]))

    eleza test_append(self):
        a = self.type2test([])
        a.append(0)
        a.append(1)
        a.append(2)
        self.assertEqual(a, self.type2test([0, 1, 2]))

        self.assertRaises(TypeError, a.append)

    eleza test_extend(self):
        a1 = self.type2test([0])
        a2 = self.type2test((0, 1))
        a = a1[:]
        a.extend(a2)
        self.assertEqual(a, a1 + a2)

        a.extend(self.type2test([]))
        self.assertEqual(a, a1 + a2)

        a.extend(a)
        self.assertEqual(a, self.type2test([0, 0, 1, 0, 0, 1]))

        a = self.type2test("spam")
        a.extend("eggs")
        self.assertEqual(a, list("spameggs"))

        self.assertRaises(TypeError, a.extend, Tupu)
        self.assertRaises(TypeError, a.extend)

        # overflow test. issue1621
        kundi CustomIter:
            eleza __iter__(self):
                rudisha self
            eleza __next__(self):
                ashiria StopIteration
            eleza __length_hint__(self):
                rudisha sys.maxsize
        a = self.type2test([1,2,3,4])
        a.extend(CustomIter())
        self.assertEqual(a, [1,2,3,4])


    eleza test_insert(self):
        a = self.type2test([0, 1, 2])
        a.insert(0, -2)
        a.insert(1, -1)
        a.insert(2, 0)
        self.assertEqual(a, [-2, -1, 0, 0, 1, 2])

        b = a[:]
        b.insert(-2, "foo")
        b.insert(-200, "left")
        b.insert(200, "right")
        self.assertEqual(b, self.type2test(["left",-2,-1,0,0,"foo",1,2,"right"]))

        self.assertRaises(TypeError, a.insert)

    eleza test_pop(self):
        a = self.type2test([-1, 0, 1])
        a.pop()
        self.assertEqual(a, [-1, 0])
        a.pop(0)
        self.assertEqual(a, [0])
        self.assertRaises(IndexError, a.pop, 5)
        a.pop(0)
        self.assertEqual(a, [])
        self.assertRaises(IndexError, a.pop)
        self.assertRaises(TypeError, a.pop, 42, 42)
        a = self.type2test([0, 10, 20, 30, 40])

    eleza test_remove(self):
        a = self.type2test([0, 0, 1])
        a.remove(1)
        self.assertEqual(a, [0, 0])
        a.remove(0)
        self.assertEqual(a, [0])
        a.remove(0)
        self.assertEqual(a, [])

        self.assertRaises(ValueError, a.remove, 0)

        self.assertRaises(TypeError, a.remove)

        kundi BadExc(Exception):
            pita

        kundi BadCmp:
            eleza __eq__(self, other):
                ikiwa other == 2:
                    ashiria BadExc()
                rudisha Uongo

        a = self.type2test([0, 1, 2, 3])
        self.assertRaises(BadExc, a.remove, BadCmp())

        kundi BadCmp2:
            eleza __eq__(self, other):
                ashiria BadExc()

        d = self.type2test('abcdefghcij')
        d.remove('c')
        self.assertEqual(d, self.type2test('abdefghcij'))
        d.remove('c')
        self.assertEqual(d, self.type2test('abdefghij'))
        self.assertRaises(ValueError, d.remove, 'c')
        self.assertEqual(d, self.type2test('abdefghij'))

        # Handle comparison errors
        d = self.type2test(['a', 'b', BadCmp2(), 'c'])
        e = self.type2test(d)
        self.assertRaises(BadExc, d.remove, 'c')
        kila x, y kwenye zip(d, e):
            # verify that original order na values are retained.
            self.assertIs(x, y)

    eleza test_index(self):
        super().test_index()
        a = self.type2test([-2, -1, 0, 0, 1, 2])
        a.remove(0)
        self.assertRaises(ValueError, a.index, 2, 0, 4)
        self.assertEqual(a, self.type2test([-2, -1, 0, 1, 2]))

        # Test modifying the list during index's iteration
        kundi EvilCmp:
            eleza __init__(self, victim):
                self.victim = victim
            eleza __eq__(self, other):
                toa self.victim[:]
                rudisha Uongo
        a = self.type2test()
        a[:] = [EvilCmp(a) kila _ kwenye range(100)]
        # This used to seg fault before patch #1005778
        self.assertRaises(ValueError, a.index, Tupu)

    eleza test_reverse(self):
        u = self.type2test([-2, -1, 0, 1, 2])
        u2 = u[:]
        u.reverse()
        self.assertEqual(u, [2, 1, 0, -1, -2])
        u.reverse()
        self.assertEqual(u, u2)

        self.assertRaises(TypeError, u.reverse, 42)

    eleza test_clear(self):
        u = self.type2test([2, 3, 4])
        u.clear()
        self.assertEqual(u, [])

        u = self.type2test([])
        u.clear()
        self.assertEqual(u, [])

        u = self.type2test([])
        u.append(1)
        u.clear()
        u.append(2)
        self.assertEqual(u, [2])

        self.assertRaises(TypeError, u.clear, Tupu)

    eleza test_copy(self):
        u = self.type2test([1, 2, 3])
        v = u.copy()
        self.assertEqual(v, [1, 2, 3])

        u = self.type2test([])
        v = u.copy()
        self.assertEqual(v, [])

        # test that it's indeed a copy na sio a reference
        u = self.type2test(['a', 'b'])
        v = u.copy()
        v.append('i')
        self.assertEqual(u, ['a', 'b'])
        self.assertEqual(v, u + ['i'])

        # test that it's a shallow, sio a deep copy
        u = self.type2test([1, 2, [3, 4], 5])
        v = u.copy()
        self.assertEqual(u, v)
        self.assertIs(v[3], u[3])

        self.assertRaises(TypeError, u.copy, Tupu)

    eleza test_sort(self):
        u = self.type2test([1, 0])
        u.sort()
        self.assertEqual(u, [0, 1])

        u = self.type2test([2,1,0,-1,-2])
        u.sort()
        self.assertEqual(u, self.type2test([-2,-1,0,1,2]))

        self.assertRaises(TypeError, u.sort, 42, 42)

        eleza revcmp(a, b):
            ikiwa a == b:
                rudisha 0
            lasivyo a < b:
                rudisha 1
            isipokua: # a > b
                rudisha -1
        u.sort(key=cmp_to_key(revcmp))
        self.assertEqual(u, self.type2test([2,1,0,-1,-2]))

        # The following dumps core kwenye unpatched Python 1.5:
        eleza myComparison(x,y):
            xmod, ymod = x%3, y%7
            ikiwa xmod == ymod:
                rudisha 0
            lasivyo xmod < ymod:
                rudisha -1
            isipokua: # xmod > ymod
                rudisha 1
        z = self.type2test(range(12))
        z.sort(key=cmp_to_key(myComparison))

        self.assertRaises(TypeError, z.sort, 2)

        eleza selfmodifyingComparison(x,y):
            z.append(1)
            ikiwa x == y:
                rudisha 0
            lasivyo x < y:
                rudisha -1
            isipokua: # x > y
                rudisha 1
        self.assertRaises(ValueError, z.sort,
                          key=cmp_to_key(selfmodifyingComparison))

        self.assertRaises(TypeError, z.sort, 42, 42, 42, 42)

    eleza test_slice(self):
        u = self.type2test("spam")
        u[:2] = "h"
        self.assertEqual(u, list("ham"))

    eleza test_iadd(self):
        super().test_iadd()
        u = self.type2test([0, 1])
        u2 = u
        u += [2, 3]
        self.assertIs(u, u2)

        u = self.type2test("spam")
        u += "eggs"
        self.assertEqual(u, self.type2test("spameggs"))

        self.assertRaises(TypeError, u.__iadd__, Tupu)

    eleza test_imul(self):
        super().test_imul()
        s = self.type2test([])
        oldid = id(s)
        s *= 10
        self.assertEqual(id(s), oldid)

    eleza test_extendedslicing(self):
        #  subscript
        a = self.type2test([0,1,2,3,4])

        #  deletion
        toa a[::2]
        self.assertEqual(a, self.type2test([1,3]))
        a = self.type2test(range(5))
        toa a[1::2]
        self.assertEqual(a, self.type2test([0,2,4]))
        a = self.type2test(range(5))
        toa a[1::-2]
        self.assertEqual(a, self.type2test([0,2,3,4]))
        a = self.type2test(range(10))
        toa a[::1000]
        self.assertEqual(a, self.type2test([1, 2, 3, 4, 5, 6, 7, 8, 9]))
        #  assignment
        a = self.type2test(range(10))
        a[::2] = [-1]*5
        self.assertEqual(a, self.type2test([-1, 1, -1, 3, -1, 5, -1, 7, -1, 9]))
        a = self.type2test(range(10))
        a[::-4] = [10]*3
        self.assertEqual(a, self.type2test([0, 10, 2, 3, 4, 10, 6, 7, 8 ,10]))
        a = self.type2test(range(4))
        a[::-1] = a
        self.assertEqual(a, self.type2test([3, 2, 1, 0]))
        a = self.type2test(range(10))
        b = a[:]
        c = a[:]
        a[2:3] = self.type2test(["two", "elements"])
        b[slice(2,3)] = self.type2test(["two", "elements"])
        c[2:3:] = self.type2test(["two", "elements"])
        self.assertEqual(a, b)
        self.assertEqual(a, c)
        a = self.type2test(range(10))
        a[::2] = tuple(range(5))
        self.assertEqual(a, self.type2test([0, 1, 1, 3, 2, 5, 3, 7, 4, 9]))
        # test issue7788
        a = self.type2test(range(10))
        toa a[9::1<<333]

    eleza test_constructor_exception_handling(self):
        # Bug #1242657
        kundi F(object):
            eleza __iter__(self):
                ashiria KeyboardInterrupt
        self.assertRaises(KeyboardInterrupt, list, F())

    eleza test_exhausted_iterator(self):
        a = self.type2test([1, 2, 3])
        exhit = iter(a)
        empit = iter(a)
        kila x kwenye exhit:  # exhaust the iterator
            next(empit)  # sio exhausted
        a.append(9)
        self.assertEqual(list(exhit), [])
        self.assertEqual(list(empit), [9])
        self.assertEqual(a, self.type2test([1, 2, 3, 9]))
