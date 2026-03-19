import math
import sys


def get_float(prompt, min_val=0.0, allow_zero=False):
    """Helper to read and validate a float input."""
    while True:
        try:
            val = float(input(prompt))
            if val < min_val or (not allow_zero and val == 0):
                print(f"Value must be >= {min_val}{'' if allow_zero else ' and >0'}.")
                continue
            return val
        except ValueError:
            print("Invalid number. Please try again.")


def get_int(prompt, min_val=1):
    """Helper to read and validate an integer input."""
    while True:
        try:
            val = int(input(prompt))
            if val < min_val:
                print(f"Value must be >= {min_val}.")
                continue
            return val
        except ValueError:
            print("Invalid integer. Please try again.")


class EOQModel:
    """Scenario 1: Single‑item EOQ with constant demand."""

    def __init__(self):
        self.demand = None
        self.ordering_cost = None
        self.holding_cost = None

    def input_data(self):
        print("\n--- Single‑item EOQ ---")
        self.demand = get_float("Annual demand (units/year): ")
        self.ordering_cost = get_float("Ordering cost ($/order): ")
        self.holding_cost = get_float("Holding cost ($/unit/year): ")

    def solve(self):
        if (
            self.demand is None
            or self.ordering_cost is None
            or self.holding_cost is None
        ):
            raise ValueError("Data not provided. Call input_data() first.")
        # EOQ formula
        q = math.sqrt(2 * self.demand * self.ordering_cost / self.holding_cost)
        num_orders = self.demand / q
        cycle_time = 1 / num_orders  # in years

        # Cost components (professor's formulas)
        ordering_cost_total = (self.demand / q) * self.ordering_cost  # D/Q * S
        holding_cost_total = (q / 2) * self.holding_cost  # Q/2 * H
        total_cost = ordering_cost_total + holding_cost_total

        return {
            "EOQ": q,
            "Total annual ordering cost (D/Q*S)": ordering_cost_total,
            "Total annual holding cost (Q/2*H)": holding_cost_total,
            "Total annual cost": total_cost,
            "Number of orders per year": num_orders,
            "Cycle time (years)": cycle_time,
        }


