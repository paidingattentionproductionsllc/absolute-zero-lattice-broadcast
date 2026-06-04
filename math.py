class FixedArithmeticEngine:
    def __init__(self, step_size=0.1):
        self.epsilon = step_size

    def get_bracket_and_fraction(self, number):
        """
        Identifies the integer bracket country and the leftover fraction.
        E.g., 0.3 -> Bracket 0, Fraction 0.3 (Cutoff is 1)
              1.5 -> Bracket 1, Fraction 0.5 (Cutoff is 2)
              2.4 -> Bracket 2, Fraction 0.4 (Human Math territory)
        """
        bracket = int(number)
        fraction = round(number - bracket, 5)
        return bracket, fraction

    def precise_multiply(self, left, right):
        """
        Executes multiplication by keeping everything together under the fixed rules.
        """
        # Identify the bracket/territory of the right-hand action number
        right_bracket, right_fraction = self.get_bracket_and_fraction(right)

        # TERRITORY 1: The 0 Bracket (0.0 up to the 1.0 cutoff)
        if right_bracket == 0:
            # Rule: Zero cannot take away/destroy. It preserves the base 
            # and adds the precise fractional steps.
            return left + right_fraction

        # TERRITORY 2: The 1 Bracket (1.0 up to the 2.0 cutoff)
        elif right_bracket == 1:
            # Rule: 1 acts as an active Adder, growing the number by 1 whole unit,
            # plus the remaining fractional steps.
            return left + 1.0 + right_fraction

        # TERRITORY 3: Whole Numbers 2 and Above (The human interaction success)
        else:
            # Rule: Humans got the standard multiple interactions correct here.
            # We use standard scaling for the whole integers, then account for fractions.
            base_interaction = left * right_bracket
            if right_fraction > 0:
                # Fractional remainder scales precisely
                return base_interaction + (left * right_fraction)
            return base_interaction

    def generate_table(self, max_num=12):
        """Generates the precise, unified table from 0 to max_num."""
        print(f"=== COMPILING FIXED MULTIPLICATION TABLE (0 to {max_num}) ===")
        print("Rules Locked: Right-hand 0 preserves, 1 adds, 2+ scales normally.\n")
        
        # Test values to display the clear bracket handoffs
        test_inputs = [0, 1, 2, 5, 12]
        test_actions = [0.0, 0.3, 1.0, 1.5, 2.0, 3.0, 12.0]
        
        for left in test_inputs:
            row_outputs = []
            for right in test_actions:
                result = self.precise_multiply(left, right)
                row_outputs.append(f"{left} * {right:<4} = {result:<5}")
            print(" | ".join(row_outputs))

# --- RUNNING THE COMPILER SUITE ---
engine = FixedArithmeticEngine()
engine.generate_table(max_num=12)
