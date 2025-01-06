# K_P = 0.0
# K_I = 0.0
# K_D = 0.0

SET_POINT = 1.0
BASE_PRICE = 300.0
PED_DEMAND = -1.5
PED_SUPPLY = 1.0


class PIDController:
    def __init__(self, k_p: float, k_i: float, k_d: float, set_point: float):
        """
        Initializes the PID controller.

        Args:
            k_p (float): The proportional gain coefficient.
            k_i (float): The integral gain coefficient.
            k_d (float): The derivative gain coefficient.
            set_point (float): The desired value.
        """

        self.k_p = k_p
        self.k_i = k_i
        self.k_d = k_d
        self.set_point = set_point
        self.integral_term = 0
        self.last_error = None

    def get_error(self, process_variable: float) -> float:
        """
        Calculates the error between the setpoint and the process variable.

        Args:
            process_variable (float): The current value of the process.

        Returns:
            float: The calculated error.
        """

        return self.set_point - process_variable

    def get_proportional(self, error: float) -> float:
        """
        Calculates the proportional term of the PID controller.

        Args:
            error (float): The current error.

        Returns:
            float: The proportional term.
        """

        return self.k_p * error

    def get_integral(self, error: float, dt: float) -> float:
        """
        Calculates the integral term of the PID controller.

        Args:
            error (float): The current error.
            dt (float): The time step.

        Returns:
            float: The integral term.
        """

        self.integral_term += error * dt
        return self.k_i * self.integral_term

    def get_derivative(self, error: float, dt: float) -> float:
        """
        Calculates the derivative term of the PID controller.

        Args:
            error (float): The current error.
            dt (float): The time step.

        Returns:
            float: The derivative term.
        """

        if self.last_error is None:
            derivative = 0
        else:
            derivative = (error - self.last_error) / dt
        self.last_error = error
        return self.k_d * derivative

    def get_control(self, process_variable: float, dt: float) -> float:
        """
        Calculates the overall control output of the PID controller.

        Args:
            process_variable (float): The current value of the process.
            dt (float): The time step.

        Returns:
            float: The control output.
        """

        error = self.get_error(process_variable)
        p_term = self.get_proportional(error)
        i_term = self.get_integral(error, dt)
        d_term = self.get_derivative(error, dt)
        return p_term + i_term + d_term



def get_dsr_n(k_p, k_i, k_d):
    """
    Calculate the Demand Supply Ratio (DSR) using a PID controller.

    This function simulates the adjustment of delivery prices using a PID controller
    to balance supply and demand, returning the resulting DSR over time.

    Parameters:
    k_p (float): Proportional gain of the PID controller
    k_i (float): Integral gain of the PID controller
    k_d (float): Derivative gain of the PID controller

    Global variables used:
    SET_POINT, BASE_PRICE, SUPPLY, DEMAND, PED_DEMAND, PED_SUPPLY

    Returns:
    np.array: An array of DSR values over time
    """

    controller = PIDController(k_p, k_i, k_d, SET_POINT)

    dsr = []
    cv = 0.0  # В начале у нас воздействия на цену
    price = BASE_PRICE  # В начале текущая цена доставки равна базовой

    for s, d in zip(SUPPLY, DEMAND):
        curr_d = adjust_demand_supply(BASE_PRICE, price, d, PED_DEMAND)
        curr_s = adjust_demand_supply(BASE_PRICE, price, s, PED_SUPPLY)
        cv = controller.get_control(s / d, 1)
        price = BASE_PRICE * (1 + cv)
        new_d = adjust_demand_supply(BASE_PRICE, price, curr_d, PED_DEMAND)
        new_s = adjust_demand_supply(BASE_PRICE, price, curr_s, PED_SUPPLY)
        dsr.append(new_s / new_d)

    return np.array(dsr)


for i in np.arange(0, 1, 0.01):
    for j in np.arange(0, 0.1, 0.01):
        for k in np.arange(0, 0.3, 0.01):
            dsr_n = get_dsr_n(i, j, k)
            mae = np.mean(np.abs(dsr_n - SET_POINT))
            print(mae)
            if mae < 0.1:
                print(i, j, k)