class PriceBreakModel:
    """Scenario 2: EOQ with all‑units quantity discounts."""

    def __init__(self):
        self.demand = None
        self.ordering_cost = None
        self.holding_cost_rate = None  # as a decimal (e.g., 0.2 for 20%)
        self.price_breaks = []  # list of (break_qty, unit_price)

    def input_data(self):
        print("\n--- EOQ with price breaks (all‑units discounts) ---")
        self.demand = get_float("Annual demand (units/year): ")
        self.ordering_cost = get_float("Ordering cost ($/order): ")
        self.holding_cost_rate = get_float(
            "Annual holding cost rate (as decimal, e.g., 0.2): "
        )

        n = get_int("Number of price break points: ")
        print("Enter break quantities and corresponding unit prices.")
        print("Break quantities are the minimum quantity to get that price.")
        breaks = []
        for i in range(n):
            q = get_float(f"Break quantity {i + 1}: ", min_val=0, allow_zero=True)
            p = get_float(f"Unit price at or above {q}: $")
            breaks.append((q, p))
        # Sort by break quantity (ascending)
        breaks.sort(key=lambda x: x[0])
        self.price_breaks = breaks

    def solve(self):
        if None in (self.demand, self.ordering_cost, self.holding_cost_rate):
            raise ValueError("Data not provided.")
        if not self.price_breaks:
            raise ValueError("Price breaks list is empty.")

        best_q = None
        best_cost = float("inf")
        best_price = None

        # Evaluate each price interval
        # For each price, the feasible order quantity must be at least the break quantity
        # for that price, and less than the next break quantity (if any).
        for idx, (break_qty, price) in enumerate(self.price_breaks):
            # Holding cost depends on price
            h = self.holding_cost_rate * price
            if h is None or self.demand is None or self.ordering_cost is None:
                continue  # skip this price break if any value is None
            # Compute EOQ for this price
            eoq = math.sqrt(2 * self.demand * self.ordering_cost / h)

            # Determine the feasible range for this price
            lower_bound = break_qty
            upper_bound = (
                self.price_breaks[idx + 1][0]
                if idx + 1 < len(self.price_breaks)
                else float("inf")
            )

            # Candidate quantities:
            # - EOQ if it falls in the range
            # - lower bound (break quantity) if it's above EOQ but still gives lower total cost?
            # Actually, the optimal order quantity for a given price is:
            #   - EOQ if it is >= lower bound
            #   - lower bound if EOQ < lower bound (since EOQ is not feasible, the lowest feasible quantity is the break point)
            #   - (For the last interval, there is no upper bound; for intermediate intervals, if EOQ exceeds upper bound,
            #      the feasible quantity for that price is upper bound? But the upper bound belongs to the next price.
            #      So for this price, the feasible quantities are only those in [break_qty, next_break_qty). If EOQ exceeds
            #      that, the optimal feasible quantity for this price is actually the next break point, which will be considered
            #      in the next interval. So we only consider EOQ if it lies in [lower_bound, upper_bound).)
            candidates = []
            if lower_bound <= eoq < upper_bound:
                candidates.append(eoq)
            # Also always consider the lower bound (break quantity) because if EOQ is below it,
            # the best you can do at this price is order exactly at the break point.
            # If EOQ is above upper bound, ordering at lower bound may be suboptimal compared to the next price,
            # but we still need to evaluate it because it might be better than the next price's EOQ.
            candidates.append(lower_bound)

            for q in set(
                candidates
            ):  # use set to avoid duplicate if eoq equals lower bound
                if q == 0:
                    continue  # skip zero quantity (not a valid order)
                # Total cost = ordering + holding + purchase cost (since price affects holding and purchase)
                # Note: purchase cost is D * price, constant for all q at same price, but we include it to compare across prices.
                total_cost = (
                    (self.demand * price)
                    + (self.demand * self.ordering_cost / q)
                    + (h * q / 2)
                )
                if total_cost < best_cost:
                    best_cost = total_cost
                    best_q = q
                    best_price = price

        if best_q is None or best_price is None:
            raise ValueError("Could not find a valid solution. Check input data.")

        # Calculate detailed cost components for the best solution
        h_best = self.holding_cost_rate * best_price
        purchase_cost = self.demand * best_price
        ordering_cost_total = (self.demand / best_q) * self.ordering_cost
        holding_cost_total = (best_q / 2) * h_best

        return {
            "Optimal order quantity": best_q,
            "Unit price": best_price,
            "Annual purchase cost (D*C)": purchase_cost,
            "Annual ordering cost (D/Q*S)": ordering_cost_total,
            "Annual holding cost (Q/2*H)": holding_cost_total,
            "Total annual cost": best_cost,
        }


