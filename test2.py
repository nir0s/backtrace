def _func2():
    try:
        filename = 'certainly_a_non_existing_path'
        with open(filename) as f:
            f.read()
        print('Wait.. you have a file under the cwd called {0}?! You '
              'crazy.'.format(filename))
        raise RuntimeError('just an error')
    except IOError as ex:
        other_func(ex)


def other_func(ex):
    raise raise_func(ex)


def raise_func(ex):
    raise RuntimeError(ex)
