# Bot for cardiovascular disease risk model

To test this model use different files in [Spanish](cardio.py) or [English](cardio_en.py).

First consider that we already have a config.py file with the API Token of your telegram bot. If not, you can follow the steps [here](../README.md).

Now we install the necessary libraries in the environment that you prefer conda or pipenv, from request.txt.

```
pip install -r request.txt
```

Nexy you just have to download the [model](model.bin).

And run the python file chosen according to the language, for example:
```python cardio_en.py```