class ProbabilisticModel:
    """Scenario 4: Probabilistic demand with safety stock and reorder point.
    Uses EOQ for order quantity and calculates reorder point with safety stock
    based on desired service level.
    """

    def __init__(self):
        self.demand_annual = None
        self.demand_daily_avg = None
        self.demand_daily_std = None
        self.lead_time = None
        self.service_level = None
        self.ordering_cost = None
        self.holding_cost_rate = None
        self.unit_cost = None
        self.working_days = None

    def input_data(self):
        print("\n--- Probabilistic Demand Model (with Safety Stock) ---")
        print("\nDemand Information:")
        self.demand_daily_avg = get_float("  Average daily demand (units/day): ")
        self.demand_daily_std = get_float("  Std dev of daily demand (units/day): ")
        self.working_days = get_int("  Working days per year: ")
        self.demand_annual = self.demand_daily_avg * self.working_days
        print(f"  Annual demand (calculated): {self.demand_annual:.2f} units/year")

        print("\nLead Time & Service Level:")
        self.lead_time = get_float("  Lead time (days): ")
        self.service_level = get_float(
            "  Desired service level (as decimal, e.g., 0.95): ",
            min_val=0,
            allow_zero=False,
        )

        print("\nCost Parameters:")
        self.ordering_cost = get_float("  Ordering cost ($/order): ")
        self.unit_cost = get_float("  Unit cost ($/unit): ")
        self.holding_cost_rate = get_float(
            "  Annual holding cost rate (as decimal, e.g., 0.2): "
        )

    def solve(self):
        if None in (
            self.demand_annual,
            self.demand_daily_avg,
            self.demand_daily_std,
            self.lead_time,
            self.service_level,
            self.ordering_cost,
            self.holding_cost_rate,
            self.unit_cost,
        ):
            raise ValueError("Data not provided.")

        # Calculate H (annual holding cost per unit)
        H = self.holding_cost_rate * self.unit_cost

        # EOQ calculation
        D = self.demand_annual
        S = self.ordering_cost
        eoq = math.sqrt(2 * D * S / H)

        # Number of orders per year
        num_orders = D / eoq

        # Reorder point calculation
        # Mean demand during lead time
        mu_LT = self.demand_daily_avg * self.lead_time

        # Std dev of demand during lead time
        sigma_LT = self.demand_daily_std * math.sqrt(self.lead_time)

        # Z value for service level (using inverse of standard normal CDF)
        # Approximation using Abramowitz and Stegun
        Z = self._get_z_score(self.service_level)

        # Safety stock
        safety_stock = Z * sigma_LT

        # Reorder point
        reorder_point = mu_LT + safety_stock

        # Cost components
        purchase_cost = D * self.unit_cost
        ordering_cost_total = (D / eoq) * S
        holding_cost_cycle = (eoq / 2) * H  # Holding cost for cycle stock
        holding_cost_safety = safety_stock * H  # Holding cost for safety stock
        total_holding_cost = holding_cost_cycle + holding_cost_safety
        total_cost = ordering_cost_total + total_holding_cost + purchase_cost

        return {
            "Optimal order quantity (EOQ)": eoq,
            "Number of orders per year": num_orders,
            "Reorder point": reorder_point,
            "Safety stock": safety_stock,
            "Z-value (service level)": Z,
            "Mean demand during lead time": mu_LT,
            "Std dev during lead time": sigma_LT,
            "Annual purchase cost (D*C)": purchase_cost,
            "Annual ordering cost (D/Q*S)": ordering_cost_total,
            "Annual holding cost (cycle stock)": holding_cost_cycle,
            "Annual holding cost (safety stock)": holding_cost_safety,
            "Total annual holding cost": total_holding_cost,
            "Total annual cost": total_cost,
        }

    def _get_z_score(self, service_level):
        """Approximate inverse of standard normal CDF using Abramowitz and Stegun."""
        # For service_level >= 0.5
        if service_level >= 0.5:
            p = 1 - service_level
        else:
            p = service_level

        # Coefficients for rational approximation
        c0, c1, c2 = 2.515517, 0.802853, 0.010328
        d1, d2, d3 = 1.432788, 0.189269, 0.001308

        t = math.sqrt(-2 * math.log(p))
        z = t - (c0 + c1 * t + c2 * t * t) / (1 + d1 * t + d2 * t * t + d3 * t * t * t)

        return z if service_level >= 0.5 else -z


