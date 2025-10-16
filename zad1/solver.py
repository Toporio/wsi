import numpy as np
import matplotlib.pyplot as plt

def rosen_func(x,a=1,b=100):
    x= np.asarray(x, dtype=float)
    return np.sum(b * (x[1:] - x[:-1]**2)**2 + (a - x[:-1])**2)

def ackley_func(x, a=20, b=0.2, c=2*np.pi):
    x = np.asarray(x, dtype=float)
    n = x.size
    sum_sq = np.sum(x**2)
    sum_cos = np.sum(np.cos(c * x))
    term1 = -a * np.exp(-b * np.sqrt(sum_sq / n))
    term2 = -np.exp(sum_cos / n)
    return term1 + term2 + a + np.e

def quadratic_func(x0):
    return sum([x**2 +2*x-3 for x in x0])

def draw_plot(data):
    for function_name, params in data.items():
        plt.figure()
        for power in params[2]:
            eval_func, n, update_power_period, max_without_new_best_value = params[0], params[1], params[3], params[4]
            data = solver(eval_func, np.random.randint(-n*10,n*10,n).tolist(), power,  update_power_period, n*100, max_without_new_best_value)
            plt.plot(list(data.keys()),list(data.values()),label=f'sigma={power}')
        plt.title(f'{function_name}')
        plt.legend()
        plt.savefig(f'{function_name}.png')

def solver(
    eval_func, x0, step_size, update_step_size_period, max_iterations, max_iterations_without_new_best_value
):
    values_at_points = {}
    print(f"x0:{x0}")
    iteration_counter,better_solution_counter, iterations_without_new_value = 0, 0,0
    current_min = eval_func(x0)
    print(f"first min:{current_min} " )
    while iteration_counter <= max_iterations and iterations_without_new_value <=max_iterations_without_new_best_value:
        new_x = [x + step_size* np.random.normal() for x in x0]
        #print(new_x)
        new_point_value = eval_func(new_x)
        values_at_points[iteration_counter] = new_point_value
        #print(new_func_value)
        if new_point_value <= current_min:
            current_min = new_point_value
            x0 = new_x
            better_solution_counter+=1
            iterations_without_new_value = 0
        if iteration_counter % update_step_size_period == 0:
            if better_solution_counter / update_step_size_period >= 1/5:
                step_size*=1.21
            else:
                step_size*=0.82
            better_solution_counter=0
           # print(step_size)
        iteration_counter+=1
        iterations_without_new_value+=1
    print(iteration_counter)
    print((current_min))
    return values_at_points

#solver(quadratic_func,[5,-100,183],1,10,1000)
data = {
    "funkcja kwadratowa, n=10": [quadratic_func, 1, [0.1, 0.5, 1, 5], 10, 50],
    "funkcja rosen, n=10": [rosen_func, 10, [0.2, 0.5, 1, 5], 10, 50],
    "funkcja kwadratowa, n=30": [quadratic_func, 30, [0.1, 0.5, 1, 5], 10, 50],
    "funkcja rosen, n=30": [rosen_func, 30, [0.1, 0.5, 1, 5], 10, 50],
    "funkcja ackley, n=10": [ackley_func, 10, [0.1, 0.5, 1, 5], 10, 50],
    "funkcja ackley, n=30": [ackley_func, 30, [0.1, 0.5, 1, 5], 10, 50]
}
draw_plot(data)
