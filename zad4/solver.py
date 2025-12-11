import autograd.numpy as np
import matplotlib.pyplot as plt
from autograd import grad


def rosen_func(x):
    a, b = 1, 100
    return np.sum(b * (x[1:] - x[:-1] ** 2) ** 2 + (a - x[:-1]) ** 2)


def ackley_func(x):
    a = 20.0
    b = 0.2
    c = 2.0 * np.pi
    n = x.size
    sum_sq = np.sum(x**2)
    sum_cos = np.sum(np.cos(c * x))
    term1 = -a * np.exp(-b * np.sqrt(sum_sq / n))
    term2 = -np.exp(sum_cos / n)
    return term1 + term2 + a + np.e


def quadratic_func(x):
    return np.sum(x**2 + 1)


def draw_plot(data):
    for function_name, params in data.items():
        x0 = np.random.uniform(-params[1], params[1] + 1, params[1]).astype(float)
        plt.figure(figsize=(8, 5))
        for learning_rate in params[2]:
            eval_func, n, max_iterations, max_iterations_without_new_best_value = (
                params[0],
                params[1],
                params[3],
                params[4],
            )
            data = solver(
                eval_func,
                x0,
                learning_rate,
                max_iterations,
                max_iterations_without_new_best_value,
            )
            plt.plot(
                list(data.keys()),
                list(x for x in data.values()),
                label=f"q(x_t), learning_rate={learning_rate}",
            )
        # plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Iteracje t")
        plt.ylabel("f(t)")
        plt.title(f"{function_name}")
        plt.legend()
        plt.savefig(f"{function_name}.png")


def solver(
    eval_func,
    x0,
    learning_rate,
    max_iterations,
    max_iterations_without_improvement,
):
    np.seterr(over="raise", invalid="raise")
    values_at_points = {}
    iteration_counter, iterations_without_improvement = 0, 0

    grad_eval_func = grad(eval_func)
    current_min = float(eval_func(x0.astype(float)))
    values_at_points[iteration_counter] = current_min
    while (
        iteration_counter < max_iterations
        and iterations_without_improvement < max_iterations_without_improvement
    ):
        grad_x0 = grad_eval_func(x0)
        new_x = x0 - learning_rate * grad_x0
        try:
            new_point_value = float(eval_func(new_x))
        except (OverflowError, FloatingPointError):
            break
        if (
            np.isnan(new_point_value)
            or np.isinf(new_point_value)
            or new_point_value > 1e150
        ):
            break
        if new_point_value < current_min:
            current_min = new_point_value
            iterations_without_improvement = 0
        else:
            iterations_without_improvement += 1

        values_at_points[iteration_counter] = new_point_value
        x0 = new_x.copy()
        iteration_counter += 1
    return values_at_points


data = {
    "funkcja kwadratowa, n=10": [
        quadratic_func,
        10,
        [1, 10, 10],
        1000,
        200,
    ],
    "funkcja rosenbrock, n=10": [
        rosen_func,
        10,
        [1, 10, 10],
        1000,
        200,
    ],
    "funkcja ackley, n=10": [
        ackley_func,
        10,
        [1, 10, 100],
        1000,
        200,
    ],
}

draw_plot(data)
