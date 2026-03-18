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
        if self.demand is None or self.ordering_cost is None or self.holding_cost is None:
            raise ValueError("Data not provided. Call input_data() first.")
        # EOQ formula
        q = math.sqrt(2 * self.demand * self.ordering_cost / self.holding_cost)
        total_cost = math.sqrt(2 * self.demand * self.ordering_cost * self.holding_cost)
        num_orders = self.demand / q
        cycle_time = 1 / num_orders  # in years
        return {
            "EOQ": q,
            "Total annual cost": total_cost,
            "Number of orders per year": num_orders,
            "Cycle time (years)": cycle_time
        }

class PriceBreakModel:
    """Scenario 2: EOQ with all‑units quantity discounts."""
    def __init__(self):
        self.demand = None
        self.ordering_cost = None
        self.holding_cost_rate = None   # as a decimal (e.g., 0.2 for 20%)
        self.price_breaks = []           # list of (break_qty, unit_price)

    def input_data(self):
        print("\n--- EOQ with price breaks (all‑units discounts) ---")
        self.demand = get_float("Annual demand (units/year): ")
        self.ordering_cost = get_float("Ordering cost ($/order): ")
        self.holding_cost_rate = get_float("Annual holding cost rate (as decimal, e.g., 0.2): ")

        n = get_int("Number of price break points: ")
        print("Enter break quantities and corresponding unit prices.")
        print("Break quantities are the minimum quantity to get that price.")
        breaks = []
        for i in range(n):
            q = get_float(f"Break quantity {i+1}: ", min_val=0, allow_zero=True)
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
        best_cost = float('inf')
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
            upper_bound = self.price_breaks[idx+1][0] if idx+1 < len(self.price_breaks) else float('inf')

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

            for q in set(candidates):   # use set to avoid duplicate if eoq equals lower bound
                # Total cost = ordering + holding + purchase cost (since price affects holding and purchase)
                # Note: purchase cost is D * price, constant for all q at same price, but we include it to compare across prices.
                total_cost = (self.demand * price) + (self.demand * self.ordering_cost / q) + (h * q / 2)
                if total_cost < best_cost:
                    best_cost = total_cost
                    best_q = q
                    best_price = price

        return {
            "Optimal order quantity": best_q,
            "Unit price": best_price,
            "Total annual cost (including purchase)": best_cost
        }

class MultiItemConstraintModel:
    """Scenario 3: Multi‑item EOQ with a space constraint.
       Each item has demand, ordering cost, holding cost, and space per unit.
       Total average space used (sum of (Q_i/2)*space_i) cannot exceed total_space.
    """
    def __init__(self):
        self.items = []          # list of dicts with keys: demand, order_cost, hold_cost, space
        self.total_space = None

    def input_data(self):
        print("\n--- Multi‑item EOQ with space constraint ---")
        n = get_int("Number of items: ")
        self.items = []
        for i in range(n):
            print(f"\nItem {i+1}:")
            d = get_float("  Annual demand: ")
            o = get_float("  Ordering cost per order: ")
            h = get_float("  Holding cost per unit per year: ")
            s = get_float("  Space occupied per unit (e.g., sq ft): ")
            self.items.append({
                "demand": d,
                "order_cost": o,
                "hold_cost": h,
                "space": s
            })
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
            total_cost = sum(math.sqrt(2 * it["demand"] * it["order_cost"] * it["hold_cost"]) for it in self.items)
            return {
                "Constraint not binding": True,
                "Optimal quantities": unconstrained_q,
                "Total annual cost": total_cost,
                "Total space used": total_space_unconstrained
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
            if lmbda_high > 1e12:   # safety
                raise RuntimeError("Cannot find lambda upper bound. Check data.")

        # Bisection
        for _ in range(100):   # 100 iterations should give high precision
            lmbda_mid = (lmbda_low + lmbda_high) / 2
            space_mid = space_used(lmbda_mid)
            if abs(space_mid - self.total_space) < 1e-8:
                break
            if space_mid > self.total_space:
                lmbda_low = lmbda_mid   # need larger lambda to reduce space
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
            total_cost += d * o / q + h * q / 2   # holding cost uses original h, not including lambda

        total_space_actual = sum((q/2)*it["space"] for q, it in zip(quantities, self.items))

        return {
            "Constraint binding": True,
            "Lagrange multiplier (lambda)": lmbda,
            "Optimal quantities": quantities,
            "Total annual cost": total_cost,
            "Total space used": total_space_actual,
            "Space target": self.total_space
        }

def main():
    models = {
        '1': EOQModel,
        '2': PriceBreakModel,
        '3': MultiItemConstraintModel
    }
    while True:
        print("\n" + "="*50)
        print("INVENTORY MANAGEMENT SCENARIOS")
        print("1. Single‑item EOQ")
        print("2. EOQ with price breaks (all‑units discounts)")
        print("3. Multi‑item EOQ with space constraint")
        print("0. Exit")
        choice = input("Select an option: ").strip()
        if choice == '0':
            print("Goodbye!")
            break
        if choice not in models:
            print("Invalid choice. Please enter 1, 2, 3, or 0.")
            continue

        model_class = models[choice]
        model = model_class()
        try:
            model.input_data()
            result = model.solve()
            print("\n" + "-"*40)
            print("OPTIMAL SOLUTION")
            for key, value in result.items():
                if isinstance(value, float):
                    print(f"{key}: {value:.4f}")
                elif isinstance(value, list):
                    print(f"{key}:")
                    for i, v in enumerate(value):
                        print(f"  Item {i+1}: {v:.4f}")
                else:
                    print(f"{key}: {value}")
            print("-"*40)
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()