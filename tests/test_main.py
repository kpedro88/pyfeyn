from pyfeyn2.mkfeyndiag import main


def test_main_tikz(capsys):
    main(["tests/test.fml", "-r", "tikz"])
