import numpy as np
import matplotlib.pyplot as plt
import math


def rosen_func(x, a=1, b=100):
    x = np.asarray(x, dtype=float)
    return float(np.sum(b * (x[1:] - x[:-1] ** 2) ** 2 + (a - x[:-1]) ** 2))


def ackley_func(x):
    x = np.asarray(x, dtype=float)
    a = 20.0
    b = 0.2
    c = 2.0 * math.pi
    n = x.size
    sum_sq = np.sum(x**2)
    sum_cos = np.sum(np.cos(c * x))
    term1 = -a * math.exp(-b * math.sqrt(sum_sq / n))
    term2 = -math.exp(sum_cos / n)
    return float(term1 + term2 + a + math.e)


def quadratic_func(x0):
    return float(sum([x**2  for x in x0]))


def draw_plot(data, R=10):
    for function_name, params in data.items():
        plt.figure(figsize=(8, 5))
        plt.xlabel("Iteracje t")
        plt.ylabel("Wartość funkcji f(t)")
        x0 = np.random.randint(-params[1], params[1], params[1]).tolist()
        for power in params[2]:
            eval_func, n, update_power_period, max_without_new_best_value = (
                params[0],
                params[1],
                params[3],
                params[4],
            )
            test_data = []
            for _ in range(R):
                data = solver(
                    eval_func,
                    x0,
                    power,
                    update_power_period,
                    n * 100,
                    max_without_new_best_value,
                )
                best_so_far_values = list(x[1] for x in data.values())
                test_data.append(best_so_far_values)
            min_length = min(len(x) for x in test_data)
            avg_test_data = [x[:min_length] for x in test_data]
            avg_test_data = np.mean(avg_test_data, axis=0)

            if len(avg_test_data) > 2000:
                plt.xscale("log")
            plt.plot(
                range(1, len(avg_test_data) + 1),
                avg_test_data,
                label=f"best-so-far, sigma={power}",
            )
            plt.title(f"{function_name} (avg)")
            plt.legend()
            plt.savefig(f"{function_name}_avg.png")

        plt.figure(figsize=(8, 5))
        for power in params[2]:
            eval_func, n, update_power_period, max_without_new_best_value = (
                params[0],
                params[1],
                params[3],
                params[4],
            )
            data = solver(
                eval_func,
                x0,
                power,
                update_power_period,
                n * 100,
                max_without_new_best_value,
            )
            if len(data) > 800:
                plt.xscale("log")
            plt.plot(
                list(data.keys()),
                list(x[0] for x in data.values()),
                label=f"q(x_t), sigma={power}",
            )
            plt.plot(
                list(data.keys()),
                list(x[1] for x in data.values()),
                label=f"best-so-far, sigma={power}",
            )
        plt.xlabel("Iteracje t")
        plt.ylabel("f(t)/best-so-far")
        plt.title(f"{function_name}")
        plt.legend()
        plt.savefig(f"{function_name}.png")


def solver(
    eval_func,
    x0,
    step_size,
    update_step_size_period,
    max_iterations,
    max_iterations_without_improvement,
):
    values_at_points = {}
    iteration_counter, better_solution_counter, iterations_without_improvement = 1, 0, 0
    current_min = float(eval_func(x0))
    values_at_points[iteration_counter] = [current_min, current_min]
    while (
        iteration_counter < max_iterations
        and iterations_without_improvement < max_iterations_without_improvement
    ):
        iteration_counter += 1
        new_x = [x + step_size * np.random.normal() for x in x0]
        new_point_value = float(eval_func(new_x))
        values_at_points[iteration_counter] = [new_point_value, current_min]
        if new_point_value < current_min:
            current_min = new_point_value
            x0 = new_x.copy()
            better_solution_counter += 1
            iterations_without_improvement = 0
        else:
            iterations_without_improvement += 1

        if iteration_counter % update_step_size_period == 0:
            if better_solution_counter / update_step_size_period >= 1 / 5:
                step_size *= 1.21
            else:
                step_size *= 0.82
            better_solution_counter = 0
    print(current_min)
    return values_at_points


data = {
    "funkcja kwadratowa, n=10": [quadratic_func, 10, [0.5, 1, 5], 10, 200],
    "funkcja kwadratowa, n=30": [quadratic_func, 30, [0.5, 1, 5], 10, 200],
    "funkcja rosen, n=10": [rosen_func, 10, [0.5, 1, 5], 10, 200],
    "funkcja rosen, n=30": [rosen_func, 30, [0.5, 1, 5], 10, 200],
    "funkcja ackley, n=10": [ackley_func, 10, [0.5, 1, 2, 5], 10, 200],
    "funkcja ackley, n=30": [ackley_func, 30, [0.5, 1, 2, 5, 10], 10, 3000],
}
draw_plot(data, 20)
