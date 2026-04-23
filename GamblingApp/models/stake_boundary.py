class StakeBoundary:
    def __init__(self,lower_limit,upper_limit):
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit

    def validate(self,stake):
        if(stake<self.lower_limit):
            return "Below minimum limit"
        
        if(stake > self.upper_limit):
            return "Above maximum limit"

        return "within limits"
    
    def warning(self,stake):
        if stake <= self.lower_limit * 1.2:
            return "Approaching lower limit"
        if stake >= self.upper_limit * 0.8:
            return "Approaching upper limit"
        return None