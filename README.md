# Rated gNBSim

Expanded from [gNBSim](https://github.com/omec-project/gnbsim)

## Usage
run from ue10
```
python simulator.py
```

To change the request rate (default 0) make requests to port 3001 with the "rps" field set in form data, example
```
requests.post("http://localhost:3001/", data = {"rps": 1})
```

To modify the gNBSim profile, see default.yaml in ue10
