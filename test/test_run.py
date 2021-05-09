from sclblpy import run
from sclblonnx import sclbl_input
import numpy as np
from PIL import Image


def test_run_inputs(_verbose=True):
    """
    Function testing in sp.run for various input options.

    Models:
    * Linear regression from sklearn
        * cfid: e871d8e5-b2e2-11ea-a47d-9600004e79cc
        * input: [[1,3]]

    * XGBoost model:
        * cfid: 007bdbaa-b093-11ea-a47d-9600004e79cc
        * input: [[17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019.0, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189]]

    * Add model (from ONNX)
        * cfid: 7c351fff-ad9c-11eb-af86-9600004e79cc
        * {"input": ["CAEQAUoEmpmZPw==","CAEQAUoEAAAgQA=="], "type":"pb"}
        * {"input": ["mpmZPw==","AAAgQA=="], "type":"raw"}

    * Image empty check:
        * cfid: 8e3a52c2-ad9c-11eb-af86-9600004e79cc
        * Image from file  files/1.JPG

    """

    # Lin reg model
    cfid = "e871d8e5-b2e2-11ea-a47d-9600004e79cc"
    csv1 = [1, 2]
    result = run(cfid, csv1)
    assert result['statusCode'] == 1, "Lin reg example fails..."
    if _verbose:
        print(result['result'])

    # XGBoost model
    cfid = "007bdbaa-b093-11ea-a47d-9600004e79cc"
    csv2 = [17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019.0, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189]
    result = run(cfid, csv2)
    assert result['statusCode'] == 1, "XGBoots example fails..."
    if _verbose:
        print(result['result'])

    # Add example (with pb and raw):
    cfid = "7c351fff-ad9c-11eb-af86-9600004e79cc"
    example = {"x1": np.array([1.2]).astype(np.float32), "x2": np.array([2.5]).astype(np.float32)}
    pb1 = sclbl_input(example, "pb", False)
    result = run(cfid, pb1)
    assert result['statusCode'] == 1, "Add example w. pb example fails..."
    if _verbose:
        print(result['result'])

    raw1 = sclbl_input(example, "raw", False)
    result = run(cfid, raw1)
    assert result['statusCode'] == 1, "Add example w. raw example fails..."
    if _verbose:
        print(result['result'])

    # Image example:
    cfid = "8e3a52c2-ad9c-11eb-af86-9600004e79cc"
    img_data = np.array(Image.open("files/1.JPG"), dtype=np.int32)
    example = {"in": img_data.astype(np.int32)}
    pb = sclbl_input(example, _verbose=False)
    result = run(cfid, pb)
    assert result['statusCode'] == 1, "Add example w. pb example fails..."
    if _verbose:
        print(result['result'])

    cfid = "8e3a52c2-ad9c-11eb-af86-9600004e79cc"
    img_data = np.array(Image.open("files/3.JPG"), dtype=np.int32)
    example = {"in": img_data.astype(np.int32)}
    pb = sclbl_input(example, _verbose=False)
    result = run(cfid, pb)
    assert result['statusCode'] == 1, "Add example w. pb example fails..."
    if _verbose:
        print(result['result'])


    # Image raw:
    cfid = "8e3a52c2-ad9c-11eb-af86-9600004e79cc"
    img_data = np.array(Image.open("files/1.JPG"), dtype=np.int32)
    example = {"in": img_data.astype(np.int32)}
    pb = sclbl_input(example, "raw", _verbose=False)
    result = run(cfid, pb)
    assert result['statusCode'] == 1, "Add example w. raw example fails..."
    if _verbose:
        print(result['result'])

    cfid = "8e3a52c2-ad9c-11eb-af86-9600004e79cc"
    img_data = np.array(Image.open("files/3.JPG"), dtype=np.int32)
    example = {"in": img_data.astype(np.int32)}
    pb = sclbl_input(example, "raw", _verbose=False)
    result = run(cfid, pb)
    assert result['statusCode'] == 1, "Add example w. raw example fails..."
    if _verbose:
        print(result['result'])


test_run_inputs()