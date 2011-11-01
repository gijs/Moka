from __future__ import print_function

import unittest

prn = print

class List(list):
    """
    join
    map
    compact
    keep
    rem
    some/has
    all
    count () = len, (x|f)
    empty () == [], (f) -> x in [0, None]..
    attr
    item
    invoke
    Uniq -> Can take f to specify on what it should uniq.
    Flatten
    Do do(lambda seq: ...)
       (and last_value = the result of the last operation)
       also do will pass extra arg. so do(self.assertTrue, ...)
       = do(lambda seq: self.assertTrue(seq, ...)
       = self.assertTrue(seq, ...)

     aliases:
     'append', 'extend', 'sort', 'reverse', 'insert'


    idea:
    create -> Easy way to initialize a list.. List().create(20, rand)
    """

    @staticmethod
    def _proxy(method_name):
        def wrap(self, *args, **kwargs):
            inst = List(self)
            getattr(list, method_name)(inst, *args, **kwargs)
            return inst

        setattr(List, method_name, wrap)

    def _f(self, f, x):
        if hasattr(f, '__call__'):
            return f(x)
        else:
            return f == x

    def join(self, s):
        return s.join(self)

    def compact(self, f=None):
        if not f:
            f = lambda x: not not x

        return self.keep(f)

    def map(self, f):
        return List(f(x) if hasattr(f, '__call__') else f
                    for x in self)

    def do(self, function, *args, **kwargs):
        self.last_value = function(self, *args, **kwargs)
        return self

    def uniq(self, f=None):
        if not self:
            return self

        if f:
            d = {}
            for k in self:
                d[f(k)] = k

            return List(d.values())

        return List(set(self))

    def invoke(self, name, *args, **kwargs):
        return self.map(lambda x: getattr(x, name)(*args, **kwargs))

    def attr(self, attr):
        return self.map(lambda x: getattr(x, attr))

    def item(self, item):
        return self.map(lambda x: x[item])

    def empty(self, *args):
        if not args:
            return len(self) == 0
        else:
            return len(List(self).rem(args[0])) == 0

    def count(self, *args):
        if not args:
            return len(self)
        else:
            return len(List(self).keep(args[0]))

    def find(self, f):
        for x in self:
            if self._f(f, x):
                return x

    def keep(self, f):
        return List(x for x in self if self._f(f, x))

    def rem(self, f):
        return List(x for x in self if not self._f(f, x))

    def some(self, f):
        for x in self:
            if self._f(f, x):
                return True

        return False

    def flatten(self):
        elements = []

        for el in self:
            try:
                elements.extend(List(el).flatten())
            except TypeError:
                elements.append(el)

        return elements

    def all(self, f):
        for x in self:
            if not self._f(f, x):
                return False

        return True

    # aliases
    has = some

    def __getslice__(self, *args, **kwargs):
        return List(list.__getslice__(self, *args, **kwargs))


(List(['append', 'extend', 'sort', 'reverse', 'insert'])
   .map(List._proxy))