class MultiItemConstraintModel:
    """Scenario 3: Multi‑item EOQ with a space constraint.
    Each item has demand, ordering cost, holding cost, and space per unit.
    Total average space used (sum of (Q_i/2)*space_i) cannot exceed total_space.
    """

    def __init__(self):
        self.items = []  # list of dicts with keys: demand, order_cost, hold_cost, space
        self.total_space = None

    def input_data(self):
        print("\n--- Multi‑item EOQ with space constraint ---")
        n = get_int("Number of items: ")
        self.items = []
        for i in range(n):
            print(f"\nItem {i + 1}:")
            d = get_float("  Annual demand: ")
            o = get_float("  Ordering cost per order: ")
            h = get_float("  Holding cost per unit per year: ")
            s = get_float("  Space occupied per unit (e.g., mts2): ")
            self.items.append(
                {"demand": d, "order_cost": o, "hold_cost": h, "space": s}
            )
        self.total_space = get_float("Total available space (average): ")

    def solve(self):
        if not self.items or self.total_space is None:
            raise ValueError("Data not provided.")

        # First compute unconstrained EOQs and total space used
        unconstrained_q = []
        total_space_unconstrained = 0.0
        for it in self.items:
            d = it["demand"]
            o = it["order_cost"]
            h = it["hold_cost"]
            s = it["space"]
            q = math.sqrt(2 * d * o / h)
            unconstrained_q.append(q)
            total_space_unconstrained += (q / 2) * s

        # If unconstrained already fits, return those
        if total_space_unconstrained <= self.total_space:
            total_cost = sum(
                math.sqrt(2 * it["demand"] * it["order_cost"] * it["hold_cost"])
                for it in self.items
            )
            return {
                "Constraint not binding": True,
                "Optimal quantities": unconstrained_q,
                "Total annual cost": total_cost,
                "Total space used": total_space_unconstrained,
            }

        # Otherwise, find lambda > 0 using bisection such that sum(s_i * Q_i(lambda)/2) = total_space
        # Q_i(lambda) = sqrt(2 * D_i * O_i / (H_i + lambda * s_i))
        def space_used(lmbda):
            total = 0.0
            for it in self.items:
                d = it["demand"]
                o = it["order_cost"]
                h = it["hold_cost"]
                s = it["space"]
                if lmbda == 0:
                    q = math.sqrt(2 * d * o / h)
                else:
                    q = math.sqrt(2 * d * o / (h + lmbda * s))
                total += (q / 2) * s
            return total

        # Find upper bound for lambda. Start with a small guess and increase until space_used < total_space.
        # Since lambda increases, Q decreases, space decreases.
        lmbda_low = 0.0
        lmbda_high = 1.0
        while space_used(lmbda_high) > self.total_space:
            lmbda_high *= 2
            if lmbda_high > 1e12:  # safety
                raise RuntimeError("Cannot find lambda upper bound. Check data.")

        # Bisection
        for _ in range(100):  # 100 iterations should give high precision
            lmbda_mid = (lmbda_low + lmbda_high) / 2
            space_mid = space_used(lmbda_mid)
            if abs(space_mid - self.total_space) < 1e-8:
                break
            if space_mid > self.total_space:
                lmbda_low = lmbda_mid  # need larger lambda to reduce space
            else:
                lmbda_high = lmbda_mid

        lmbda = (lmbda_low + lmbda_high) / 2
        # Compute final quantities
        quantities = []
        total_cost = 0.0
        for it in self.items:
            d = it["demand"]
            o = it["order_cost"]
            h = it["hold_cost"]
            s = it["space"]
            q = math.sqrt(2 * d * o / (h + lmbda * s))
            quantities.append(q)
            total_cost += (
                d * o / q + h * q / 2
            )  # holding cost uses original h, not including lambda

        total_space_actual = sum(
            (q / 2) * it["space"] for q, it in zip(quantities, self.items)
        )

        return {
            "Constraint binding": True,
            "Lagrange multiplier (lambda)": lmbda,
            "Optimal quantities": quantities,
            "Total annual cost": total_cost,
            "Total space used": total_space_actual,
            "Space target": self.total_space,
        }


class EOQWithSafetyStock:
    """Scenario 5: EOQ with a fixed safety stock."""

    def __init__(self):
        self.demand = None
        self.ordering_cost = None
        self.holding_cost = None
        self.safety_stock = None

    def input_data(self):
        print("\n--- EOQ with Fixed Safety Stock ---")
        self.demand = get_float("Annual demand (units/year): ")
        self.ordering_cost = get_float("Ordering cost ($/order): ")
        self.holding_cost = get_float("Holding cost ($/unit/year): ")
        self.safety_stock = get_float(
            "Safety stock (units): ", min_val=0, allow_zero=True
        )

    def solve(self):
        if None in (
            self.demand,
            self.ordering_cost,
            self.holding_cost,
            self.safety_stock,
        ):
            raise ValueError("Data not provided.")
        # EOQ
        q = math.sqrt(2 * self.demand * self.ordering_cost / self.holding_cost)
        num_orders = self.demand / q
        cycle_time = 1 / num_orders
        ordering_cost_total = (self.demand / q) * self.ordering_cost
        holding_cost_cycle = (q / 2) * self.holding_cost
        holding_cost_safety = self.safety_stock * self.holding_cost
        total_holding_cost = holding_cost_cycle + holding_cost_safety
        total_cost = ordering_cost_total + total_holding_cost

        return {
            "EOQ": q,
            "Safety stock": self.safety_stock,
            "Total annual ordering cost": ordering_cost_total,
            "Total annual holding cost (cycle stock)": holding_cost_cycle,
            "Total annual holding cost (safety stock)": holding_cost_safety,
            "Total annual holding cost": total_holding_cost,
            "Total annual cost (ordering + holding)": total_cost,
            "Number of orders per year": num_orders,
            "Cycle time (years)": cycle_time,
        }


