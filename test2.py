def moose_bites_kan_be_pretty_nasti():
    try:
        filename = 'certainly_a_non_existing_path'
        with open(filename) as f:
            f.read()
        print('Wait.. you have a file under the cwd called {0}?! You '
              'crazy.'.format(filename))
        raise RuntimeError('just an error')
    except IOError as ex:
        moose_func(ex)


def moose_func(ex):
    raise raise_moose(ex)


def raise_moose(ex):
    raise MooseError(ex)


class MooseError(Exception):
    pass
