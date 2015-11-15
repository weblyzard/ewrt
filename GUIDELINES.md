# eWRT Programming Guidelines:

1. New code **must** be python2 and python3 compatible
2. Use logging.debug rather than print and also use its string expansion.
   ```python
   print "Debug: %s." % (message)       # avoid
   logging.debug("Debug: %s", message)  # use (python3 compatible, allows filtering, faster)
   ```
3. Exclusively use `pytest` for testing and `pytest.mark` rather than `nose.attr` to annotate unit tests

## Recommended unit-test tags:

```
 db     ... test case requires a database connection
 new    ... indicates new test case (run with 'nosetest ./mypackage.py -a new')
 remote ... test case requires remote resources (e.g. Web Services, ...)
 slow   ... slow test case
```