class MultiItemConstraintBudgetModel:
    """
    Scenario 6: Multi‑item EOQ with space and budget constraints.
    Each item has annual demand, ordering cost, holding cost, unit cost,
    space per unit, daily demand, and lead time.
    Constraints: total average space ≤ available space,
                 total average inventory value ≤ available budget.
    Also computes reorder point for each item.
    """

    def __init__(self):
        self.items = []  # list of dicts with keys: demand, order_cost, hold_cost, unit_cost, space, daily_demand, lead_time
        self.total_space = None
        self.total_budget = None

    def input_data(self):
        print("\n--- Multi‑item EOQ with space and budget constraints ---")
        n = get_int("Number of items: ")
        self.items = []
        for i in range(n):
            print(f"\nItem {i + 1}:")
            d = get_float("  Annual demand (units/year): ")
            o = get_float("  Ordering cost per order ($): ")
            h = get_float("  Holding cost per unit per year ($): ")
            c = get_float("  Unit cost ($/unit): ")
            s = get_float("  Space occupied per unit (e.g., mts2): ")
            dd = get_float("  Average daily demand (units/day): ")
            lt = get_float("  Lead time (days): ")
            self.items.append(
                {
                    "demand": d,
                    "order_cost": o,
                    "hold_cost": h,
                    "unit_cost": c,
                    "space": s,
                    "daily_demand": dd,
                    "lead_time": lt,
                }
            )
        self.total_space = get_float("Total available space (average): ")
        self.total_budget = get_float(
            "Total available budget (average inventory value): "
        )

    def solve(self):
        if not self.items or self.total_space is None or self.total_budget is None:
            raise ValueError("Data not provided.")

        # Extract lists for convenience
        D = [it["demand"] for it in self.items]
        S = [it["order_cost"] for it in self.items]
        H = [it["hold_cost"] for it in self.items]
        C = [it["unit_cost"] for it in self.items]
        space = [it["space"] for it in self.items]
        n = len(self.items)

        # Unconstrained EOQs
        Q_uncon = [math.sqrt(2 * D[i] * S[i] / H[i]) for i in range(n)]
        space_uncon = sum((Q_uncon[i] / 2) * space[i] for i in range(n))
        budget_uncon = sum((Q_uncon[i] / 2) * C[i] for i in range(n))

        # If unconstrained already satisfies both constraints, return them
        if (
            space_uncon <= self.total_space + 1e-8
            and budget_uncon <= self.total_budget + 1e-8
        ):
            total_cost = sum(
                D[i] * S[i] / Q_uncon[i] + H[i] * Q_uncon[i] / 2 for i in range(n)
            )
            return self._build_result(
                Q_uncon,
                total_cost,
                space_uncon,
                budget_uncon,
                lambda1=0,
                lambda2=0,
                binding=False,
            )

        # Helper: compute space, budget, and Q given lambda1 and lambda2
        def compute(l1, l2):
            Q = []
            for i in range(n):
                denom = H[i] + l1 * space[i] + l2 * C[i]
                # denom > 0 always because l1,l2 >=0 and H>0
                q = math.sqrt(2 * D[i] * S[i] / denom)
                Q.append(q)
            space_used = sum((Q[i] / 2) * space[i] for i in range(n))
            budget_used = sum((Q[i] / 2) * C[i] for i in range(n))
            return Q, space_used, budget_used

        # Tolerance for bisection
        tol = 1e-8

        # First, try l1 = 0, and find l2 that satisfies budget (if needed)
        # Check if budget is violated at l1=0, l2=0
        _, space0, budget0 = compute(0, 0)
        budget_violated = budget0 > self.total_budget + tol
        space_violated = space0 > self.total_space + tol

        # If only space is violated, we can use single‑constraint method (l2=0)
        if not budget_violated and space_violated:
            # Use a bisection on l1 only (similar to scenario 3)
            def space_used_l1(l1):
                Q, s, _ = compute(l1, 0)
                return s

            # Find upper bound for l1
            l1_low = 0
            l1_high = 1.0
            while space_used_l1(l1_high) > self.total_space:
                l1_high *= 2
                if l1_high > 1e12:
                    raise RuntimeError("Cannot find lambda upper bound for space.")
            # Bisection
            for _ in range(100):
                l1_mid = (l1_low + l1_high) / 2
                s_mid = space_used_l1(l1_mid)
                if abs(s_mid - self.total_space) < tol:
                    break
                if s_mid > self.total_space:
                    l1_low = l1_mid
                else:
                    l1_high = l1_mid
            l1_opt = (l1_low + l1_high) / 2
            Q_opt, space_opt, budget_opt = compute(l1_opt, 0)
            total_cost = sum(
                D[i] * S[i] / Q_opt[i] + H[i] * Q_opt[i] / 2 for i in range(n)
            )
            return self._build_result(
                Q_opt,
                total_cost,
                space_opt,
                budget_opt,
                lambda1=l1_opt,
                lambda2=0,
                binding=True,
            )

        # If budget is violated (possibly also space), we need to consider l2
        # At l1=0, find l2 that satisfies budget (if budget violated)
        def find_l2_for_l1(l1, target_budget):
            # Check if at l2=0, budget <= target
            _, _, b0 = compute(l1, 0)
            if b0 <= target_budget + tol:
                return 0.0
            # Otherwise, find l2 such that budget = target
            l2_low = 0
            l2_high = 1.0
            while True:
                _, _, b_high = compute(l1, l2_high)
                if b_high < target_budget:
                    break
                l2_high *= 2
                if l2_high > 1e12:
                    raise RuntimeError("Cannot find l2 upper bound for budget.")
            for _ in range(100):
                l2_mid = (l2_low + l2_high) / 2
                _, _, b_mid = compute(l1, l2_mid)
                if abs(b_mid - target_budget) < tol:
                    break
                if b_mid > target_budget:
                    l2_low = l2_mid
                else:
                    l2_high = l2_mid
            return (l2_low + l2_high) / 2

        # For l1=0, get l2 that satisfies budget
        l2_at_0 = find_l2_for_l1(0, self.total_budget)
        _, space_at_0, budget_at_0 = compute(0, l2_at_0)

        # If space already ok, we are done
        if space_at_0 <= self.total_space + tol:
            Q_opt, space_opt, budget_opt = compute(0, l2_at_0)
            total_cost = sum(
                D[i] * S[i] / Q_opt[i] + H[i] * Q_opt[i] / 2 for i in range(n)
            )
            return self._build_result(
                Q_opt,
                total_cost,
                space_opt,
                budget_opt,
                lambda1=0,
                lambda2=l2_at_0,
                binding=True,
            )

        # Otherwise, both constraints are binding: need to find l1>0 and corresponding l2
        # Define a function that returns space for a given l1, with l2 adjusted to meet budget
        def space_for_l1(l1):
            l2 = find_l2_for_l1(l1, self.total_budget)
            _, s, _ = compute(l1, l2)
            return s

        # Find upper bound for l1 such that space becomes <= target
        l1_low = 0
        l1_high = 1.0
        while space_for_l1(l1_high) > self.total_space:
            l1_high *= 2
            if l1_high > 1e12:
                raise RuntimeError("Cannot find lambda1 upper bound.")
        # Bisection on l1
        for _ in range(100):
            l1_mid = (l1_low + l1_high) / 2
            s_mid = space_for_l1(l1_mid)
            if abs(s_mid - self.total_space) < tol:
                break
            if s_mid > self.total_space:
                l1_low = l1_mid
            else:
                l1_high = l1_mid
        l1_opt = (l1_low + l1_high) / 2
        l2_opt = find_l2_for_l1(l1_opt, self.total_budget)
        Q_opt, space_opt, budget_opt = compute(l1_opt, l2_opt)
        total_cost = sum(D[i] * S[i] / Q_opt[i] + H[i] * Q_opt[i] / 2 for i in range(n))
        return self._build_result(
            Q_opt,
            total_cost,
            space_opt,
            budget_opt,
            lambda1=l1_opt,
            lambda2=l2_opt,
            binding=True,
        )

    def _build_result(
        self, Q, total_cost, space_used, budget_used, lambda1, lambda2, binding
    ):
        """Format the result dictionary."""
        result = {
            "Constraints binding": binding,
            "Lagrange multiplier (space)": lambda1,
            "Lagrange multiplier (budget)": lambda2,
            "Total annual cost (ordering + holding)": total_cost,
            "Total space used (average)": space_used,
            "Total budget used (average inventory value)": budget_used,
            "Space target": self.total_space,
            "Budget target": self.total_budget,
        }
        # Item details - store as nested dict for better formatting
        item_details = []
        for idx, it in enumerate(self.items):
            q = Q[idx]
            rop = it["daily_demand"] * it["lead_time"]
            # Optional: include cost components per item
            ord_cost = (it["demand"] / q) * it["order_cost"]
            hold_cost = (q / 2) * it["hold_cost"]
            budget_item = (q / 2) * it["unit_cost"]
            space_item = (q / 2) * it["space"]
            item_details.append(
                {
                    "order_quantity": q,
                    "reorder_point": rop,
                    "annual_ordering_cost": ord_cost,
                    "annual_holding_cost": hold_cost,
                    "budget_used": budget_item,
                    "space_used": space_item,
                }
            )
        result["item_details"] = item_details
        return result


