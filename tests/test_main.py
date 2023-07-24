from pyfeyn2.mkfeyndiag import main


def test_main_help(capsys):
    main(["--help"])
    captured = capsys.readouterr()
    assert "Draw FeynML diagrams with pyfeyn2." in captured.out


def test_main_tikz(capsys):
    main(["tests/test.fml", "-r", "tikz"])
