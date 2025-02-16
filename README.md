#Observability
A lightweight Python library for monitoring system metrics. Currently supports CPU usage monitoring with a simple and efficient interface.

##Usage
```
from observability import Observability

# Start CPU monitoring
Observability.CPU.start_monitoring()

# Monitor for some time...

# Stop monitoring and get results as pandas DataFrame
output = Observability.CPU.stop_monitoring()
```

The output DataFrame contains per-core CPU usage data collected at one-second intervals.