def main():
    models = {
        "1": EOQModel,
        "2": PriceBreakModel,
        "3": MultiItemConstraintModel,
        "4": ProbabilisticModel,
        "5": EOQWithSafetyStock,
        "6": MultiItemConstraintBudgetModel,  # New scenario
    }
    while True:
        print("\n" + "=" * 50)
        print("INVENTORY MANAGEMENT SCENARIOS")
        print("1. Single‑item EOQ")
        print("2. EOQ with price breaks (all‑units discounts)")
        print("3. Multi‑item EOQ with space constraint")
        print("4. Probabilistic demand (with safety stock)")
        print("5. EOQ with fixed safety stock")
        print("6. Multi‑item EOQ with space and budget constraints")  # New option
        print("0. Exit")
        choice = input("Select an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        if choice not in models:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, or 0.")
            continue

        model_class = models[choice]
        model = model_class()
        try:
            model.input_data()
            result = model.solve()

            # For scenario 1 and 5, optionally calculate reorder point
            if choice in ("1", "5"):
                ans = (
                    input("\nDo you want to calculate the reorder point? (y/n): ")
                    .strip()
                    .lower()
                )
                if ans in ("y", "yes"):
                    lead_time = get_float(
                        "Enter lead time (days): ", min_val=0, allow_zero=False
                    )
                    days_per_year = get_float(
                        "Enter working days per year: ", min_val=1, allow_zero=False
                    )
                    annual_demand = model.demand
                    daily_demand = annual_demand / days_per_year
                    reorder_point = daily_demand * lead_time
                    # If safety stock exists (scenario 5), add it to reorder point
                    if (
                        hasattr(model, "safety_stock")
                        and model.safety_stock is not None
                    ):
                        reorder_point += model.safety_stock
                        result["Reorder point (with safety stock)"] = reorder_point
                    else:
                        result["Reorder point (without safety stock)"] = reorder_point

            # For scenario 1 only, also offer comparison with current policy
            if choice == "1":
                ans2 = (
                    input("\nDo you want to compare with current policy? (y/n): ")
                    .strip()
                    .lower()
                )
                if ans2 in ("y", "yes"):
                    current_q = get_float(
                        "Enter current order quantity (units): ",
                        min_val=0,
                        allow_zero=False,
                    )
                    D = model.demand
                    S = model.ordering_cost
                    H = model.holding_cost
                    current_ordering = (D / current_q) * S
                    current_holding = (current_q / 2) * H
                    current_total = current_ordering + current_holding
                    optimal_total = result["Total annual cost"]
                    savings = optimal_total - current_total
                    result["Current order quantity"] = current_q
                    result["Current total cost (ordering+holding)"] = current_total
                    result["Optimal total cost"] = optimal_total
                    result["Difference (Optimal - Current)"] = savings
                    if savings < 0:
                        result["Savings with optimal policy"] = -savings
                    else:
                        result["Note"] = "Current policy is already optimal or better."

            print("\n" + "-" * 40)
            print("OPTIMAL SOLUTION")
            # Print summary totals first
            for key, value in result.items():
                if key == "item_details":
                    continue  # Skip item details for now
                if isinstance(value, float):
                    print(f"{key}: {value:.4f}")
                elif isinstance(value, list):
                    print(f"{key}:")
                    for i, v in enumerate(value):
                        print(f"  Item {i + 1}: {v:.4f}")
                else:
                    print(f"{key}: {value}")

            # Print individual item details
            if "item_details" in result:
                print("\nItem Details:")
                for idx, item in enumerate(result["item_details"]):
                    print(f"\n  Item {idx + 1}:")
                    print(f"    Order quantity: {item['order_quantity']:.4f}")
                    print(f"    Reorder point: {item['reorder_point']:.4f}")
                    print(
                        f"    Annual ordering cost: {item['annual_ordering_cost']:.4f}"
                    )
                    print(f"    Annual holding cost: {item['annual_holding_cost']:.4f}")
                    print(
                        f"    Budget used (average inventory value): {item['budget_used']:.4f}"
                    )
                    print(f"    Space used (average): {item['space_used']:.4f}")
            print("-" * 40)
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()
