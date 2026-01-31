import pytest
import agentpy as ap
from utils.analysis import sum_params
from utils.analysis import create_matrices_from_params
from utils.analysis import create_matrices_from_output


def test_sum_params_with_prefix():
    p = {"x1": 1, "x2": 2, "y3": 3}
    assert sum_params(p, "x") == 3
    assert sum_params(p, "y") == 3
    assert sum_params(p, "x2") == 2
    assert sum_params(p, "z") == 0


@pytest.fixture
def keys():
    account_keys = ["H", "F", "B", "G", "CB"]
    stock_keys = ["Y_inv", "M", "A", "D", "B", "L", "E"]
    flow_keys = [
        "C",
        "W",
        "Z",
        "T",
        "iota_A",
        "iota_B",
        "iota_L",
        "iota_D",
        "Pi_d",
        "Pi",
        "DeltaA",
        "DeltaB",
        "DeltaM",
        "DeltaL",
        "DeltaD",
        "DeltaE",
        "L_def",
    ]
    return account_keys, stock_keys, flow_keys


def test_create_sfc_matrices_from_empty_params(keys):
    params = {}
    stocks, flows = create_matrices_from_params(params)
    print("stocks\n", stocks, "\nflows\n", flows)

    account_keys, stock_keys, flow_keys = keys
    assert list(stocks.columns) == account_keys + ["sigma"]
    assert list(stocks.index) == stock_keys + ["V", "sigma"]
    assert list(flows.columns) == account_keys + ["sigma"]
    assert list(flows.index) == flow_keys + ["sigma"]

    for key in account_keys:
        assert stocks.loc["sigma", key] == 0
        assert flows.loc["sigma", key] == 0
    for key in stock_keys:
        assert stocks.loc[key, "sigma"] == 0
    for key in flow_keys:
        assert flows.loc[key, "sigma"] == 0


def test_create_sfc_matrices_from_partial_params():
    for i in range(3):
        params = {"M_H": 5 * i, "C": 10 * i, "W_F": 15 * i}
        stocks, flows = create_matrices_from_params(params)
        print("stocks\n", stocks, "\nflows\n", flows)

        assert stocks.loc["sigma", "H"] == 0
        assert stocks.loc["sigma", "F"] == 0
        assert stocks.loc["sigma", "B"] == 0
        assert stocks.loc["V", "H"] == -5 * i
        assert stocks.loc["M", "sigma"] == 5 * i

        assert flows.loc["sigma", "H"] == -10 * i
        assert flows.loc["sigma", "F"] == -15 * i
        assert flows.loc["sigma", "B"] == 0
        assert flows.loc["C", "sigma"] == -10 * i
        assert flows.loc["W", "sigma"] == -15 * i


def test_create_sfc_matrices_from_params_with_precision():
    for i in range(3):
        for j in range(3):
            params = {"M_H": 1.2345 * i, "W_F": 6.789 * i}
            stocks, flows = create_matrices_from_params(params, digits=j)
            print("stocks\n", stocks, "\nflows\n", flows)

            assert stocks.loc["sigma", "H"] == 0.0
            assert stocks.loc["sigma", "F"] == 0.0
            assert stocks.loc["V", "H"] == round(-1.2345 * i, j)
            assert stocks.loc["M", "sigma"] == round(1.2345 * i, j)

            assert flows.loc["sigma", "F"] == -round(6.789 * i, j)
            assert flows.loc["W", "sigma"] == -round(6.789 * i, j)


class FakeModel1(ap.Model):
    def step(self):
        self.record("M_H", 5)
        self.record("C", 10)
        self.record("W_F", 15)


def test_create_sfc_matrices_from_model_output():
    for t in range(1, 3):
        params = {"steps": t}
        model = FakeModel1(params)
        output = model.run()
        stocks, flows = create_matrices_from_output(output, t, model_name="FakeModel1")
        print(f"stocks {t}\n", stocks, f"\nflows{t}\n", flows)

        assert stocks.loc["sigma", "H"] == 0
        assert stocks.loc["sigma", "F"] == 0
        assert stocks.loc["sigma", "B"] == 0
        assert stocks.loc["V", "H"] == -5
        assert stocks.loc["M", "sigma"] == 5

        assert flows.loc["sigma", "H"] == -10
        assert flows.loc["sigma", "F"] == -15
        assert flows.loc["sigma", "B"] == 0
        assert flows.loc["C", "sigma"] == -10
        assert flows.loc["W", "sigma"] == -15


class FakeModel2(ap.Model):
    def step(self):
        self.record("M_H", 5.1234)
        self.record("C", 10.1234)
        self.record("W_F", 15.1234)


def test_create_sfc_matrices_from_output_with_precision():
    for d in range(3):
        params = {"steps": 1}
        model = FakeModel2(params)
        output = model.run()
        stocks, flows = create_matrices_from_output(
            output, 1, model_name="FakeModel2", digits=d
        )
        print(f"stocks\n", stocks, f"\nflows\n", flows)

        assert stocks.loc["sigma", "H"] == 0.0
        assert stocks.loc["sigma", "F"] == 0.0
        assert stocks.loc["V", "H"] == -round(5.1234, d)
        assert stocks.loc["M", "sigma"] == round(5.1234, d)

        assert flows.loc["sigma", "H"] == -round(10.1234, d)
        assert flows.loc["sigma", "F"] == -round(15.1234, d)
        assert flows.loc["C", "sigma"] == -round(10.1234, d)
        assert flows.loc["W", "sigma"] == -round(15.1234, d)