class ListTest(unittest.TestCase):

    def setUp(self):
        self.seq = List(range(1, 6))

    def test_is_list(self):
        self.assertEqual(range(1, 6), self.seq)

    def test_map(self):
        self.assertEqual(self.seq.map(lambda x: x * 2), [2, 4, 6, 8, 10])

        self.assertEqual(self.seq.map(2), [2, 2, 2, 2, 2])

    def test_keep(self):
        self.assertEqual(self.seq.keep(lambda x: x < 3), [1, 2])
        self.assertEqual(self.seq.keep(3), [3])

    def test_rem(self):
        self.assertEqual(self.seq.rem(lambda x: x < 3), [3, 4, 5])
        self.assertEqual(self.seq.rem(3), [1, 2, 4, 5])

    def test_mix(self):
        r = (self.seq
                 .map(lambda x: x * 2)
                 .rem(lambda x: x < 5)
                 .keep(lambda x: x % 2 == 0)
                 .rem(6))

        self.assertEqual(r, [8, 10])

    def test_self(self):
        self.assertEqual(
            (self.seq
             .map(lambda x: x * 2)
             .rem(lambda x: x < 5)
             .keep(lambda x: x % 2 == 0)
             .rem(6)
             .do(self.assertEqual, [8, 10])),
             [8, 10])

        (self.seq
              .keep(lambda x: x > 4)
              .do(self.assertEqual, [5])
              .last_value) = [5]

    def test_some(self):
        self.assert_(self.seq.some(lambda x: x < 3))

        self.assert_(self.seq.some(4))

        self.assertFalse(List([1, 1, 1]).some(2))

        self.assertFalse(self.seq.some(lambda x: x < 1))

    def test_has(self):
        self.assert_(List(range(10)).has(5))
        self.assert_(List(range(10)).has(lambda x: x in [1, 2]))

    def test_find(self):
        self.assertEqual(self.seq.find(3), 3)

        self.assertEqual(self.seq.find(lambda x: x == 3), 3)

        self.assertEqual(self.seq.find(lambda x: x != 3), 1)

    def test_all(self):
        self.assertFalse(self.seq.all(lambda x: x < 3))

        self.assertFalse(self.seq.all(4))

        self.assert_(List([1, 1, 1]).all(1))

        self.assert_(self.seq.all(lambda x: x < 10))

    def test_append(self):
        self.assertEqual(self.seq.append(6), [1, 2, 3, 4, 5, 6])
        self.assertEqual(self.seq, [1, 2, 3, 4, 5])

    def test_extend(self):
        self.assertEqual(self.seq.extend([1, 2]), [1, 2, 3, 4, 5, 1, 2])
        self.assertEqual(self.seq, [1, 2, 3, 4, 5])

    def test_insert(self):
        self.assertEqual(self.seq.insert(0, 4), [4, 1, 2, 3, 4, 5])
        self.assertEqual(self.seq, [1, 2, 3, 4, 5])

    def test_getslice(self):
        self.assertEqual(self.seq[:2], [1, 2])
        self.assertEqual(type(self.seq[:1]), List)
        self.assertEqual(self.seq[:2].map(lambda x: x * 2), [2, 4])

    def test_setslice(self):
        self.seq[2:] = [9, 9]
        self.assertEqual(self.seq, [1, 2, 9, 9])
        self.assertEqual(type(self.seq), List)

    def test_reverse(self):
        self.assertEqual(self.seq.reverse(), [5, 4, 3, 2, 1])
        self.assertEqual(type(self.seq), List)

    def test_sort(self):
        self.seq = List([1, 4, 2, 5, 3])
        self.assertEqual(self.seq.sort(), [1, 2, 3, 4, 5])
        self.assertEqual(type(self.seq), List)

    def test_count(self):
        self.assertEqual(self.seq.count(), 5)
        self.assertEqual(self.seq.count(3), 1)
        self.assertEqual(self.seq.count(lambda x: x in [1, 3]), 2)

    def test_empty(self):
        self.assertFalse(self.seq.empty())
        self.assertTrue(List().empty())
        self.assertTrue(List([None, 0, 0]).empty(lambda x: x in [None, 0]))
        self.assertFalse(List([None, [], 0]).empty(lambda x: x in [None, 0]))

    def test_attr(self):
        self.assertEqual(self.seq.attr('real'), [1, 2, 3, 4, 5])
        self.assertEqual(self.seq.attr('imag'), [0, 0, 0, 0, 0])

    def test_item(self):
        self.assertEqual(List([dict(a=1), dict(a=2)]).item('a'), [1, 2])

    def test_invoke(self):
        self.assertEqual(self.seq.invoke('__str__'),
                         ['1', '2', '3', '4', '5'])

    def test_uniq(self):
        self.assertEqual(List([2, 1, 2, 3, 2, 1, 2, 3]).uniq().sort(),
                         [1, 2, 3])

        (List([dict(a=1), dict(b=1), dict(c=2)])
           .uniq(lambda x: x.items()[0][1])
           .do(lambda seq: self.assertTrue(dict(a=1) in seq or
                                           dict(b=1) in seq))

           .do(lambda seq: self.assertTrue(dict(c=2) in seq))
           .do(lambda seq: self.assertEqual(seq.count(), 2)))

        (List("test")
          .uniq()
          .sort()
          .do(self.assertEqual, list('est')))

    def test_join(self):
        self.assertEqual(List(['t', 'e', 's', 't']).join(','), 't,e,s,t')

    def test_compact(self):
        self.assertEqual(List([None, 0, 2, []]).compact(), [2])
        self.assertEqual(List([None, 0, 2, []]).compact(lambda x: x != None),
                        [0, 2, []])

    def test_flatten(self):
        self.assertEqual(List([1, List([2, 3, 6, [7, [8]]])]).flatten(),
                         [1, 2, 3, 6, 7, 8])


class Dict(dict):
    """
    map x,y -> new y
    keep
    rem
    compact
    some/has
    all
    count () = len, (x|f)
    empty () == [], (f) -> x in [0, None]..

    wrapper: clear(), clone(), fromkeys()
       (and last_value = the result of the last operation)
       also do will pass extra arg. so do(self.assertTrue, ...)
       = do(lambda seq: self.assertTrue(seq, ...)
       = self.assertTrue(seq, ...)

    # todo
    init()
    invoke
    Uniq -> Can take f to specify on what it should uniq.
    Do do(lambda seq: ...)
    """

    @staticmethod
    def _proxy(method_name):
        def wrap(self, *args, **kwargs):
            inst = Dict(self)
            getattr(dict, method_name)(inst, *args, **kwargs)
            return inst

        setattr(Dict, method_name, wrap)

    def _f(self, f, x, y):
        if hasattr(f, '__call__'):
            return f(x, y)
        else:
            return f == y

    def map(self, f):
        d = Dict()

        for k, v in self.iteritems():
            if hasattr(f, '__call__'):
                d[k] = f(k, v)
            else:
                d[k] = f

        return d

    def keep(self, f):
        d = Dict()

        for k, v in self.iteritems():
            if self._f(f, k, v):
                d[k] = v

        return d

    def rem(self, f):
        d = Dict()

        for k, v in self.iteritems():
            if not self._f(f, k, v):
                d[k] = v

        return d

    def compact(self, f=None):
        if f:
            return self.rem(f)
        else:
            return self.rem(lambda x, y: not y)

    def all(self, f):
        for x,y in self.iteritems():
            if not self._f(f, x, y):
                return False

        return True

    def some(self, f):
        for x,y in self.iteritems():
            if self._f(f, x, y):
                return True

        return False

    def count(self, *args):
        if not args:
            return len(self)
        else:
            return len(Dict(self).keep(args[0]))

    def do(self, function, *args, **kwargs):
        self.last_value = function(self, *args, **kwargs)
        return self

    def copy(self):
        return Dict(self)

    def invoke(self, f, *args, **kwargs):
        return self.map(lambda x, y: getattr(y, f)(*args, **kwargs))

    @classmethod
    def fromkeys(cls, *args, **kwargs):
        return Dict(dict.fromkeys(*args, **kwargs))

    def empty(self, *args):
        if not args:
            return len(self) == 0
        else:
            return len(Dict(self).rem(args[0])) == 0


