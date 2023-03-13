from pgzero.clock import clock

# Class for a count down timer
# My first attempt at a class with dad's help

class CountdownTimer:
    # Create timer
    def __init__(self):
        self.time_remaining = 0
        clock.schedule_interval(self.update,1) # Call update(), every second
    
    # Will get called once every second
    def update(self):  
        if self.time_remaining > 0:
            self.time_remaining -= 1
    
    # Set the timer
    def set(self,time):  
        self.time_remaining = time
        
    # Add more time    
    def extend(self,time):
        self.time_remaining += time
    
    # Return time remianing as a string (m:ss)
    def as_string(self):
        mins = self.time_remaining // 60
        secs = self.time_remaining % 60        
        return f"{mins}:{secs:02d}"  # print minutes followed by secs with 2 digits and leading zero
    
    # Check if time is up
    def is_time_up(self):
        if self.time_remaining > 0:
            return False
        else:
            return True
