in_file = "01_input.txt"

class Dial:

    def __init__(self, start_val):
        self.current_val = start_val
        self.zero_count = 0
        self.any_zero_count = 0
    
    def turn(self, turn_str):
        out_val = self.current_val
        assert turn_str[0] in ("R", "L"), f"Value {turn_str} doesn't contain 'L' or 'R'!"
        turn_val = int(turn_str[1:])

        # Subtract or add based on turn type
        for i in range(turn_val):

            if turn_str.startswith("L"):
                out_val -= 1
                if out_val < 0:
                    out_val = 99

            else:
                out_val += 1
                if out_val == 100:
                    out_val = 0
            
            # Keep track of zeros at steps of rotation
            if out_val == 0:
                self.any_zero_count += 1    
        
        # Keep track of zeros at end of rotations 
        if out_val == 0:
            self.zero_count += 1
        
        self.current_val = out_val
        print(f"Turned dial. New val: {self.current_val}")

    def get_zero_count(self):
        return self.zero_count
    
    def get_any_zero_count(self):
        return self.any_zero_count

# Instantiate the dial
dial = Dial(50)
#dial.turn("R57")

# Run it with the file input
with open(in_file) as content:
    in_seq = [line for line in content.readlines()]
    for turn_str in in_seq:
        dial.turn(turn_str)

#print(f"Done. Had {dial.get_zero_count()} zeros along the way")
print(f"Done. Had {dial.get_any_zero_count()} zero steps along the way")