List(['update', 'clear']).map(Dict._proxy)


class DictTest(unittest.TestCase):

    def setUp(self):
        self.seq = Dict(a=1, b=2, c=3)

    def test_is_dict(self):
        self.assertEqual(self.seq, dict(a=1, b=2, c=3))

    def test_map(self):
        self.assertEqual(self.seq.map(3), dict(a=3, b=3, c=3))
        self.assertEqual(self.seq.map(lambda x, y: x),
                         dict(a='a', b='b', c='c'))

        self.assertEqual(self.seq.map(lambda x, y: y * 2),
                         dict(a=2, b=4, c=6))

    def test_keep(self):
        self.assertEqual(self.seq.keep(3), dict(c=3))
        self.assertEqual(self.seq.keep(lambda x, y: y > 2), dict(c=3))

    def test_rem(self):
        self.assertEqual(self.seq.rem(3), dict(a=1, b=2))
        self.assertEqual(self.seq.rem(lambda x, y: y > 2), dict(a=1, b=2))

    def test_update(self):
        self.assertEqual(self.seq.update(dict(a=5, d=1)),
                         dict(a=5, b=2, c=3, d=1))
        self.assertTrue(isinstance(self.seq.update(dict(a=5, d=1)), Dict))

    def test_clear(self):
        self.assertEqual(self.seq.clear(), {})
        self.assertTrue(isinstance(self.seq.clear(), Dict))

    def test_copy(self):
        a = []

        self.assertEqual(id(Dict(a=a).copy()['a']), id(a))
        self.assertEqual(self.seq.copy(), self.seq)
        self.assertTrue(isinstance(self.seq.copy(), Dict))

    def test_fromkeys(self):
        self.assertTrue(isinstance(Dict.fromkeys([1, 2, 3]), Dict))
        self.assertEqual(Dict.fromkeys([1, 2, 3]),
                         {1:None, 2:None, 3:None})

    def test_compact(self):
        self.assertEqual(self.seq.update(a=None, b=[]).compact(),
                         dict(c=3))

        self.assertEqual(self.seq
                           .update(a=None, b=[])
                           .compact(lambda x, y: y == None),
                         dict(b=[], c=3))

    def test_all(self):
        self.assertTrue(self.seq.all(lambda x, y: y in [1, 2, 3]))
        self.assertTrue(self.seq.update(a=2, c=2).all(2))
        self.assertFalse(self.seq.all(4))

    def test_some(self):
        self.assertTrue(self.seq.some(lambda x, y: y == 3))
        self.assertTrue(self.seq.some(2))
        self.assertFalse(self.seq.some(4))

    def test_count(self):
        self.assertEqual(self.seq.count(), 3)
        self.assertEqual(self.seq.count(3), 1)
        self.assertEqual(self.seq.count(lambda x, y: y in [1, 3]), 2)

    def test_empty(self):
        self.assertFalse(self.seq.empty())
        self.assertTrue(Dict().empty())
        self.assertTrue(Dict(zip([1, 2, 3], [None, 0, 0]))
                          .empty(lambda x, y: y in [None, 0]))

        self.assertFalse(Dict(zip([1, 2, 3], [None, [], 0]))
                          .empty(lambda x, y: y in [None, 0]))

    def test_do(self):
        self.assertEqual(
            (self.seq
             .map(lambda x, y: y * 2)
             .rem(4)
             .do(self.assertEqual, dict(a=2, c=6))),
             dict(a=2, c=6))

        self.assertEqual(self.seq.do(lambda self: 1 + 1).last_value, 2)

    def test_invoke(self):
        (Dict(a='hello', b='hi')
           .invoke('upper')
           .do(self.assertEqual, dict(a='HELLO', b='HI')))

        (Dict(a='hello', b='hi')
           .invoke('find', 'h')
           .do(self.assertEqual, dict(a=0, b=0)))


if __name__ == '__main__':
    unittest.main()
