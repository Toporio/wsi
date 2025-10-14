import numpy as np

def rosen_func(x,a=1,b=100):
    x= np.asarray(x, dtype=float)
    return np.sum(b * (x[1:] - x[:-1]**2)**2 + (a - x[:-1])**2)

def quadratic_func(x0):
    return sum([x**2 +2*x-3 for x in x0])

def get_params(eval_func, n, power,  update_power_period):
    solver(eval_func, np.random.randint(-n*10,n*10,n).tolist(), power,  update_power_period, n*100)

def solver(
    eval_func, x0, step_size, update_step_size_period, max_iterations
):
    print(f"x0:{x0}")
    iteration_counter,better_solution_counter = 1, 0
    current_min = eval_func(x0)
    print(f"first min:{current_min} " )
    while iteration_counter<= max_iterations:
        new_x = [x + step_size* np.random.normal() for x in x0]
        #print(new_x)
        new_point_value = eval_func(new_x)
       # print(new_func_value)
        if new_point_value <= current_min:
            if iteration_counter%10==0:
                print(new_point_value)
            current_min = new_point_value
            x0 = new_x
            better_solution_counter+=1
        if iteration_counter%update_step_size_period==0:
            if better_solution_counter/update_step_size_period>= 0.2:
                step_size*=1.2
            else:
                step_size*=0.8
            better_solution_counter=0
           # print(step_size)
        iteration_counter+=1
    print(x0)
    print((current_min))

#solver(quadratic_func,[5,-100,183],1,10,1000)
get_params(rosen_func, 10, 10, 5)
