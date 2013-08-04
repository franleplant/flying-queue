flying-queue
=======================

## Simple Simulation script


### Objective
To simulate the functional behavior of a simple system. 
Uniform distribution generator and server (only one allowed).
Infinite FIFO queue 

### How to use it? 

```python
import sim

sys = sim.System(generator_dis, server_dis, Total_simulation_time, time_slice)
results = sys.run_simulation()
sys.print_results()
```

where 

* generator_dis = [ __a__ , __b__ ], where __a__ is the lower distribution limit and __b__ is the upper distribution limit
* server_dis = [ __a__ , __b__ ], where __a__ is the lower distribution limit and __b__ is the upper distribution limit
* Total_simulation_time is a integer that represents the Total simulation time. It must be in seconds
* time_slice represent the frames in which the Total_simulation_time is divided. It must be and integer

* results is a dictionary with this shape 		

```python
results =  { 
			'Lq_mean': lq_mean_value,
			'Ls_mean': ls_mean_value,			
			'Wq_mean': wq_mean_value, 
			'Ws_mean': ws_mean_value,
			'Cm_mean': cm_mean_value
			}
```

* print_results() method will print the result (the same as above) in this shape

```python
Lq_mean: lq_mean_value
Ls_mean: ls_mean_value
Wq_mean: wq_mean_value
Ws_mean: ws_mean_value
Cm_mean: cm_mean_value

```