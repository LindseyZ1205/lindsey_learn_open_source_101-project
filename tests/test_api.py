# -*- coding: utf-8 -*-

from lindsey_learn_open_source_101 import api


def test():
    _ = api
    assert api.add_two(1, 2) == 3
    assert api.add_two(0, 0) == 0
    assert api.add_two(-1, 1) == 0
    assert api.add_two(100, 200) == 300


if __name__ == "__main__":
    from lindsey_learn_open_source_101.tests import run_cov_test

    run_cov_test(
        __file__,
        "lindsey_learn_open_source_101.api",
        preview=False,
    )
