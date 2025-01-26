from functools import reduce
from utils import sliding_window, is_cycle


class Rule:
    def run(self, data, mean, std, verbose=False):
        pass


class LimitRule(Rule):
    def __init__(self, sigmas=3, window_size=1, fail_count=1):
        self.sigmas = sigmas
        self.window_size = window_size
        self.fail_count = fail_count
    
    def run(self, data, mean, std, verbose=False):
        issues = []
        upper_limit = mean + (self.sigmas * std)
        lower_limit = mean - (self.sigmas * std)

        if verbose:
            print(f"===== {type(self).__name__} =====")
            print(f"sigmas: {self.sigmas}, window: {self.window_size}, fail_count: {self.fail_count}")
            print(f"upper limit: {upper_limit}")
            print(f"lower limit: {lower_limit}")

        last = None
        for idx, window in enumerate(
            sliding_window(data, self.window_size)
        ):
            count_above = sum([ 
                1 if point > upper_limit else 0 
                for point in window
            ])
            count_below = sum([
                1 if point < lower_limit else 0 
                for point in window
            ])
            if count_above >= self.fail_count or count_below >= self.fail_count:
                issues.append((type(self).__name__, idx + 1))
            
        if verbose:
            print(f"detected: {issues}")
    
        return issues


class ControlLimitRule(LimitRule):
    def __init__(self):
        super().__init__()


class WarningLimitRule(LimitRule):
    def __init__(self):
        super().__init__(sigmas=2, window_size=3, fail_count=2)


class ZoneCLimitRule(LimitRule):
    def __init__(self):
        super().__init__(sigmas=1, window_size=5, fail_count=4)


class SingleSideConsecutiveRule(Rule):
    def run(self, data, mean, std, verbose=False):
        issues = []
        
        if verbose:
            print(f"===== {type(self).__name__} =====")
            
        for idx, window in enumerate(
            sliding_window(data, 8)
        ):
            if (
                (max(window) > mean and min(window) > mean)
                or (max(window) < mean and min(window) < mean)
            ):
                issues.append((type(self).__name__, idx + 1))
        
        if verbose:
            print(f"detected: {issues}")     
            
        return issues


class RunRule(Rule):
    def run(self, data, mean, std, verbose=False):
        issues = []
        
        if verbose:
            print(f"===== {type(self).__name__} =====")

        for idx, window in enumerate(
            sliding_window(data, 6)
        ):
            if window == sorted(window) or window == sorted(window, reverse=True):
                issues.append((type(self).__name__, idx + 1))
        
        if verbose:
            print(f"detected: {issues}")
            
        return issues


class CycleRule(Rule):
    def run(self, data, mean, std, verbose=False):
        issues = []
        
        if verbose:
            print(f"===== {type(self).__name__} =====")

        last_cycle = None
        for idx, window in enumerate(
            sliding_window(data, 15)
        ):
            if is_cycle(window):
                # detects cycles larger than the window size
                if last_cycle != idx - 1: 
                    issues.append((type(self).__name__, idx + 1))
                last_cycle = idx
        
        if verbose:
            print(f"detected: {issues}")        
        
        return issues


class ZoneCCycleRule(Rule):
    def run(self, data, mean, std, verbose=False):
        issues = []
        upper_limit = mean + std
        lower_limit = mean - std

        if verbose:
            print(f"===== {type(self).__name__} =====")
            print(f"upper_limit: {upper_limit}")
            print(f"lower_limit: {lower_limit}")

        for idx, window in enumerate(
            sliding_window(data, 14)
        ):
            if (
                is_cycle(window)
                and min(window) > lower_limit 
                and max(window) < upper_limit
            ):
                issues.append((type(self).__name__, idx + 1))
        
        if verbose:
            print(f"detected: {issues}")  
        
        return issues


class MissingZoneCRule(Rule):
    def _points_in_zone_c(self, points, mean, std):
        upper_limit = mean + std
        lower_limit = mean - std

        for point in points:
            if point > lower_limit and point < upper_limit:
                return True
        return False
        
    def run(self, data, mean, std, verbose=False):
        issues = []

        if verbose:
            print(f"===== {type(self).__name__} =====")
            print(f"upper_limit: {mean + std}")
            print(f"lower_limit: {mean - std}")

        for idx, window in enumerate(
            sliding_window(data, 8)
        ):
            if not self._points_in_zone_c(window, mean, std):
                issues.append((type(self).__name__, idx + 1))
        
        if verbose:
            print(f"detected: {issues}")  
        
        return issues


class NearLimitRule(Rule):
    def run(self, data, mean, std, verbose=False):
        issues = []
        near = 0.25
        ucl = mean + (3 * std)
        lcl = mean - (3 * std)
        uwl = mean + (2 * std)
        lwl = mean - (2 * std)

        if verbose:
            print(f"===== {type(self).__name__} =====")
            print(f"nearness: {near}")
            print(f"ucl: {ucl}\nlcl: {lcl}")
            print(f"uwl: {uwl}\nlwl: {lwl}")

        for idx, point in enumerate(data):
            if (
                (point < ucl and point > ucl - (near * std))
                or (point < uwl and point > uwl - (near * std))
                or (point > lcl and point < lcl + (near * std))
                or (point > lwl and point < lwl + (near * std))
            ):
                issues.append((type(self).__name__, idx + 1))
        
        if verbose:
            print(f"detected: {issues}")  
        
        return issues
        

rules = [
    ControlLimitRule(),
    WarningLimitRule(),
    ZoneCLimitRule(),
    SingleSideConsecutiveRule(),
    RunRule(),
    CycleRule(),
    ZoneCCycleRule(),
    MissingZoneCRule(),
    MissingZoneCRule(),
    NearLimitRule()
]